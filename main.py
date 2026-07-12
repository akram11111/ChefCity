import flet as ft
from products import products  # استيراد قائمة المنتجات من ملفك
import urllib.parse  # لترميز نصوص الرسائل بشكل صحيح للروابط

def main(page: ft.Page):
    page.title = "منيو مطعم Chef City الإلكتروني"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True  # تفعيل الواجهة باللغة العربية بالكامل

    # 📞 ضع هنا رقم هاتف الواتساب الخاص بمطعمك (مع رمز الدولة وبدون أصفار أو علامة +)
    RESTAURANT_WHATSAPP = "9647817651238" # تأكد من وضع رقمك الحقيقي هنا

    # تفعيل الخط العربي المرفوع مباشرة (تم تصحيح المسار ليتوافق مع الويب)
    page.fonts = {"CustomArabic": "Cairo.ttf"}
    page.theme = ft.Theme(font_family="CustomArabic")

    # سلة المشتريات (الطلبات الحالية للزبون)
    cart = {}

    # حقول معلومات الزبون المطلوبة للتوصيل
    customer_phone = ft.TextField(label="رقم الهاتف للتواصل معكم ", height=45, text_size=13, keyboard_type=ft.KeyboardType.NUMBER)
    customer_address = ft.TextField(label="عنوان التوصيل بدقة", height=45, text_size=13, hint_text="المنطقة / اقرب نقطة داله   ")

    # عناصر واجهة السلة الجانبية
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

    # دالة إرسال الطلب عبر الواتساب
    def send_order_to_whatsapp(e):
        if not cart:
            page.snack_bar = ft.SnackBar(ft.Text("سلة الطلبات فارغة! اختر وجباتك أولاً."), bgcolor="red600")
            page.snack_bar.open = True
            page.update()
            return
        
        if not customer_name.value or not customer_phone.value or not customer_address.value:
            page.snack_bar = ft.SnackBar(ft.Text("كملت طلبك .. رجاءا رقم الهاتف ضروري!"), bgcolor="orange800")
            page.snack_bar.open = True
            page.update()
            return

        message = f"📌 *طلب جديد من المنيو الإلكتروني - ChefCity* 📌\n\n"
        message += f"👤 *الزبون:* {customer_name.value}\n"
        message += f"📞 *الهاتف:* {customer_phone.value}\n"
        message += f"📍 *العنوان:* {customer_address.value}\n\n"
        message += f"📋 *الطلبات:* \n"
        
        total_price = 0
        for item_name, details in cart.items():
            item_total = details["price"] * details["quantity"]
            total_price += item_total
            message += f"▪️ {item_name} (الكمية: {details['quantity']}) -> {item_total:,} د.ع\n"
        
        message += f"\n💰 *المجموع الإجمالي:* {total_price:,} د.ع"
        
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me{RESTAURANT_WHATSAPP}?text={encoded_message}"
        page.launch_url(whatsapp_url)

    # بناء شبكة المنتجات (المنيو)
    menu_grid = ft.GridView(
        expand=True, runs_count=4, max_extent=140, child_aspect_ratio=0.75, spacing=8, run_spacing=8,
    )

    for item_name, item_price in products:
        # ✨ حل مشكلة الشاشة البيضاء: توليد مسار ويب متوافق مع استضافة GitHub Pages
        image_path = f"assets/{item_name}.png"
        
        menu_grid.controls.append(
            ft.Container(
                content=ft.Card(
                    elevation=2,
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Image(src=image_path, width=90, height=90, fit="contain"),
                                ft.Text(item_name, size=11, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, max_lines=1),
                                ft.Text(f"{item_price:,} د.ع", size=11, color="bluegrey700"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
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

    def build_responsive_layout():
        menu_container = ft.Container(
            content=ft.Column([ft.Text("قائمة مأكولات ومشروبات المطعم 🍽️", size=16, weight=ft.FontWeight.BOLD), menu_grid], expand=True),
            padding=5
        )
        
        invoice_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("بيانات التوصيل والزبون 👤", size=11, weight=ft.FontWeight.BOLD),
                    customer_name, customer_phone, customer_address,
                    ft.Divider(height=5),
                    ft.Text("سلة مشترياتك 🛒", size=14, weight=ft.FontWeight.BOLD),
                    ft.Container(content=invoice_header, padding=5),
                    cart_items_list,
                    ft.Divider(height=5),
                    lbl_total,
                    ft.ElevatedButton("إرسال الطلب عبر الواتساب 📲", on_click=send_order_to_whatsapp, bgcolor="green700", color="white", width=float("inf"), height=42)
                ],
                expand=True
            ),
            padding=10, bgcolor="grey200", border_radius=8
        )

        if page.width < 600:
            return ft.Column([ft.Container(menu_container, height=380), ft.Container(invoice_container, expand=True)], expand=True)
        else:
            return ft.Row([ft.Container(menu_container, expand=7), ft.Container(invoice_container, expand=3)], expand=True)

    def on_page_resize(e):
        page.controls.clear()
        page.add(build_responsive_layout())
        page.update()

    page.on_resize = on_page_resize
    page.add(build_responsive_layout())

ft.app(target=main)
