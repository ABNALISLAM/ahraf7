import streamlit as st
import pandas as pd
import datetime
import os
import json

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="الأحرف السـ7ـبعة لعلوم القرآن والقراءات",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. إنشاء مجلدات التخزين المحلي للبيانات الدائمة
if not os.path.exists("uploaded_images"):
    os.makedirs("uploaded_images")

DB_FILE = "store_database.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return None

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

saved_db = load_data()

if 'site_settings' not in st.session_state:
    if saved_db and "site_settings" in saved_db:
        st.session_state.site_settings = saved_db["site_settings"]
    else:
        st.session_state.site_settings = {
            "site_title": "📖 الأحرف السـ7ـبعة لعلوم القرآن والقراءات",
            "whatsapp_number": "201033393575",
            "shipping_cost": 60.0,
            "banner_image": "https://images.unsplash.com/photo-1584286519137-01cb6f20455e?auto=format&fit=crop&w=1200&q=80",
            "bg_color": "#F8FAF9",
            "theme_color": "#0B3C26",
            "admin_name": "المدير العام",
            "admin_password": "1234"
        }

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if 'subscribers' not in st.session_state:
    st.session_state.subscribers = saved_db["subscribers"] if saved_db and "subscribers" in saved_db else []

if 'customer_logged_in' not in st.session_state:
    st.session_state.customer_logged_in = False

if 'current_customer_phone' not in st.session_state:
    st.session_state.current_customer_phone = ""

if 'current_customer_name' not in st.session_state:
    st.session_state.current_customer_name = ""

if 'customer_wishlists' not in st.session_state:
    st.session_state.customer_wishlists = saved_db["customer_wishlists"] if saved_db and "customer_wishlists" in saved_db else {}

if 'orders' not in st.session_state:
    st.session_state.orders = saved_db["orders"] if saved_db and "orders" in saved_db else []

if 'inventory' not in st.session_state:
    if saved_db and "inventory" in saved_db:
        st.session_state.inventory = pd.DataFrame(saved_db["inventory"])
    else:
        st.session_state.inventory = pd.DataFrame([
            {
                "رقم_الكتاب": 1, 
                "عنوان الكتاب": "مصحف الصحابة بالهامش لجمع القراءات العشر (أصفر)", 
                "المؤلف / المحقق": "الشيخ توفيق ضمرة", 
                "دار النشر": "دار الصحابة للتراث", 
                "وصف الطبعة": "الطبعة الأولى - طنطا",
                "سعر البيع": 380.0, 
                "الكمية": 15, 
                "التصنيف": "مصاحف القراءات", 
                "صورة_الغلاف": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=400&q=80"
            }
        ])

if 'customer_cart' not in st.session_state:
    st.session_state.customer_cart = []

if 'admin_chat_history' not in st.session_state:
    st.session_state.admin_chat_history = [
        {"role": "assistant", "content": "أهلاً بك يا شيخنا الفاضل في لوحة التحكم الخاصة بموقعك. اطلب مني أي كود أو تطوير وسأقوم بصياغته لك فوراً."}
    ]

def commit_to_database():
    data = {
        "site_settings": st.session_state.site_settings,
        "subscribers": st.session_state.subscribers,
        "customer_wishlists": st.session_state.customer_wishlists,
        "orders": st.session_state.orders,
        "inventory": st.session_state.inventory.to_dict(orient="records")
    }
    save_data(data)

# 3. التصميم الديناميكي الكامل
bg_col = st.session_state.site_settings['bg_color']
theme_col = st.session_state.site_settings['theme_color']

