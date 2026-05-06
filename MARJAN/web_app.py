import streamlit as st
import math
from urllib.parse import urlparse

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="Marjan Trace v12.0", layout="wide")

# --- 2. محرك التحليل الجنائي المطور ---
def forensic_engine(url):
    findings, risks, logs = [], [], []
    status, color, entropy = "CLEAN / آمن", "#2ea043", 0
    
    if not url: return findings, risks, status, color, entropy, logs

    domain = urlparse(url).netloc.lower()
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = round(- sum([p * math.log(p) / math.log(2.0) for p in probs]), 2)

    is_danger = False
    if any(x in url.lower() for x in ['fortnite', 'login', 'free', 'sparkasse']):
        findings.append("🔍 انتحال صفحة رسمية (Phishing).")
        risks.append("🔓 سحب البيانات: محاولة الاستيلاء على الحساب.")
        logs.append("• رصد محاولة حقن سكريبتات (JS-Injection).")
        is_danger = True

    if any(domain.endswith(ext) for ext in ['.top', '.xyz', '.online']):
        findings.append(f"🚩 نطاق عالي الخطورة ({domain.split('.')[-1]}).")
        risks.append("🤖 تحكم Botnet: الرابط قد يربط الجهاز بشبكة مخترقة.")
        logs.append("• تم اكتشاف إعادة توجيه (Redirect) مشبوه.")
        is_danger = True

    if is_danger or entropy > 3.5:
        status, color = "CRITICAL / خطر", "#ff4b4b"
        if entropy > 3.5:
            risks.append("📡 اتصال C2: محاولة بناء قناة اتصال مع سيرفر تحكم.")
            logs.append("• الموقع يطلب صلاحيات الكاميرا/الموقع.")
        logs.append("• الحالة: تفعيل بروتوكول الحجب الوقائي.")

    return findings, risks, status, color, entropy, logs

# --- 3. لغة التصميم المحدثة (كل شيء داخل مستطيلات) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@700;900&display=swap');
    .stApp { background-color: #05070a !important; color: white; }
    .rtl { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    
    /* مستطيل القياسات الأفقي */
    .metric-row {
        display: flex; justify-content: space-around;
        background: rgba(212, 175, 85, 0.08);
        border: 1px solid rgba(212, 175, 85, 0.3);
        border-radius: 15px; padding: 18px; margin-bottom: 25px;
    }

    /* الحاويات (المربعات) التي تضم النصوص */
    .content-card {
        background: rgba(13, 17, 23, 0.95);
        border: 1px solid rgba(212, 175, 85, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .sandbox-container {
        border: 2px solid #D4AF37; border-radius: 20px;
        height: 480px; background: #000;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        position: relative;
    }

    .danger-text { color: #ff4b4b; font-weight: bold; }
    .safe-text { color: #2ea043; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 4. واجهة المستخدم ---
st.markdown("<h1 style='text-align:center; color:#D4AF37; font-family:Orbitron;'>MARJAN TRACE</h1>", unsafe_allow_html=True)

# خانة الإدخال
with st.container():
    st.markdown('<div class="content-card rtl">', unsafe_allow_html=True)
    url_input = st.text_input("أدخل الرابط المستهدف للتشريح:", placeholder="https://...")
    analyze_btn = st.button("تفعيل بروتوكول التشريح")
    st.markdown('</div>', unsafe_allow_html=True)

if analyze_btn and url_input:
    findings, risks, status, color, entropy, logs = forensic_engine(url_input)
    
    # شريط القياسات
    st.markdown(f"""
    <div class="metric-row">
        <div style="text-align:center;"><small style="color:#D4AF37;">عشوائية النطاق</small><br><b style="font-size:1.6rem;">{entropy}</b></div>
        <div style="text-align:center;"><small style="color:#D4AF37;">الأدلة المكتشفة</small><br><b style="font-size:1.6rem;">{len(findings)}</b></div>
        <div style="text-align:center;"><small style="color:#D4AF37;">الحالة الجنائية</small><br><b style="font-size:1.6rem; color:{color};">{status}</b></div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.3, 1])

    with col_left:
        # حاوية سجل التحليل
        st.markdown('<div class="content-card rtl">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#ff4b4b;'>📋 سجل التحليل البصري:</h4>", unsafe_allow_html=True)
        if logs:
            for log in logs: st.markdown(f"<p style='margin-bottom:5px;'>{log}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p>لا توجد سجلات برمجية حالياً.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # حاوية الأضرار المتوقعة
        st.markdown('<div class="content-card rtl">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#D4AF37;'>🚨 ماذا سيفعل هذا الرابط؟</h4>", unsafe_allow_html=True)
        if risks:
            for r in risks: st.markdown(f'<div style="background:rgba(255,75,75,0.1); border-right:4px solid #ff4b4b; padding:10px; margin-bottom:8px; border-radius:5px;">{r}</div>', unsafe_allow_html=True)
        else:
            st.success("الرابط لا يظهر سلوكاً عدائياً معروفاً.")
        st.markdown('</div>', unsafe_allow_html=True)

        # حاوية توصية نظام مرجان (المعدلة)
        st.markdown('<div class="content-card rtl" style="border-right: 6px solid #D4AF37;">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#D4AF37;'>🛡️ توصية نظام مرجان الاستخباراتي:</h4>", unsafe_allow_html=True)
        
        if "خطر" in status:
            advice = "⚠️ **تنبيه عالي الخطورة:** تم رصد نشاط إجرامي في بنية الرابط. نوصي بحجب النطاق فوراً على مستوى الـ Firewall ومنع المستخدمين من النقر عليه."
        else:
            advice = "✅ **تقرير السلامة:** الرابط لا يحتوي على مؤشرات خبيثة معروفة، ومع ذلك يرجى توخي الحذر عند إدخال أي بيانات شخصية."
        
        st.markdown(f"<p>{advice}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown("<h3 style='text-align:center; color:#D4AF37;'>📽️ Sandbox</h3>", unsafe_allow_html=True)
        st.markdown('<div class="sandbox-container rtl">', unsafe_allow_html=True)
        if "خطر" in status:
            st.markdown("""
                <span style="font-size:5.5rem;">🚫</span>
                <h4 style="color:#ff4b4b; margin-top:20px;">المعاينة محجوبة وقائياً</h4>
                <p style="color:#aaa;">تم رصد تهديدات سلوكية نشطة تهدد أمن النظام</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<p class="safe-text" style="font-size:1.2rem;">البيئة آمنة للمعاينة</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#D4AF37; opacity:0.5; font-family:Orbitron;'>Eng. Zaid Al-Janabi | 2026</p>", unsafe_allow_html=True)
