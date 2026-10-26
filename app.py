import streamlit as st
import pandas as pd
import datetime
import os

# -------------------------------------------------------------
# 1. إعدادات الصفحة وتهيئة السيو (SEO & Page Config)
# -------------------------------------------------------------
st.set_page_config(
    page_title="مكتبة الأحرف السبعة | المتجر الإلكتروني لعلوم القرآن والقراءات",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS & Styling (Emerald & Gold Theme)
st.markdown("""
<style>
    .stApp { direction: rtl; background-color: #F8FAF9; }
    
    /* Header Banner */
    .header-box {
        background: linear-gradient(135deg, #0B3C26 0%, #1F5E3B 100%);
        padding: 25px;
        border-radius: 15px;
        color: #FFD700;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }
    .header-title { font-size: 32px; font-weight: bold; margin-bottom: 8px; font-family: 'Amiri', serif; }
    .header-sub { font-size: 16px; color: #E8F5E9; }

    /* Book Card Styling */
    .book-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .book-title { font-size: 18px; font-weight: bold; color: #0B3C26; margin-bottom: 5px; }
    .book-cat { font-size: 13px; color: #666; background-color: #E8F5E9; padding: 2px 8px; border-radius: 10px; display: inline-block; }
    .book-price { font-size: 20px; font-weight: bold; color: #B8860B; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# Create uploads folder for images if not exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# -------------------------------------------------------------
# 2. تهيئة قاعدة البيانات بمكتبة القراءات والمتون الأساسية
# -------------------------------------------------------------
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {
            "id": 1, 
            "title": "مصحف الصحابة (طبعة دار الصحابة / توفيق ضمرة)", 
            "buy_price": 300.0, "sell_price": 360.0, "qty": 15, 
            "category": "مصاحف القراءات", 
            "author": "الشيخ توفيق ضمرة", 
            "image": ""
        },
        {
            "id": 2, 
            "title": "متن الشاطبية (حرز الأماني ووجه التهاني في القراءات السبع)", 
            "buy_price": 70.0, "sell_price": 90.0, "qty": 30, 
            "category": "المتون", 
            "author": "الإمام الشاطبي", 
            "image": ""
        },
        {
            "id": 3, 
            "title": "متن الدرة المضيئة في القراءات الثلاث المتممة للعشر", 
            "buy_price": 50.0, "sell_price": 70.0, "qty": 20, 
            "category": "المتون", 
            "author": "الإمام ابن الجزري", 
            "image": ""
        },
        {
            "id": 4, 
            "title": "متن طيبة النشر في القراءات العشر", 
            "buy_price": 90.0, "sell_price": 120.0, "qty": 25, 
            "category": "المتون", 
            "author": "الإمام ابن الجزري", 
            "image": ""
        },
        {
            "id": 5, 
            "title": "متن المقدمة الجزرية في تجود القرآن", 
            "buy_price": 30.0, "sell_price": 45.0, "qty": 40, 
            "category": "المتون", 
            "author": "الإمام ابن الجزري", 
            "image": ""
        },
        {
            "id": 6, 
            "title": "الوافي في شرح الشاطبية في القراءات السبع", 
            "buy_price": 220.0, "sell_price": 270.0, "qty": 12, 
            "category": "الشروحات", 
            "author": "د. عبد الفتاح القاضي", 
            "image": ""
        },
        {
            "id": 7, 
            "title": "البرهان في تجويد القرآن (مع شرح الجزرية)", 
            "buy_price": 100.0, "sell_price": 130.0, "qty": 15, 
            "category": "الشروحات", 
            "author": "الشيخ محمد الصادق قمحاوي", 
            "image": ""
        },
        {
            "id": 8, 
            "title": "كتاب قالون عن نافع (سلسلة تقريب القراءات)", 
            "buy_price": 110.0, "sell_price": 140.0, "qty": 18, 
            "category": "سلسلة ضمرة", 
            "author": "الشيخ توفيق ضمرة", 
            "image": ""
        },
        {
            "id": 9, 
            "title": "مقنع الداني في رسم المصاحف العثمانية", 
            "buy_price": 150.0, "sell_price": 190.0, "qty": 10, 
            "category": "رسم وضبط المصحف", 
            "author": "الإمام أبو عمرو الداني", 
            "image": ""
        },
        {
            "id": 10, 
            "title": "التنزيل في رسم المصحف وضبطه", 
            "buy_price": 130.0, "sell_price": 170.0, "qty": 10, 
            "category": "رسم وضبط المصحف", 
            "author": "د. أحمد حسن فرحات", 
            "image": ""
        },
        {
            "id": 11, 
            "title": "ألفية ابن مالك في النحو والصرف", 
            "buy_price": 60.0, "sell_price": 80.0, "qty": 25, 
            "category": "كتب اللغة والنحو", 
            "author": "الإمام ابن مالك الطائي", 
            "image": ""
        }
    ])

if 'customer_cart' not in st.session_state:
    st.session_state.customer_cart = []

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# Header Banner
st.markdown("""
<div class="header-box">
    <div class="header-title">📖 مَكْتَبَةُ الأَحْرُفِ السـ7ـبْعَة</div>
    <div class="header-sub">المتجر المتخصص في متون وكتب القراءات والمصاحف وعلوم القرآن</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📌 Navigation / القائمة")
mode = st.sidebar.radio("اختر الواجهة:", ["🛍️ المتجر الإلكتروني (للعملاء)", "🔒 لوحة تحكم الإدارة (خاص بالمالك)"])

# =============================================================
# 🛍️ WAJHA 1: المتجر الإلكتروني للعملاء (Customer Storefront)
# =============================================================
if mode == "🛍️ المتجر الإلكتروني (للعملاء)":
    
    st.subheader("🔍 تصفح وابحث في المكتبة")
    
    col_search1, col_search2 = st.columns([3, 1])
    with col_search1:
        search_kw = st.text_input("ابحث عن كتاب، مؤلف، أو موضوع:", "", placeholder="مثال: الشاطبية، الجزرية، القاضي...")
    with col_search2:
        categories = ["الكل"] + list(st.session_state.inventory['category'].unique())
        selected_cat = st.selectbox("التصنيف:", categories)

    # Filtering Books
    df_books = st.session_state.inventory.copy()
    if search_kw:
        df_books = df_books[df_books['title'].str.contains(search_kw, case=False) | df_books['author'].str.contains(search_kw, case=False)]
    if selected_cat != "الكل":
        df_books = df_books[df_books['category'] == selected_cat]

    st.markdown("---")
    st.markdown("### 📚 الكتب المتوفرة في المكتبة")

    # Display Books Grid
    cols = st.columns(2)
    for idx, book in df_books.iterrows():
        col_idx = idx % 2
        with cols[col_idx]:
            # Display image if exists
            if book.get('image') and os.path.exists(book['image']):
                st.image(book['image'], use_container_width=True)
            
            st.markdown(f"""
            <div class="book-card">
                <div class="book-title">{book['title']}</div>
                <div style="color: #555; font-size: 14px;">المؤلف/المحقق: {book['author']}</div>
                <span class="book-cat">{book['category']}</span>
                <div class="book-price">{book['sell_price']:,.2f} ج.م</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add to Cart Button
            avail = int(book['qty'])
            if avail > 0:
                col_btn1, col_btn2 = st.columns([1, 2])
                with col_btn1:
                    qty_to_buy = st.number_input("الكمية:", min_value=1, max_value=avail, value=1, key=f"qty_{book['id']}")
                with col_btn2:
                    st.write(" ")
                    if st.button("🛒 إضافة للسلة", key=f"btn_{book['id']}"):
                        st.session_state.customer_cart.append({
                            "title": book['title'],
                            "price": book['sell_price'],
                            "qty": qty_to_buy,
                            "total": book['sell_price'] * qty_to_buy
                        })
                        st.success(f"تمت إضافة '{book['title']}' إلى سلة التسوق!")
            else:
                st.error("عذراً، نفدت الكمية حالياً")

    # 🛒 Customer Shopping Cart & Checkout Section
    st.markdown("---")
    st.markdown("## 🛒 سلة التسوق وإتمام الطلب")
    
    if st.session_state.customer_cart:
        cart_df = pd.DataFrame(st.session_state.customer_cart)
        st.dataframe(cart_df[['title', 'price', 'qty', 'total']], use_container_width=True)
        
        books_total = cart_df['total'].sum()
        shipping_cost = 60.0  # Default shipping
        grand_total = books_total + shipping_cost

        st.markdown(f"#### إجمالي الكتب: **{books_total:,.2f} ج.م** | الشحن: **{shipping_cost:,.2f} ج.م**")
        st.markdown(f"### الإجمالي الكلي: <span style='color:#0B3C26;'>**{grand_total:,.2f} ج.م**</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📝 بيانات الشحن والتوصيل")
        with st.form("checkout_form"):
            c_name = st.text_input("الاسم بالكامل:")
            c_phone = st.text_input("رقم الهاتف (واتساب):")
            c_address = st.text_input("العنوان التفصيلي والمدينة:")
            c_notes = st.text_area("ملاحظات إضافية على الطلب (اختياري):")

            submit_order = st.form_submit_button("✅ تأكيد وإرسال الطلب")
            if submit_order:
                if c_name and c_phone and c_address:
                    order_id = len(st.session_state.orders) + 1001
                    st.session_state.orders.append({
                        "order_id": order_id,
                        "date": datetime.date.today().strftime("%Y-%m-%d"),
                        "customer_name": c_name,
                        "phone": c_phone,
                        "address": c_address,
                        "notes": c_notes,
                        "total": grand_total,
                        "status": "قيد المراجعة",
                        "items": st.session_state.customer_cart.copy()
                    })
                    st.session_state.customer_cart = []
                    st.balloons()
                    st.success(f"تم إرسال طلبك بنجاح! رقم الطلب: #{order_id}. سنتواصل معك قريباً عبر الواتساب لتأكيد الشحن.")
                else:
                    st.error("يرجى ملء جميع البيانات الأساسية (الاسم، الهاتف، والعنوان).")
    else:
        st.info("سلة التسوق فارغة حالياً. اضغط على 'إضافة للسلة' عند أي كتاب تود شراءه.")

# =============================================================
# 🔒 WAJHA 2: لوحة تحكم الإدارة (Admin Panel)
# =============================================================
else:
    st.subheader("🔒 لوحة تحكم مالك المكتبة")

    # Login Logic
    if not st.session_state.admin_logged_in:
        pwd = st.text_input("أدخل كلمة مرور الإدارة:", type="password")
        if st.button("تسجيل الدخول"):
            if pwd == "1234":  # Password
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    else:
        st.sidebar.button("🚪 تسجيل الخروج", on_click=lambda: st.session_state.update({"admin_logged_in": False}))
        
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📋 طلبات العملاء الجديدة", "📦 إدارة المخزون والأسعار", "➕ إضافة كتاب جديد"])

        # Tab 1: Orders
        with admin_tab1:
            st.markdown("### 📋 طلبات الشراء القادمة من المتجر")
            if st.session_state.orders:
                orders_df = pd.DataFrame(st.session_state.orders)
                st.dataframe(orders_df[['order_id', 'date', 'customer_name', 'phone', 'total', 'status']], use_container_width=True)
                
                selected_ord_id = st.selectbox("اختر رقم الطلب لعرض تفاصيله:", orders_df['order_id'].tolist())
                ord_data = next(item for item in st.session_state.orders if item["order_id"] == selected_ord_id)
                
                st.write(f"**اسم العميل:** {ord_data['customer_name']}")
                st.write(f"**الهاتف:** {ord_data['phone']}")
                st.write(f"**العنوان:** {ord_data['address']}")
                st.write(f"**الأصناف المطلوبة:**")
                st.table(pd.DataFrame(ord_data['items']))
            else:
                st.info("لا توجد طلبات جديدة حتى الآن.")

        # Tab 2: Inventory
        with admin_tab2:
            st.markdown("### 📦 المخزون الحالي والأسعار")
            st.dataframe(st.session_state.inventory, use_container_width=True)

        # Tab 3: Add Book with Image Upload
        with admin_tab3:
            st.markdown("### ➕ إضافة كتاب جديد للمكتبة مع صورة الغلاف")
            with st.form("admin_add_book"):
                b_title = st.text_input("اسم الكتاب:")
                b_author = st.text_input("المؤلف / المحقق:")
                b_cat = st.selectbox("التصنيف:", ["مصاحف القراءات", "المتون", "الشروحات", "رسم وضبط المصحف", "سلسلة ضمرة", "كتب اللغة والنحو", "أخرى"])
                b_buy = st.number_input("سعر الشراء (التكلفة):", value=50.0)
                b_sell = st.number_input("سعر البيع للعميل:", value=100.0)
                b_qty = st.number_input("الكمية بالمخزون:", value=10)
                
                b_image = st.file_uploader("صورة غلاف الكتاب (اختر صورة من جهازك):", type=["jpg", "png", "jpeg"])
                
                if st.form_submit_button("حفظ الكتاب بالمكتبة"):
                    image_path = ""
                    if b_image is not None:
                        image_path = os.path.join("uploads", b_image.name)
                        with open(image_path, "wb") as f:
                            f.write(b_image.getbuffer())

                    new_id = len(st.session_state.inventory) + 1
                    new_row = {
                        "id": new_id, 
                        "title": b_title, 
                        "author": b_author, 
                        "buy_price": b_buy, 
                        "sell_price": b_sell, 
                        "qty": b_qty, 
                        "category": b_cat,
                        "image": image_path
                    }
                    st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"تمت إضافة الكتاب '{b_title}' بنجاح مع الصورة!")
