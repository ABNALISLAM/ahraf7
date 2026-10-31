import streamlit as st
import pandas as pd
import datetime
import os
import random

# 1. إعدادات الصفحة وعنوان التبويب
st.set_page_config(
    page_title="الأحرف السـ7ـبعة | لعلوم القرآن والقراءات",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. فحص الرابط للتحقق من المالك (الوضع السري برقمك السري 1181A@)
query_params = st.query_params
is_admin_via_url = query_params.get("admin") == "1181A@"

if is_admin_via_url:
    st.session_state.admin_logged_in = True

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"رقم_الكتاب": 1, "عنوان الكتاب": "مصحف الصحابة بالهامش لجمع القراءات العشر (أصفر)", "المؤلف / المحقق": "الشيخ توفيق ضمرة", "دار النشر": "دار الصحابة للتراث", "بلد النشر": "مصر", "وصف الطبعة": "طبعة دار الصحابة طنطا", "سعر الشراء": 320.0, "سعر البيع": 380.0, "الكمية": 15, "التصنيف": "مصاحف القراءات", "الباركود": "622100001001"},
        {"رقم_الكتاب": 2, "عنوان الكتاب": "مصحف الصحابة بالهامش لجمع القراءات العشر (جوامعي)", "المؤلف / المحقق": "الشيخ توفيق ضمرة", "دار النشر": "دار الصحابة للتراث", "بلد النشر": "مصر", "وصف الطبعة": "الطبعة الكبرى الجوامعية", "سعر الشراء": 450.0, "سعر البيع": 520.0, "الكمية": 10, "التصنيف": "مصاحف القراءات", "الباركود": "622100001002"},
        {"رقم_الكتاب": 3, "عنوان الكتاب": "مصحف القراءات التعليمي بالترميز اللوني", "المؤلف / المحقق": "لجنة من العلماء", "دار النشر": "دار المعرفة", "بلد النشر": "سوريا", "وصف الطبعة": "طبعة دار المعرفة دمشق", "سعر الشراء": 380.0, "سعر البيع": 450.0, "الكمية": 12, "التصنيف": "مصاحف القراءات", "الباركود": "622100001003"},
        {"رقم_الكتاب": 4, "عنوان الكتاب": "متن حرز الأماني ووجه التهاني (الشاطبية)", "المؤلف / المحقق": "الإمام الشاطبي", "دار النشر": "دار الغوثاني للدراسات", "بلد النشر": "سوريا", "وصف الطبعة": "طبعة دار الغوثاني", "سعر الشراء": 85.0, "سعر البيع": 110.0, "الكمية": 30, "التصنيف": "المتون", "الباركود": "622100001008"},
        {"رقم_الكتاب": 5, "عنوان الكتاب": "متن المقدمة الجزرية في تجويد القرآن", "المؤلف / المحقق": "الإمام ابن الجزري", "دار النشر": "دار ابن الجزري", "بلد النشر": "السعودية", "وصف الطبعة": "تحقيق د. أيمن سويد", "سعر الشراء": 45.0, "سعر البيع": 60.0, "الكمية": 50, "التصنيف": "المتون", "الباركود": "622100001012"},
        {"رقم_الكتاب": 6, "عنوان الكتاب": "الوافي في شرح الشاطبية", "المؤلف / المحقق": "د. عبد الفتاح القاضي", "دار النشر": "دار السلام بالقاهرة", "بلد النشر": "مصر", "وصف الطبعة": "طبعة دار السلام", "سعر الشراء": 240.0, "سعر البيع": 290.0, "الكمية": 15, "التصنيف": "الشروحات", "الباركود": "622100001022"}
    ])

if 'customer_cart' not in st.session_state:
    st.session_state.customer_cart = []

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'reports' not in st.session_state:
    st.session_state.reports = []

