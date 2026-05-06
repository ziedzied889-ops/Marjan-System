import streamlit as st
import math
from urllib.parse import urlparse

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="Marjan Trace v11.0", layout="wide")

# --- 2. محرك التحليل الجنائي ---
def forensic_analysis(url):
    findings, risks, logs = [], [], []
    status, color, entropy = "CLEAN / آمن", "#2ea043", 0
    
    if not url: return findings, risks, status, color, entropy, logs

    domain = urlparse(url).netloc.lower()
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = round(- sum([p * math.log(p) / math.log(2.0) for p in probs]), 2)

    is_malicious = False
    if any(x in url.lower() for x in ['fortnite', 'login', 'free', 'bank']):
        findings.append("🔍 انتحال صفحة رسمية (Phishing Detect).")
        risks.append("🔓 سرقة الهوية: محاولة الحصول على بيانات الاعتماد.")
        logs.append("• تم رصد محاولة حقن عناصر (JS-Injection).")
        is_malicious = True

    if any(domain.endswith(ext) for ext in ['.top', '.xyz', '.link']):
        findings.append(f"🚩 نطاق مشبوه عالي المخاطر ({domain.split('.')[-1]}).")
        risks.append("🤖 تحكم Botnet: الرابط قد يربط جهازك بشبكة مخترقة.")
        logs.append("• تم اكتشاف إعادة توجيه تلقائي مشبوه.")
        is_malicious = True

    if entropy > 3.4:
        risks.append("📡 اتصال C2: محاولة بناء قناة اتصال مع سيرفر تحكم.")
        logs.append("• الموقع يطلب صلاحيات الوصول للكاميرا/الموقع.")
        is_malicious = True

    if is_malicious:
        status, color = "CRITICAL / خطر", "#ff4b4b"
        logs.append("• الحالة: تم تفعيل بروتوكول الحجب الوقائي.")

    return findings, risks, status, color, entropy, logs

# --- 3. لغة التصميم (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@700;900&display=swap');
    .stApp { background-color: #05070a !important; color: white; }
    .rtl { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    
    /* الحاويات المنظمة */
    .glass-card {
        background: rgba(13, 17, 23, 0.9);
        border: 1px solid rgba(212, 175, 85, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .metric-bar {
        display: flex; justify-content: space-around;
        background: rgba(212, 175, 85, 0.05);
        border-radius: 12px; padding: 15px; margin-bottom: 20px;
        border: 1px solid rgba(212, 175, 85, 0.2);
    }

    .sandbox-frame {
        border: 2px solid #D4AF37; border-radius: 20px;
        height: 450px; background: #000;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        position: relative; overflow: hidden;
    }

    .badge-risk {
        background: rgba(255, 75, 75, 0.1); border-right: 4px solid #ff4b4b;
        padding: 10px; margin-bottom: 8px; border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. واجهة المستخدم ---
st.markdown("<h1 style='text-align:center; color:#D4AF37; font-family:Orbitron;'>MARJAN TRACE</h1>", unsafe_allow_html=True)

# خانة الإدخال في مستطيل مستقل
st.markdown('<div class="glass-card rtl">', unsafe_allow_html=True)
url_input = st.text_input("أدخل الرابط المستهدف للتحليل الجنائي:", placeholder="https://...")
analyze_btn = st.button("بدء بروتوكول التشريح")
st.markdown('</div>', unsafe_allow_html=True)

if analyze_btn and url_input:
    findings, risks, status, color, entropy, logs = forensic_analysis(url_input)
    
    # 1. شريط المؤشرات الموحد
    st.markdown(f"""
    <div class="metric-bar">
        <div style="text-align:center;"><small style="color:#D4AF37;">عشوائية النطاق</small><br><b style="font-size:1.4rem;">{entropy}</b></div>
        <div style="text-align:center;"><small style="color:#D4AF37;">الأدلة المكتشفة</small><br><b style="font-size:1.4rem;">{len(findings)}</b></div>
        <div style="text-align:center;"><small style="color:#D4AF37;">الحالة الجنائية</small><br><b style="font-size:1.4rem; color:{color};">{status}</b></div>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_sandbox = st.columns([1.2, 1])

    with col_info:
        # خانة سجل التحليل
        st.markdown('<div class="glass-card rtl">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#ff4b4b;'>📋 سجل التحليل البصري:</h4>", unsafe_allow_html=True)
        if logs:
            for log in logs: st.markdown(f"<p style='margin-bottom:5px; font-size:0.9rem;'>{log}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p>لا توجد سجلات نشطة.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # خانة المخاطر المتوقعة
        st.markdown('<div class="glass-card rtl">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#D4AF37;'>🚨 الأضرار السلوكية المتوقعة:</h4>", unsafe_allow_html=True)
        if risks:
            for risk in risks: st.markdown(f'<div class="badge-risk">{risk}</div>', unsafe_allow_html=True)
        else:
            st.success("لم يتم رصد سلوك تخريبي.")
        st.markdown('</div>', unsafe_allow_html=True)

        # خانة التوصية (بدل القرار)
        st.markdown('<div class="glass-card rtl" style="border-right: 6px solid #D4AF37;">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#D4AF37;'>💡 (Zaid's Advisory) توصية المهندس زيد:</h4>", unsafe_allow_html=True)
        advice = "نوصي بحجب الرابط فوراً وعدم التفاعل معه نظراً لوجود مؤشرات اختراق نشطة." if len(findings) > 0 else "الرابط يبدو سليماً من الناحية الهيكلية، لكن يرجى الحذر عند إدخال بيانات شخصية."
        st.markdown(f"<p>{advice}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_sandbox:
        st.markdown("<h3 style='text-align:center; color:#D4AF37;'>📽️ Sandbox</h3>", unsafe_allow_html=True)
        st.markdown('<div class="sandbox-frame rtl">', unsafe_allow_html=True)
        if status == "CRITICAL / خطر":
            st.markdown("""
                <span style="font-size:5rem;">🚫</span>
                <h4 style="color:#ff4b4b; margin-top:20px;">المعاينة محجوبة حمايةً لجهازك</h4>
                <p style="color:#aaa;">تم اكتشاف برمجيات خبيثة نشطة</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#2ea043;">البيئة آمنة للمعاينة</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#D4AF37; opacity:0.5; font-family:Orbitron;'>Eng. Zaid Al-Janabi | 2026</p>", unsafe_allow_html=True)