st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    .stApp { 
        direction: rtl; 
        text-align: right; 
        font-family: 'Amiri', Tahoma, sans-serif;
    }
    .book-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .slider-container {
        display: flex; overflow-x: auto; gap: 15px; padding: 15px 5px; scroll-behavior: smooth; margin-bottom: 25px; white-space: nowrap;
    }
    .slider-container::-webkit-scrollbar { display: none; }
    .slider-card {
        min-width: 180px; max-width: 180px; background: white; border-radius: 10px; border: 1px solid #ddd; padding: 10px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.08); flex-shrink: 0;
    }
    .slider-card img { width: 100%; height: 120px; object-fit: cover; border-radius: 6px; }
    .whatsapp-float {
        position: fixed; bottom: 25px; left: 25px; background-color: #25D366; color: #FFF;
        border-radius: 50px; text-align: center; font-size: 30px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
        z-index: 999; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; text-decoration: none;
    }
    .footer-box {
        padding: 25px; border-radius: 12px; text-align: center; margin-top: 40px; border-top: 3px solid #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# عنوان الموقع الرئيسي والبانر
st.markdown(f"<h1 style='text-align: center; color: {theme_col};'>{st.session_state.site_settings['site_title']}</h1>", unsafe_allow_html=True)
st.image(st.session_state.site_settings['banner_image'], use_container_width=True)

# =============================================================
# 🔒 لوحة الإدارة الشاملة (تظهر للمدير فقط بعد تسجيل الدخول)
# =============================================================
if st.session_state.admin_logged_in:
    col_t1, col_t2 = st.columns([4, 1])
    with col_t1:
        st.markdown(f"## 🛠️ لوحة التحكم المطلقة (مخصصة للمدير)")
    with col_t2:
        if st.button("🚪 تسجيل خروج المدير"):
            st.session_state.admin_logged_in = False
            st.rerun()

    tab_inv, tab_add, tab_bulk, tab_orders, tab_subs, tab_set, tab_ai = st.tabs([
        "📦 إدارة المخزون", 
        "➕ إضافة كتاب", 
        "📂 استيراد شيت", 
        "📋 طلبات العملاء", 
        "👥 العملاء المسجلون", 
        "⚙️ تصميم ومظهر الموقع", 
        "🤖 المساعد الذكي المطور"
    ])

    with tab_inv:
        st.markdown("### 📦 إدارة وتعديل المخزون")
        if not st.session_state.inventory.empty:
            edited_df = st.data_editor(st.session_state.inventory, use_container_width=True, num_rows="dynamic")
            if st.button("💾 حفظ التعديلات نهائياً"):
                st.session_state.inventory = edited_df
                commit_to_database()
                st.success("تم الحفظ في قاعدة البيانات بنجاح!")
                st.rerun()
        else:
            st.warning("المخزون فارغ.")

    with tab_add:
        st.markdown("### ➕ إضافة كتاب جديد للمتجر")
        with st.form("add_book_form"):
            c_title = st.text_input("عنوان الكتاب:")
            c_author = st.text_input("المؤلف / المحقق:")
            c_pub = st.text_input("دار النشر:")
            c_edition = st.text_input("وصف الطبعة:")
            c_price = st.number_input("سعر البيع (جنيه):", min_value=0.0, value=100.0)
            c_qty = st.number_input("الكمية المتوفرة:", min_value=1, value=10)
            c_cat = st.selectbox("التصنيف:", ["مصاحف القراءات", "المتون", "الشروحات", "الأبحاث والرسائل"])
            uploaded_image = st.file_uploader("رفع صورة الغلاف من جهازك:", type=["png", "jpg", "jpeg"])
            
            if st.form_submit_button("✅ حفظ وإضافة الكتاب"):
                if c_title:
                    img_path = "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=400&q=80"
                    if uploaded_image is not None:
                        img_saved_path = os.path.join("uploaded_images", uploaded_image.name)
                        with open(img_saved_path, "wb") as f:
                            f.write(uploaded_image.getbuffer())
                        img_path = img_saved_path

                    new_id = len(st.session_state.inventory) + 1
                    new_row = pd.DataFrame([{
                        "رقم_الكتاب": new_id, "عنوان الكتاب": c_title, "المؤلف / المحقق": c_author,
                        "دار النشر": c_pub, "وصف الطبعة": c_edition, "سعر البيع": c_price,
                        "الكمية": c_qty, "التصنيف": c_cat, "صورة_الغلاف": img_path
                    }])
                    st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                    commit_to_database()
                    st.success("تمت إضافة الكتاب وحفظه بنجاح!")
                    st.rerun()

    with tab_bulk:
        st.markdown("### 📂 استيراد شيت كتب كامل (Excel أو CSV)")
        uploaded_sheet = st.file_uploader("اختر ملف الشيت من جهازك:", type=["xlsx", "csv"])
        if uploaded_sheet is not None:
            if st.button("🚀 استيراد وإضافة الكتب"):
                try:
                    df_sheet = pd.read_csv(uploaded_sheet) if uploaded_sheet.name.endswith('.csv') else pd.read_excel(uploaded_sheet)
                    st.session_state.inventory = pd.concat([st.session_state.inventory, df_sheet], ignore_index=True)
                    commit_to_database()
                    st.success("تم استيراد الشيت بنجاح!")
                    st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

    with tab_orders:
        st.markdown("### 📋 طلبات العملاء")
        if st.session_state.orders:
            st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد طلبات جديدة.")

    with tab_subs:
        st.markdown("### 👥 العملاء المسجلون")
        if st.session_state.subscribers:
            st.dataframe(pd.DataFrame(st.session_state.subscribers), use_container_width=True, hide_index=True)
        else:
            st.info("لا يوجد زوار مسجلون بعد.")

    with tab_set:
        st.markdown("### ⚙️ إعدادات الموقع وتغيير بيانات دخول المدير")
        with st.form("design_form"):
            new_title_site = st.text_input("عنوان الموقع الرئيسي:", value=st.session_state.site_settings['site_title'])
            bg_input = st.text_input("لون الخلفية (Hex Color):", value=st.session_state.site_settings['bg_color'])
            theme_input = st.text_input("لون الهوية (Hex Color):", value=st.session_state.site_settings['theme_color'])
            banner_input = st.text_input("رابط البانر:", value=st.session_state.site_settings['banner_image'])
            wa_input = st.text_input("رقم الواتساب للتواصل:", value=st.session_state.site_settings['whatsapp_number'])
            ship_input = st.number_input("تكلفة الشحن الثابتة:", value=float(st.session_state.site_settings['shipping_cost']))
            
            st.markdown("---")
            new_adm = st.text_input("تغيير اسم دخول المدير:", value=st.session_state.site_settings['admin_name'])
            new_pas = st.text_input("تغيير الرقم السري للمدير:", value=st.session_state.site_settings['admin_password'], type="password")
            
            if st.form_submit_button("🎨 حفظ وتطبيق كافة الإعدادات"):
                st.session_state.site_settings['site_title'] = new_title_site
                st.session_state.site_settings['bg_color'] = bg_input
                st.session_state.site_settings['theme_color'] = theme_input
                st.session_state.site_settings['banner_image'] = banner_input
                st.session_state.site_settings['whatsapp_number'] = wa_input
                st.session_state.site_settings['shipping_cost'] = ship_input
                st.session_state.site_settings['admin_name'] = new_adm
                st.session_state.site_settings['admin_password'] = new_pas
                commit_to_database()
                st.success("تم تحديث وحفظ الإعدادات بنجاح!")
                st.rerun()

    with tab_ai:
        st.markdown("### 🤖 المساعد الذكي المطور للموقع")
        st.info("أنا مساعدك البرمجي والذكاء الاصطناعي الخاص بالمنصة. اطلب مني أي كود أو تطوير وسأصيغه لك فوراً.")
        
        for chat in st.session_state.admin_chat_history:
            if chat["role"] == "user":
                st.markdown(f"**👤 أنت:** {chat['content']}")
            else:
                st.markdown(f"**🤖 المساعد الذكي:** {chat['content']}")
        
        with st.form("ai_chat_form", clear_on_submit=True):
            ai_prompt = st.text_input("اطلب استشارة أو صياغة كود:")
            if st.form_submit_button("إرسال للمساعد الذكي") and ai_prompt:
                st.session_state.admin_chat_history.append({"role": "user", "content": ai_prompt})
                ai_reply = f"أهلاً بك يا شيخنا الفاضل. بخصوص طلبك ('{ai_prompt}'): يمكننا تنفيذ ذلك بسهولة عبر تحديث كود Streamlit وإعادة الحفظ في قاعدة البيانات."
                st.session_state.admin_chat_history.append({"role": "assistant", "content": ai_reply})
                st.rerun()

# =============================================================
# 🛍️ واجهة المتجر الطبيعية (للجمهور والعملاء فقط)
# =============================================================
else:
    # زر إداري مخفي بعناية في الزاوية للوصول للوحة التحكم
    with st.popover("⚙️", help="إدارة المنصة"):
        st.markdown("#### تسجيل دخول إدارة المنصة")
        a_u = st.text_input("المستخدم:", key="pop_u")
        a_p = st.text_input("كلمة السر:", type="password", key="pop_p")
        if st.button("دخول الإدارة"):
            if a_u.strip() == st.session_state.site_settings['admin_name'] and a_p.strip() == st.session_state.site_settings['admin_password']:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("خطأ في بيانات الدخول")

    if not st.session_state.inventory.empty:
        slider_html = '<div class="slider-container" id="autoSlider">'
        for idx, book in st.session_state.inventory.iterrows():
            slider_html += f'<div class="slider-card"><img src="{book.get("صورة_الغلاف","")}" alt="book"><p>{book.get("عنوان الكتاب","")}</p></div>'
        slider_html += '</div><script>const s=document.getElementById("autoSlider");let l=0;setInterval(()=>{if(s){l+=200;if(l>=s.scrollWidth-s.clientWidth)l=0;s.scrollTo({left:l,behavior:"smooth"});}},3000);</script>'
        st.markdown(slider_html, unsafe_allow_html=True)

    if st.session_state.customer_logged_in:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.success(f"👤 أهلاً بك يا **{st.session_state.current_customer_name}** (مفضلاتك محفوظة ⭐)")
        with c2:
            if st.button("🚪 خروج"):
                st.session_state.customer_logged_in = False
                st.session_state.current_customer_phone = ""
                st.session_state.current_customer_name = ""
                st.rerun()

    st.subheader("🔍 تصفح جميع العناوين والكتب")
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        search_kw = st.text_input("ابحث عن كتاب أو مؤلف:", "")
    with col_s2:
        categories = ["الكل"] + list(st.session_state.inventory['التصنيف'].unique()) if not st.session_state.inventory.empty else ["الكل"]
        selected_cat = st.selectbox("القسم:", categories)

    df_books = st.session_state.inventory.copy()
    if search_kw and not df_books.empty:
        df_books = df_books[df_books['عنوان الكتاب'].str.contains(search_kw, case=False, na=False) | df_books['المؤلف / المحقق'].str.contains(search_kw, case=False, na=False)]
    if selected_cat != "الكل" and not df_books.empty:
        df_books = df_books[df_books['التصنيف'] == selected_cat]

    current_phone = st.session_state.current_customer_phone
    if current_phone and current_phone not in st.session_state.customer_wishlists:
        st.session_state.customer_wishlists[current_phone] = []
    user_wishlist = st.session_state.customer_wishlists.get(current_phone, []) if current_phone else []

    if not df_books.empty:
        cols = st.columns(2)
        for idx, book in df_books.iterrows():
            with cols[idx % 2]:
                t_val = book.get('عنوان الكتاب', '')
                a_val = book.get('المؤلف / المحقق', '')
                p_val = float(book.get('سعر البيع', 0))
                pub_val = book.get('دار النشر', '')
                
                st.markdown(f'''
                <div class="book-card">
                    <div class="book-title">{t_val}</div>
                    <div class="book-author">المؤلف: <b>{a_val}</b></div>
                    <div style="font-size: 13px; color: #666; margin-top: 4px;">دار النشر: {pub_val}</div>
                    <div class="book-price">السعر: {p_val:,.2f} جنيه</div>
                </div>
                ''', unsafe_allow_html=True)
                
                is_f = t_val in user_wishlist
                b1, b2, b3 = st.columns([1, 1, 2])
                with b1:
                    if st.button("❤️" if is_f else "🤍", key=f"f_{idx}"):
                        if not current_phone:
                            st.warning("⚠️ سجل دخولك أولاً لحفظ المفضلة!")
                        else:
                            if is_f:
                                st.session_state.customer_wishlists[current_phone].remove(t_val)
                            else:
                                st.session_state.customer_wishlists[current_phone].append(t_val)
                            commit_to_database()
                            st.rerun()
                with b2:
                    q_buy = st.number_input("الكمية:", min_value=1, value=1, key=f"q_{idx}")
                with b3:
                    st.write(" ")
                    if st.button("🛒 إضافة للسلة", key=f"b_{idx}"):
                        st.session_state.customer_cart.append({"عنوان الكتاب": t_val, "سعر القطعة": p_val, "الكمية": q_buy, "الإجمالي": p_val * q_buy})
                        st.success("تمت الإضافة!")
    else:
        st.info("لا توجد كتب مطابقة لبحثك.")

    if current_phone and user_wishlist:
        st.markdown("---")
        st.markdown(f"### ⭐ كتبك المفضلة يا {st.session_state.current_customer_name}")
        for fw in user_wishlist:
            st.markdown(f"- 📖 {fw}")

    st.markdown("---")
    st.markdown("## 🛒 سلة التسوق وإتمام الطلب")
    if st.session_state.customer_cart:
        cart_df = pd.DataFrame(st.session_state.customer_cart)
        st.dataframe(cart_df, use_container_width=True, hide_index=True)
        tot = cart_df['الإجمالي'].sum() + st.session_state.site_settings['shipping_cost']
        st.markdown(f"### الإجمالي الكلي: **{tot:,.2f} جنيه مصري**")

        with st.form("checkout_form"):
            cn = st.text_input("الاسم بالكامل:", value=st.session_state.current_customer_name)
            cp = st.text_input("رقم الواتساب:", value=st.session_state.current_customer_phone)
            ca = st.text_input("عنوان التوصيل:")
            if st.form_submit_button("✅ تأكيد الطلب"):
                if cn and cp and ca:
                    oid = len(st.session_state.orders) + 1001
                    order_record = {"رقم_الطلب": oid, "التاريخ": datetime.date.today().strftime("%Y-%m-%d"), "الاسم": cn, "الهاتف": cp, "العنوان": ca, "الإجمالي": tot, "الحالة": "قيد المراجعة"}
                    st.session_state.orders.append(order_record)
                    commit_to_database()
                    st.session_state.customer_cart = []
                    st.balloons()
                    st.success(f"تم استقبال طلبك بنجاح! رقم الطلب: #{oid}")
                else:
                    st.error("املأ كافة البيانات.")
    else:
        st.info("السلة فارغة.")

    st.markdown("---")
    st.markdown("### 👤 تسجيل دخول العملاء والزوار")
    with st.form("login_form"):
        lv_name = st.text_input("الاسم الكريم:")
        lv_phone = st.text_input("رقم الواتساب:")
        if st.form_submit_button("🔑 دخول / تسجيل"):
            if lv_name.strip() == st.session_state.site_settings['admin_name'] and lv_phone.strip() == st.session_state.site_settings['admin_password']:
                st.session_state.admin_logged_in = True
                st.success("مرحباً بك يا مدير المنصة!")
                st.rerun()
            elif lv_name and lv_phone:
                st.session_state.customer_logged_in = True
                st.session_state.current_customer_name = lv_name
                st.session_state.current_customer_phone = lv_phone
                subscriber_record = {"التاريخ": datetime.date.today().strftime("%Y-%m-%d"), "الاسم": lv_name, "الهاتف": lv_phone}
                if lv_phone not in [s['الهاتف'] for s in st.session_state.subscribers]:
                    st.session_state.subscribers.append(subscriber_record)
                    commit_to_database()
                st.success(f"أهلاً بك يا {lv_name}!")
                st.rerun()
            else:
                st.error("أدخل الاسم والرقم.")

    wa_n = st.session_state.site_settings['whatsapp_number']
    st.markdown(f'<a href="https://wa.me/{wa_n}" class="whatsapp-float" target="_blank">💬</a>', unsafe_allow_html=True)
    st.markdown(f'<div class="footer-box" style="background-color: {theme_col}; color: #FFFFFF;"><h3>{st.session_state.site_settings["site_title"]}</h3><p>جميع الحقوق محفوظة © 2026</p></div>', unsafe_allow_html=True)
