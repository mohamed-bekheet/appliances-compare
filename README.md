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
| غسالة  | `capacity_kg`, `spin_rpm`, `energy_class`, `programs`, `noise_db` |
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
