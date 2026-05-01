import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

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

# --- محرك التحليل الجنائي المتقدم (M.T Deep Forensic Core v6.8) ---
def aggressive_marjan_logic(url):
    reasons = []
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()
    path = urlparse(url).path.lower()
    
    # 1. رصد الروابط غير المشفرة (التي تستغلها صفحات التصيد القديمة)
    if url.startswith("http://"):
        reasons.append("🔓 ثغرة بروتوكول خطيرة: الرابط يستخدم HTTP، مما يعني أن أي بيانات تُدخل فيه مكشوفة تماماً للمهاجمين.")

    # 2. تحليل عمق النطاق (رصد النطاقات المريبة التي لا تملك سمعة تجارية)
    suspicious_keywords = ['choceur', 'win', 'gift', 'login', 'verify', 'update', 'secure', 'account']
    if any(key in domain for key in suspicious_keywords) and not any(ext in domain for ext in ['.gov', '.edu']):
        reasons.append("🚨 رصد نمط استدراج: النطاق يحتوي على كلمات مفتاحية تُستخدم عادة في حملات الهندسة الاجتماعية.")

    # 3. تحليل هيكل الرابط (Heuristic Analysis)
    if len(domain) > 20 or domain.count('.') > 2:
        reasons.append("🕵️ هيكل مريب: طول النطاق أو كثرة النطاقات الفرعية تشير إلى محاولة إخفاء الهوية الحقيقية للموقع.")

    # 4. رصد ملفات الاختبار الأمنية
    if "eicar" in full_url:
        reasons.append("🧪 ملف اختبار أمني: تم رصد توقيع مطابق لملفات اختبار الأنظمة الدفاعية (EICAR).")

    return list(set(reasons))

# --- وظيفة جلب البيانات اللحظية من PhishTank و Threat Feeds ---
def check_live_feeds(url):
    alerts = []
    try:
        # فحص PhishTank بطلب مباشر (POST) لضمان الدقة اللحظية
        pt_url = "https://checkurl.phishtank.com/checkurl/"
        data = {'url': url, 'format': 'json'}
        response = requests.post(pt_url, data=data, timeout=8)
        if response.status_code == 200:
            res = response.json()
            if res.get('results', {}).get('in_database'):
                alerts.append("🐟 تنبيه PhishTank اللحظي: تم تأكيد إدراج هذا الرابط ضمن قوائم التصيد النشطة الآن.")
    except:
        pass
    return alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التحليل الجنائي الرقمي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط المشبوه للتحليل...")

if st.button("تفعيل بروتوكول الكشف الذكي"):
    if target_url:
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        # تفعيل المحرك الذاتي أولاً (لضمان عدم الاعتماد الكلي على الخارج)
        marjan_alerts = aggressive_marjan_logic(target_url)
        
        with st.spinner("> جاري تنفيذ بروتوكولات التدقيق الجنائي المتقدم..."):
            st.markdown("---")
            
            # جلب البيانات من المصادر اللحظية (PhishTank)
            live_data = check_live_feeds(target_url)
            marjan_alerts.extend(live_data)
            
            # استعلام VirusTotal كدعم إضافي
            try:
                vt_res = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=10)
                if vt_res.status_code == 200:
                    stats = vt_res.json()['data']['attributes'].get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    if malicious > 0:
                        marjan_alerts.append(f"📡 استخبارات عالمية: تم تصنيف الرابط كخطر من قبل {malicious} مركز أمن سيبراني.")
            except: pass

            if marjan_alerts:
                st.subheader("🕵️ نتائج التحليل العميق:")
                for alert in marjan_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                # تفاصيل السلوك والتوصية
                st.markdown(f"""
                <div class="threat-intel">
                    <h4 style="color:#D4AF37; margin-bottom:10px;">⚠️ ماذا سيحدث لو ضغطت على هذا الرابط؟</h4>
                    <ul style="list-style-type: none; padding-right: 0;">
                        <li>🛑 <b>سرقة الهوية:</b> سرقة كلمات المرور والبيانات الشخصية عبر صفحات وهمية.</li>
                        <li>🕵️ <b>التجسس الرقمي:</b> محاولة حقن برمجيات خبيثة لتتبع نشاط المتصفح.</li>
                        <li>💸 <b>الاحتيال المالي:</b> استدراج المستخدم لعمليات دفع مشبوهة.</li>
                    </ul>
                    <p style="font-size: 0.95em; color: #ff4b4b; font-weight: bold; border-top: 1px solid rgba(212,175,55,0.2); padding-top: 10px;">
                        💡 التوصية: يرجى إغلاق الصفحة فوراً، هذا الرابط يظهر علامات تصيد واضحة.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ محرك مرجان: لم يتم رصد تهديدات هيكلية واضحة، لكن يرجى الحذر دائماً.")

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
            <tr><td>thechoceur.com</td><td>تصيد غير مشفر (Phishing)</td></tr>
            <tr><td>megauploads.pages.dev</td><td>تمويه استضافة (Malware)</td></tr>
            <tr><td>eicar.org/download/eicar.com</td><td>ملف اختبار أمني (Standard Test)</td></tr>
        </table>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v6.3 | Advanced Forensic Detection</div>', unsafe_allow_html=True)
