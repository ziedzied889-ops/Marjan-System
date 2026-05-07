import streamlit as st
import math
from urllib.parse import urlparse

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="Marjan Trace v15.0", layout="wide")

# --- 2. محرك التحليل الجنائي ---
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
    
    return findings, risks, status, color, entropy, logs

# --- 3. التصميم (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@700;900&display=swap');
    .stApp { background-color: #05070a !important; color: white; }
    .rtl { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    
    .metric-row {
        display: flex; justify-content: space-around;
        background: rgba(212, 175, 85, 0.08);
        border: 1px solid rgba(212, 175, 85, 0.3);
        border-radius: 15px; padding: 18px; margin-bottom: 25px;
    }

    .content-card {
        background: rgba(13, 17, 23, 0.95);
        border: 1px solid rgba(212, 175, 85, 0.2);
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
    }
    
    .sandbox-frame {
        border: 2px solid #D4AF37; border-radius: 20px;
        height: 500px; width: 100%; background: #fff; overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. واجهة المستخدم ---
st.markdown("<h1 style='text-align:center; color:#D4AF37; font-family:Orbitron;'>MARJAN TRACE</h1>", unsafe_allow_html=True)

st.markdown('<div class="content-card rtl">', unsafe_allow_html=True)
url_input = st.text_input("أدخل الرابط المستهدف للتشريح:", placeholder="https://...")
analyze_btn = st.button("تفعيل بروتوكول التشريح")
st.markdown('</div>', unsafe_allow_html=True)

if analyze_btn and url_input:
    findings, risks, status, color, entropy, logs = forensic_engine(url_input)
    
    st.markdown(f"""
    <div class="metric-row">
        <div style="text-align:center;"><small style="color:#D4AF37;">عشوائية النطاق</small><br><b style="font-size:1.6rem;">{entropy}</b></div>
        <div style="text-align:center;"><small style="color:#D4AF37;">الأدلة المكتشفة</small><br><b style="font-size:1.6rem;">{len(findings)}</b></div>
        <div style="text-align:center;"><small style="color:#D4AF37;">الحالة الجنائية</small><br><b style="font-size:1.6rem; color:{color};">{status}</b></div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown('<div class="content-card rtl">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#ff4b4b;'>📋 سجل التحليل البصري:</h4>", unsafe_allow_html=True)
        for log in logs: st.markdown(f"<p>{log}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="content-card rtl">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#D4AF37;'>🚨 ماذا سيفعل هذا الرابط؟</h4>", unsafe_allow_html=True)
        for r in risks: st.markdown(f'<div style="background:rgba(255,75,75,0.1); border-right:4px solid #ff4b4b; padding:10px; margin-bottom:8px;">{r}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="content-card rtl" style="border-right: 6px solid #D4AF37;">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#D4AF37;'>🛡️ توصية نظام مرجان الاستخباراتي:</h4>", unsafe_allow_html=True)
        advice = "⚠️ تنبيه عالي الخطورة: نوصي بحجب الرابط فوراً." if "خطر" in status else "✅ تقرير السلامة: الرابط لا يحتوي على مؤشرات خبيثة حالياً."
        st.markdown(f"<p>{advice}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown("<h3 style='text-align:center; color:#D4AF37;'>📽️ Sandbox</h3>", unsafe_allow_html=True)
        # تم الإبقاء على المعاينة الداخلية فقط وحذف الرابط الخارجي لزيادة الأمان
        st.markdown(f'<div class="sandbox-frame"><iframe src="{url_input}" width="100%" height="100%" style="border:none;"></iframe></div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#D4AF37; opacity:0.5; font-family:Orbitron;'>Eng. Zaid Al-Janabi | 2026</p>", unsafe_allow_html=True)
