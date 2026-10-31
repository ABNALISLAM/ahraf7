import streamlit as st
import pandas as pd
import datetime

# 1. إعدادات الصفحة (بدون شريط جانبي نهائياً لمنع أي تقطيع)
st.set_page_config(
    page_title="الأحرف السـ7ـبعة | لعلوم القرآن والقراءات",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تهيئة إعدادات الموقع والبيانات الأساسية
if 'site_settings' not in st.session_state:
    st.session_state.site_settings = {
        "whatsapp_number": "201033393575",
        "facebook_url": "https://facebook.com",
        "shipping_cost": 60.0,
        "banner_image": "https://images.unsplash.com/photo-1584286519137-01cb6f20455e?auto=format&fit=crop&w=1200&q=80",
        "admin_name": "المدير العام",
        "admin_password": "1234"
    }

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if 'subscribers' not in st.session_state:
    st.session_state.subscribers = []

if 'wishlist' not in st.session_state:
    st.session_state.wishlist = []  # قائمة المفضلة (الكتب المعلمة بنجمة)

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

# 3. تنسيقات التصميم النظيفة (إخفاء الشريط الجانبي بالكامل عبر CSS)
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    .stApp { 
        direction: rtl !important; 
        text-align: right !important; 
        background-color: #F8FAF9 !important; 
        font-family: 'Amiri', Tahoma, sans-serif;
    }
    .book-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: right;
        word-wrap: break-word;
    }
    .book-title { font-size: 18px; font-weight: bold; color: #0B3C26; margin-bottom: 5px; }
    .book-author { color: #555; font-size: 14px; }
    .book-price { font-size: 19px; font-weight: bold; color: #B8860B; margin-top: 8px; }
    .edition-badge { background-color: #FFF3CD; color: #856404; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; display: inline-block; }
    .whatsapp-float {
        position: fixed; bottom: 25px; left: 25px; background-color: #25D366; color: #FFF;
        border-radius: 50px; text-align: center; font-size: 30px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
        z-index: 999; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; text-decoration: none;
    }
    .footer-box {
        background-color: #0B3C26; color: #FFFFFF; padding: 25px; border-radius: 12px; text-align: center; margin-top: 40px; border-top: 3px solid #FFD700;
    }
    .footer-links a { color: #FFD700; text-decoration: none; margin: 0 15px; font-weight: bold; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# رأس الصفحة والبانر
st.markdown("<h1 style='text-align: center; color: #0B3C26;'>📖 الأحرف السـ7ـبعة لعلوم القرآن والقراءات</h1>", unsafe_allow_html=True)
st.image(st.session_state.site_settings['banner_image'], use_container_width=True)

# =============================================================
# 🔒 لوحة الإدارة (تظهر فقط للمدير)
# =============================================================
if st.session_state.admin_logged_in:
    col_top1, col_top2 = st.columns([4, 1])
    with col_top1:
        st.markdown("## 🔒 لوحة إدارة المتجر والإعدادات")
    with col_top2:
        if st.button("🚪 تسجيل خروج المدير"):
            st.session_state.admin_logged_in = False
            st.rerun()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 طلبات الشراء", "👥 الزوار المسجلين", "📦 المخزون", "⚙️ الإعدادات", "⚠️ البلاغات"])

    with tab1:
        st.markdown("### 📋 طلبات الشراء الواردة")
        if st.session_state.orders:
            st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد طلبات جديدة حالياً.")

    with tab2:
        st.markdown("### 👥 الزوار والعملاء المسجلون لتلقي العروض")
        if st.session_state.subscribers:
            st.dataframe(pd.DataFrame(st.session_state.subscribers), use_container_width=True, hide_index=True)
        else:
            st.info("لا يوجد زوار مسجلون حتى الآن.")

    with tab3:
        st.markdown("### 📦 سجل مخزون الكتب")
        st.dataframe(st.session_state.inventory, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("### ⚙️ إعدادات المتجر وبيانات دخول المدير")
        with st.form("settings_form"):
            new_wa = st.text_input("رقم الواتساب:", value=st.session_state.site_settings['whatsapp_number'])
            new_fb = st.text_input("رابط صفحة الفيسبوك:", value=st.session_state.site_settings['facebook_url'])
            new_shipping = st.number_input("تكلفة الشحن الثابتة:", value=float(st.session_state.site_settings['shipping_cost']))
            new_banner = st.text_input("رابط صورة البانر:", value=st.session_state.site_settings['banner_image'])
            
            st.markdown("---")
            new_admin_name = st.text_input("اسم المدير للدخول:", value=st.session_state.site_settings['admin_name'])
            new_admin_pass = st.text_input("الرقم السري للمدير:", value=st.session_state.site_settings['admin_password'], type="password")
            
            if st.form_submit_button("💾 حفظ الإعدادات"):
                st.session_state.site_settings['whatsapp_number'] = new_wa
                st.session_state.site_settings['facebook_url'] = new_fb
                st.session_state.site_settings['shipping_cost'] = new_shipping
                st.session_state.site_settings['banner_image'] = new_banner
                st.session_state.site_settings['admin_name'] = new_admin_name
                st.session_state.site_settings['admin_password'] = new_admin_pass
                st.success("تم التحديث بنجاح!")
                st.rerun()

    with tab5:
        st.markdown("### ⚠️ شكاوى وبلاغات الأعطال")
        if st.session_state.reports:
            st.dataframe(pd.DataFrame(st.session_state.reports), use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد بلاغات.")

# =============================================================
# 🛍️ واجهة المتجر الطبيعية (للعملاء والزوار - تصفح حر ومستمر)
# =============================================================
else:
    st.subheader("🔍 تصفح جميع العناوين والكتب")
    
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

    # عرض الكتب بشبكة سلسة (عمودين مع التمرير الحر)
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
                <div style="margin-top: 6px;"><span class="edition-badge">📖 {pub_val}</span></div>
                <div class="book-price">السعر: {price_val:,.2f} جنيه</div>
            </div>
            """, unsafe_allow_html=True)
            
            # أزرار الإضافة للمفضلة (⭐ نجمة) والسلة
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            with col_btn1:
                is_fav = title_val in st.session_state.wishlist
                fav_label = "❤️ مفضلة" if is_fav else "🤍 نجمة"
                if st.button(fav_label, key=f"fav_{barcode_val}_{idx}"):
                    if is_fav:
                        st.session_state.wishlist.remove(title_val)
                        st.toast("تم إزالة الكتاب من المفضلة")
                    else:
                        st.session_state.wishlist.append(title_val)
                        st.toast("تمت إضافة الكتاب لمفضلتك ⭐")
                    st.rerun()
            with col_btn2:
                avail = int(book.get('الكمية', 0))
                qty_to_buy = st.number_input("الكمية:", min_value=1, max_value=max(1, avail), value=1, key=f"q_{barcode_val}_{idx}")
            with col_btn3:
                st.write(" ")
                if avail > 0:
                    if st.button("🛒 إضافة للسلة", key=f"b_{barcode_val}_{idx}"):
                        st.session_state.customer_cart.append({
                            "عنوان الكتاب": f"{title_val} ({pub_val})",
                            "سعر القطعة": price_val,
                            "الكمية": qty_to_buy,
                            "الإجمالي": price_val * qty_to_buy
                        })
                        st.success(f"تمت إضافة '{title_val}' بنجاح!")
                else:
                    st.error("نفدت الكمية")

    # عرض قائمة المفضلة (الأمنيات) للزائر
    if st.session_state.wishlist:
        st.markdown("---")
        st.markdown("### ⭐ كتبك المفضلة التي اخترتها (قائمة الأمنيات)")
        for fav_book in st.session_state.wishlist:
            st.markdown(f"- 📖 **{fav_book}**")

    # سلة التسوق
    st.markdown("---")
    st.markdown("## 🛒 سلة التسوق وإتمام الطلب")
    if st.session_state.customer_cart:
        cart_df = pd.DataFrame(st.session_state.customer_cart)
        st.dataframe(cart_df, use_container_width=True, hide_index=True)
        
        books_total = cart_df['الإجمالي'].sum()
        shipping_cost = float(st.session_state.site_settings['shipping_cost'])
        grand_total = books_total + shipping_cost

        st.markdown(f"### الإجمالي الكلي: **{grand_total:,.2f} جنيه مصري** (شاملاً الشحن {shipping_cost} ج.م)")

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

    # نظام تسجيل الزوار (اختياري) + دخول المدير من نفس الخانة بالأسفل
    st.markdown("---")
    st.markdown("### 🔔 انضم لقائمة المهتمين بالعروض")
    st.markdown("<p style='font-size:14px; color:#555;'>سجل هاتفك ليصلك كل جديد وعروض الكتب على الواتساب (اختياري)</p>", unsafe_allow_html=True)
    
    with st.form("visitor_reg_form"):
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            v_name = st.text_input("الاسم الكريم:")
        with col_v2:
            v_phone = st.text_input("رقم الواتساب:")
        
        submitted = st.form_submit_button("📩 تسجيل المتابعة")
        if submitted:
            # التحقق هل هو المدير يكتب بيانات دخوله؟
            if v_name.strip() == st.session_state.site_settings['admin_name'] and v_phone.strip() == st.session_state.site_settings['admin_password']:
                st.session_state.admin_logged_in = True
                st.success("مرحباً بك يا مدير الموقع!")
                st.rerun()
            elif v_name and v_phone:
                st.session_state.subscribers.append({"التاريخ": datetime.date.today().strftime("%Y-%m-%d"), "الاسم": v_name, "الهاتف": v_phone})
                st.success("تم تسجيلك بنجاح لتلقي العروض!")
            else:
                st.error("يرجى إدخال البيانات المطلوبة.")

    # بلاغات الأعطال
    st.markdown("---")
    with st.expander("🛠️ واجهتك مشكلة أو عطل بالموقع؟ أبلغنا هنا"):
        with st.form("report_form"):
            r_name = st.text_input("اسم الكريم:")
            r_msg = st.text_area("صف لنا المشكلة:")
            submit_report = st.form_submit_button("إرسال الإبلاغ")
            if submit_report:
                if r_name and r_msg:
                    st.session_state.reports.append({"التاريخ": datetime.date.today().strftime("%Y-%m-%d"), "الاسم": r_name, "المشكلة": r_msg})
                    st.success("تم إرسال ملاحظتك بنجاح!")
                else:
                    st.error("يرجى ملء الحقول.")

    # زر الواتساب العائم
    wa_num = st.session_state.site_settings['whatsapp_number']
    st.markdown(f"""
    <a href="https://wa.me/{wa_num}?text=السلام%20عليكم،%20أريد%20الاستفسار%20عن%20كتب%20القراءات" class="whatsapp-float" target="_blank" title="تواصل معنا">
        💬
    </a>
    """, unsafe_allow_html=True)

    # التذييل (Footer)
    fb_url = st.session_state.site_settings['facebook_url'] if 'site_settings' in st.session_state else "https://facebook.com"
    st.markdown(f"""
    <div class="footer-box">
        <h3>منصة الأحرف السـ7ـبعة لعلوم القرآن والقراءات</h3>
        <p>نسعى لتقديم أثمن الكتب والمتون العلمية لعلوم القرآن والقراءات بخدمة دقيقة ومميزة</p>
        <div class="footer-links" style="margin-top: 15px;">
            <a href="https://wa.me/{wa_num}" target="_blank">💬 واتساب</a>
            <a href="{fb_url}" target="_blank">📘 فيسبوك</a>
        </div>
        <p style="margin-top: 15px; font-size: 13px; color: #ccc;">جميع الحقوق محفوظة © 2026 الأحرف السـ7ـبعة</p>
    </div>
    """, unsafe_allow_html=True)