# 4. تنسيقات التصميم وأزرار التفاعل
st.markdown("""
<style>
    .stApp { 
        direction: rtl !important; 
        text-align: right !important; 
        background-color: #F8FAF9 !important; 
        font-family: 'Amiri', Tahoma, sans-serif;
    }
    
    [data-testid="stSidebar"] {
        white-space: normal !important;
        overflow-wrap: break-word !important;
    }

    /* البانر الخلفي الفخم */
    .hero-banner {
        background: linear-gradient(rgba(11, 60, 38, 0.8), rgba(31, 94, 59, 0.8)), 
                    url('https://images.unsplash.com/photo-1590073844006-33379778ae09?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 45px 20px;
        border-radius: 16px;
        color: #FFD700;
        text-align: center;
        margin-bottom: 25px;
        border: 2px solid #FFD700;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }
    .hero-title { font-size: 40px; font-weight: 900; margin-bottom: 8px; text-shadow: 2px 2px 6px rgba(0,0,0,0.6); letter-spacing: 1px; }
    .hero-sub { font-size: 17px; color: #FFFFFF; font-weight: bold; text-shadow: 1px 1px 4px rgba(0,0,0,0.6); }

    .book-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: right;
    }
    .book-title { font-size: 18px; font-weight: bold; color: #0B3C26; margin-bottom: 5px; }
    .book-author { color: #555; font-size: 14px; }
    .book-price { font-size: 19px; font-weight: bold; color: #B8860B; margin-top: 8px; }
    .edition-badge { background-color: #FFF3CD; color: #856404; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; }

    /* تصميم زر الواتساب العائم الثابت في الشاشة */
    .whatsapp-float {
        position: fixed;
        bottom: 25px;
        left: 25px;
        background-color: #25D366;
        color: #FFF;
        border-radius: 50px;
        text-align: center;
        font-size: 30px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
        z-index: 999;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        transition: 0.3s;
    }
    .whatsapp-float:hover {
        background-color: #20ba5a;
        transform: scale(1.1);
    }

    /* تصميم تذييل الصفحة (Footer) */
    .footer-box {
        background-color: #0B3C26;
        color: #FFFFFF;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 40px;
        border-top: 3px solid #FFD700;
    }
    .footer-links a {
        color: #FFD700;
        text-decoration: none;
        margin: 0 15px;
        font-weight: bold;
        font-size: 16px;
    }
    .footer-links a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

if st.session_state.admin_logged_in:
    st.sidebar.title("🔒 لوحة الإدارة")
    mode = st.sidebar.radio("الواجهة:", ["🔒 لوحة تحكم الإدارة", "🛍️ معاينة المتجر"])
    if st.sidebar.button("🚪 خروج من الإدارة"):
        st.session_state.admin_logged_in = False
        st.query_params.clear()
        st.rerun()
else:
    mode = "🛍️ المتجر الإلكتروني (للعملاء والزوار)"

# البانر الرئيسي
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">📖 الأَحْرُفُ السـ7ـبْعَة</div>
    <div class="hero-sub">✦ لِكُتُبِ القِرَاءَاتِ وَعُلُومِ القُرْآنِ الكَرِيمِ ✦</div>
</div>
""", unsafe_allow_html=True)

