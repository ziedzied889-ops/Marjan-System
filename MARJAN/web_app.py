import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري ---
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
    .threat-intel { padding: 15px; border-radius: 10px; background-color: rgba(212, 175, 55, 0.1); border: 1px solid #D4AF37; color: #eee; text-align: right; margin-top: 15px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.98); border-top: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك التحليل الجنائي المتقدم (M.T Deep Forensic Core v6.1) ---
def aggressive_marjan_logic(url):
    reasons = []
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()
    path = urlparse(url).path.lower()
    
    social_threats = ['merit', 'king', 'bet', 'win', 'prize', 'bonus', 'claim', 'verify', 'update', 'vave', 'login', 'crypto', 'divida', 'debt', 'zero', 'loan', 'gift']
    if any(word in full_url for word in social_threats):
        reasons.append("🚨 هندسة اجتماعية: رصد أنماط استدراج مالي/أمني في بنية الرابط.")

    if any(trigger in path for trigger in ['vote', 'event', 'active', 'check', 'pague']):
         reasons.append("🚨 نمط تفاعل مشبوه: الرابط يطلب إجراءً فورياً لتنفيذ هجوم تصيد.")

    entities = ['bybit', 'binance', 'metamask', 'trust', 'paypal', 'netflix', 'apple', 'instagram', 'facebook', 'whatsapp', 'telegram']
    for e in entities:
        if e in domain and domain != f"{e}.com":
            reasons.append(f"⚠️ انتحال كيان: محاولة تمويه النطاق ليبدو كأنه تابع لشركة {e.capitalize()}.")

    if url.startswith("http://"):
        reasons.append("🔓 ثغرة بروتوكول: الرابط يفتقر لتشفير SSL (غير آمن).")
    
    dangerous_tlds = ['.mobi', '.br', '.xyz', '.top', '.zip', '.info']
    if any(domain.endswith(tld) for tld in dangerous_tlds):
        reasons.append(f"❗ تصنيف النطاق: استخدام TLD يشتهر باستضافة حملات الاحتيال.")

    return list(set(reasons))

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التحليل الجنائي الرقمي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط المشبوه للتحليل...")

if st.button("تفعيل بروتوكول الكشف الذكي"):
    if target_url:
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        marjan_alerts = aggressive_marjan_logic(target_url)
        global_danger_count = 0
        
        with st.spinner("> جاري تنفيذ الفحص الشامل..."):
            st.markdown("---")
            
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=12)
                if response.status_code == 200:
                    stats = response.json()['data']['attributes'].get('last_analysis_stats', {})
                    global_danger_count = stats.get('malicious', 0) + stats.get('suspicious', 0)
                
                if global_danger_count > 0:
                    marjan_alerts.append(f"📡 تأكيد استخباراتي: تم رصد الرابط كخطر بواسطة {global_danger_count} مختبر أمن سيبراني عالمي.")
            except:
                pass

            if marjan_alerts:
                st.subheader("🕵️ نتائج التحليل العميق:")
                for alert in marjan_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                # --- القسم الجديد: نبذة عن مخاطر الروابط (يظهر فقط عند وجود خطر) ---
                st.markdown(f"""
                <div class="threat-intel">
                    <h4 style="color:#D4AF37; margin-bottom:10px;">⚠️ ماذا سيحدث لو ضغطت على هذا الرابط؟</h4>
                    <ul style="list-style-type: none; padding-right: 0;">
                        <li>🛑 <b>سرقة الهوية:</b> محاولة الحصول على كلمات مرورك وبياناتك البنكية عبر صفحات مزيفة.</li>
                        <li>🕵️ <b>التجسس الرقمي:</b> زرع برمجيات خبيثة (Malware) لتتبع نشاطك أو الوصول لصورك وملفاتك.</li>
                        <li>💸 <b>الاحتيال المالي:</b> استدراجك لعمليات دفع وهمية أو استغلال رصيدك البنكي.</li>
                        <li>📱 <b>اختراق الحسابات:</b> السيطرة على حسابات التواصل الاجتماعي عبر سحب (Session Cookies).</li>
                    </ul>
                    <p style="font-size: 0.9em; color: #ff9999;">توصية: يرجى إغلاق الصفحة فوراً وعدم إدخال أي بيانات شخصية.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ محرك مرجان: الرابط يبدو آمناً هيكلياً وعالمياً.")

            st.info(f"🔗 [لمراجعة السلوك التقني التفصيلي اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v6.1 | Cyber Awareness</div>', unsafe_allow_html=True)
