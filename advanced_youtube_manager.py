import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from googleapiclient.discovery import build

# --- 1. إعدادات الحالة (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'credentials' not in st.session_state:
    st.session_state.credentials = {
        "youtube_api_key": "", # سيتم إدخاله من واجهة التطبيق
        "telegram_token": "",
        "telegram_chat_id": ""
    }
if 'reports' not in st.session_state:
    st.session_state.reports = []

# --- 2. إعدادات الصفحة والتصميم (حل مشكلة الألوان) ---
st.set_page_config(page_title="YouTube Manager Pro", layout="wide")

st.markdown("""
    <style>
    /* إجبار التطبيق على ألوان واضحة للقراءة */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* تنسيق صناديق التقارير لتبدو كبطاقات بيضاء بنص أسود */
    .report-box { 
        background-color: #f8f9fa !important; 
        color: #1a1a1a !important; 
        padding: 20px; 
        border-radius: 12px; 
        border-right: 6px solid #ff4b4b; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border: 1px solid #eee;
    }
    
    /* العناوين باللون الأسود */
    h1, h2, h3, h4, p, span, label {
        color: #000000 !important;
    }

    /* تنسيق الشات (منطقة عرض التقارير) */
    .chat-container { 
        background-color: #e9ecef; 
        padding: 20px; 
        border-radius: 15px; 
        min-height: 450px; 
        border: 1px solid #ccc;
    }

    /* تحسين شكل الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. وظيفة البحث الدقيق (حل مشكلة كمال الأجسام) ---
def fetch_targeted_content(api_key, query):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        # البحث بالكلمة المفتاحية لضمان الدقة
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
        return f"خطأ تقني: {str(e)}"

# ==========================================
# 🏠 الصفحة الرئيسية
# ==========================================
if st.session_state.page == 'home':
    col_h1, col_h2 = st.columns([0.7, 0.3])
    with col_h1:
        st.title("🚀 مدير اليوتيوب الذكي 2026")
        st.write("قم باختيار التخصص وسيقوم النظام بالبحث والتحليل تلقائياً.")
    with col_h2:
        st.button("⚙️ الإعدادات والصلاحيات", on_click=lambda: st.session_state.update({"page": "settings"}))

    st.divider()

    c1, c2 = st.columns([0.6, 0.4])

    with c1:
        st.subheader("🎯 تحديد التخصص")
        niches = {
            "الرياضة 🏋️": ["كمال الأجسام", "تدريبات الكارديو", "اليوجا", "تخسيس"],
            "التكنولوجيا 💻": ["الذكاء الاصطناعي", "الربح من الإنترنت", "مراجعات تقنية"]
        }
        main_n = st.selectbox("المحتوى العام:", list(niches.keys()))
        sub_n = st.selectbox("التخصص الفرعي:", niches[main_n])
        
        if st.button("▶️ تشغيل التحليل الآن"):
            api_key = st.session_state.credentials['youtube_api_key']
            if not api_key:
                st.error("⚠️ يرجى إدخال YouTube API Key في صفحة الإعدادات أولاً!")
            else:
                with st.spinner(f"جاري البحث عن فيديوهات {sub_n} الحقيقية..."):
                    vids = fetch_targeted_content(api_key, sub_n)
                    if isinstance(vids, list) and vids:
                        report_content = f"✅ تم العثور على أفضل فيديوهات {sub_n}!\n\n"
                        report_content += f"🏆 العنوان: {vids[0]['title']}\n"
                        report_content += f"🔗 الرابط: {vids[0]['url']}\n\n"
                        report_content += "السكريبت المقترح: 'أهلاً بكم، اليوم سنتحدث عن أسرار المحترفين في {sub_n}...'"
                        
                        st.session_state.reports.append({
                            "time": datetime.now().strftime("%H:%M"), 
                            "text": report_content
                        })
                        st.success("✨ اكتمل التحليل بنجاح!")
                    else:
                        st.error("❌ لم يتم العثور على نتائج. تأكد من صحة مفتاح الـ API.")

    with c2:
        st.subheader("💬 شات التقارير والنتائج")
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        if not st.session_state.reports:
            st.markdown('<p style="color:#777; text-align:center; padding-top:180px;">لا توجد تقارير حالياً</p>', unsafe_allow_html=True)
        else:
            for m in st.session_state.reports:
                st.markdown(f'<div class="report-box"><b>[{m["time"]}]</b><br>{m["text"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ⚙️ صفحة الإعدادات
# ==========================================
else:
    st.button("⬅️ العودة للرئيسية", on_click=lambda: st.session_state.update({"page": "home"}))
    st.title("⚙️ الإعدادات والصلاحيات")
    
    st.write("أدخل بياناتك هنا ليقوم التطبيق بالدخول التلقائي للمنصات.")
    
    st.session_state.credentials['youtube_api_key'] = st.text_input("YouTube API Key v3:", value=st.session_state.credentials['youtube_api_key'], type="password")
    
    st.divider()
    st.subheader("ربط تيليجرام (اختياري)")
    st.session_state.credentials['telegram_token'] = st.text_input("Telegram Bot Token:", value=st.session_state.credentials['telegram_token'])
    st.session_state.credentials['telegram_chat_id'] = st.text_input("Telegram Chat ID:", value=st.session_state.credentials['telegram_chat_id'])
    
    if st.button("💾 حفظ الإعدادات"):
        st.success("✅ تم حفظ الإعدادات بنجاح!")
