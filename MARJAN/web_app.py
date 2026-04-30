import streamlit as st
import requests
import base64

st.set_page_config(page_title="Marjan Trace Pro", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #05070a; }
    h1 { color: #D4AF37 !important; text-align: center; font-family: 'Arial'; }
    .result-box { padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; background-color: #000; text-align: right; }
    .warning-box { padding: 20px; border-radius: 15px; border: 1px solid #ff8c00; background-color: #1a1100; color: #ff8c00; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🛡️ Marjan Trace Pro</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التدقيق السيبراني المعمق</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="...أدخل الرابط للفحص المعمق")

if st.button("بدء التحليل الجنائي"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال الرابط")
    else:
        target_url = target_url.strip()
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        
        try:
            url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
            
            with st.spinner("🔍 جاري تشريح الرابط وفحص السلوك الخفي..."):
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                if response.status_code == 200:
                    data = response.json()['data']['attributes']
                    stats = data.get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0) # إضافة فحص الروابط المشبوهة
                    
                    st.markdown("---")
                    
                    # منطق التدقيق الجديد:
                    if malicious > 0:
                        st.error(f"🚨 تحذير أمني خطير: الرابط خبيث!")
                        st.markdown(f'<div class="result-box" style="color:#ff4b4b; border-color:#ff4b4b;">تم تأكيد التهديد من قبل {malicious} مختبر أمني عالمي.</div>', unsafe_allow_html=True)
                    
                    elif suspicious > 0:
                        st.warning("⚠️ تنبيه: الرابط يظهر سلوكاً مشبوهاً!")
                        st.markdown(f'<div class="warning-box">هذا الرابط قد يكون للتصيد الاحتيالي أو يحتوي على برمجيات غير مرغوب فيها.</div>', unsafe_allow_html=True)
                    
                    else:
                        # تدقيق إضافي في تاريخ الفحص
                        st.success("✅ الرابط سليم حسب السجلات الحالية")
                        st.markdown('<div class="result-box" style="color:#00ff41;">الحالة: نظيفة. ينصح دائماً بالحذر عند فتح روابط من مصادر مجهولة.</div>', unsafe_allow_html=True)
                    
                    # عرض تفاصيل فنية لتعزيز الثقة
                    col1, col2 = st.columns(2)
                    col1.metric("المحركات الآمنة", stats.get('harmless', 0))
                    col2.metric("محركات التحذير", malicious + suspicious)

                    st.info(f"🔗 [للاطلاع على تحليل السلوك العميق (Sandboxing) اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")

                elif response.status_code == 404:
                    st.info("🔎 هذا الرابط مجهول تماماً للمحركات. جاري إرساله لتحليله لأول مرة...")
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    st.success("✅ تم الإرسال. انتظر دقيقتين ثم أعد الفحص للحصول على التقرير.")
                
                elif response.status_code == 429:
                    st.error("⚠️ الخادم مشغول (4 طلبات/دقيقة كحد أقصى). انتظر قليلاً.")
                else:
                    st.error("⚠️ خطأ في الاتصال بالقاعدة الأمنية.")

        except Exception as e:
            st.error(f"خطأ تقني: {str(e)}")

st.markdown('<div style="text-align:center; color:#D4AF37; margin-top:50px;">Zaid Al-Janabi | Cybersecurity Expert in Training</div>', unsafe_allow_html=True)
