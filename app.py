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

# 3. تهيئة الإعدادات الديناميكية (القابلة للتعديل من لوحة الإدارة)
if 'site_settings' not in st.session_state:
    st.session_state.site_settings = {
        "whatsapp_number": "201033393575",
        "facebook_url": "https://facebook.com",
        "btn_whatsapp_label": "💬 تواصل عبر الواتساب",
        "btn_facebook_label": "📘 صفحة الفيسبوك",
        "hero_title": "📖 الأَحْرُفُ السـ7ـبْعَة",
        "hero_subtitle": "✦ لِكُتُبِ القِرَاءَاتِ وَعُلُومِ القُرْآنِ الكَرِيمِ ✦",
        "shipping_cost": 60.0
    }

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

# 4. تنسيقات التصميم الفخمة
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

    .hero-banner {
        background: linear-gradient(rgba(11, 60, 38, 0.75), rgba(31, 94, 59, 0.75)), 
                    url('https://images.unsplash.com/photo-1590073844006-33379778ae09?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 50px 20px;
        border-radius: 16px;
        color: #FFD700;
        text-align: center;
        margin-bottom: 25px;
        border: 2px solid #FFD700;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .hero-title { font-size: 42px; font-weight: 900; margin-bottom: 8px; text-shadow: 2px 2px 8px rgba(0,0,0,0.7); color: #FFD700; }
    .hero-sub { font-size: 18px; color: #FFFFFF; font-weight: bold; text-shadow: 1px 1px 5px rgba(0,0,0,0.7); }

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
    .book-price { font-size: 19px; font-weight: bold; color: #B8860B; margin-top:
