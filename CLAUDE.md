# appliances-compare — guide for any new chat / agent

Read this first. It explains what the project is, how the data flows, and what to do when the owner
sends something in chat. The owner writes in Egyptian Arabic (sometimes English); answer in Egyptian Arabic.

## What this is
A price-comparison site for home appliances sold in Egypt: washing machines, fridges, deep freezers,
cookers, ovens, hobs, hoods, microwaves, dishwashers, dryers, water heaters, bundles.
Goal: for every device, show **where it is cheapest** and **which one is the best value**.

- Site (GitHub Pages): https://mohamed-bekheet.github.io/appliances-compare/
- Repo: `mohamed-bekheet/appliances-compare`, branch `main`. GitHub Pages deploys `main` automatically.
- The owner's laptop clone (Windows): `E:\Personal\compare_appliances`. Use that path if anything
  must run on the laptop (for example `run_local.bat`).

## Ground rules
1. **Always commit and push your changes to `main`** when a task is done; the owner expects the repo to
   be up to date. Keep `data.json` valid JSON (`python3 -c "import json;json.load(open('data.json'))"`).
2. Never invent prices, specs or model numbers. Each value comes from a source you saw (photo, store
   page, official spec page). If unsure, leave the field out and say so.
3. Respect each site's robots.txt and rate limits. Never get around a block (no fake browser
   user-agents, proxies, mirrors, caches, or private APIs with harvested tokens). If a site refuses,
   report it.
4. Keep the UI in Arabic, right-to-left.

## Files
| path | what |
|---|---|
| `index.html` | the whole site (static, RTL Arabic, vanilla JS); loads `data.json` |
| `data.json` | `{"meta": {...}, "products": [...]}`: one entry per **listing** (same device in 3 shops = 3 entries) |
| `tools/pricebook.py` | `model_key()` / `product_key()`: how the same model is recognised across shops |
| `tools/upsert.py` | add/update listings and keep price history (`python3 tools/upsert.py items.json --date YYYY-MM-DD`) |
| `tools/to_check.py` | lists listings that have URLs (oldest first) |
| `tools/scrape/` | the scraper: `run.py`, `stores.py` (one adapter per store), `normalize.py`, `common.py`, `merge.py` |
| `.github/workflows/scrape.yml` | weekly scrape (Friday 06:17 Cairo) and manual runs from the Actions tab |
| `run_local.bat` | runs the stores that block cloud servers (Carrefour, Berty, El Araby, Jumia) from the laptop |
| `scraped/` | `report.md` (summary, price changes, cheapest shop per model), per-store JSON, `local/` = laptop results |

## Listing schema (data.json → products[])
Required: `id`, `name`, `brand`, `category`, `price_after` (current EGP), `price_before` (crossed-out
price, 0 if none), `discount_pct`, `shop`, `source`, `features` (list), `history`, `first_seen`, `last_seen`.

Common optional fields: `model`, `product_key` (e.g. `TOSHIBA:TWBK100GF4`, computed, do not hand-edit),
`url`, `in_stock`, `seller` (marketplace seller), `scraped` (true = written by the scraper; hand-entered
listings have no flag and keep their own specs), `capacity_kg`, `capacity_liters`, `capacity_feet`,
`spin_rpm`, `width_cm`, `burners`, `oven_capacity_liters`, `motor_class` (`dd` / `inverter` /
`universal` / `unknown`), `motor_type`, `made_in`, `made_in_verified`, `drum_material`,
`motor_warranty_years`, `warranty_years`, `energy_class`, `annual_kwh`, `noise_db`, `programs`,
`dimensions`, `rating`, `reviews_count`, `rating_source`, `review_summary`, `model_note`, `url_note`,
`price_note`, `bundle_items`.

Categories (Arabic, must match the tabs): `غسالة`, `مجفف`, `ثلاجة`, `ديب فريزر`, `بوتاجاز`, `فرن`,
`مسطح غاز`, `مسطح كهرباء`, `شفاط`, `مايكروويف`, `غسالة أطباق`, `سخان`, `باكدج` (bundles).

`history` = `[{date, price, price_before, in_stock?}]`. A point is added only when something changed.
Do not edit history by hand: use `upsert.py`, which handles history, `last_seen` and matching.

Shop names already in use (reuse exactly): `B.TECH`, `Carrefour`, `Jumia`, `Raneen`, `Wazen`,
`Ehab Center`, `Berty Center`, `Azmy`, `Al Reyada`, `El Araby`, `Zanussi Official`, `Zanussi Showroom`,
`Cairo Sales`, `Nomor`, `Dream 2000`. For a marketplace third-party seller, use the shop name plus
`"seller": "<name>"`.

