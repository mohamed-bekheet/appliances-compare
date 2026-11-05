# مقارنة الأجهزة الكهربائية

## الملفات
- `index.html` — واجهة المقارنة (افتح في أي متصفح)
- `data.json`  — قاعدة البيانات (أضف منتجات هنا)

## إزاي تضيف منتج جديد؟
افتح `data.json` وأضف entry جديدة في آخر array الـ `products`:

```json
{
  "id": 57,
  "name": "اسم الجهاز",
  "brand": "الماركة",
  "category": "بوتاجاز | شفاط | مسطح غاز | مسطح كهرباء | فرن | مايكروويف | غسالة | باكدج",
  "features": ["ميزة 1", "ميزة 2"],
  "price_before": 10000,
  "price_after": 9000,
  "discount_pct": 10,
  "shop": "B.TECH | Carrefour | Hyper One | ...",
  "source": "Facebook post / website / ..."
}
```

### حقول اختيارية حسب نوع الجهاز
| الجهاز | الحقول الإضافية |
|--------|----------------|
| غسالة  | `capacity_kg`, `spin_rpm`, `energy_class`, `programs`, `noise_db`, `motor_class` (dd/inverter/unknown), `motor_type`, `made_in`, `made_in_verified`, `drum_material`, `motor_warranty_years`, `rating`, `reviews_count`, `rating_source`, `review_summary`, `dryer_capacity_kg` |
| ثلاجة  | `capacity_liters`, `energy_class` |
| بوتاجاز | `burners`, `oven_capacity_liters`, `gas_consumption_kg_h` |
| شفاط   | `width_cm`, `speeds`, `power_w`, `noise_db` |
| فرن    | `capacity_liters`, `width_cm`, `power_w` |
| مسطح   | `burners`, `width_cm` |
| مايكروويف | `capacity_liters`, `power_w` |
| باكدج  | `bundle_items: ["item 1", "item 2"]` |

## المتاجر المقترحة للمقارنة
- B.TECH
- Carrefour Egypt
- Hyper One
- El Araby
- Raya

## 🏆 ترشيح أفضل قيمة مقابل السعر (الغسالات)
لما الفلتر الحالي فيه غسالتين أو أكتر، الموقع بيعرض لوحة ترشيح: أفضل قيمة، وأعلى جودة، وبديل قوي، والأرخص.

- **درجة الجودة**: نوع الموتور (دفع مباشر 25، انفرتر 18، غير محدد 10) + اللفات (حتى 10) + السعة (2 لكل كيلو، حتى 26) + بخار 5 + Wi-Fi 3 + مجفف 6 + ضمان موتور 10 سنين 5 + بلد الصنع (أوروبا 8، تركيا/مصر 6، غير محدد 4) + سمعة الماركة وشبكة الصيانة (**تقديري**، حتى 10) + تقييم العملاء (التقييمات الأقل من 3 بتاخد نص الوزن).
- **مؤشر القيمة** = الجودة ÷ السعر، والأفضل في الفلتر الحالي بياخد 100.
- أوزان سمعة الماركات موجودة في `BRAND_TIER` جوه `index.html` ولو حابب تعدّلها عدّلها من هناك.
- `made_in_verified: false` معناها إن بلد الصنع **مش مؤكد** من مصدر رسمي.
