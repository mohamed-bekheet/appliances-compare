# Store probe

## twob (https://2b.com.eg)
- domains tried: ['https://2b.com.eg'] -> using https://2b.com.eg
- home title: توبي|  اكبر موقع تسوق اون لاين في مصر لشراء الالكترونيات (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 20102 (appliance-looking product URLs: 465)
- URL prefixes in sitemap: [('ar', 10054), ('en', 10048)]
- sample URLs: ['https://2b.com.eg/en/tp-link-tl-wa850re-range-extender.html', 'https://2b.com.eg/en/2b-connecting-usb-a-b-m-m-1-8m-orange-connector.html', 'https://2b.com.eg/en/tp-link-wi-fi-range-extender-300mbps-tl-wa855re.html', 'https://2b.com.eg/en/toshiba-aew-8460sp-top-load-automatic-washing-machine-8-kg-white.html', 'https://2b.com.eg/en/sharp-refrigerator-sj-pc58a-bk-no-frost-2-doors-digital-18-ft.html']
- page https://2b.com.eg/en/tp-link-tl-wa850re-range-extender.html -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "MerchantReturnPolicy", "OfferShippingDetails", "Organization", "Product", "Store", "WebSite"], "price_meta": ["product:price:amount", "product:price:currency"], "microdata_price": true, "next_data": false, "title": "TP-Link 300Mbps Universal WiFi Range Extender TL-WA850RE | 2B"}
- page https://2b.com.eg/en/2b-connecting-usb-a-b-m-m-1-8m-orange-connector.html -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "MerchantReturnPolicy", "OfferShippingDetails", "Organization", "Product", "Store", "WebSite"], "price_meta": ["product:price:amount", "product:price:currency"], "microdata_price": true, "next_data": false, "title": "2B (DC107) Printer Cable USB 2.0 -1.8M | 2B"}
- page https://2b.com.eg/en/tp-link-wi-fi-range-extender-300mbps-tl-wa855re.html -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "MerchantReturnPolicy", "OfferShippingDetails", "Organization", "Product", "Store", "WebSite"], "price_meta": ["product:price:amount", "product:price:currency"], "microdata_price": true, "next_data": false, "title": "TP-Link Wi-Fi Range Extender 300Mbps - TL-WA855RE| 2B"}
- page https://2b.com.eg/en/toshiba-aew-8460sp-top-load-automatic-washing-machine-8-kg-white.html -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "MerchantReturnPolicy", "OfferShippingDetails", "Organization", "Product", "Store", "WebSite"], "price_meta": ["product:price:amount", "product:price:currency"], "microdata_price": true, "next_data": false, "title": "Toshiba AEW-8460SP Top Load Automatic Washing Machine - 8 Kg - White|2B Egypt"}
- JSON-LD sample: {"name": "TP-Link 300Mbps Universal WiFi Range Extender - White - TL-WA850RE", "price": 819, "in_stock": true, "url": "https://2b.com.eg/en/tp-link-tl-wa850re-range-extender.html"}
- **jsonld OK: set platform=jsonld, enabled=true**

## sharaf (https://egypt.sharafdg.com)
- domains tried: ['https://egypt.sharafdg.com'] -> using https://egypt.sharafdg.com
- home title: - (check it is the right shop)
- robots.txt: unreachable (HTTP 403)
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 403
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass**

## rayashop (https://rayashop.com)
- domains tried: ['https://rayashop.com'] -> using https://rayashop.com
- home title: رايه شوب - تسوق من افضل موقع اونلاين في مصر - رايه شوب مصر (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 47930 (appliance-looking product URLs: 9522)
- URL prefixes in sitemap: [('ar', 23965), ('en', 23965)]
- sample URLs: ['https://www.rayashop.com/ar/home-theaters', 'https://www.rayashop.com/ar/refrigerators', 'https://www.rayashop.com/ar/freezers', 'https://www.rayashop.com/ar/washing-machines', 'https://www.rayashop.com/ar/dishwashers']
- page https://www.rayashop.com/ar/home-theaters -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "CollectionPage", "Organization", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "مسرح منزلي وسماعات منزلية أفضل الأسعار | راية شوب"}
- page https://www.rayashop.com/ar/refrigerators -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "CollectionPage", "Organization", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "ثلاجات في مصر أفضل الأسعار والتقسيط | راية شوب"}
- page https://www.rayashop.com/ar/freezers -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "CollectionPage", "Organization", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "ديب فريزر في مصر أفضل الأسعار والتقسيط | راية شوب"}
- page https://www.rayashop.com/ar/washing-machines -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "CollectionPage", "Organization", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "غسالات في مصر أفضل الأسعار والتقسيط | راية شوب"}
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## shaheen (https://shaheeneg.com)
- domains tried: ['https://shaheeneg.com'] -> using https://shaheeneg.com
- home title: Home - شاهين للأجهزة الكهربائية. (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: True
- home page HTTP: 200
- sitemap URLs: 833 (appliance-looking product URLs: 387)
- URL prefixes in sitemap: [('store', 769), ('%d9%85%d9%85%d9%8a%d8%b2%d8%a7%d8%aa-%d9%85%d9%86%d8%aa%d8%ac%d8%a7%d8%aa-%d8%a8%d9%8a%d8%b3%d9%84-%d8%a7%d9%84%d8%a3%d9%85%d8%b1%d9%8a%d9%83%d9%8a%d8%a9-2026-%d8%a7%d9%84%d9%85%d9%83%d8%a7%d9%86', 1), ('%d8%a7%d9%84%d9%82%d9%84%d8%a7%d9%8a%d8%a9-%d8%a7%d9%84%d9%87%d9%88%d8%a7%d8%a6%d9%8a%d8%a9-vs-%d8%a7%d9%84%d9%85%d9%8a%d9%83%d8%b1%d9%88%d9%88%d9%8a%d9%81-%d8%a7%d9%84%d9%81%d8%b1%d9%82-%d9%88%d8%a7', 1), ('elementor-35084', 1), ('33075-2', 1), ('32839-2', 1), ('%d8%aa%d9%83%d9%86%d9%88%d9%84%d9%88%d8%ac%d9%8a%d8%a7-%d8%a7%d9%84%d9%85%d9%86%d8%a7%d8%b2%d9%84-%d8%a7%d9%84%d8%b0%d9%83%d9%8a%d8%a9-%d8%a3%d8%ac%d9%87%d8%b2%d8%a9-%d9%83%d9%87%d8%b1%d8%a8%d8%a7', 1), ('%d8%a3%d9%81%d8%b6%d9%84-%d8%a3%d9%86%d9%88%d8%a7%d8%b9-%d8%a7%d9%84%d8%af%d9%81%d8%a7%d9%8a%d8%a7%d8%aa-%d9%84%d9%84%d8%b4%d8%aa%d8%a7%d8%a1-%d8%af%d9%81%d8%a7%d9%8a%d8%a9-%d8%b2%d9%8a%d8%aa%d8%8c', 1)]
- sample URLs: ['https://shaheeneg.com/%d8%a3%d8%ac%d9%87%d8%b2%d8%a9-%d8%a7%d9%84%d9%80-built-in-%d9%84%d9%84%d9%85%d8%b7%d8%a7%d8%a8%d8%ae-%d8%a7%d9%84%d8%b5%d8%ba%d9%8a%d8%b1%d8%a9-%d8%ad%d9%84%d9%88%d9%84-%d8%b0%d9%83%d9%8a%d8%a9/', 'https://shaheeneg.com/store/washing-drying/washing-machines/front-loading-washers/lg-7kg-front-load-washer-f4y2qyg6p/', 'https://shaheeneg.com/store/small-appliances/water-heaters/ariston-heater-30l/', 'https://shaheeneg.com/store/washing-drying/brands/lg/lg-11kg-top-load-washer-t11v1tehgx/', 'https://shaheeneg.com/store/washing-drying/brands/lg/lg-10kg-top-load-washer-t10v1tehg2/']
- page https://shaheeneg.com/%d8%a3%d8%ac%d9%87%d8%b2%d8%a9-%d8%a7%d9%84%d9%80-built-in-%d9%84%d9%84%d9%85%d8%b7%d8%a7%d8%a8%d8%ae-%d8%a7%d9%84%d8%b5%d8%ba%d9%8a%d8%b1%d8%a9-%d8%ad%d9%84%d9%88%d9%84-%d8%b0%d9%83%d9%8a%d8%a9/ -> HTTP 200 {"jsonld_types": ["BlogPosting", "BreadcrumbList", "ImageObject", "Organization", "Person", "WebPage", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "أجهزة الـ Built-in للمطابخ الصغيرة: حلول ذكية وعصرية للعروسين - شاهين للأجهزة ال"}
- page https://shaheeneg.com/store/washing-drying/washing-machines/front-loading-washers/lg-7kg-front-load-washer-f4y2qyg6p/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "ImageObject", "ItemPage", "Organization", "Product", "WebSite"], "price_meta": ["product:price:amount", "product:price:currency", "product:availability"], "microdata_price": false, "next_data": false, "title": "غسالة ال جي 7 كيلو تحميل أمامي F4Y2QYG6P انفرتر بالبخار 1400 لفة | شاهين"}
- page https://shaheeneg.com/store/small-appliances/water-heaters/ariston-heater-30l/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "FAQPage", "ImageObject", "ItemPage", "Organization", "Product", "WebSite"], "price_meta": ["product:price:amount", "product:price:currency", "product:availability"], "microdata_price": false, "next_data": false, "title": "Ariston Heater 30L سخان أريستون 30 لتر كهربائي Official Best | شاهين"}
- page https://shaheeneg.com/store/washing-drying/brands/lg/lg-11kg-top-load-washer-t11v1tehgx/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "ImageObject", "ItemPage", "Organization", "Product", "WebSite"], "price_meta": ["product:price:amount", "product:price:currency", "product:availability"], "microdata_price": false, "next_data": false, "title": "غسالة ال جي 11 كيلو فوق اتوماتيك T11V1TEHGX سمارت انفرتر - اسود | شاهين"}
- JSON-LD sample: {"name": "غسالة ال جي 7 كيلو تحميل أمامي F4Y2QYG6P انفرتر بالبخار 1400 لفة | شاهين", "price": 19299, "in_stock": true, "url": "https://shaheeneg.com/store/washing-drying/washing-machines/front-loading-washers/lg-7kg-front-load-washer-f4y2qyg6p/"}
- **woo: set platform=woo_all**

## abdulaziz (https://www.abdelaziz-stores.com)
- domains tried: ['https://abdulaziz.com.eg', 'https://abdulazizstores.com', 'https://www.abdelaziz-stores.com'] -> using https://www.abdelaziz-stores.com
- home title: - (check it is the right shop)
- robots.txt: unreachable (HTTP no response)
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: None
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass**

## almorshedy (https://almorshedymarts.com.eg)
- domains tried: ['https://almorshedymarts.com', 'https://almorshedy.com', 'https://almorshedymarts.com.eg'] -> using https://almorshedymarts.com.eg
- home title: - (check it is the right shop)
- robots.txt: unreachable (HTTP no response)
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: None
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass**

## awadserag (https://awadserag.com)
- domains tried: ['https://awadserag.com', 'https://awadserag.com.eg'] -> using https://awadserag.com
- home title: عوض سراج | أجهزة كهربائية بأفضل الأسعار في مصر (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 1411 (appliance-looking product URLs: 34)
- URL prefixes in sitemap: [('shop', 1394), ('helpdesk', 4), ('livechat', 2), ('website', 1), ('terms', 1), ('/', 1), ('about-us-1', 1), ('brand', 1)]
- sample URLs: ['https://www.awadserag.com/shop/category/refrigerators-freezers-55', 'https://www.awadserag.com/shop/category/refrigerators-57', 'https://www.awadserag.com/shop/category/freezers-58', 'https://www.awadserag.com/shop/category/double-door-refrigerator-76', 'https://www.awadserag.com/shop/category/combi-refrigerators-75']
- page https://www.awadserag.com/shop/category/refrigerators-freezers-55 -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": true, "next_data": false, "title": "ثلاجات وفريزرات بأفضل الأسعار في مصر | عوض سراج"}
- page https://www.awadserag.com/shop/category/refrigerators-57 -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": true, "next_data": false, "title": "أحدث أنواع الثلاجات نوفروست وديفروست أسعار مميزة | عوض سراج"}
- page https://www.awadserag.com/shop/category/freezers-58 -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": true, "next_data": false, "title": "أسعار وأنواع الفريزرات - فريزرات رأسي وأفقي  | عوض سراج"}
- page https://www.awadserag.com/shop/category/double-door-refrigerator-76 -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": true, "next_data": false, "title": "ثلاجات بابين | أسعار ثلاجة 2 باب في مصر | عوض سراج"}
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## boschhome (https://bosch-home.com.eg)
- domains tried: ['https://www.bosch-home.com.eg', 'https://bosch-home.com.eg'] -> using https://bosch-home.com.eg
- home title: - (check it is the right shop)
- robots.txt: unreachable (HTTP no response)
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: None
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass**

## cairocart (https://cairocart.com)
- domains tried: ['https://cairocart.com', 'https://www.cairocart.com'] -> using https://cairocart.com
- home title: CairoCart (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 14069 (appliance-looking product URLs: 4951)
- URL prefixes in sitemap: [('en', 14069)]
- sample URLs: ['https://cairocart.com/en/tvs-audio/home-theaters.html', 'https://cairocart.com/en/home-appliances/large-appliances/refrigerators-freezers.html', 'https://cairocart.com/en/home-appliances/large-appliances/washing-machines-dryers/washingmachines.html', 'https://cairocart.com/en/home-appliances/large-appliances/dishwashers.html', 'https://cairocart.com/en/home-appliances/large-appliances/waterheaters.html']
- page https://cairocart.com/en/tvs-audio/home-theaters.html -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Home Theaters - TVs & Audio"}
- page https://cairocart.com/en/home-appliances/large-appliances/refrigerators-freezers.html -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Best Prices Refrigerators  & Hot Offers with Free Delivery In Egypt - Cairo Cart"}
- page https://cairocart.com/en/home-appliances/large-appliances/washing-machines-dryers/washingmachines.html -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Washing Machines - Washing Machines & Dryers - Large Appliances - Appliances"}
- page https://cairocart.com/en/home-appliances/large-appliances/dishwashers.html -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Dishwashers - Large Appliances - Appliances"}
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## elbadr (https://elbadr.com.eg)
- domains tried: ['https://elbadrgroup.com', 'https://elbadr.com.eg'] -> using https://elbadr.com.eg
- home title: - (check it is the right shop)
- robots.txt: unreachable (HTTP no response)
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: None
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass**

## elghazawy (https://elghazawy.com)
- domains tried: ['https://elghazawy.com', 'https://elghazawystores.com'] -> using https://elghazawy.com
- home title: تسوق اونلاين في مصر الكترونيات موبايلات اجهزة منزلية صحة و جمال الغزاوي (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 145570 (appliance-looking product URLs: 15008)
- URL prefixes in sitemap: [('ar', 72785), ('en', 72785)]
- sample URLs: ['https://elghazawy.com/ar/product/107480/IKU+R180+Dual+SIM+Mobile%2C+32MB+Internal+Memory%2C+32MB+RAM%2C+2G+network%2C+Orange', 'https://elghazawy.com/en/product/107480/IKU+R180+Dual+SIM+Mobile%2C+32MB+Internal+Memory%2C+32MB+RAM%2C+2G+network%2C+Orange', 'https://elghazawy.com/ar/product/137137/Viwa+F1715+Dual+SIM+Mobile%2C+32MB+Internal+Memory%2C+32MB+RAM%2C+2G+Network%2C+Orange', 'https://elghazawy.com/en/product/137137/Viwa+F1715+Dual+SIM+Mobile%2C+32MB+Internal+Memory%2C+32MB+RAM%2C+2G+Network%2C+Orange', 'https://elghazawy.com/ar/product/141146/Toshiba+TV%2C+32+Inch%2C+LED%2C+HD%2C+Built-in+Receiver%2C+32L3965EA']
- page https://elghazawy.com/ar/product/107480/IKU+R180+Dual+SIM+Mobile%2C+32MB+Internal+Memory%2C+32MB+RAM%2C+2G+network%2C+Orange -> HTTP 200 {"jsonld_types": ["Product"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "موبايل اي كي يو R180، ثنائي الشريحة، ذاكرة داخلية 32 ميجابايت، رامات 32 ميجابايت"}
- page https://elghazawy.com/en/product/107480/IKU+R180+Dual+SIM+Mobile%2C+32MB+Internal+Memory%2C+32MB+RAM%2C+2G+network%2C+Orange -> HTTP 200 {"jsonld_types": ["Product"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "IKU R180 Dual SIM Mobile, 32MB Internal Memory, 32MB RAM, 2G network, Orange Elg"}
- page https://elghazawy.com/ar/product/137137/Viwa+F1715+Dual+SIM+Mobile%2C+32MB+Internal+Memory%2C+32MB+RAM%2C+2G+Network%2C+Orange -> HTTP 200 {"jsonld_types": ["Product"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "موبايل فيوا F1715، ثنائي الشريحة، ذاكرة داخلية 32 ميجابايت، رامات 32 ميجابايت، ش"}
- page https://elghazawy.com/en/product/137137/Viwa+F1715+Dual+SIM+Mobile%2C+32MB+Internal+Memory%2C+32MB+RAM%2C+2G+Network%2C+Orange -> HTTP 200 {"jsonld_types": ["Product"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Viwa F1715 Dual SIM Mobile, 32MB Internal Memory, 32MB RAM, 2G Network, Orange E"}
- JSON-LD sample: {"name": "موبايل اي كي يو R180، ثنائي الشريحة، ذاكرة داخلية 32 ميجابايت، رامات 32 ميجابايت، شبكة الجيل الثاني، برتقالي", "price": 165, "in_stock": true, "url": "https://elghazawy.com/ar/product/107480/IKU+R180+Dual+SIM+Mobile%2C+32MB+Internal+Memory%2C+32MB+RAM%2C+2G+network%2C+Orange"}
- **jsonld OK: set platform=jsonld, enabled=true**

## elmasreyeen (https://elmasreyeen.com.eg)
- domains tried: ['https://elmasreyeen.com', 'https://elmasreyeen.com.eg'] -> using https://elmasreyeen.com.eg
- home title: - (check it is the right shop)
- robots.txt: unreachable (HTTP no response)
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: None
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass**

## gaballah (https://gaballah.com)
- domains tried: ['https://gaballah.com', 'https://gaballahstore.com', 'https://gaballah.com.eg'] -> using https://gaballah.com
- home title: اقوى العروض على الأجهزة المنزلية | تسوق الآن من جاب الله ستورز (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: True | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 3499 (appliance-looking product URLs: 1380)
- URL prefixes in sitemap: [('ar', 1749), ('products', 1572), ('collections', 161), ('pages', 12), ('blogs', 3), ('agents.md', 1), ('/', 1)]
- sample URLs: ['https://gaballah.com/products/bosch-inox-series-4-refrigerator-with-freezer-kdn43vl2e8', 'https://gaballah.com/products/bosch-serie-2-no-frost-refrigerator-328-liters-kdn43nl2e8', 'https://gaballah.com/products/toshiba-inverter-no-frost-refrigerator-395-liters-gref51gzxk', 'https://gaballah.com/products/toshiba-inverter-no-frost-refrigerator-395-liters-gref51zfs', 'https://gaballah.com/products/beko-refrigerator-rdne430k12b']
- page https://gaballah.com/products/bosch-inox-series-4-refrigerator-with-freezer-kdn43vl2e8 -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "Product"], "price_meta": ["product:price:amount", "product:price:currency", "product:availability"], "microdata_price": false, "next_data": false, "title": "Bosch 328L Top Freezer Refrigerator - KDN43VL2E8 | Egypt"}
- page https://gaballah.com/products/bosch-serie-2-no-frost-refrigerator-328-liters-kdn43nl2e8 -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "Product"], "price_meta": ["product:price:amount", "product:price:currency", "product:availability"], "microdata_price": false, "next_data": false, "title": "Bosch 328L Top Freezer Refrigerator - KDN43NL2E8 | Gaballah Stores"}
- page https://gaballah.com/products/toshiba-inverter-no-frost-refrigerator-395-liters-gref51gzxk -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "Product"], "price_meta": ["product:price:amount", "product:price:currency", "product:availability"], "microdata_price": false, "next_data": false, "title": "Toshiba Top Freezer 395 L Inverter Refrigerator - GR-EF51GZ-XK"}
- page https://gaballah.com/products/toshiba-inverter-no-frost-refrigerator-395-liters-gref51zfs -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "Product"], "price_meta": ["product:price:amount", "product:price:currency", "product:availability"], "microdata_price": false, "next_data": false, "title": "Toshiba Top Freezer 395 L Inverter Refrigerator - GR-EF51Z-FS"}
- JSON-LD sample: {"name": "Bosch Series 4 | Top Freezer 328 L Refrigerator - KDN43VL2E8", "price": 24699, "in_stock": false, "url": "https://gaballah.com/products/bosch-inox-series-4-refrigerator-with-freezer-kdn43vl2e8"}
- **shopify: set platform=shopify**

## martegypt (https://martegypt.com)
- domains tried: ['https://martegypt.com', 'https://mart-egypt.com'] -> using https://martegypt.com
- home title: مارت مصر | ماكينات حلاقة وأجهزة عناية شخصية بأفضل سعر في مصر (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: True | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 1896 (appliance-looking product URLs: 51)
- URL prefixes in sitemap: [('products', 1726), ('collections', 158), ('pages', 5), ('blogs', 5), ('agents.md', 1), ('/', 1)]
- sample URLs: ['https://martegypt.com/products/hair-dryer-hg-2288', 'https://martegypt.com/products/hair-dryer-hg-9933', 'https://martegypt.com/products/hair-dryer-hg-8800', 'https://martegypt.com/products/hair-dryer-hg-3800', 'https://martegypt.com/products/hair-dryer-hg-5554']
- page https://martegypt.com/products/hair-dryer-hg-2288 -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "FAQPage", "Product"], "price_meta": ["og:price:amount", "og:price:currency"], "microdata_price": false, "next_data": false, "title": "استشوار هوم جولد HG-2288 | سعر في مصر - مارت مصر"}
- page https://martegypt.com/products/hair-dryer-hg-9933 -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "FAQPage", "Product"], "price_meta": ["og:price:amount", "og:price:currency"], "microdata_price": false, "next_data": false, "title": "استشوار هوم جولد HG-9933 بأفضل سعر في مصر | مارت مصر"}
- page https://martegypt.com/products/hair-dryer-hg-8800 -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "FAQPage", "Product"], "price_meta": ["og:price:amount", "og:price:currency"], "microdata_price": false, "next_data": false, "title": "استشوار هوم جولد HG-8800 بأفضل سعر في مصر | مارت مصر"}
- page https://martegypt.com/products/hair-dryer-hg-3800 -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "FAQPage", "Product"], "price_meta": ["og:price:amount", "og:price:currency"], "microdata_price": false, "next_data": false, "title": "استشوار هوم جولد HG-3800 بأفضل سعر في مصر | مارت مصر"}
- JSON-LD sample: {"name": "استشوار هوم جولد HG-2288", "price": 260, "in_stock": true, "url": "https://martegypt.com/products/hair-dryer-hg-2288"}
- **shopify: set platform=shopify**

## radiotalaat (https://radiotalaat.com)
- domains tried: ['https://radiotalaat.com', 'https://radiotalaat.com.eg'] -> using https://radiotalaat.com
- home title: راديو طلعت | متجر الإلكترونيات والأجهزة المنزلية في مصر (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 12105 (appliance-looking product URLs: 2902)
- URL prefixes in sitemap: [('en', 6053), ('ar', 6052)]
- sample URLs: ['https://radiotalaat.com/ar/small-appliances/microwaves-ovens.html', 'https://radiotalaat.com/ar/large-appliances/refrigerators-freezers/refrigerators.html', 'https://radiotalaat.com/ar/large-appliances/water-heaters.html', 'https://radiotalaat.com/ar/large-appliances/washing-machines-dryers.html', 'https://radiotalaat.com/ar/large-appliances/cookers-hoods/tabletop-gas-stoves.html']
- page https://radiotalaat.com/ar/small-appliances/microwaves-ovens.html -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": false, "next_data": false, "title": "الميكروويف والأفران - ميكروويف بشواية وأفران كهربائية | راديو طلعت"}
- page https://radiotalaat.com/ar/large-appliances/refrigerators-freezers/refrigerators.html -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": false, "next_data": false, "title": "ثلاجات - نوفروست وإنفرتر وفريزر سفلي وسايد باي سايد | راديو طلعت"}
- page https://radiotalaat.com/ar/large-appliances/water-heaters.html -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": false, "next_data": false, "title": "السخانات - سخان كهرباء وفوري وغاز طبيعي وأنبوبة | راديو طلعت"}
- page https://radiotalaat.com/ar/large-appliances/washing-machines-dryers.html -> HTTP 200 {"jsonld_types": [], "price_meta": [], "microdata_price": false, "next_data": false, "title": "الغسالات والمجففات - غسالة أمامي وفوق أوتوماتيك ونشافة | راديو طلعت"}
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## rafegypt (https://raf-egypt.com)
- domains tried: ['https://rafegypt.com', 'https://raf-egypt.com'] -> using https://raf-egypt.com
- home title: - (check it is the right shop)
- robots.txt: unreachable (HTTP no response)
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: None
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass**

## rizkalla (https://rizkalla.com)
- domains tried: ['https://rizkalla.com', 'https://rizkalla.com.eg'] -> using https://rizkalla.com
- home title: - (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## hyperone (https://hyperone.com.eg)
- domains tried: ['https://hyperone.com.eg'] -> using https://hyperone.com.eg
- home title: - (check it is the right shop)
- robots.txt: unreachable (HTTP no response)
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: None
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass**

## kimo (https://kimostore.com)
- domains tried: ['https://kimostore.com', 'https://kimostore.net'] -> using https://kimostore.com
- home title: Domain For Sale (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## kenzz (https://kenzz.com)
- domains tried: ['https://kenzz.com', 'https://kenzz.com.eg'] -> using https://kenzz.com
- home title: عروض وخصومات كنز | اشتري اونلاين (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 109264 (appliance-looking product URLs: 3398)
- URL prefixes in sitemap: [('en', 54632), ('product', 51669), ('brand', 1564), ('category', 1079), ('tag', 313), ('/', 1), ('categories', 1), ('what-is-kenzz', 1)]
- sample URLs: ['https://kenzz.com/en/category/BGY3NQH3X6YN-RZ25L69CRELL-SGV8PEWZUFJR-XMAECRBVZ8MM/All/Kitchen/Tools-%26-Gadgets/Gas-Stove-Accessories', 'https://kenzz.com/en/category/BGY3NQH3X6YN-9VVS6PBBJ5ZD-UZDJZAE2A6NH-2YCKMU5A6VQA-Q9EPFPWBYWAZ/All/Automotive/Automotive-Care/Exterior-Care/Pressure-Washer', 'https://kenzz.com/en/category/BGY3NQH3X6YN-9VVS6PBBJ5ZD-UZDJZAE2A6NH-2YCKMU5A6VQA-NAVK8YUFWWM2/All/Automotive/Automotive-Care/Exterior-Care/Car-Wash-Shampoo', 'https://kenzz.com/en/category/BGY3NQH3X6YN-JBXSPWXJZH54-F7A2GNRU2XZT-UWF9EA9DD8VB-7GRSGPW89MML/All/Supermarket/Detergents/Laundry/Capsules-Detergent', 'https://kenzz.com/en/category/BGY3NQH3X6YN-JBXSPWXJZH54-F7A2GNRU2XZT-UWF9EA9DD8VB-6DZQ4YGT4N5G/All/Supermarket/Detergents/Laundry/Powder-Detergent']
- page https://kenzz.com/en/category/BGY3NQH3X6YN-RZ25L69CRELL-SGV8PEWZUFJR-XMAECRBVZ8MM/All/Kitchen/Tools-%26-Gadgets/Gas-Stove-Accessories -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "CollectionPage"], "price_meta": [], "microdata_price": false, "next_data": true, "title": "ملحقات البوتجاز"}
- page https://kenzz.com/en/category/BGY3NQH3X6YN-9VVS6PBBJ5ZD-UZDJZAE2A6NH-2YCKMU5A6VQA-Q9EPFPWBYWAZ/All/Automotive/Automotive-Care/Exterior-Care/Pressure-Washer -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "CollectionPage"], "price_meta": [], "microdata_price": false, "next_data": true, "title": "ماكينة التنظيف بالضغط"}
- page https://kenzz.com/en/category/BGY3NQH3X6YN-9VVS6PBBJ5ZD-UZDJZAE2A6NH-2YCKMU5A6VQA-NAVK8YUFWWM2/All/Automotive/Automotive-Care/Exterior-Care/Car-Wash-Shampoo -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "CollectionPage"], "price_meta": [], "microdata_price": false, "next_data": true, "title": "شامبو العربيات"}
- page https://kenzz.com/en/category/BGY3NQH3X6YN-JBXSPWXJZH54-F7A2GNRU2XZT-UWF9EA9DD8VB-7GRSGPW89MML/All/Supermarket/Detergents/Laundry/Capsules-Detergent -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "CollectionPage"], "price_meta": [], "microdata_price": false, "next_data": true, "title": "كبسولات غسيل"}
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## tabseeta (https://tabseeta.com)
- domains tried: ['https://tabseeta.com', 'https://tabseeta.com.eg'] -> using https://tabseeta.com
- home title: Tabseeta (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: True | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 799 (appliance-looking product URLs: 108)
- URL prefixes in sitemap: [('ar', 399), ('products', 295), ('collections', 79), ('pages', 21), ('blogs', 3), ('agents.md', 1), ('/', 1)]
- sample URLs: ['https://tabseeta.com/products/ariston-refrigerator-450l-art70f1452xna', 'https://tabseeta.com/products/ariston-refrigerator-342l-entm-18020-f-ex', 'https://tabseeta.com/products/bosch-refrigerator-combi-13-feet-302l-kgn36nl30u', 'https://tabseeta.com/products/haier-refrigerator-4-doors-502l-hrf-550tdpd', 'https://tabseeta.com/products/haier-washing-machine-8kg-with-steam-hw80-bp14929as6']
- page https://tabseeta.com/products/ariston-refrigerator-450l-art70f1452xna -> HTTP 200 {"jsonld_types": ["Organization", "Product"], "price_meta": ["og:price:amount", "og:price:currency"], "microdata_price": false, "next_data": false, "title": "Ariston Refrigerator 450L ART70F1452XNA\n – Tabseeta"}
- page https://tabseeta.com/products/ariston-refrigerator-342l-entm-18020-f-ex -> HTTP 200 {"jsonld_types": ["Organization", "Product"], "price_meta": ["og:price:amount", "og:price:currency"], "microdata_price": false, "next_data": false, "title": "Ariston Refrigerator 342L ENTM 18020 F (EX)\n – Tabseeta"}
- page https://tabseeta.com/products/bosch-refrigerator-combi-13-feet-302l-kgn36nl30u -> HTTP 200 {"jsonld_types": ["Organization", "Product"], "price_meta": ["og:price:amount", "og:price:currency"], "microdata_price": false, "next_data": false, "title": "BOSCH Refrigerator Combi 13 Feet 302L KGN36NL30U\n – Tabseeta"}
- page https://tabseeta.com/products/haier-refrigerator-4-doors-502l-hrf-550tdpd -> HTTP 200 {"jsonld_types": ["Organization", "Product"], "price_meta": ["og:price:amount", "og:price:currency"], "microdata_price": false, "next_data": false, "title": "Haier Refrigerator 4 Doors 502L HRF-550TDPD\n – Tabseeta"}
- JSON-LD sample: {"name": "Ariston Refrigerator 450L ART70F1452XNA", "price": 29400, "in_stock": true, "url": "https://tabseeta.com/products/ariston-refrigerator-450l-art70f1452xna"}
- **shopify: set platform=shopify**

## ovanza (https://ovanza.com)
- domains tried: ['https://ovanza.com', 'https://ovanza.com.eg'] -> using https://ovanza.com
- home title: - (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## hypertechno (https://hypertechno.com)
- domains tried: ['https://hypertechno.com.eg', 'https://hypertechno.com'] -> using https://hypertechno.com
- home title: - (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 403
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## switchplus (https://switchplus.net)
- domains tried: ['https://switchplus.com.eg', 'https://switchplus.net'] -> using https://switchplus.net
- home title: - (check it is the right shop)
- robots.txt: unreachable (HTTP 403)
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 403
- sitemap URLs: 0 (appliance-looking product URLs: 0)
- URL prefixes in sitemap: []
- sample URLs: []
- JSON-LD sample: none
- **blocked for this server (cloud IP) - try from the laptop (probe_local.bat), do not bypass**

## fresh (https://fresh.com.eg)
- domains tried: ['https://fresh.com.eg'] -> using https://fresh.com.eg
- home title: Fresh.com : فريش للأجهزة المنزلية - تسوق الأن عروض الأونلاين (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 558 (appliance-looking product URLs: 210)
- URL prefixes in sitemap: [('ar', 279), ('en', 279)]
- sample URLs: ['https://fresh.com.eg/ar/categories/washing-machines', 'https://fresh.com.eg/ar/categories/cooker-appliances', 'https://fresh.com.eg/ar/categories/cooling-appliances/refrigerators', 'https://fresh.com.eg/ar/categories/appliance/heaters', 'https://fresh.com.eg/ar/categories/cooling-appliances/refrigerators/no-frost']
- page https://fresh.com.eg/ar/categories/washing-machines -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Fresh.com : غسالات فريش - تسوق غسالة فريش أونلاين الأن"}
- page https://fresh.com.eg/ar/categories/cooker-appliances -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Fresh.com : بوتاجاز فريش - تسوق بوتاجازات فريش بأفضل الأسعار"}
- page https://fresh.com.eg/ar/categories/cooling-appliances/refrigerators -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Fresh.com : ثلاجات فريش - تسوق ثلاجة فريش الأن بأفضل أسعار"}
- page https://fresh.com.eg/ar/categories/appliance/heaters -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Fresh.com : سخانات فريش - تسوق سخان فريش أونلاين بأفضل سعر"}
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## unionaire (https://unionaire.com)
- domains tried: ['https://unionaire.com'] -> using https://unionaire.com
- home title: Home - Unionaire (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: True
- home page HTTP: 200
- sitemap URLs: 581 (appliance-looking product URLs: 402)
- URL prefixes in sitemap: [('ar', 285), ('product', 241), ('product-category', 30), ('catalogs', 3), ('/', 1), ('my-account', 1), ('offers', 1), ('about-us', 1)]
- sample URLs: ['https://unionaire.com/catalogs/freezers/', 'https://unionaire.com/catalogs/fridges/', 'https://unionaire.com/product/washing-machine-13-kg-from-unionaire-uw130tplb2pbk/', 'https://unionaire.com/product/unionaire-washing-machine-diamond-drum-touch-13-kg/', 'https://unionaire.com/product/unioanire-top-load-washing-machine-13kg/']
- page https://unionaire.com/catalogs/freezers/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "Organization", "WebPage", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Freezers - Unionaire"}
- page https://unionaire.com/catalogs/fridges/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "Organization", "WebPage", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Fridges - Unionaire"}
- page https://unionaire.com/product/washing-machine-13-kg-from-unionaire-uw130tplb2pbk/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "ImageObject", "ItemPage", "Organization", "WebPage", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Washing Machine 13 kg from Unionaire- UW130TPLB2PBK - Unionaire"}
- page https://unionaire.com/product/unionaire-washing-machine-diamond-drum-touch-13-kg/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "ImageObject", "ItemPage", "Organization", "WebPage", "WebSite"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "Washing Machine Diamond Drum Touch 13 kg from Unionaire- UW130TPLB2MBK - Unionai"}
- JSON-LD sample: none
- **woo: set platform=woo_all**

## lgeg (https://www.lg.com/eg_en)
- domains tried: ['https://www.lg.com/eg_en'] -> using https://www.lg.com/eg_en
- home title: Shop Electronics & Home Appliances at the Best Price | LG Egypt (check it is the right shop)
- robots.txt: reachable
- Shopify products.json: False | WooCommerce API: False
- home page HTTP: 200
- sitemap URLs: 2449 (appliance-looking product URLs: 601)
- URL prefixes in sitemap: [('eg_en', 2449)]
- sample URLs: ['https://www.lg.com/eg_en/about-lg/press-and-media/lg-egypt-launched-its-all-new-premium-dual-inverter-heat-pump-dryer-in-home-appliances/', 'https://www.lg.com/eg_en/about-lg/press-and-media/lg-egypt-launches-its-all-new-2022-top-freezer/', 'https://www.lg.com/eg_en/about-lg/press-and-media/lg-s-eco-conscious-bottom-freezer-shows-off-top-tier-energy-efficiency-at-ifa-2022/', 'https://www.lg.com/eg_en/about-lg/press-and-media/lg-eg-launched-all-new-neo-chef-microwave-with-smart-inverter/', 'https://www.lg.com/eg_en/about-lg/press-and-media/lg-eg-levels-up-laundry-experience-with-lg-wash-tower/']
- page https://www.lg.com/eg_en/about-lg/press-and-media/lg-egypt-launched-its-all-new-premium-dual-inverter-heat-pump-dryer-in-home-appliances/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "NewsArticle", "WebPage"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "LG Egypt launched its all-new premium DUAL Inverter Heat Pump Dryer in home appl"}
- page https://www.lg.com/eg_en/about-lg/press-and-media/lg-egypt-launches-its-all-new-2022-top-freezer/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "NewsArticle", "WebPage"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "LG Egypt launches its all-new 2022 Top Freezer"}
- page https://www.lg.com/eg_en/about-lg/press-and-media/lg-s-eco-conscious-bottom-freezer-shows-off-top-tier-energy-efficiency-at-ifa-2022/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "NewsArticle", "WebPage"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "LG’S ECO-CONSCIOUS BOTTOM-FREEZER SHOWS OFF TOP-TIER ENERGY EFFICIENCY AT IFA 20"}
- page https://www.lg.com/eg_en/about-lg/press-and-media/lg-eg-launched-all-new-neo-chef-microwave-with-smart-inverter/ -> HTTP 200 {"jsonld_types": ["BreadcrumbList", "NewsArticle", "WebPage"], "price_meta": [], "microdata_price": false, "next_data": false, "title": "LG Egypt launched its all-new Neo Chef Microwave with a smart inverter"}
- JSON-LD sample: none
- **reachable but no Product JSON-LD on the sampled pages - see page types below; a custom adapter may be possible**

## Skipped on purpose

- Amazon.eg: Amazon's terms and robots.txt forbid automated price collection
- Dubai Phone: phones/electronics, no large appliances
- e& eShop: telecom eShop
- Vodafone eShop: telecom eShop
- Orange E-Shop: telecom eShop
- Mobilaty: phones
- myXPRS: electronics
- iMedia Stores: Apple reseller
- Egypt Laptop: laptops
- Compumarts: computers
- Sigma Computer: computers
- Etisal Store: telecom
- Tradeline: Apple reseller