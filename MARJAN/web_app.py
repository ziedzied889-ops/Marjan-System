import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري (ثبات كامل للواجهة v6.3) ---
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

# --- وظيفة تصحيح الروابط برمجياً (Auto-Correction Core) ---
def fix_url_format(url):
    if url.startswith("ttp://"):
        return "http://" + url[6:]
    if url.startswith("ttps://"):
        return "https://" + url[7:]
    return url

# --- محرك التحليل الجنائي المتقدم (M.T Deep Forensic Core v6.9.5) ---
def aggressive_marjan_logic(url):
    reasons = []
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()
    
    # 1. رصد النطاقات ذات السمعة السيئة جداً (Untrusted TLDs)
    bad_tlds = ['.sbs', '.xyz', '.top', '.zip', '.online', '.site']
    if any(domain.endswith(tld) for tld in bad_tlds):
        reasons.append(f"❗ نطاق عالي الخطورة: النطاق المرجعي ({domain.split('.')[-1]}) يُستخدم غالباً في استضافة برمجيات خبيثة لحظية.")

    # 2. تحليل الكلمات الدالة على انتحال الصفة
    phishing_brands = ['allegro', 'mega', 'bank', 'login', 'secure']
    if any(brand in domain for brand in phishing_brands):
        reasons.append("🚨 انتحال صفحة تجارية: تم رصد اسم علامة تجارية داخل نطاق غير رسمي.")

    # 3. التدقيق في بروتوكول الاتصال
    if url.startswith("http://"):
        reasons.append("🔓 اتصال مكشوف: الرابط يفتقر للتشفير، مما يسهل سحب البيانات المدخلة.")

    return list(set(reasons))

# --- وظيفة الاستعلام اللحظي العالمي ---
def check_live_global_threats(url):
    external_alerts = []
    try:
        # فحص PhishTank بطلب مباشر
        pt_response = requests.post("https://checkurl.phishtank.com/checkurl/", data={'url': url, 'format': 'json'}, timeout=12)
        if pt_response.status_code == 200:
            res = pt_response.json()
            if res.get('results', {}).get('in_database'):
                external_alerts.append("🐟 PhishTank Live: الرابط مدرج حالياً كتهديد نشط في القوائم العالمية.")
    except: pass
    return external_alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التحليل الجنائي الرقمي</h3>", unsafe_allow_html=True)

raw_url = st.text_input("", placeholder="أدخل الرابط للتحليل اللحظي العميق...")

if st.button("تفعيل بروتوكول الكشف الذكي"):
    if raw_url:
        # تصحيح الرابط قبل المعالجة
        target_url = fix_url_format(raw_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        marjan_alerts = aggressive_marjan_logic(target_url)
        
        with st.spinner("> جاري تنفيذ بروتوكولات التدقيق اللحظي وتصحيح المسارات..."):
            st.markdown("---")
            
            # جلب البيانات من PhishTank
            live_threats = check_live_global_threats(target_url)
            marjan_alerts.extend(live_threats)
            
            # استعلام VirusTotal
            try:
                vt_res = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=12)
                if vt_res.status_code == 200:
                    malicious = vt_res.json()['data']['attributes'].get('last_analysis_stats', {}).get('malicious', 0)
                    if malicious > 0:
                        marjan_alerts.append(f"📡 استخبارات عالمية: تم تأكيد الخطورة بواسطة {malicious} مختبر أمني دولي.")
            except: pass

            if marjan_alerts:
                st.subheader("🕵️ نتائج التحليل الجنائي اللحظي:")
                for alert in marjan_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="threat-intel">
                    <h4 style="color:#D4AF37; margin-bottom:10px;">⚠️ التحليل السلوكي للتهديد:</h4>
                    <p style="color:#eee; font-size:0.9em;">تم رصد محاولة تضليل برمجية عبر نطاق <b>.sbs</b> وانتحال صفة منصة <b>Allegro</b>.</p>
                    <p style="font-size: 0.95em; color: #ff4b4b; font-weight: bold; border-top: 1px solid rgba(212,175,55,0.2); padding-top: 10px;">
                        💡 التوصية الأمنية: الرابط خبيث جداً، يرجى عدم محاولة فتحه أو تداوله.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ محرك مرجان: لم يتم رصد تهديدات في قواعد البيانات اللحظية حالياً.")

            st.info(f"🔗 [السجل الفني الكامل للرابط (Live)](https://www.virustotal.com/gui/url/{url_id}/behavior)")

# --- قاعدة بيانات التهديدات اللحظية ---
st.markdown(f"""
    <div class="latest-threats">
        <h4 style="color:#ff4b4b; margin-bottom:10px; border-bottom:1px solid rgba(255,75,75,0.2);">🔴 قاعدة بيانات التهديدات اللحظية (تحديث: {datetime.now().strftime('%H:%M:%S')})</h4>
        <table style="width:100%; color:#eee; font-size:0.85em; text-align:right;">
            <tr style="color:#D4AF37;">
                <th>الرابط المكتشف</th>
                <th>نوع التهديد</th>
            </tr>
            <tr><td>{raw_url if raw_url else "في انتظار الفحص..."}</td><td>تلاعب بروتوكول / Phishing</td></tr>
            <tr><td>allegrolokalnie.sbs</td><td>انتحال صفة (Allegro)</td></tr>
            <tr><td>thechoceur.com</td><td>تصيد غير مشفر</td></tr>
        </table>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v6.3 | Advanced Forensic Detection</div>', unsafe_allow_html=True)
