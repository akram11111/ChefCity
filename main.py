import flet as ft
from products import products  # استيراد قائمة المنتجات من ملفك

def main(page: ft.Page):
    page.title = "نظام كاشير الوجبات السريعة الاحترافي"
    page.window_width = 1200
    page.window_height = 750
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True  # تفعيل الواجهة باللغة العربية بالكامل

    # تفعيل الخط العربي
    page.fonts = {"CustomArabic": "fonts/Cairo.ttf"}
    page.theme = ft.Theme(font_family="CustomArabic")

    # سلة المشتريات (الفاتورة الحالية)
    cart = {}

    # حقول معلومات الزبون
    customer_name = ft.TextField(label="اسم الزبون", height=40, text_size=12)
    customer_phone = ft.TextField(label="رقم الهاتف", height=40, text_size=12, keyboard_type=ft.KeyboardType.NUMBER)

    # عناصر واجهة الفاتورة الجانبية
    cart_items_list = ft.ListView(expand=True, spacing=5)
    lbl_total = ft.Text("المجموع: 0 د.ع", size=20, weight=ft.FontWeight.BOLD, color="green800")

    # دالة لتحديث واجهة الفاتورة الحية بنظام الأعمدة المحاذية
    def update_cart_ui():
        cart_items_list.controls.clear()
        total_price = 0
        
        for item_name, details in cart.items():
            item_total = details["price"] * details["quantity"]
            total_price += item_total
            
            # بناء سطر الفاتورة كأعمدة منظمة ومنحازة تلقائياً
            cart_items_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            # العمود الأول: اسم المنتج
                            ft.Text(item_name, weight=ft.FontWeight.BOLD, size=12, expand=4, max_lines=1),
                            
                            # العمود الثاني: التحكم بالكمية والزيادة والنقصان
                            ft.Row(
                                [
                                    ft.TextButton("-", on_click=lambda e, name=item_name: change_quantity(name, -1), width=30),
                                    ft.Text(str(details["quantity"]), size=13, weight=ft.FontWeight.BOLD),
                                    ft.TextButton("+", on_click=lambda e, name=item_name: change_quantity(name, 1), width=30),
                                ],
                                expand=3,
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=0
                            ),
                            
                            # العمود الثالث: السعر الإجمالي للمنتج
                            ft.Text(f"{item_total:,} د.ع", size=12, expand=3, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.W_500),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=5,
                    bgcolor="white",
                    border_radius=5
                )
            )
        
        lbl_total.value = f"المجموع: {total_price:,} د.ع"
        page.update()

    # دالة إضافة الوجبة عند النقر
    def add_to_cart(name, price):
        if name in cart:
            cart[name]["quantity"] += 1
        else:
            cart[name] = {"price": price, "quantity": 1}
        update_cart_ui()

    # دالة تعديل الكمية
    def change_quantity(name, change):
        if name in cart:
            cart[name]["quantity"] += change
            if cart[name]["quantity"] <= 0:
                del cart[name]
        update_cart_ui()

    # دالة مسح الطلب وتأكيده
    def checkout(e):
        if not cart:
            return
        cart.clear()
        customer_name.value = ""
        customer_phone.value = ""
        update_cart_ui()
        page.snack_bar = ft.SnackBar(ft.Text("تمت طباعة الفاتورة بنجاح! 🧾"), bgcolor="green700")
        page.snack_bar.open = True
        page.update()

    # بناء شبكة المنتجات (المنيو)
    menu_grid = ft.GridView(
        expand=True,
        runs_count=4,
        max_extent=165,
        child_aspect_ratio=0.8,
        spacing=8,
        run_spacing=9,
        
    )

    for item_name, item_price in products:
        menu_grid.controls.append(
            ft.Container(
                content=ft.Card(
                    elevation=2,
                    bgcolor="orange250",     # يمكنك تغيير لون خلفية البطاقة بالكامل من هنا ⬇️
                                     # أمثلة للألوان المتاحة: "white", "amber50", "orange50", "bluegrey50"
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Image(src=f"images/{item_name}.png", width=135, height=130, fit="contain"),
                                #ft.Text(item_name, size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, max_lines=1),
                                ft.Text(f"{item_price:,} د.ع", size=11,weight=ft.FontWeight.BOLD, color="amber50"),
                                #ft.Row([ft.Text("إضافة سريعة +", color="orange700", size=10, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=6
                    )
                ),
                on_click=lambda e, n=item_name, p=item_price: add_to_cart(n, p)
            )
        )

    # الرأس التوضيحي للأعمدة داخل الفاتورة (اسم المنتج | الكمية | السعر)
    invoice_header = ft.Row(
        [
            ft.Text("نوعية الطعام ", size=12, weight=ft.FontWeight.BOLD, color="bluegrey700", expand=4),
            ft.Text("الكمية", size=12, weight=ft.FontWeight.BOLD, color="bluegrey700", expand=3, text_align=ft.TextAlign.CENTER),
            ft.Text("السعر", size=12, weight=ft.FontWeight.BOLD, color="bluegrey700", expand=3, text_align=ft.TextAlign.LEFT),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # تقسيم الشاشة الرئيسي الثابت (المنيو 70% والفاتورة 30%)
    main_layout = ft.Row(
        [
            # قسم المنيو
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("قائمة الوجبات والمنتجات 🍽️", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(height=5),
                        menu_grid
                    ],
                    expand=True
                ),
                expand=7,
                padding=10
            ),
            
            # قسم الفاتورة الجانبي المتناسق بنظام الأعمدة القياسي (تم تبسيط الـ padding هنا لتجنب الأخطاء)
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("بيانات الزبون 👤", size=15, weight=ft.FontWeight.BOLD),
                        customer_name,
                        customer_phone,
                        ft.Divider(height=10),
                        #ft.Text("الفاتورة الحالية 🛒", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(content=invoice_header, padding=5), # تم تعديل التنسيق لـ رقم مباشر مضمون
                        ft.Divider(height=5),
                        cart_items_list, # قائمة السلع المنظمة كجدول
                        ft.Divider(height=10),
                        lbl_total,
                        ft.Container(height=5),
                        ft.ElevatedButton(
                            "تأكيد وطباعة الطلب", 
                            on_click=checkout, 
                            bgcolor="green700", 
                            color="white", 
                            width=float("inf"),
                            height=45
                        )
                    ],
                    expand=True
                ),
                expand=3,
                padding=12,
                bgcolor="grey200",
                border_radius=8
            )
        ],
        expand=True
    )

    page.add(main_layout)

ft.app(target=main, assets_dir=".")