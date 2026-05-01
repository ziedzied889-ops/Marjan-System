import streamlit as st
import requests
import base64
import re
from urllib.parse import urlparse
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- قاعدة بيانات الجلسة اللحظية ---
if 'threat_vault' not in st.session_state:
    st.session_state.threat_vault = []

# --- التنسيق البصري (ثبات الواجهة v6.3) ---
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

# --- محرك التحليل الشامل (Marjan Ultimate Intelligence) ---
def analyze_everything(url):
    reasons = []
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    
    # 1. تحليل النطاقات (TLD & Entropy)
    bad_tlds = ['.sbs', '.xyz', '.top', '.zip', '.online', '.site', '.monster']
    if any(domain.endswith(tld) for tld in bad_tlds):
        reasons.append(f"❗ نطاق مشبوه (TLD): الامتداد .{domain.split('.')[-1]} يسجل أعلى معدلات استضافة التصيد.")

    # 2. كشف انتحال الصفة (Brand Hijacking)
    brands = ['allegro', 'netflix', 'bank', 'wix', 'google', 'microsoft', 'secure', 'login', 'update']
    if any(b in domain for b in brands):
        reasons.append("🚨 انتحال هوية: تم رصد اسم مؤسسة أو كلمة "أمان" داخل نطاق غير رسمي.")

    # 3. تحليل هيكل المسار (Path & Media Analysis)
    if any(p in path for p in ['/media/', '/na/', '/verify/', '/cdn/', '/assets/']):
        reasons.append("🕵️ تحليل المسار: الرابط يوجه لملفات وسائط داخل مجلدات تستخدم عادةً لتخزين صفحات التصيد.")

    # 4. كشف الروابط غير المشفرة
    if url.startswith("http://"):
        reasons.append("🔓 اتصال مكشوف: الرابط لا يستخدم بروتوكول HTTPS، البيانات معرضة للاختراق.")

    return list(set(reasons))

# --- وظيفة جلب البيانات من المحركات العالمية ---
def global_intelligence_fetch(url):
    external_alerts = []
    # PhishTank Live Data
    try:
        res = requests.post("https://checkurl.phishtank.com/checkurl/", data={'url': url, 'format': 'json'}, timeout=12)
        if res.status_code == 200 and res.json().get('results', {}).get('in_database'):
            external_alerts.append("🐟 PhishTank Alert: الرابط مصنف عالمياً كتهديد نشط.")
    except: pass
    return external_alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التحليل الجنائي الرقمي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل أي رابط للتحليل الشامل...")

if st.button("تفعيل بروتوكول الكشف الذكي"):
    if target_url:
        # تصحيح البروتوكول
        if target_url.startswith("ttp"): target_url = "h" + target_url
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تنفيذ المسح الشامل وجمع الاستخبارات العالمية..."):
            st.markdown("---")
            
            # التحليل الداخلي + الاستخبارات العالمية
            all_alerts = analyze_everything(target_url)
            all_alerts.extend(global_intelligence_fetch(target_url))
            
            # VirusTotal Search
            try:
                vt_res = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=12)
                if vt_res.status_code == 200:
                    malicious = vt_res.json()['data']['attributes'].get('last_analysis_stats', {}).get('malicious', 0)
                    if malicious > 0:
                        all_alerts.append(f"📡 VirusTotal: تم رصد خطورة بواسطة {malicious} مركز أمني دولي.")
            except: pass

            if all_alerts:
                st.subheader("🕵️ نتائج التحليل الشامل:")
                for alert in all_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                # التوصية الأمنية
                st.markdown(f"""
                <div class="threat-intel">
                    <h4 style="color:#D4AF37; margin-bottom:10px;">⚠️ التوصية الأمنية (Eng. Zaid Advisory):</h4>
                    <p style="color:#eee; font-size:0.9em;">تم تصنيف هذا الرابط كخطر بناءً على تحليل السلوك وقواعد البيانات العالمية اللحظية.</p>
                    <p style="font-size: 0.95em; color: #ff4b4b; font-weight: bold; border-top: 1px solid rgba(212,175,55,0.2); padding-top: 10px;">
                        💡 القرار: حظر الرابط فوراً وعدم استخدامه في بيئة العمل.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # إضافة للسجل
                st.session_state.threat_vault.insert(0, {
                    "url": target_url[:30] + "...", 
                    "type": "تهديد مكتشف", 
                    "time": datetime.now().strftime("%H:%M")
                })
            else:
                st.success("✅ محرك مرجان: لم يتم رصد تهديدات واضحة حالياً. يرجى المراقبة المستمرة.")

            st.info(f"🔗 [السجل الفني الكامل للرابط (Live)](https://www.virustotal.com/gui/url/{url_id}/behavior)")

# --- سجل التهديدات اللحظية ---
st.markdown(f"""
    <div class="latest-threats">
        <h4 style="color:#ff4b4b; margin-bottom:10px; border-bottom:1px solid rgba(255,75,75,0.2);">🔴 سجل التهديدات اللحظية (Live Storage)</h4>
        <table style="width:100%; color:#eee; font-size:0.85em; text-align:right;">
            <tr style="color:#D4AF37;">
                <th>الرابط</th>
                <th>نوع التهديد</th>
                <th>الوقت</th>
            </tr>
            {"".join([f"<tr><td>{t['url']}</td><td>{t['type']}</td><td>{t['time']}</td></tr>" for t in st.session_state.threat_vault[:5]])}
        </table>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v6.3 | Advanced Forensic Detection</div>', unsafe_allow_html=True)
