import streamlit as st
import pandas as pd
import datetime
import os
import random

# -------------------------------------------------------------
# 1. إعدادات الصفحة وتهيئة الجلسة
# -------------------------------------------------------------
st.set_page_config(
    page_title="مكتبة الأحرف السبعة | لعلوم القرآن والقراءات",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# التهيئة الافتراضية لألوان وتنسيقات الموقع
if 'theme_primary' not in st.session_state:
    st.session_state.theme_primary = "#0B3C26"
if 'theme_secondary' not in st.session_state:
    st.session_state.theme_secondary = "#1F5E3B"
if 'theme_gold' not in st.session_state:
    st.session_state.theme_gold = "#FFD700"
if 'text_color' not in st.session_state:
    st.session_state.text_color = "#0B3C26"
if 'font_weight' not in st.session_state:
    st.session_state.font_weight = "bold"
if 'bg_color' not in st.session_state:
    st.session_state.bg_color = "#F8FAF9"

# -------------------------------------------------------------
# 2. لوحة التحكم الجانبية للتخصيص
# -------------------------------------------------------------
st.sidebar.title("📌 القائمة الرئيسية")
mode = st.sidebar.radio("اختر الواجهة المطلوبة:", ["🛍️ المتجر الإلكتروني (للعملاء والزوار)", "🔒 لوحة تحكم الإدارة (خاصة بالمالك)"])

st.sidebar.markdown("---")
with st.sidebar.expander("🎨 تخصيص ألوان وسمك الخطوط بالموقع"):
    st.write("تحكم في مظهر متجرك بسهولة:")
    st.session_state.theme_primary = st.color_picker("اللون الرئيسي للموقع والشريط:", st.session_state.theme_primary)
    st.session_state.text_color = st.color_picker("لون عناوين الكتب والأسعار:", st.session_state.text_color)
    st.session_state.theme_gold = st.color_picker("لون الخط الذهبي في البانر:", st.session_state.theme_gold)
    st.session_state.bg_color = st.color_picker("لون خلفية الموقع العامة:", st.session_state.bg_color)
    
    font_weight_choice = st.selectbox("سُمك خط عناوين الكتب:", ["عريض ممتاز (Bold)", "متوسط (Medium)", "ثقيل جداً (Black)"])
    if "ثقيل" in font_weight_choice:
        st.session_state.font_weight = "900"
    elif "عريض" in font_weight_choice:
        st.session_state.font_weight = "bold"
    else:
        st.session_state.font_weight = "500"

st.markdown(f"""
<style>
    .stApp {{ 
        direction: rtl !important; 
        text-align: right !important; 
        background-color: {st.session_state.bg_color} !important; 
        font-family: 'Amiri', 'Traditional Arabic', Tahoma, sans-serif;
    }}
    
    /* تصميم بانر مبهر ومطور باسم المكتبة الفاخر */
    .header-box {{
        background: radial-gradient(circle, {st.session_state.theme_secondary} 0%, {st.session_state.theme_primary} 100%);
        padding: 30px 20px;
        border-radius: 18px;
        color: {st.session_state.theme_gold};
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 6px 20px rgba(11, 60, 38, 0.25);
        border: 2px solid {st.session_state.theme_gold};
        direction: rtl;
        position: relative;
        overflow: hidden;
    }}
    .header-title {{ 
        font-size: 40px; 
        font-weight: 900; 
        margin-bottom: 10px; 
        font-family: 'Amiri', serif;
        letter-spacing: 1px;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.4);
    }}
    .header-title span {{
        color: #FFFFFF;
        background: linear-gradient(180deg, #FFFFFF 0%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .header-sub {{ 
        font-size: 18px; 
        color: #E8F5E9; 
        font-weight: 500;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    }}

    .book-card {{
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        text-align: right;
        direction: rtl;
    }}
    .book-title {{ font-size: 20px; font-weight: {st.session_state.font_weight}; color: {st.session_state.text_color}; margin-bottom: 6px; }}
    .book-author {{ color: #444; font-size: 15px; margin-bottom: 4px; }}
    .book-cat {{ font-size: 13px; color: {st.session_state.theme_primary}; background-color: #E8F5E9; padding: 3px 10px; border-radius: 12px; display: inline-block; font-weight: bold; }}
    .book-price {{ font-size: 22px; font-weight: bold; color: #B8860B; margin-top: 10px; }}
    .edition-badge {{ background-color: #FFF3CD; color: #856404; padding: 3px 8px; border-radius: 8px; font-size: 13px; font-weight: bold; display: inline-block; }}

    table {{
        width: 100%;
        border-collapse: collapse;
        direction: rtl;
        text-align: right;
        background-color: #FFFFFF;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    th {{
        background-color: {st.session_state.theme_primary} !important;
        color: {st.session_state.theme_gold} !important;
        padding: 12px 15px;
        font-size: 16px;
        font-weight: {st.session_state.font_weight};
        font-family: 'Amiri', serif;
        border-bottom: 2px solid #072A1B;
    }}
    td {{
        padding: 10px 15px;
        border-bottom: 1px solid #EAEAEA;
        color: #333333;
        font-size: 14px;
    }}
    tr:nth-child(even) {{
        background-color: #F2F7F4 !important;
    }}
    tr:hover {{
        background-color: #E8F5E9 !important;
    }}
</style>
""", unsafe_allow_html=True)

if not os.path.exists("uploads"):
    os.makedirs("uploads")

# -------------------------------------------------------------
# 3. قاعدة البيانات الأساسية الآمنة
# -------------------------------------------------------------
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"رقم_الكتاب": 1, "عنوان الكتاب": "مصحف الصحابة بالهامش لجمع القراءات العشر (أصفر)", "المؤلف / المحقق": "الشيخ توفيق ضمرة", "دار النشر": "دار الصحابة للتراث", "بلد النشر": "مصر", "وصف الطبعة": "طبعة دار الصحابة طنطا", "سعر الشراء": 320.0, "سعر البيع": 380.0, "الكمية": 15, "التصنيف": "مصاحف القراءات", "الباركود": "622100001001", "الصورة": ""},
        {"رقم_الكتاب": 2, "عنوان الكتاب": "مصحف الصحابة بالهامش لجمع القراءات العشر (جوامعي)", "المؤلف / المحقق": "الشيخ توفيق ضمرة", "دار النشر": "دار الصحابة للتراث", "بلد النشر": "مصر", "وصف الطبعة": "الطبعة الكبرى الجوامعية", "سعر الشراء": 450.0, "سعر البيع": 520.0, "الكمية": 10, "التصنيف": "مصاحف القراءات", "الباركود": "622100001002", "الصورة": ""},
        {"رقم_الكتاب": 3, "عنوان الكتاب": "مصحف القراءات التعليمي بالترميز اللوني", "المؤلف / المحقق": "لجنة من العلماء", "دار النشر": "دار المعرفة", "بلد النشر": "سوريا", "وصف الطبعة": "طبعة دار المعرفة دمشق", "سعر الشراء": 380.0, "سعر البيع": 450.0, "الكمية": 12, "التصنيف": "مصاحف القراءات", "الباركود": "622100001003", "الصورة": ""},
        {"رقم_الكتاب": 4, "عنوان الكتاب": "متن حرز الأماني ووجه التهاني (الشاطبية)", "المؤلف / المحقق": "الإمام الشاطبي", "دار النشر": "دار الغوثاني للدراسات", "بلد النشر": "سوريا", "وصف الطبعة": "طبعة دار الغوثاني", "سعر الشراء": 85.0, "سعر البيع": 110.0, "الكمية": 30, "التصنيف": "المتون", "الباركود": "622100001008", "الصورة": ""},
        {"رقم_الكتاب": 5, "عنوان الكتاب": "متن المقدمة الجزرية في تجويد القرآن", "المؤلف / المحقق": "الإمام ابن الجزري", "دار النشر": "دار ابن الجزري", "بلد النشر": "السعودية", "وصف الطبعة": "تحقيق د. أيمن سويد", "سعر الشراء": 45.0, "سعر البيع": 60.0, "الكمية": 50, "التصنيف": "المتون", "الباركود": "622100001012", "الصورة": ""},
        {"رقم_الكتاب": 6, "عنوان الكتاب": "الوافي في شرح الشاطبية", "المؤلف / المحقق": "د. عبد الفتاح القاضي", "دار النشر": "دار السلام بالقاهرة", "بلد النشر": "مصر", "وصف الطبعة": "طبعة دار السلام", "سعر الشراء": 240.0, "سعر البيع": 290.0, "الكمية": 15, "التصنيف": "الشروحات", "الباركود": "622100001022", "الصورة": ""}
    ])