# =============================================================
# 🛍️ واجهة المتجر
# =============================================================
if mode == "🛍️ المتجر الإلكتروني (للعملاء والزوار)" or not st.session_state.admin_logged_in:
    st.subheader("🔍 تصفح الكتب والمتون")
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        search_kw = st.text_input("ابحث عن كتاب أو مؤلف:", "", placeholder="مثال: الشاطبية...")
    with col_s2:
        categories = ["الكل"] + list(st.session_state.inventory['التصنيف'].unique())
        selected_cat = st.selectbox("القسم:", categories)

    df_books = st.session_state.inventory.copy()

    if search_kw:
        df_books = df_books[df_books['عنوان الكتاب'].str.contains(search_kw, case=False, na=False) | df_books['المؤلف / المحقق'].str.contains(search_kw, case=False, na=False)]
    if selected_cat != "الكل":
        df_books = df_books[df_books['التصنيف'] == selected_cat]

    cols = st.columns(2)
    for idx, book in df_books.iterrows():
        col_idx = idx % 2
        with cols[col_idx]:
            title_val = book.get('عنوان الكتاب', '')
            author_val = book.get('المؤلف / المحقق', '')
            pub_val = book.get('دار النشر', '')
            price_val = float(book.get('سعر البيع', 0))
            barcode_val = book.get('الباركود', '')

            st.markdown(f"""
            <div class="book-card">
                <div class="book-title">{title_val}</div>
                <div class="book-author">المؤلف: <b>{author_val}</b></div>
                <div style="margin-top: 4px;"><span class="edition-badge">📖 {pub_val}</span></div>
                <div class="book-price">السعر: {price_val:,.2f} جنيه</div>
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
                st.error("نفدت الكمية حالياً")

    st.markdown("---")
    st.markdown("## 🛒 سلة التسوق وإتمام الطلب")
    if st.session_state.customer_cart:
        cart_df = pd.DataFrame(st.session_state.customer_cart)
        st.dataframe(cart_df, use_container_width=True, hide_index=True)
        
        books_total = cart_df['الإجمالي'].sum()
        shipping_cost = 60.0
        grand_total = books_total + shipping_cost

        st.markdown(f"### الإجمالي الكلي: **{grand_total:,.2f} جنيه مصري** (شاملاً الشحن)")

        with st.form("checkout_form"):
            c_name = st.text_input("الاسم بالكامل:")
            c_phone = st.text_input("رقم الهاتف / الواتساب:")
            c_address = st.text_input("عنوان التوصيل والمدينة:")
            submit_order = st.form_submit_button("✅ تأكيد الطلب")
            if submit_order:
                if c_name and c_phone and c_address:
                    order_id = len(st.session_state.orders) + 1001
                    st.session_state.orders.append({
                        "رقم_الطلب": order_id, "التاريخ": datetime.date.today().strftime("%Y-%m-%d"),
                        "اسم_العميل": c_name, "الهاتف": c_phone, "العنوان": c_address,
                        "الإجمالي": grand_total, "حالة_الطلب": "قيد المراجعة"
                    })
                    st.session_state.customer_cart = []
                    st.balloons()
                    st.success(f"تم استقبال طلبك بنجاح! رقم الطلب: #{order_id}")
                else:
                    st.error("يرجى إدخال البيانات كاملة.")
    else:
        st.info("سلة التسوق فارغة حالياً.")

    # --- قسم الإبلاغ عن الأعطال للعملاء ---
    st.markdown("---")
    with st.expander("🛠️ واجهتك مشكلة أو عطل بالموقع؟ أبلغنا هنا"):
        with st.form("report_form"):
            r_name = st.text_input("اسمك الكريم:")
            r_msg = st.text_area("صف لنا المشكلة أو العطل الذي واجهك:")
            submit_report = st.form_submit_button("إرسال الإبلاغ للإدارة")
            if submit_report:
                if r_name and r_msg:
                    st.session_state.reports.append({"التاريخ": datetime.date.today().strftime("%Y-%m-%d"), "الاسم": r_name, "المشكلة": r_msg})
                    st.success("تم إرسال ملاحظتك للإدارة بنجاح، شكراً لتعاونك معنا!")
                else:
                    st.error("يرجى كتابة الاسم ووصف المشكلة.")

    # --- زر الواتساب العائم برقمك الصحيح ---
    st.markdown("""
    <a href="https://wa.me/201033393575?text=السلام%20عليكم،%20أريد%20الاستفسار%20عن%20كتب%20القراءات" class="whatsapp-float" target="_blank" title="تواصل معنا عبر الواتساب">
        💬
    </a>
    """, unsafe_allow_html=True)

    # --- تذييل الصفحة (Footer) مع روابط التواصل برقمك ---
    st.markdown("""
    <div class="footer-box">
        <h3>منصة الأحرف السـ7ـبعة لعلوم القرآن</h3>
        <p>نسعى لتقديم أثمن الكتب والمتون العلمية بخدمة دقيقة ومميزة</p>
        <div class="footer-links" style="margin-top: 15px;">
            <a href="https://wa.me/201033393575" target="_blank">💬 واتساب</a>
            <a href="https://facebook.com" target="_blank">📘 فيسبوك</a>
        </div>
        <p style="margin-top: 15px; font-size: 13px; color: #ccc;">جميع الحقوق محفوظة © 2026 الأحرف السـ7ـبعة</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================
# 🔒 واجهة لوحة الإدارة
# =============================================================
else:
    st.subheader("🔒 لوحة إدارة المتجر والمخزون")
    tab1, tab2, tab3 = st.tabs(["📋 طلبات الشراء", "📦 المخزون", "⚠️ بلاغات الأعطال الواردة"])

    with tab1:
        st.markdown("### 📋 قائمة الطلبات الواردة")
        if st.session_state.orders:
            orders_df = pd.DataFrame(st.session_state.orders)
            st.dataframe(orders_df, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد طلبات جديدة.")

    with tab2:
        st.markdown("### 📦 سجل مخزون الكتب")
        st.dataframe(st.session_state.inventory, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("### ⚠️ شكاوى وبلاغات الأعطال من العملاء")
        if st.session_state.reports:
            reports_df = pd.DataFrame(st.session_state.reports)
            st.dataframe(reports_df, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد بلاغات أعطال حالياً.")
