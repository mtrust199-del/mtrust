import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
from googleapiclient.discovery import build

# --- 1. إعدادات الحالة ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'credentials' not in st.session_state:
    st.session_state.credentials = {"youtube_api_key": "AIzaSyA7mpBkFaeN6-G04aMppS5tF4dwXtF_BaQ"}
if 'reports' not in st.session_state:
    st.session_state.reports = []

# --- 2. إعدادات التصميم (ألوان واضحة جداً) ---
st.set_page_config(page_title="YouTube AI Manager", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; color: #000000 !important; }
    .report-box { 
        background-color: #fdfdfd !important; color: #1a1a1a !important; 
        padding: 25px; border-radius: 15px; border-right: 8px solid #ff4b4b; 
        margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #eee;
    }
    h1, h2, h3, h4, p, span, label { color: #000000 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .chat-container { background-color: #f1f3f5; padding: 25px; border-radius: 20px; min-height: 500px; border: 1px solid #ddd; }
    .stButton>button { border-radius: 10px; background-color: #ff4b4b; color: white; height: 3em; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 3. وظيفة التحليل الذكي (إصدار المحترفين) ---
def fetch_and_analyze(api_key, query):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        # 1. البحث عن أفضل 5 فيديوهات في آخر 5 أيام
        five_days_ago = (datetime.utcnow() - timedelta(days=5)).isoformat() + "Z"
        
        request = youtube.search().list(
            q=query, part="snippet", type="video", order="viewCount",
            publishedAfter=five_days_ago, maxResults=5
        )
        response = request.execute()
        
        vids = []
        titles = []
        for item in response.get('items', []):
            title = item['snippet']['title']
            vids.append({"title": title, "url": f"https://youtube.com/watch?v={item['id']['videoId']}"})
            titles.append(title)
        
        if not vids: return "لم يتم العثور على فيديوهات جديدة في آخر 5 أيام."

        # 2. محاكاة تحليل الذكاء الاصطناعي للترند والسكريبت
        main_topic = titles[0]
        summary = f"الموضوع الأكثر رواجاً الآن في {query} هو: '{main_topic}'، حيث تركز الفيديوهات المتصدرة على النتائج السريعة والتقنيات الحديثة."
        
        script = f"""
        🎬 **السكريبت الاحترافي للقناة (شخصية خبير كمال أجسام)**
        
        ⚡ **[الإنترو - 30 ثانية]:**
        "أهلاً بكم يا وحوش! هل سألت نفسك لماذا يتطور الجميع وأنت مكانك؟ اليوم، وبعد تحليل أكثر الفيديوهات تفاعلاً هذا الأسبوع، سأعطيك الخلاصة التي ستغير تمرينك 180 درجة."
        
        📚 **[المحتوى الرئيسي]:**
        بناءً على ما حقق ملايين المشاهدات مؤخراً، سنركز على 3 نقاط:
        1. التقنية الصحيحة التي ذكرها فيديو '{titles[0]}'.
        2. خطأ شائع يقع فيه المبتدئون كما رأينا في فيديوهات هذا الأسبوع.
        3. سر الاستشفاء العضلي لضمان الضخامة.
        
        🎯 **[الخاتمة]:**
        "جرب هذه النصائح واكتب لي في التعليقات النتيجة. لا تنسَ الاشتراك لتكون أول من يحصل على أسرار الترند القادم. نراكم في القمة!"
        """
        
        return {"vids": vids, "analysis": summary, "script": script}
    except Exception as e:
        return f"خطأ: {str(e)}"

# ==========================================
# 🏠 الصفحة الرئيسية
# ==========================================
if st.session_state.page == 'home':
    col_h1, col_h2 = st.columns([0.7, 0.3])
    with col_h1:
        st.title("🎬 مدير القناة الذكي (إصدار التحليل)")
    with col_h2:
        st.button("⚙️ الإعدادات", on_click=lambda: st.session_state.update({"page": "settings"}), use_container_width=True)

    st.divider()
    c1, c2 = st.columns([0.55, 0.45])

    with c1:
        st.subheader("🎯 اختيار التخصص")
        main_n = st.selectbox("المحتوى العام:", ["الرياضة 🏋️", "التكنولوجيا 💻", "الصحة 🥗"])
        sub_n = st.selectbox("التخصص الفرعي:", ["كمال الأجسام", "تخسيس", "تدريبات منزلية"] if "الرياضة" in main_n else ["الذكاء الاصطناعي", "أدوات تقنية"])
        
        if st.button("🚀 تشغيل التحليل العميق"):
            api_key = st.session_state.credentials['youtube_api_key']
            with st.spinner(f"جاري تجميع وتحليل فيديوهات {sub_n}..."):
                result = fetch_and_analyze(api_key, sub_n)
                if isinstance(result, dict):
                    # بناء نص التقرير الكامل
                    full_report = f"### 📊 تحليل الترند لـ {sub_n}\n\n"
                    full_report += f"🔍 **الخلاصة:** {result['analysis']}\n\n"
                    full_report += "🔗 **أفضل 5 فيديوهات اعتمدنا عليها:**\n"
                    for v in result['vids']:
                        full_report += f"- [{v['title']}]({v['url']})\n"
                    full_report += "\n---\n"
                    full_report += result['script']
                    
                    st.session_state.reports.append({"time": datetime.now().strftime("%H:%M"), "text": full_report})
                    st.success("✨ تم إنشاء التقرير والسكريبت!")
                else:
                    st.error(result)

    with c2:
        st.subheader("💬 التقارير والسكريبتات الجاهزة")
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        if not st.session_state.reports:
            st.markdown('<p style="color:#777; text-align:center; padding-top:200px;">بانتظار تشغيل التحليل...</p>', unsafe_allow_html=True)
        else:
            for m in st.session_state.reports:
                st.markdown(f'<div class="report-box"><b>[{m["time"]}]</b><br>{m["text"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ⚙️ صفحة الإعدادات
# ==========================================
else:
    st.button("⬅️ العودة", on_click=lambda: st.session_state.update({"page": "home"}))
    st.title("⚙️ الإعدادات")
    st.session_state.credentials['youtube_api_key'] = st.text_input("YouTube API Key:", value=st.session_state.credentials['youtube_api_key'], type="password")
    if st.button("💾 حفظ"):
        st.success("✅ تم الحفظ!")
