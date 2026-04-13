import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from googleapiclient.discovery import build

# --- إعدادات الحالة (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'credentials' not in st.session_state:
    st.session_state.credentials = {
        "youtube_api_key": "", # ضع مفتاحك هنا أو في صفحة الإعدادات
        "telegram_token": "",
        "telegram_chat_id": ""
    }
if 'reports' not in st.session_state:
    st.session_state.reports = []

# --- إعدادات الصفحة ---
st.set_page_config(page_title="YouTube Manager Pro", layout="wide")

# --- تنسيق CSS لإصلاح مشكلة الألوان والرؤية ---
st.markdown("""
    <style>
    /* تحديد لون النص العام ليكون واضحاً */
    .stApp { color: #1a1a1a; }
    
    /* تنسيق صناديق التقارير لتعمل في كل الأوضاع */
    .report-box { 
        background-color: #ffffff !important; 
        color: #1a1a1a !important; 
        padding: 20px; 
        border-radius: 12px; 
        border-right: 6px solid #ff4b4b; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* تنسيق الشات */
    .chat-container { 
        background-color: #f0f2f6; 
        padding: 20px; 
        border-radius: 20px; 
        min-height: 400px; 
        border: 1px solid #ddd;
    }

    /* إصلاح لون العناوين */
    h1, h2, h3, h4 { color: #0e1117 !important; }
    
    /* زر التشغيل */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- وظيفة البحث الدقيق (إصلاح مشكلة كمال الأجسام) ---
def fetch_targeted_content(api_key, query):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        # البحث بالكلمة المفتاحية (Search) لضمان الدقة
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            order="relevance",
            maxResults=5
        )
        response = request.execute()
        videos = []
        for item in response.get('items', []):
            videos.append({
                "title": item['snippet']['title'],
                "url": f"https://youtube.com/watch?v={item['id']['videoId']}"
            })
        return videos
    except Exception as e:
        return f"خطأ: {str(e)}"

# ==========================================
# 🏠 الصفحة الرئيسية
# ==========================================
if st.session_state.page == 'home':
    col_h1, col_h2 = st.columns([0.7, 0.3])
    with col_h1:
        st.title("🚀 لوحة تحكم اليوتيوب الذكية")
    with col_h2:
        st.button("⚙️ الإعدادات والصلاحيات", on_click=lambda: st.session_state.update({"page": "settings"}))

    c1, c2 = st.columns([0.6, 0.4])

    with c1:
        st.subheader("🎯 استهداف النيتش")
        niches = {
            "الرياضة 🏋️": ["كمال الأجسام", "تدريبات الكارديو", "اليوجا"],
            "التكنولوجيا 💻": ["الذكاء الاصطناعي", "الربح من الإنترنت", "مراجعات تقنية"]
        }
        main_n = st.selectbox("المحتوى العام:", list(niches.keys()))
        sub_n = st.selectbox("التخصص الفرعي:", niches[main_n])
        
        if st.button("▶️ تشغيل التحليل الآن"):
            api_key = st.session_state.credentials['youtube_api_key']
            if not api_key:
                st.error("❌ يرجى إدخال YouTube API Key في الإعدادات أولاً!")
            else:
                with st.spinner(f"جاري البحث عن ترندات {sub_n}..."):
                    vids = fetch_targeted_content(api_key, sub_n)
                    if isinstance(vids, list) and vids:
                        report = f"✅ تقرير {sub_n} جاهز!\n\nأفضل فيديو: {vids[0]['title']}\nالرابط: {vids[0]['url']}"
                        st.session_state.reports.append({"time": datetime.now().strftime("%H:%M"), "text": report})
                        st.success("تم التوليد بنجاح!")
                    else:
                        st.error("لم نجد نتائج دقيقة. تأكد من المفتاح أو جرب تخصصاً آخر.")

    with c2:
        st.subheader("💬 شات التقارير")
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        if not st.session_state.reports:
            st.markdown('<p style="color:#666; text-align:center; padding-top:150px;">لا توجد تقارير حالياً</p>', unsafe_allow_html=True)
        for m in st.session_state.reports:
            st.markdown(f'<div class="report-box"><b>[{m["time"]}]</b><br>{m["text"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ⚙️ صفحة الإعدادات
# ==========================================
else:
    st.button("⬅️ العودة للرئيسية", on_click=lambda: st.session_state.update({"page": "home"}))
    st.title("⚙️ الإعدادات")
    
    st.session_state.credentials['youtube_api_key'] = st.text_input("YouTube API Key:", value=st.session_state.credentials['youtube_api_key'], type="password")
    st.session_state.credentials['telegram_token'] = st.text_input("Telegram Token:", value=st.session_state.credentials['telegram_token'])
    st.session_state.credentials['telegram_chat_id'] = st.text_input("Chat ID:", value=st.session_state.credentials['telegram_chat_id'])
    
    if st.button("💾 حفظ"):
        st.success("تم الحفظ بنجاح!")import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from googleapiclient.discovery import build

# --- إعدادات الحالة (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'credentials' not in st.session_state:
    st.session_state.credentials = {
        "youtube_api_key": "", # ضع مفتاحك هنا أو في صفحة الإعدادات
        "telegram_token": "",
        "telegram_chat_id": ""
    }
if 'reports' not in st.session_state:
    st.session_state.reports = []

# --- إعدادات الصفحة ---
st.set_page_config(page_title="YouTube Manager Pro", layout="wide")

# --- تنسيق CSS لإصلاح مشكلة الألوان والرؤية ---
st.markdown("""
    <style>
    /* تحديد لون النص العام ليكون واضحاً */
    .stApp { color: #1a1a1a; }
    
    /* تنسيق صناديق التقارير لتعمل في كل الأوضاع */
    .report-box { 
        background-color: #ffffff !important; 
        color: #1a1a1a !important; 
        padding: 20px; 
        border-radius: 12px; 
        border-right: 6px solid #ff4b4b; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* تنسيق الشات */
    .chat-container { 
        background-color: #f0f2f6; 
        padding: 20px; 
        border-radius: 20px; 
        min-height: 400px; 
        border: 1px solid #ddd;
    }

    /* إصلاح لون العناوين */
    h1, h2, h3, h4 { color: #0e1117 !important; }
    
    /* زر التشغيل */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- وظيفة البحث الدقيق (إصلاح مشكلة كمال الأجسام) ---
def fetch_targeted_content(api_key, query):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        # البحث بالكلمة المفتاحية (Search) لضمان الدقة
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            order="relevance",
            maxResults=5
        )
        response = request.execute()
        videos = []
        for item in response.get('items', []):
            videos.append({
                "title": item['snippet']['title'],
                "url": f"https://youtube.com/watch?v={item['id']['videoId']}"
            })
        return videos
    except Exception as e:
        return f"خطأ: {str(e)}"

# ==========================================
# 🏠 الصفحة الرئيسية
# ==========================================
if st.session_state.page == 'home':
    col_h1, col_h2 = st.columns([0.7, 0.3])
    with col_h1:
        st.title("🚀 لوحة تحكم اليوتيوب الذكية")
    with col_h2:
        st.button("⚙️ الإعدادات والصلاحيات", on_click=lambda: st.session_state.update({"page": "settings"}))

    c1, c2 = st.columns([0.6, 0.4])

    with c1:
        st.subheader("🎯 استهداف النيتش")
        niches = {
            "الرياضة 🏋️": ["كمال الأجسام", "تدريبات الكارديو", "اليوجا"],
            "التكنولوجيا 💻": ["الذكاء الاصطناعي", "الربح من الإنترنت", "مراجعات تقنية"]
        }
        main_n = st.selectbox("المحتوى العام:", list(niches.keys()))
        sub_n = st.selectbox("التخصص الفرعي:", niches[main_n])
        
        if st.button("▶️ تشغيل التحليل الآن"):
            api_key = st.session_state.credentials['youtube_api_key']
            if not api_key:
                st.error("❌ يرجى إدخال YouTube API Key في الإعدادات أولاً!")
            else:
                with st.spinner(f"جاري البحث عن ترندات {sub_n}..."):
                    vids = fetch_targeted_content(api_key, sub_n)
                    if isinstance(vids, list) and vids:
                        report = f"✅ تقرير {sub_n} جاهز!\n\nأفضل فيديو: {vids[0]['title']}\nالرابط: {vids[0]['url']}"
                        st.session_state.reports.append({"time": datetime.now().strftime("%H:%M"), "text": report})
                        st.success("تم التوليد بنجاح!")
                    else:
                        st.error("لم نجد نتائج دقيقة. تأكد من المفتاح أو جرب تخصصاً آخر.")

    with c2:
        st.subheader("💬 شات التقارير")
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        if not st.session_state.reports:
            st.markdown('<p style="color:#666; text-align:center; padding-top:150px;">لا توجد تقارير حالياً</p>', unsafe_allow_html=True)
        for m in st.session_state.reports:
            st.markdown(f'<div class="report-box"><b>[{m["time"]}]</b><br>{m["text"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ⚙️ صفحة الإعدادات
# ==========================================
else:
    st.button("⬅️ العودة للرئيسية", on_click=lambda: st.session_state.update({"page": "home"}))
    st.title("⚙️ الإعدادات")
    
    st.session_state.credentials['youtube_api_key'] = st.text_input("YouTube API Key:", value=st.session_state.credentials['youtube_api_key'], type="password")
    st.session_state.credentials['telegram_token'] = st.text_input("Telegram Token:", value=st.session_state.credentials['telegram_token'])
    st.session_state.credentials['telegram_chat_id'] = st.text_input("Chat ID:", value=st.session_state.credentials['telegram_chat_id'])
    
    if st.button("💾 حفظ"):
        st.success("تم الحفظ بنجاح!")