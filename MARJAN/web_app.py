import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري (الهوية البصرية المعتمدة - ثابتة تماماً) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #05070a !important;
        background-image: 
            url("https://www.transparentpng.com/download/security/shield-security-icon-9.png"),
            linear-gradient(rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            radial-gradient(circle at center, #11141a 0%, #05070a 100%) !important;
        background-position: center 40%, center, center, center !important;
        background-repeat: no-repeat, repeat, repeat, no-repeat !important;
        background-size: 380px auto, 30px 30px, 30px 30px, 100% 100% !important;
        background-attachment: fixed !important;
    }
    h1 { color: #D4AF37 !important; text-align: center; text-shadow: 0px 0px 20px rgba(212, 175, 55, 0.8) !important; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { width: 100%; background-color: #D4AF37 !important; color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em; }
    .heuristic-danger { padding: 15px; border-radius: 10px; border-right: 6px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.25); color: #ff9999; text-align: right; margin-bottom: 10px; font-weight: bold; border-left: 1px solid rgba(255,75,75,0.4); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.98); border-top: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك التحليل الجنائي المتقدم (M.T Aggressive Core v5.8) ---
def aggressive_marjan_logic(url):
    reasons = []
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()
    
    # 1. كشف كلمات التهديد المباشرة (هندسة اجتماعية)
    danger_keywords = ['merit', 'king', 'bet', 'win', 'prize', 'bonus', 'claim', 'verify', 'update', 'vave', 'login', 'crypto']
    if any(word in full_url for word in danger_keywords):
        reasons.append("🚨 هندسة اجتماعية: تم رصد كلمات استدراج مخصصة لهجمات التصيد المباشر.")

    # 2. كشف "الاحتيال المالي وتصفية الديون" (تحديث خاص لحالتك الجديدة)
    # نكشف كلمات مثل 'divida' (دين بالبرتغالية) أو 'debt' أو 'zero' في سياق مريب
    financial_scam_keywords = ['divida', 'debt', 'zero', 'pague', 'acordo', 'credit', 'loan']
    if any(word in full_url for word in financial_scam_keywords) and ('.com' in domain or '.br' in domain):
         reasons.append("🚨 احتيال مالي محتمل: الرابط يحتوي على نمط 'تصفية الديون' المشبوه الذي يستهدف استدراج الضحايا مالياً.")

    # 3. كشف خدعة "التصويت والفعاليات"
    if 'vote' in full_url or ('event' in full_url and 'vote' in full_url):
         reasons.append("🚨 نمط تصويت احتيالي: المهاجم يستخدم نظام 'التصويت' (Vote) كغطاء لسرقة البيانات.")

    # 4. كشف انتحال الهوية
    brands = ['bybit', 'binance', 'metamask', 'trust', 'paypal', 'netflix', 'apple', 'instagram', 'facebook', 'whatsapp']
    for b in brands:
        if b in domain and domain != f"{b}.com":
            reasons.append(f"⚠️ انتحال علامة تجارية: النطاق يحاول تقليد منصة '{b.capitalize()}' بشكل غير رسمي.")

    # 5. تحليل بنية النطاق والبروتوكول
    if url.startswith("http://"):
        reasons.append("🔓 بروتوكول غير آمن: الرابط لا يدعم التشفير، مما يسهل عملية اعتراض البيانات.")
    if len(domain) > 20 or domain.count('-') > 1:
        reasons.append("❗ بنية مريبة: اسم النطاق طويل أو يحتوي على فواصل متعددة لإخفاء الهوية الحقيقية.")

    return list(set(reasons))

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التحليل الجنائي الرقمي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط المشبوه للتحليل...")

if st.button("تفعيل بروتوكول الكشف"):
    if target_url:
        marjan_alerts = aggressive_marjan_logic(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تنفيذ بروتوكولات الفحص المتقدمة..."):
            st.markdown("---")
            
            if marjan_alerts:
                st.subheader("🕵️ نتائج تحليل محرك مرجان الاستباقي:")
                for alert in marjan_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
            else:
                st.info("ℹ️ محرك مرجان: لم يتم رصد مؤشرات خطر برمجية في بنية الرابط.")

            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=10)
                if response.status_code == 200:
                    malicious = response.json()['data']['attributes'].get('last_analysis_stats', {}).get('malicious', 0)
                    if malicious > 0:
                        st.error(f"🚨 تأكيد خطر عالمي: الرابط خبيث بناءً على تقارير {malicious} مختبر دولي.")
                    else:
                        st.success("✅ الرابط سليم ظاهرياً في قواعد البيانات العالمية.")
                    
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.warning("⚠️ قواعد البيانات العالمية مشغولة؛ تم الاعتماد على تحليل مرجان الذكي.")
                    st.info(f"🔗 [يمكنك المراجعة اليدوية من هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
            except:
                st.warning("⚠️ فشل الاتصال الخارجي؛ تم الاكتفاء بنتائج الفحص الداخلي.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v5.8</div>', unsafe_allow_html=True)
