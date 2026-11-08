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

st.markdown(f"""
<style>
    [data-testid="stSidebar"] {{ display: none; }}
    .stApp {{ 
        direction: rtl !important; 
        text-align: right !important; 
        background-color: {bg_col} !important; 
        font-family: 'Amiri', Tahoma, sans-serif;
    }}
    .book-card {{
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .book-title {{ font-size: 18px; font-weight: bold; color: {theme_col}; margin-bottom: 5px; }}
    .book-author {{ color: #555; font-size: 14px; }}
    .book-price {{ font-size: 19px; font-weight: bold; color: #B8860B; margin-top: 8px; }}
    .slider-container {{
        display: flex; overflow-x: auto; gap: 15px; padding: 15px 5px; scroll-behavior: smooth; margin-bottom: 25px; white-space: nowrap;
    }}
    .slider-container::-webkit-scrollbar {{ display: none; }}
    .slider-card {{
        min-width: 180px
