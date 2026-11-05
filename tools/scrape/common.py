"""Polite HTTP fetching: identifies itself, obeys robots.txt, rate-limits per host."""
import re, time, logging, urllib.parse
import requests

UA = ("AppliancesCompareBot/1.0 (+https://github.com/mohamed-bekheet/appliances-compare; "
      "weekly price comparison, ~1 request/2s)")
log = logging.getLogger("scrape")


class Robots:
    """robots.txt for one host, '*' group, with * and $ wildcards (RFC 9309, longest match wins)."""

    def __init__(self, text):
        self.rules = []                       # (allow: bool, regex, pattern length)
        self.crawl_delay = 0
        groups, cur, in_agents = [], None, False
        for raw in (text or "").splitlines():
            line = raw.split("#", 1)[0].strip()
            if ":" not in line:
                continue
            k, v = [x.strip() for x in line.split(":", 1)]
            k = k.lower()
            if k == "user-agent":
                if not in_agents:
                    cur = {"agents": [], "rules": []}
                    groups.append(cur)
                cur["agents"].append(v.lower())
                in_agents = True
            elif k == "crawl-delay" and cur is not None:
                in_agents = False
                cur["delay"] = v
            elif k in ("allow", "disallow") and cur is not None:
                in_agents = False
                if v:
                    cur["rules"].append((k == "allow", v))
            else:
                in_agents = False
        mine = [g for g in groups if "appliancescomparebot" in g["agents"]] or \
               [g for g in groups if "*" in g["agents"]]
        for g in mine:
            try:
                self.crawl_delay = max(self.crawl_delay, float(g.get("delay") or 0))
            except ValueError:
                pass
            for allow, pat in g["rules"]:
                rx = re.escape(pat).replace(r"\*", ".*")
                if rx.endswith(r"\$"):
                    rx = rx[:-2] + "$"
                self.rules.append((allow, re.compile(rx), len(pat)))

    def allowed(self, path):
        best = None
        for allow, rx, ln in self.rules:
            if rx.match(path):
                if best is None or ln > best[1] or (ln == best[1] and allow):
                    best = (allow, ln)
        return True if best is None else best[0]


class Fetcher:
    def __init__(self, delay=2.0, timeout=40):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": UA, "Accept-Language": "en,ar;q=0.8"})
        self.delay, self.timeout = delay, timeout
        self.robots, self.last = {}, {}
        self.stats = {"ok": 0, "blocked_robots": 0, "http_error": 0}

    def _robots(self, host_url):
        if host_url not in self.robots:
            try:
                r = self.s.get(host_url + "/robots.txt", timeout=self.timeout)
                txt = r.text if r.status_code == 200 else ""
            except requests.RequestException:
                txt = ""
            self.robots[host_url] = Robots(txt)
        return self.robots[host_url]

    def allowed(self, url):
        u = urllib.parse.urlsplit(url)
        path = u.path + ("?" + u.query if u.query else "")
        return self._robots(f"{u.scheme}://{u.netloc}").allowed(path)

    def get(self, url, as_json=False, **kw):
        if not self.allowed(url):
            self.stats["blocked_robots"] += 1
            log.info("robots.txt disallows %s", url)
            return None
        u = urllib.parse.urlsplit(url)
        host = u.netloc
        delay = max(self.delay, min(self._robots(f"{u.scheme}://{u.netloc}").crawl_delay, 30))
        wait = self.last.get(host, 0) + delay - time.time()
        if wait > 0:
            time.sleep(wait)
        for attempt in range(3):
            try:
                r = self.s.get(url, timeout=self.timeout, **kw)
                self.last[host] = time.time()
                if r.status_code == 200:
                    self.stats["ok"] += 1
                    return r.json() if as_json else r.text
                if r.status_code in (429, 503) and attempt < 2:
                    time.sleep(15 * (attempt + 1))
                    continue
                self.stats["http_error"] += 1
                log.warning("HTTP %s %s :: %s", r.status_code, url, re.sub(r"\s+", " ", r.text[:160]))
                return None
            except (requests.RequestException, ValueError) as e:
                self.last[host] = time.time()
                if attempt == 2:
                    self.stats["http_error"] += 1
                    log.warning("fetch failed %s: %s", url, e)
                    return None
                time.sleep(5)


def to_num(s):
    """'17,899.00 جنيه' / 'EGP 17,899' / 17899.0 -> 17899 (int) or 0."""
    if s is None:
        return 0
    if isinstance(s, (int, float)):
        return int(round(s))
    s = str(s).translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    m = re.search(r"\d[\d,]*(?:\.\d+)?", s)
    return int(round(float(m.group(0).replace(",", "")))) if m else 0
