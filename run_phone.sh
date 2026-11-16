#!/data/data/com.termux/files/usr/bin/bash
# Android (Termux): scrape the stores that block cloud servers, then push the results.
# GitHub Actions merges them into data.json automatically. Takes ~1 hour.
# First-time setup is in README_PHONE.md.
set -e
cd "$(dirname "$0")"
termux-wake-lock 2>/dev/null || true          # keep the phone awake while scraping
echo "==== [1/4] git pull";                      git pull --rebase
echo "==== [2/4] python packages";               python -m pip install -q -r tools/scrape/requirements.txt
echo "==== [3/4] scraping (about 40 minutes)";       python -u tools/scrape/run.py --stores berty,elaraby --dry-run --out scraped/local
echo "==== [4/4] pushing";                        git add scraped/local
git commit -m "Phone scrape $(date +%F)" || echo "nothing new to commit"
git pull --rebase && git push
termux-wake-unlock 2>/dev/null || true
echo "Done. GitHub merges the results into the site in a few minutes."
