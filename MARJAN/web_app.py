import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري (v6.3 الأصلي - ثبات كامل) ---
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
    .latest-threats { padding: 15px; border-radius: 10px; background: rgba(255, 75, 75, 0.05); border: 1px solid rgba(255, 75, 75, 0.3); margin-top: 30px; margin-bottom: 50px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.98); border-top: 1px solid #D4AF37; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

# --- وظيفة فحص PhishTank (إضافة جديدة) ---
def check_phishtank(url):
    try:
        # استخدام واجهة PhishTank للتحقق اللحظي
        pt_url = "https://checkurl.phishtank.com/checkurl/"
        data = {'url': url, 'format': 'json'}
        response = requests.post(pt_url, data=data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result.get('results', {}).get('in_database', False):
                return True
    except:
        pass
    return False

# --- محرك التحليل الجنائي المتقدم (M.T Deep Forensic Core v6.6) ---
def aggressive_marjan_logic(url):
    reasons = []
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()
    
    # تحسين رصد الاستضافات المخادعة
    cloud_hosting = ['pages.dev', 'workers.dev', 'github.io', 'vercel.app']
    if any(h in domain for h in cloud_hosting) and any(k in domain for k in ['mega', 'login', 'secure']):
        reasons.append("🚨 تمويه سحابي: محاولة استخدام منصات موثوقة لإخفاء نشاط تصيد.")

    if url.startswith("http://"):
        reasons.append("🔓 ثغرة بروتوكول: الاتصال غير مشفر ومعرض للاعتراض.")

    # فحص الكلمات المفتاحية للهندسة الاجتماعية
    if any(word in full_url for word in ['win', 'prize', 'claim', 'verify', 'update', 'bank']):
        reasons.append("🚨 هندسة اجتماعية: تم رصد أنماط استدراج وتلاعب نفسي.")

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
        
        with st.spinner("> جاري تنفيذ بروتوكولات التدقيق الجنائي..."):
            st.markdown("---")
            
            # 1. الاستعلام من PhishTank (لحظي)
            if check_phishtank(target_url):
                marjan_alerts.append("🐟 تنبيه PhishTank: تم العثور على الرابط في قاعدة بيانات التصيد اللحظية.")
            
            # 2. الاستعلام من VirusTotal
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=10)
                if response.status_code == 200:
                    malicious = response.json()['data']['attributes'].get('last_analysis_stats', {}).get('malicious', 0)
                    if malicious > 0:
                        marjan_alerts.append(f"📡 استخبارات عالمية: تم تصنيف الرابط كخطر بواسطة {malicious} مختبر دولي.")
            except: pass

            if marjan_alerts:
                st.subheader("🕵️ نتائج التحليل العميق:")
                for alert in marjan_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                # قسم التوعية والتوصية
                st.markdown(f"""
                <div class="threat-intel">
                    <h4 style="color:#D4AF37; margin-bottom:10px;">⚠️ ماذا سيحدث لو ضغطت على هذا الرابط؟</h4>
                    <ul style="list-style-type: none; padding-right: 0;">
                        <li>🛑 <b>سرقة الهوية:</b> محاولة الحصول على كلمات مرورك وبياناتك البنكية.</li>
                        <li>🕵️ <b>التجسس الرقمي:</b> زرع برمجيات خبيثة لتتبع نشاطك.</li>
                        <li>💸 <b>الاحتيال المالي:</b> استدراجك لعمليات دفع وهمية.</li>
                    </ul>
                    <p style="font-size: 0.95em; color: #ff4b4b; font-weight: bold; border-top: 1px solid rgba(212,175,55,0.2); padding-top: 10px;">
                        💡 التوصية: يرجى إغلاق الصفحة فوراً وتجنب التفاعل مع المحتوى.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ محرك مرجان: لم يتم رصد تهديدات هيكلية واضحة.")

            st.info(f"🔗 [لمراجعة السلوك التقني التفصيلي اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")

# --- قاعدة بيانات التهديدات الحديثة (ثابتة في الأسفل) ---
st.markdown("""
    <div class="latest-threats">
        <h4 style="color:#ff4b4b; margin-bottom:10px; border-bottom:1px solid rgba(255,75,75,0.2);">🔴 قاعدة بيانات التهديدات الحديثة (Live)</h4>
        <table style="width:100%; color:#eee; font-size:0.85em; text-align:right;">
            <tr style="color:#D4AF37;">
                <th>الرابط المشبوه</th>
                <th>نوع التهديد</th>
            </tr>
            <tr><td>megauploads.pages.dev</td><td>تمويه استضافة (Phishing)</td></tr>
            <tr><td>update-system-win11.top</td><td>برمجيات فدية (Ransomware)</td></tr>
            <tr><td>gift-card-free.xyz</td><td>سرقة بيانات بنكية (Fraud)</td></tr>
        </table>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v6.6 | Advanced Forensic Detection</div>', unsafe_allow_html=True)
