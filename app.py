import streamlit as st
import pandas as pd
import datetime

# 1. إعدادات الصفحة (بدون شريط جانبي نهائياً)
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
        "admin_password": "1234",
        "theme_color": "#0B3C26"
    }

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if 'subscribers' not in st.session_state:
    st.session_state.subscribers = []

if 'customer_logged_in' not in st.session_state:
    st.session_state.customer_logged_in = False

if 'current_customer_phone' not in st.session_state:
    st.session_state.current_customer_phone = ""

if 'current_customer_name' not in st.session_state:
    st.session_state.current_customer_name = ""

if 'customer_wishlists' not in st.session_state:
    st.session_state.customer_wishlists = {} 

if 'admin_chat_history' not in st.session_state:
    st.session_state.admin_chat_history = [
        {"role": "assistant", "content": "أهلاً بك يا مديرنا الفاضل في لوحة التحكم الذكية! أنا مساعدك الآلي، اطلب مني أي شيء (تغيير لون الموقع، تعديل صورة البانر، إضافة خصم، أو الاستفسار عن الطلبات) وسأقوم بتنفيذه ومناقشتك فوراً."}
    ]

if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"رقم_الكتاب": 1, "عنوان الكتاب": "مصحف الصحابة بالهامش لجمع القراءات العشر (أصفر)", "المؤلف / المحقق": "الشيخ توفيق ضمرة", "دار النشر": "دار الصحابة للتراث", "بلد النشر": "مصر", "وصف الطبعة": "طبعة دار الصحابة طنطا", "سعر الشراء": 320.0, "سعر البيع": 380.0, "الكمية": 15, "التصنيف": "مصاحف القراءات", "الباركود": "622100001001", "صورة_الغلاف": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=400&q=80"},
        {"رقم_الكتاب": 2, "عنوان الكتاب": "مصحف الصحابة بالهامش لجمع القراءات العشر (جوامعي)", "المؤلف / المحقق": "الشيخ توفيق ضمرة", "دار النشر": "دار الصحابة للتراث", "بلد النشر": "مصر", "وصف الطبعة": "الطبعة الكبرى الجوامعية", "سعر الشراء": 450.0, "سعر البيع": 520.0, "الكمية": 10, "التصنيف": "مصاحف القراءات", "الباركود": "622100001002", "صورة_الغلاف": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=400&q=80"},
        {"رقم_الكتاب": 3, "عنوان الكتاب": "مصحف القراءات التعليمي بالترميز اللوني", "المؤلف / المحقق": "لجنة من العلماء", "دار النشر": "دار المعرفة", "بلد النشر": "سوريا", "وصف الطبعة": "طبعة دار المعرفة دمشق", "سعر الشراء": 380.0, "سعر البيع": 450.0, "الكمية": 12, "التصنيف": "مصاحف القراءات", "الباركود": "622100001003", "صورة_الغلاف": "https://images.unsplash.com/photo-1495640388908-05fa85288e61?auto=format&fit=crop&w=400&q=80"},
        {"رقم_الكتاب": 4, "عنوان الكتاب": "متن حرز الأماني ووجه التهاني (الشاطبية)", "المؤلف / المحقق": "الإمام الشاطبي", "دار النشر": "دار الغوثاني للدراسات", "بلد النشر": "سوريا", "وصف الطبعة": "طبعة دار الغوثاني", "سعر الشراء": 85.0, "سعر البيع": 110.0, "الكمية": 30, "التصنيف": "المتون", "الباركود": "622100001008", "صورة_الغلاف": "https://images.unsplash.com/photo-1532012197267-da84d127e765?auto=format&fit=crop&w=400&q=80"},
        {"رقم_الكتاب": 5, "عنوان الكتاب": "متن المقدمة الجزرية في تجويد القرآن", "المؤلف / المحقق": "الإمام ابن الجزري", "دار النشر": "دار ابن الجزري", "بلد النشر": "السعودية", "وصف الطبعة": "تحقيق د. أيمن سويد", "سعر الشراء": 45.0, "سعر البيع": 60.0, "الكمية": 50, "التصنيف": "المتون", "الباركود": "622100001012", "صورة_الغلاف": "https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?auto=format&fit=crop&w=400&q=80"},
        {"رقم_الكتاب": 6, "عنوان الكتاب": "الوافي في شرح الشاطبية", "المؤلف / المحقق": "د. عبد الفتاح القاضي", "دار النشر": "دار السلام بالقاهرة", "بلد النشر": "مصر", "وصف الطبعة": "طبعة دار السلام", "سعر الشراء": 240.0, "سعر البيع": 290.0, "الكمية": 15, "التصنيف": "الشروحات", "الباركود": "622100001022", "صورة_الغلاف": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=400&q=80"}
    ])

if 'customer_cart' not in st.session_state:
    st.session_state.customer_cart = []

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'reports' not in st.session_state:
    st.session_state.reports = []

# 3. تنسيقات التصميم الديناميكية
theme_color = st.session_state.site_settings['theme_color']
st.markdown(f"""
<style>
    [data-testid="stSidebar"] {{ display: none; }}
    .stApp {{ 
        direction: rtl !important; 
        text-align: right !important; 
        background-color: #F8FAF9 !important; 
        font-family: 'Amiri', Tahoma, sans-serif;
    }}
    .book-card {{
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: right;
        word-wrap: break-word;
    }}
    .book-title {{ font-size: 18px; font-weight: bold; color: {theme_color}; margin-bottom: 5px; }}
    .book-author {{ color: #555; font-size: 14px; }}
    .book-price {{ font-size: 19px; font-weight: bold; color: #B8860B; margin-top: 8px; }}
    .edition-badge {{ background-color: #FFF3CD; color: #856404; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; display: inline-block; }}
    
    .slider-container {{
        display: flex; overflow-x: auto; gap: 15px; padding: 15px 5px; scroll-behavior: smooth; margin-bottom: 25px; white-space: nowrap;
    }}
    .slider-container::-webkit-scrollbar {{ display: none; }}
    .slider-card {{
        min-width: 180px; max-width: 180px; background: white; border-radius: 10px; border: 1px solid #ddd; padding: 10px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.08); flex-shrink: 0;
    }}
    .slider-card img {{ width: 100%; height: 120px; object-fit: cover; border-radius: 6px; }}
    .slider-card p {{ font-size: 13px; font-weight: bold; color: {theme_color}; margin-top: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

    .whatsapp-float {{
        position: fixed; bottom: 25px; left: 25px; background-color: #25D366; color: #FFF;
        border-radius: 50px; text-align: center; font-size: 30px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
        z-index: 999; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; text-decoration: none;
    }
    .footer-box {{
        background-color: {theme_color}; color: #FFFFFF; padding: 25px; border-radius: 12px; text-align: center; margin-top: 40px; border-top: 3px solid #FFD700;
    }
    .footer-links a {{ color: #FFD700; text-decoration: none; margin: 0 15px; font-weight: bold; font-size: 16px;