## How the site decides "best"
- Same model in several shops is grouped by `product_key` + `category`. "أرخص سعر لكل موديل" (on by
  default) shows each model once at its cheapest in-stock price. Clicking "في N محلات" opens every
  shop's price and the history chart.
- Washers get a quality score (motor type, capacity, rpm, inverter, steam, drum, warranty, brand
  reputation, rating) and a value score = quality ÷ price. Other categories rank by price and savings.
- A scraped listing not seen for 21+ days is ignored for "cheapest".
- Smart search box: parses sentences like "غسالة LG 8 كيلو انفرتر تحت 20 الف" (category, brand, shop, features, kg/liters/cm, burners, rpm, price ranges, "ارخص") into filters, shows what it understood, and "ثبّتها كفلاتر" turns them into real filter controls. With no results it suggests which filter to drop. Features are normalised to canonical names (`FEAT_CANON` in index.html). Tables render 150 rows then "اعرض أكتر".
- Filters: multi-select brand / shop / features (features = must have all) / motor, ranges for price, capacity (kg, liters or cm width by category) and discount, "in stock only". Filter state lives in the URL hash, so a filtered view can be shared.

## Scraper (automatic)
`python3 tools/scrape/run.py --stores <list|all> [--limit N] [--dry-run]`.
Stores: `btech, zanussi, jumia, ehab, wazen, raneen, azmy, alreyada` (GitHub Actions) and
`carrefour, berty, elaraby` (laptop only: they refuse cloud servers). Details per store are in
README.md. To add a store: write an adapter in `stores.py` returning raw dicts (see existing ones),
add it to `STORES` and to the workflow matrix, test with `--limit 15 --dry-run`, then push.

## When the owner sends a PICTURE in chat
Photos are usually a store shelf/price tag, a Facebook/WhatsApp offer, or a screenshot of a store page.

1. **Read the image carefully.** For every appliance in it, get: brand, model number (exact, as
   printed), category, capacity/size, the price and any old/crossed-out price, the store (logo, page
   name, shop sign, or ask), any offer conditions (installments, cash only, voucher, bundle), and the
   date if shown. Several devices in one picture means one listing each.
2. **If something essential is unreadable** (price, store, model), ask about just that one thing
   instead of guessing. If the store is unknown and can't be inferred, ask.
3. **Look for technical details** for each model with web search, preferring the brand's official
   Egyptian page, then the official global page, then big Egyptian retailers' spec tabs. Collect what
   applies to the category, e.g.:
   - washers: capacity_kg, spin_rpm, motor_class/motor_type (direct drive / inverter / universal),
     drum_material, programs, steam, Wi-Fi, energy_class, made_in, motor_warranty_years, dimensions
   - fridges/freezers: capacity_liters, no-frost/defrost, inverter, freezer position, energy_class,
     dimensions, made_in
   - cookers/ovens/hobs/hoods: width_cm, burners, full safety, oven_capacity_liters, fan/grill,
     suction m³/h for hoods
   - add the store's product URL if you find it. Ratings only from a real source (`rating_source`).
   Only record specs you found for **that exact model**; note uncertainty in `model_note`.
4. **Check for an existing entry** (same `product_key` + shop, or same URL) so you update it instead of
   duplicating. Mention if the same model is cheaper at another shop in the data.
5. **Write the listing(s)** to a temp JSON list and run
   `python3 tools/upsert.py /tmp/new.json --date <today>`. For a photo source, set `source` to e.g.
   `"Facebook post"`, `"صورة من المحل"` or the site name. Leave out `scraped`, so the scraper will only
   update price and stock later and won't overwrite your hand-checked specs.
6. Validate JSON, commit (`Add <brand> <model> from <shop> photo`), push.
7. **Reply in Arabic, briefly**: what you added or updated (model, shop, price), the key specs and where
   they came from, what you could not find, and how it compares with other shops.

## When the owner sends a LINK
Same as a picture: read the page (respect blocks; the built-in browser can read JS-heavy pages), extract
price, old price, stock, seller, model, then specs, upsert, push, report. If it is a whole store or
category, consider adding a scraper adapter instead (see above).

## Known limits
- Carrefour: only the first page of each category (robots.txt disallows `?currentPage=`).
- B.TECH, Raneen and Jumia are marketplaces: the price is the shown seller's and can change by seller.
- Midea's official site shows prices only through JavaScript, so it is not scraped.
- Model matching needs the model number in the title (about 80% of listings).
