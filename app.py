import streamlit as st
import pandas as pd
import datetime
import os
import random

# -------------------------------------------------------------
# 1. إعدادات الصفحة والتصميم (RTL & Emerald Theme)
# -------------------------------------------------------------
st.set_page_config(
    page_title="مكتبة الأحرف السبعة | النظام الاحترافي للمتجر والمخزون",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { 
        direction: rtl !important; 
        text-align: right !important; 
        background-color: #F8FAF9; 
        font-family: 'Amiri', Tahoma, sans-serif;
    }
    .header-box {
        background: linear-gradient(135deg, #0B3C26 0%, #1F5E3B 100%);
        padding: 25px;
        border-radius: 15px;
        color: #FFD700;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
        direction: rtl;
    }
    .header-title { font-size: 32px; font-weight: bold; margin-bottom: 8px; }
    .header-sub { font-size: 16px; color: #E8F5E9; }

    .book-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        text-align: right;
        direction: rtl;
    }
    .book-title { font-size: 18px; font-weight: bold; color: #0B3C26; margin-bottom: 5px; }
    .book-cat { font-size: 13px; color: #666; background-color: #E8F5E9; padding: 2px 8px; border-radius: 10px; display: inline-block; }
    .book-price { font-size: 20px; font-weight: bold; color: #B8860B; margin-top: 10px; }
    .edition-badge { background-color: #FFF3CD; color: #856404; padding: 2px 6px; border-radius: 6px; font-size: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

if not os.path.exists("uploads"):
    os.makedirs("uploads")

# -------------------------------------------------------------
# 2. التهيئة وقاعدة البيانات الافتراضية
# -------------------------------------------------------------
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {
            "id": 1, 
            "title": "متن حرز الأماني ووجه التهاني (الشاطبية)", 
            "author": "الإمام الشاطبي", 
            "publisher": "دار الغوثاني", 
            "country": "سوريا",
            "edition": "طبعة دار الغوثاني للدراسات",
            "buy_price": 80.0, "sell_price": 105.0, "qty": 35, 
            "category": "المتون", 
            "barcode": "622100000201",
            "image": ""
        },
        {
            "id": 2, 
            "title": "متن حرز الأماني ووجه التهاني (الشاطبية)", 
            "author": "الإمام الشاطبي", 
            "publisher": "دار المحدثين", 
            "country": "مصر",
            "edition": "طبعة دار المحدثين بالقاهرة",
            "buy_price": 65.0, "sell_price": 85.0, "qty": 50, 
            "category": "المتون", 
            "barcode": "622100000202",
            "image": ""
        }
    ])

if 'customer_cart' not in st.session_state:
    st.session_state.customer_cart = []

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# Header
st.markdown("""
<div class="header-box">
    <div class="header-title">📖 مَكْتَبَةُ الأَحْرُفِ السـ7ـبْعَة</div>
    <div class="header-sub">النظام الإلكتروني المتكامل لعلوم القرآن والقراءات وإدارة المخزون بالباركود</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📌 القائمة الرئيسية")
mode = st.sidebar.radio("اختر الواجهة:", ["🛍️ المتجر الإلكتروني (للعملاء)", "🔒 لوحة تحكم الإدارة (خاص بالمالك)"])

# =============================================================
# 🛍️ الواجهة الأولى: متجر العملاء + البحث بالباركود
# =============================================================
if mode == "🛍️ المتجر الإلكتروني (للعملاء)":
    st.subheader("🔍 تصفح المكتبة أو البحث السريع بالباركود")
    
    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
    with col_s1:
        search_kw = st.text_input("ابحث باسم الكتاب أو المؤلف:", "", placeholder="مثال: الشاطبية، الجزرية...")
    with col_s2:
        scan_barcode = st.text_input("مسح/إدخال الباركود:", "", placeholder="مثال: 622100000201")
    with col_s3:
        categories = ["الكل"] + list(st.session_state.inventory['category'].unique()) if 'category' in st.session_state.inventory.columns else ["الكل"]
        selected_cat = st.selectbox("التصنيف:", categories)

    df_books = st.session_state.inventory.copy()
    if scan_barcode:
        df_books = df_books[df_books['barcode'].astype(str).str.contains(scan_barcode, case=False, na=False)]
    elif search_kw:
        df_books = df_books[df_books['title'].str.contains(search_kw, case=False, na=False) | df_books['author'].str.contains(search_kw, case=False, na=False)]
    if selected_cat != "الكل":
        df_books = df_books[df_books['category'] == selected_cat]

    st.markdown("---")
    st.markdown("### 📚 الكتب المتوفرة والطبعات المختلفة")

    cols = st.columns(2)
    for idx, book in df_books.iterrows():
        col_idx = idx % 2
        with cols[col_idx]:
            img_path = str(book.get('image', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            
            st.markdown(f"""
            <div class="book-card">
                <div class="book-title">{book.get('title', '')}</div>
                <div style="color: #555; font-size: 14px;">المؤلف: {book.get('author', '')}</div>
                <div style="margin-top: 5px;"><span class="edition-badge">📚 {book.get('edition', 'طبعة عامة')} - {book.get('publisher', '')} ({book.get('country', '')})</span></div>
                <div style="margin-top: 5px; font-size: 12px; color: #777;">الباركود: {book.get('barcode', 'غير متوفر')}</div>
                <span class="book-cat">{book.get('category', 'أخرى')}</span>
                <div class="book-price">السعر: {float(book.get('sell_price', 0)):,.2f} ج.م</div>
            </div>
            """, unsafe_allow_html=True)
            
            avail = int(book.get('qty', 0))
            if avail > 0:
                col_btn1, col_btn2 = st.columns([1, 2])
                with col_btn1:
                    qty_to_buy = st.number_input("الكمية:", min_value=1, max_value=max(1, avail), value=1, key=f"qty_{book.get('barcode', idx)}_{idx}")
                with col_btn2:
                    st.write(" ")
                    if st.button("🛒 إضافة للسلة", key=f"btn_{book.get('barcode', idx)}_{idx}"):
                        item_label = f"{book.get('title', '')} [{book.get('publisher', '')}]"
                        st.session_state.customer_cart.append({
                            "title": item_label,
                            "price": float(book.get('sell_price', 0)),
                            "qty": qty_to_buy,
                            "total": float(book.get('sell_price', 0)) * qty_to_buy
                        })
                        st.success(f"تمت إضافة '{book.get('title', '')}' بنجاح!")
            else:
                st.error("عذراً، نفدت الكمية حالياً")

    # سلة التسوق
    st.markdown("---")
    st.markdown("## 🛒 سلة التسوق وإتمام الطلب")
    if st.session_state.customer_cart:
        cart_df = pd.DataFrame(st.session_state.customer_cart)
        st.dataframe(cart_df[['title', 'price', 'qty', 'total']], use_container_width=True)
        
        books_total = cart_df['total'].sum()
        shipping_cost = 60.0
        grand_total = books_total + shipping_cost

        st.markdown(f"#### إجمالي الكتب: **{books_total:,.2f} ج.م** | الشحن: **{shipping_cost:,.2f} ج.م**")
        st.markdown(f"### الإجمالي الكلي: <span style='color:#0B3C26;'>**{grand_total:,.2f} ج.م**</span>", unsafe_allow_html=True)

        st.markdown("---")
        with st.form("checkout_form"):
            c_name = st.text_input("الاسم بالكامل:")
            c_phone = st.text_input("رقم الهاتف (واتساب):")
            c_address = st.text_input("العنوان التفصيلي والمدينة:")
            submit_order = st.form_submit_button("✅ تأكيد وإرسال الطلب")
            if submit_order:
                if c_name and c_phone and c_address:
                    order_id = len(st.session_state.orders) + 1001
                    st.session_state.orders.append({
                        "order_id": order_id, "date": datetime.date.today().strftime("%Y-%m-%d"),
                        "customer_name": c_name, "phone": c_phone, "address": c_address,
                        "total": grand_total, "status": "قيد المراجعة", "items": st.session_state.customer_cart.copy()
                    })
                    st.session_state.customer_cart = []
                    st.balloons()
                    st.success(f"تم إرسال طلبك بنجاح! رقم الطلب: #{order_id}")
                else:
                    st.error("يرجى ملء جميع البيانات الأساسية.")
    else:
        st.info("سلة التسوق فارغة حالياً.")

# =============================================================
# 🔒 الواجهة الثانية: لوحة تحكم الإدارة (إدارة المخزون والطبعات والباركود)
# =============================================================
else:
    st.subheader("🔒 لوحة تحكم مالك المكتبة")

    if not st.session_state.admin_logged_in:
        pwd = st.text_input("أدخل كلمة مرور الإدارة:", type="password")
        if st.button("تسجيل الدخول"):
            if pwd == "1234":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    else:
        st.sidebar.button("🚪 تسجيل الخروج", on_click=lambda: st.session_state.update({"admin_logged_in": False}))
        
        admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs([
            "📋 طلبات العملاء", 
            "📦 المخزون (تجميع العناوين والطبعات)", 
            "➕ إضافة كتاب / طبعة جديدة بالباركود", 
            "📊 رفع ملف الـ CSV"
        ])

        with admin_tab1:
            st.markdown("### 📋 طلبات الشراء القادمة")
            if st.session_state.orders:
                orders_df = pd.DataFrame(st.session_state.orders)
                st.dataframe(orders_df[['order_id', 'date', 'customer_name', 'phone', 'total', 'status']], use_container_width=True)
            else:
                st.info("لا توجد طلبات جديدة.")

        with admin_tab2:
            st.markdown("### 📦 المخزون الكامل للمكتبة")
            st.dataframe(st.session_state.inventory, use_container_width=True)

        with admin_tab3:
            st.markdown("### ➕ إضافة كتاب جديد أو طبعة جديدة لنفس العنوان مع توليد باركود")
            
            with st.form("admin_add_book_advanced"):
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    b_title = st.text_input("عنوان الكتاب الأساسي (مثال: متن الشاطبية):")
                    b_author = st.text_input("المؤلف / المحقق:")
                    b_cat = st.selectbox("التصنيف الرئيسي:", ["مصاحف القراءات", "المتون", "الشروحات", "رسم وضبط المصحف", "سلسلة ضمرة", "كتب اللغة والنحو", "تحريرات القراءات"])
                with col_m2:
                    b_publisher = st.text_input("دار النشر (مثال: دار الغوثاني):")
                    b_country = st.text_input("بلد النشر (مثال: سوريا / مصر / لبنان):", value="مصر")
                    b_edition = st.text_input("اسم الطبعة أو وصفها (مثال: طبعة دار الغوثاني - تحقيق فلان):")

                col_p1, col_p2, col_p3, col_p4 = st.columns(4)
                with col_p1:
                    b_buy = st.number_input("سعر الشراء:", value=50.0)
                with col_p2:
                    b_sell = st.number_input("سعر البيع:", value=90.0)
                with col_p3:
                    b_qty = st.number_input("الكمية المضافة:", value=10)
                with col_p4:
                    # توليد باركود تلقائي أو يدوي
                    auto_barcode = str(random.randint(622100001000, 622100009999))
                    b_barcode = st.text_input("الباركود (تلقائي أو أدخله):", value=auto_barcode)

                b_image = st.file_uploader("صورة غلاف هذه الطبعة:", type=["jpg", "png", "jpeg"])
                
                submit_new_book = st.form_submit_button("💾 حفظ الطبعة وتوليد باركود الملصق")
                if submit_new_book:
                    if b_title and b_publisher:
                        image_path = ""
                        if b_image is not None:
                            image_path = os.path.join("uploads", b_image.name)
                            with open(image_path, "wb") as f:
                                f.write(b_image.getbuffer())

                        # التحقق هل العنوان والطبعة موجودان مسبقاً؟ لتحديث الكمية بدل تكرار سطر فارغ
                        inv = st.session_state.inventory
                        existing_idx = inv[(inv['title'].str.strip() == b_title.strip()) & (inv['publisher'].str.strip() == b_publisher.strip())]
                        
                        if not existing_idx.empty:
                            # تحديث الكمية لنفس الكتاب والطبعة
                            idx_to_update = existing_idx.index[0]
                            st.session_state.inventory.loc[idx_to_update, 'qty'] += b_qty
                            st.session_state.inventory.loc[idx_to_update, 'sell_price'] = b_sell
                            st.success(f"الكتاب والطبعة موجودان مسبقاً! تم تحديث وزيادة الكمية بنجاح. الكمية الحالية: {st.session_state.inventory.loc[idx_to_update, 'qty']}")
                        else:
                            # إضافة طبعة جديدة تحت نفس العنوان
                            new_id = len(inv) + 1
                            new_row = {
                                "id": new_id, "title": b_title, "author": b_author,
                                "publisher": b_publisher, "country": b_country, "edition": b_edition,
                                "buy_price": b_buy, "sell_price": b_sell, "qty": b_qty,
                                "category": b_cat, "barcode": b_barcode, "image": image_path
                            }
                            st.session_state.inventory = pd.concat([inv, pd.DataFrame([new_row])], ignore_index=True)
                            st.balloons()
                            st.success(f"تمت إضافة الطبعة الجديدة بنجاح برقم باركود: {b_barcode}!")
                            
                            # عرض بطاقة باركود جاهزة للطباعة
                            st.markdown(f"""
                            <div style="background: #fff; padding: 15px; border: 2px dashed #0B3C26; border-radius: 10px; text-align: center; margin-top: 15px;">
                                <h4 style="color: #0B3C26; margin: 0;">🏷️ ملصق باركود جاهز للطباعة</h4>
                                <p style="font-size: 16px; margin: 5px 0;"><b>{b_title}</b></p>
                                <p style="font-size: 14px; color: #555; margin: 0;">الطبعة: {b_edition} | السعر: {b_sell} ج.م</p>
                                <h2 style="letter-spacing: 5px; color: #000; font-family: monospace; margin: 10px 0;">||| | |||| || |||</h2>
                                <p style="font-size: 14px; font-weight: bold; color: #B8860B;">Barcode: {b_barcode}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("يرجى كتابة عنوان الكتاب ودار النشر على الأقل.")

        with admin_tab4:
            st.markdown("### 📊 رفع ملف الـ CSV للكتب")
            uploaded_file = st.file_uploader("اختر ملف الـ CSV:", type=["csv"])
            if uploaded_file is not None:
                try:
                    df_uploaded = pd.read_csv(uploaded_file)
                    st.success(f"تم قراءة الملف بنجاح! عدد الكتب: {len(df_uploaded)}")
                    if st.button("🚀 اعتماد وإضافة الكتب للمخزون"):
                        st.session_state.inventory = pd.concat([st.session_state.inventory, df_uploaded], ignore_index=True)
                        st.balloons()
                        st.success("تمت الإضافة بنجاح!")
                except Exception as e:
                    st.error(f"خطأ: {e}")