if 'customer_cart' not in st.session_state:
    st.session_state.customer_cart = []

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# Header Banner بتصميم مبهر وإبراز الرقم 7 بطريقة فنية
st.markdown("""
<div class="header-box">
    <div class="header-title">📖 مَكْتَبَةُ الأَحْرُفِ السـ<span>7</span>ـبْعَة</div>
    <div class="header-sub">✦ المنصة المتخصصة في علوم القرآن، القراءات العشر، والمصاحف، والمتون العلمية ✦</div>
</div>
""", unsafe_allow_html=True)

# =============================================================
# 🛍️ الواجهة الأولى: المتجر الإلكتروني
# =============================================================
if mode == "🛍️ المتجر الإلكتروني (للعملاء والزوار)":
    st.subheader("🔍 البحث والتصفح في أروقة المكتبة")
    
    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
    with col_s1:
        search_kw = st.text_input("ابحث عن كتاب، مؤلف، أو موضوع:", "", placeholder="مثال: الشاطبية، الجزرية...")
    with col_s2:
        scan_barcode = st.text_input("إدخال / مسح الباركود:", "", placeholder="مثال: 622100001001")
    with col_s3:
        categories = ["الكل"] + list(st.session_state.inventory['التصنيف'].unique())
        selected_cat = st.selectbox("تصفية حسب القسم:", categories)

    df_books = st.session_state.inventory.copy()

    if scan_barcode:
        df_books = df_books[df_books['الباركود'].astype(str).str.contains(scan_barcode, case=False, na=False)]
    elif search_kw:
        df_books = df_books[df_books['عنوان الكتاب'].str.contains(search_kw, case=False, na=False) | df_books['المؤلف / المحقق'].str.contains(search_kw, case=False, na=False)]
    if selected_cat != "الكل":
        df_books = df_books[df_books['التصنيف'] == selected_cat]

    st.markdown("---")
    st.markdown("### 📚 الكتب والمتون المتاحة في المكتبة")

    cols = st.columns(2)
    for idx, book in df_books.iterrows():
        col_idx = idx % 2
        with cols[col_idx]:
            img_path = str(book.get('الصورة', ''))
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            
            title_val = book.get('عنوان الكتاب', '')
            author_val = book.get('المؤلف / المحقق', '')
            pub_val = book.get('دار النشر', '')
            country_val = book.get('بلد النشر', '')
            ed_val = book.get('وصف الطبعة', 'طبعة معتمدة')
            cat_val = book.get('التصنيف', 'عام')
            price_val = float(book.get('سعر البيع', 0))
            barcode_val = book.get('الباركود', 'غير محدد')

            st.markdown(f"""
            <div class="book-card">
                <div class="book-title">{title_val}</div>
                <div class="book-author">المؤلف / المحقق: <b>{author_val}</b></div>
                <div style="margin-top: 6px;"><span class="edition-badge">📖 {ed_val} - {pub_val} ({country_val})</span></div>
                <div style="margin-top: 6px; font-size: 13px; color: #666;">رمز الباركود: {barcode_val}</div>
                <div style="margin-top: 8px;"><span class="book-cat">القسم: {cat_val}</span></div>
                <div class="book-price">السعر: {price_val:,.2f} جنيه مصري</div>
            </div>
            """, unsafe_allow_html=True)
            
            avail = int(book.get('الكمية', 0))
            if avail > 0:
                col_b1, col_b2 = st.columns([1, 2])
                with col_b1:
                    qty_to_buy = st.number_input("الكمية:", min_value=1, max_value=max(1, avail), value=1, key=f"q_{barcode_val}_{idx}")
                with col_b2:
                    st.write(" ")
                    if st.button("🛒 إضافة للسلة", key=f"b_{barcode_val}_{idx}"):
                        st.session_state.customer_cart.append({
                            "عنوان الكتاب": f"{title_val} ({pub_val})",
                            "سعر القطعة": price_val,
                            "الكمية": qty_to_buy,
                            "الإجمالي": price_val * qty_to_buy
                        })
                        st.success(f"تمت إضافة '{title_val}' بنجاح!")
            else:
                st.error("تنبيه: نفدت الكمية المتاحة حالياً")

    # سلة الشراء
    st.markdown("---")
    st.markdown("## 🛒 سلة التسوق وإتمام الطلب")
    if st.session_state.customer_cart:
        cart_df = pd.DataFrame(st.session_state.customer_cart)
        st.markdown(cart_df.to_html(index=False, escape=False), unsafe_allow_html=True)
        
        books_total = cart_df['الإجمالي'].sum()
        shipping_cost = 60.0
        grand_total = books_total + shipping_cost

        st.markdown(f"#### مجموع الكتب: **{books_total:,.2f} جنيه** | الشحن: **{shipping_cost:,.2f} جنيه**")
        st.markdown(f"### الإجمالي الكلي: <span style='color:{st.session_state.theme_primary};'>**{grand_total:,.2f} جنيه مصري**</span>", unsafe_allow_html=True)

        st.markdown("---")
        with st.form("checkout_form"):
            c_name = st.text_input("اسم المشتري بالكامل:")
            c_phone = st.text_input("رقم الهاتف / الواتساب:")
            c_address = st.text_input("عنوان التوصيل التفصيلي والمدينة:")
            submit_order = st.form_submit_button("✅ تأكيد وتثبيت الطلب")
            if submit_order:
                if c_name and c_phone and c_address:
                    order_id = len(st.session_state.orders) + 1001
                    st.session_state.orders.append({
                        "رقم_الطلب": order_id, "التاريخ": datetime.date.today().strftime("%Y-%m-%d"),
                        "اسم_العميل": c_name, "الهاتف": c_phone, "العنوان": c_address,
                        "الإجمالي": grand_total, "حالة_الطلب": "قيد المراجعة", "المحتويات": st.session_state.customer_cart.copy()
                    })
                    st.session_state.customer_cart = []
                    st.balloons()
                    st.success(f"تم استقبال طلبك بنجاح! رقم الطلب: #{order_id}")
                else:
                    st.error("يرجى ملء بيانات الاسم والهاتف والعنوان.")
    else:
        st.info("سلة التسوق فارغة حالياً.")

