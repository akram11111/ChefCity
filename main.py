import flet as ft
from products import products  # استيراد قائمة المنتجات من ملفك

def main(page: ft.Page):
    page.title = "نظام كاشير الوجبات السريعة الاحترافي"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True  # تفعيل الواجهة باللغة العربية بالكامل

    # تفعيل الخط العربي المرفوع مباشرة
    page.fonts = {"CustomArabic": "Cairo.ttf"}
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
            
            cart_items_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(item_name, weight=ft.FontWeight.BOLD, size=12, expand=4, max_lines=1),
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
                            ft.Text(f"{item_total:,} د.ع", size=12, expand=3, text_align=ft.TextAlign.LEFT, weight=ft.FontWeight.W_500),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=5, bgcolor="white", border_radius=5
                )
            )
        lbl_total.value = f"المجموع: {total_price:,} د.ع"
        page.update()

    def add_to_cart(name, price):
        if name in cart: cart[name]["quantity"] += 1
        else: cart[name] = {"price": price, "quantity": 1}
        update_cart_ui()

    def change_quantity(name, change):
        if name in cart:
            cart[name]["quantity"] += change
            if cart[name]["quantity"] <= 0: del cart[name]
        update_cart_ui()

    def checkout(e):
        if not cart: return
        cart.clear()
        customer_name.value = ""
        customer_phone.value = ""
        update_cart_ui()
        page.snack_bar = ft.SnackBar(ft.Text("تمت طباعة الفاتورة بنجاح! 🧾"), bgcolor="green700")
        page.snack_bar.open = True
        page.update()

    # بناء شبكة المنتجات (المنيو) وجعلها مرنة للهواتف
    menu_grid = ft.GridView(
        expand=True,
        runs_count=4,
        max_extent=140, 
        child_aspect_ratio=0.75,
        spacing=8, run_spacing=8,
    )

    for item_name, item_price in products:
        # قراءة الصورة من المسار المباشر المرفوع منفصلاً بدون اسم مجلد
        image_path = f"{item_name}.png"
        
        menu_grid.controls.append(
            ft.Container(
                content=ft.Card(
                    elevation=2,
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Image(src=image_path, width=90, height=90, fit="contain"),
                                ft.Text(item_name, size=11, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, max_lines=1),
                                ft.Text(f"{item_price:,} د.ع", size=10, color="bluegrey700"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ), padding=4
                    )
                ),
                on_click=lambda e, n=item_name, p=item_price: add_to_cart(n, p)
            )
        )

    invoice_header = ft.Row(
        [
            ft.Text("المنتج", size=11, weight=ft.FontWeight.BOLD, color="bluegrey700", expand=4),
            ft.Text("الكمية", size=11, weight=ft.FontWeight.BOLD, color="bluegrey700", expand=3, text_align=ft.TextAlign.CENTER),
            ft.Text("السعر", size=11, weight=ft.FontWeight.BOLD, color="bluegrey700", expand=3, text_align=ft.TextAlign.LEFT),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # تصميم ذكي يتغير تلقائياً حسب حجم الشاشة
    def build_responsive_layout():
        menu_container = ft.Container(
            content=ft.Column([ft.Text("قائمة الوجبات والمنتجات 🍽️", size=18, weight=ft.FontWeight.BOLD), menu_grid], expand=True),
            padding=5
        )
        
        invoice_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("بيانات الزبون 👤", size=10, weight=ft.FontWeight.BOLD),
                    customer_name, customer_phone,
                    ft.Divider(height=5),
                    ft.Text("الفاتورة الحالية 🛒", size=10, weight=ft.FontWeight.BOLD),
                    ft.Container(content=invoice_header, padding=5),
                    cart_items_list,
                    ft.Divider(height=5),
                    lbl_total,
                    ft.ElevatedButton("تأكيد وطباعة الطلب", on_click=checkout, bgcolor="green700", color="white", width=float("inf"), height=40)
                ],
                expand=True
            ),
            padding=10, bgcolor="grey200", border_radius=8
        )

        if page.width < 600:
            return ft.Column([ft.Container(menu_container, height=350), ft.Container(invoice_container, expand=True)], expand=True)
        else:
            return ft.Row([ft.Container(menu_container, expand=7), ft.Container(invoice_container, expand=3)], expand=True)

    def on_page_resize(e):
        page.controls.clear()
        page.add(build_responsive_layout())
        page.update()

    page.on_resize = on_page_resize
    page.add(build_responsive_layout())

ft.app(target=main, assets_dir=".")
