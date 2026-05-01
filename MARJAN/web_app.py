import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري (الهوية البصرية المعتمدة) ---
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

# --- محرك التحليل الجنائي المتقدم (M.T Aggressive Core v5.6) ---
def aggressive_marjan_logic(url):
    reasons = []
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()
    
    # 1. كشف التهديدات المباشرة
    danger_keywords = [
        'merit', 'king', 'giris', 'yap', 'bet', 'win', 'prize', 
        'bonus', 'claim', 'verify', 'update', 'vave', 'login'
    ]
    if any(word in full_url for word in danger_keywords):
        reasons.append("🚨 هندسة اجتماعية: تم رصد مصطلحات مخصصة للاستدراج في عمليات المراهنة أو التصيد المباشر.")

    # 2. كشف "خدعة التصويت والفعاليات" (التحديث الأخير)
    if 'vote' in full_url or ('event' in full_url and 'vote' in full_url):
         reasons.append("🚨 هندسة اجتماعية: تم رصد نمط 'التصويت الاحتيالي'. المهاجم يستخدم 'vote' أو 'event' لسرقة الحسابات تحت غطاء المسابقات.")

    # 3. كشف انتحال الهوية
    brands = ['bybit', 'binance', 'metamask', 'trust', 'paypal', 'netflix', 'apple', 'instagram', 'facebook']
    for b in brands:
        if b in domain and domain != f"{b}.com":
            reasons.append(f"⚠️ انتحال هوية: النطاق يستخدم اسم '{b}' بشكل غير رسمي لتضليل المستخدمين.")

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
        
        with st.spinner("> جاري تنفيذ بروتوكولات الفحص..."):
            st.markdown("---")
            
            # عرض نتائج محرك مرجان دائماً
            if marjan_alerts:
                st.subheader("🕵️ نتائج تحليل محرك مرجان الاستباقي:")
                for alert in marjan_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
            else:
                st.info("ℹ️ محرك مرجان: لم يتم رصد علامات خطر واضحة في بنية الرابط.")

            # محاولة جلب النتائج العالمية مع رابط المراجعة
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=8)
                if response.status_code == 200:
                    stats = response.json()['data']['attributes'].get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    
                    if malicious > 0:
                        st.error(f"🚨 تأكيد خطر عالمي: تم تصنيف الرابط كخبيث من قبل {malicious} مختبر.")
                    else:
                        st.success("✅ الرابط سليم بناءً على قواعد البيانات العالمية الحالية.")
                    
                    # --- إرجاع رابط المراجعة هنا ---
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.warning("⚠️ تنبيه: المختبرات العالمية مشغولة، اعتمد حالياً على 'كشف مرجان' أعلاه.")
                    # إظهار الرابط حتى في حالة الانشغال لضمان وصولك للمعلومات
                    st.info(f"🔗 [يمكنك محاولة مراجعة السلوك يدوياً من هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
            except Exception:
                st.warning("⚠️ تعذر الاتصال بالمختبرات الخارجية. تم الاكتفاء بالتحليل الذكي لمرجان.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v5.6</div>', unsafe_allow_html=True)