# =============================================================
# 🔒 الواجهة الثانية: لوحة تحكم الإدارة
# =============================================================
else:
    st.subheader("🔒 لوحة إدارة المكتبة والمخزون")

    if not st.session_state.admin_logged_in:
        pwd = st.text_input("أدخل كلمة المرور الخاصة بالإدارة:", type="password")
        if st.button("تسجيل الدخول للوحة التحكم"):
            if pwd == "1234":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة!")
    else:
        st.sidebar.button("🚪 الخروج من لوحة التحكم", on_click=lambda: st.session_state.update({"admin_logged_in": False}))
        
        tab1, tab2, tab3 = st.tabs([
            "📋 طلبات الشراء الواردة", 
            "📦 جرد المخزون الحالي", 
            "➕ إضافة كتاب / طبعة جديدة بالباركود"
        ])

        with tab1:
            st.markdown("### 📋 قائمة الطلبات الواردة")
            if st.session_state.orders:
                orders_df = pd.DataFrame(st.session_state.orders)
                cols_to_show = [c for c in ['رقم_الطلب', 'التاريخ', 'اسم_العميل', 'الهاتف', 'الإجمالي', 'حالة_الطلب'] if c in orders_df.columns]
                st.markdown(orders_df[cols_to_show].to_html(index=False, escape=False), unsafe_allow_html=True)
            else:
                st.info("لا توجد طلبات جديدة.")

        with tab2:
            st.markdown("### 📦 سجل مخزون المكتبة الكامل")
            st.markdown(st.session_state.inventory.to_html(index=False, escape=False), unsafe_allow_html=True)

        with tab3:
            st.markdown("### ➕ إضافة طبعة جديدة أو كتاب جديد مع توليد باركود")
            with st.form("add_new_arabic_book"):
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    b_title = st.text_input("عنوان الكتاب الرئيسي:")
                    b_author = st.text_input("اسم المؤلف / المحقق:")
                    b_cat = st.selectbox("قسم الكتاب:", ["مصاحف القراءات", "المتون", "الشروحات", "رسم وضبط المصحف", "سلسلة ضمرة", "كتب اللغة والنحو", "تحريرات القراءات"])
                with col_m2:
                    b_publisher = st.text_input("اسم دار النشر:")
                    b_country = st.text_input("بلد دار النشر:", value="مصر")
                    b_edition = st.text_input("وصف الطبعة:")

                col_p1, col_p2, col_p3, col_p4 = st.columns(4)
                with col_p1:
                    b_buy = st.number_input("سعر الشراء:", value=50.0)
                with col_p2:
                    b_sell = st.number_input("سعر البيع:", value=85.0)
                with col_p3:
                    b_qty = st.number_input("الكمية:", value=10)
                with col_p4:
                    auto_barcode = str(random.randint(622100002000, 622100009999))
                    b_barcode = st.text_input("الباركود:", value=auto_barcode)

                submit_new_book = st.form_submit_button("💾 حفظ الطبعة وتوليد باركود الملصق")
                if submit_new_book:
                    if b_title and b_publisher:
                        inv = st.session_state.inventory
                        existing_idx = inv[(inv['عنوان الكتاب'].str.strip() == b_title.strip()) & (inv['دار النشر'].str.strip() == b_publisher.strip())]
                        
                        if not existing_idx.empty:
                            idx_to_update = existing_idx.index[0]
                            st.session_state.inventory.loc[idx_to_update, 'الكمية'] += b_qty
                            st.success(f"الكتاب موجود مسبقاً! تم زيادة الكمية بنجاح.")
                        else:
                            new_row = {
                                "رقم_الكتاب": len(inv) + 1, "عنوان الكتاب": b_title, "المؤلف / المحقق": b_author,
                                "دار النشر": b_publisher, "بلد النشر": b_country, "وصف الطبعة": b_edition,
                                "سعر الشراء": b_buy, "سعر البيع": b_sell, "الكمية": b_qty,
                                "التصنيف": b_cat, "الباركود": b_barcode, "الصورة": ""
                            }
                            st.session_state.inventory = pd.concat([inv, pd.DataFrame([new_row])], ignore_index=True)
                            st.balloons()
                            st.success(f"تمت إضافة الطبعة الجديدة بنجاح برقم باركود: {b_barcode}!")
                    else:
                        st.error("يرجى كتابة عنوان الكتاب ودار النشر.")
