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

# --- محرك التحليل الجنائي المتقدم (M.T Deep Forensic Core v5.9) ---
def aggressive_marjan_logic(url):
    reasons = []
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()
    path = urlparse(url).path.lower()
    
    # 1. الذكاء اللغوي والمالي (Social Engineering Intelligence)
    # تشمل كلمات الاستدراج، الديون، المراهنات، والجوائز بمختلف اللغات
    social_threats = ['merit', 'king', 'bet', 'win', 'prize', 'bonus', 'claim', 'verify', 'update', 'vave', 'login', 'crypto', 'divida', 'debt', 'zero', 'loan', 'gift']
    if any(word in full_url for word in social_threats):
        reasons.append("🚨 هندسة اجتماعية: تم رصد أنماط لغوية تستهدف استدراج المستخدم عبر وعود مالية أو أمنية زائفة.")

    # 2. تحليل "خدعة التفاعل الموجه" (Directional Trigger Analysis)
    # تحليل الروابط التي تطلب فعلاً محدداً (تصويت، مشاركة، فحص)
    if any(trigger in path for trigger in ['vote', 'event', 'active', 'check', 'pague']):
         reasons.append("🚨 نمط تفاعل مشبوه: الرابط يطلب إجراءً فورياً (Action) من المستخدم، وهو أسلوب شائع في روابط التصيد المتطورة.")

    # 3. كشف "انتحال الكيانات" (Typosquatting & Brand Impersonation)
    entities = ['bybit', 'binance', 'metamask', 'trust', 'paypal', 'netflix', 'apple', 'instagram', 'facebook', 'whatsapp', 'telegram', 'google', 'microsoft']
    for e in entities:
        if e in domain and domain != f"{e}.com":
            reasons.append(f"⚠️ انتحال كيان رقمي: محاولة تمويه النطاق ليوحي بتبعيته لشركة '{e.capitalize()}' بشكل غير قانوني.")

    # 4. التحليل الهيكلي العميق (Structural Integrity Check)
    # كشف الروابط التي تستخدم بروتوكولات قديمة أو نطاقات فرعية مبالغ فيها
    if url.startswith("http://"):
        reasons.append("🔓 ثغرة بروتوكول: الرابط يفتقر لتشفير SSL، مما يجعله قناة مفتوحة لتسريب البيانات الحساسة.")
    
    # كشف النطاقات عالية الخطورة (TLD Analysis)
    dangerous_tlds = ['.mobi', '.br', '.xyz', '.top', '.zip', '.info']
    if any(domain.endswith(tld) for tld in dangerous_tlds):
        reasons.append(f"❗ تصنيف النطاق: الرابط يستخدم نطاق (TLD) يشتهر باستضافة حملات الاحتيال والمحتوى الضار.")

    if len(domain) > 20 or domain.count('.') > 2:
        reasons.append("❗ تمويه هيكلي: استخدام بنية تقنية معقدة جداً للنطاق تهدف لتضليل أدوات الفحص التلقائية.")

    return list(set(reasons))

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التحليل الجنائي الرقمي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط المشبوه للتحليل الجنائي...")

if st.button("تفعيل بروتوكول الكشف الذكي"):
    if target_url:
        # الطبقة الأولى: التحليل الذاتي العميق لمرجان
        marjan_alerts = aggressive_marjan_logic(target_url)
        
        # الطبقة الثانية: التحليل العالمي المتصل
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تشغيل محركات التحليل الذاتي والعالمي..."):
            st.markdown("---")
            
            # عرض نتائج مرجان الاستباقية
            if marjan_alerts:
                st.subheader("🕵️ نتائج محرك مرجان للتحليل الذاتي العميق:")
                for alert in marjan_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
            else:
                st.info("ℹ️ محرك مرجان الذاتي: لم يتم رصد تهديدات هيكلية أو لغوية مباشرة في بنية الرابط.")

            # عرض النتائج العالمية
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=12)
                if response.status_code == 200:
                    data = response.json()
                    stats = data['data']['attributes'].get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0)
                    
                    if malicious > 0 or suspicious > 0:
                        st.error(f"🚨 الاستخبارات العالمية: تم تصنيف الرابط كخطر (Malicious: {malicious} | Suspicious: {suspicious}).")
                    else:
                        st.success("✅ الاستخبارات العالمية: الرابط لم يتم تسجيله كخطر في قواعد البيانات الحالية.")
                    
                    # رابط المراجعة العميقة الدائم
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق ونتائج المختبرات اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.warning("⚠️ قواعد البيانات العالمية: الخدمة مشغولة، تم الاعتماد كلياً على قوة التحليل الذاتي لمرجان.")
                    st.info(f"🔗 [يمكنك محاولة فتح تقرير السلوك يدوياً من هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
            except:
                st.warning("⚠️ خطأ في الاتصال العالمي: النظام يعمل الآن بذكاء مرجان المنفصل (Standalone Mode).")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v5.9 | Deep Forensic AI</div>', unsafe_allow_html=True)
