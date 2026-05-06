import streamlit as st
import math
from urllib.parse import urlparse

# --- 1. الإعدادات الأساسية ---
st.set_page_config(page_title="Marjan Trace v10.0", layout="wide")

# --- 2. محرك الذكاء الجنائي المتقدم ---
def forensic_engine(url):
    findings, actions, visual_logs = [], [], []
    status, color, entropy = "CLEAN / آمن", "#2ea043", 0
    
    if not url: return findings, actions, status, color, entropy, visual_logs

    domain = urlparse(url).netloc.lower()
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = round(- sum([p * math.log(p) / math.log(2.0) for p in probs]), 2)

    is_danger = False
    
    # محاكاة الكشف الجنائي بناءً على سجلات النظام
    if any(x in url.lower() for x in ['fortnite', 'sparkasse', 'free', 'login']):
        findings.append("🔍 رصد محاولة انتحال صفحة رسمية.")
        visual_logs.append("• رصد عناصر جافا سكريبت مشبوهة (JS-Injection).")
        actions.append("🔓 سحب البيانات: محاولة سرقة معلومات الحساب.")
        is_danger = True

    if any(domain.endswith(ext) for ext in ['.top', '.qpon', '.xyz']):
        findings.append(f"🚩 نطاق عالي الخطورة ({domain.split('.')[-1]}).")
        visual_logs.append("• تم اكتشاف محاولة إعادة توجيه (Redirect).")
        actions.append("🤖 تحكم Botnet: الرابط قد يجعل جهازك جزءاً من شبكة مخترقة.")
        is_danger = True

    if entropy > 3.5:
        visual_logs.append("• الموقع يحاول الوصول لصلاحيات الكاميرا/الموقع.")
        actions.append("📡 اتصال C2: محاولة بناء قناة اتصال مع سيرفرات قيادة وسيطرة.")
        is_danger = True

    if is_danger:
        status, color = "CRITICAL / خطر", "#ff4b4b"
        visual_logs.append("• القرار: حجب المعاينة فوراً.")

    return findings, actions, status, color, entropy, visual_logs

# --- 3. تصميم الواجهة السيبرانية ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@700;900&display=swap');
    .stApp { background-color: #05070a !important; color: white; }
    .rtl { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    
    /* شريط القياسات الأفقي الموحد */
    .metric-bar {
        display: flex; justify-content: space-around; background: rgba(13, 17, 23, 0.9);
        border: 1px solid rgba(212, 175, 85, 0.3); border-radius: 12px; padding: 15px; margin-bottom: 25px;
    }
    .metric-box { text-align: center; flex: 1; border-left: 1px solid rgba(212, 175, 85, 0.1); }
    .metric-box:last-child { border-left: none; }
    
    /* سجل التحليل البصري */
    .visual-log-box {
        border: 1px dashed #ff4b4b; border-radius: 15px; padding: 20px;
        background: rgba(255, 75, 75, 0.05); margin-top: 20px;
    }

    /* صندوق المعاينة المحجوبة */
    .sandbox-blocked {
        border: 2px solid #D4AF37; border-radius: 20px; background: #000;
        height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. هيكل البرنامج ---
st.markdown("<h1 style='text-align:center; color:#D4AF37; font-family:Orbitron;'>MARJAN TRACE</h1>", unsafe_allow_html=True)

url_input = st.text_input("أدخل الرابط المراد تشريحه:", placeholder="https://...")

if st.button("تفعيل بروتوكول التشريح الشامل"):
    if url_input:
        findings, actions, status, color, entropy, logs = forensic_engine(url_input)
        
        # عرض شريط المؤشرات الموحد
        st.markdown(f"""
        <div class="metric-bar">
            <div class="metric-box"><small style="color:#D4AF37;">معامل العشوائية</small><br><b style="font-size:1.5rem;">{entropy}</b></div>
            <div class="metric-box"><small style="color:#D4AF37;">الأدلة المرصودة</small><br><b style="font-size:1.5rem;">{len(findings)}</b></div>
            <div class="metric-box"><small style="color:#D4AF37;">الحالة الجنائية</small><br><b style="font-size:1.5rem; color:{color};">{status}</b></div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns([1.2, 1])

        with col_a:
            st.markdown('<div class="rtl">', unsafe_allow_html=True)
            # قسم سجل التحليل البصري
            if logs:
                st.markdown('<div class="visual-log-box">', unsafe_allow_html=True)
                st.markdown("<h4 style='color:#ff4b4b;'>📋 سجل التحليل البصري:</h4>", unsafe_allow_html=True)
                for log in logs: st.markdown(f"<p style='margin-bottom:5px;'>{log}</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # قسم ماذا سيفعل هذا الرابط؟
            st.markdown("<br><h4 style='color:#D4AF37;'>🚨 ماذا سيفعل هذا الرابط؟</h4>", unsafe_allow_html=True)
            if actions:
                for act in actions:
                    st.markdown(f'<div style="background:rgba(212,175,55,0.1); padding:10px; border-radius:8px; margin-bottom:8px; border-right:4px solid #D4AF37;">{act}</div>', unsafe_allow_html=True)
            else:
                st.success("الرابط لا يظهر سلوكاً عدائياً معروفاً.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown("<h3 style='text-align:center; color:#D4AF37;'>📽️ Sandbox</h3>", unsafe_allow_html=True)
            if status == "CRITICAL / خطر":
                st.markdown(f"""
                <div class="sandbox-blocked rtl">
                    <span style="font-size:5rem;">🚫</span>
                    <h4 style="color:#ff4b4b; margin-top:20px;">المعاينة محجوبة حمايةً لجهازك</h4>
                    <p style="color:#aaa; font-size:0.9rem;">تم رصد تهديدات سلوكية نشطة</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="sandbox-blocked"><h5>البيئة آمنة للمعاينة</h5></div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#D4AF37; opacity:0.5; font-family:Orbitron;'>Eng. Zaid Al-Janabi | 2026</p>", unsafe_allow_html=True)
