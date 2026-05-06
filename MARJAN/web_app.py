import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- إعدادات النظام ---
st.set_page_config(page_title="Marjan Trace v5.5", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي المتقدم ---
def deep_analyze_url(url):
    domain = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()
    entropy = 0
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probs])

    findings = []
    impacts = []
    
    # 1. تحليل السلوك المخصص (بدل الكليشة الثابتة)
    if any(x in url for x in ['login', 'verify', 'sign-in', 'secure', 'account']):
        findings.append("🔍 رصد محاولة 'هندسة اجتماعية': الرابط يحاكي صفحات تسجيل دخول رسمية.")
        impacts.append("⚠️ سرقة بيانات الاعتماد (Credential Theft).")
        
    if any(x in url for x in ['bank', 'crypto', 'wallet', 'update-card', 'billing']):
        findings.append("💰 استهداف مالي: تم رصد كلمات دلالية مرتبطة بأنظمة الدفع والبنوك.")
        impacts.append("⚠️ اختراق الحسابات البنكية أو محافظ الكريبتو.")

    if entropy > 3.4:
        findings.append(f"🤖 تحليل DGA: اسم النطاق عشوائي جداً ({round(entropy,2)})، مما يشير لروابط مولدة برمجياً للهجمات.")
        impacts.append("⚠️ اتصال مع سيرفرات قيادة وسيطرة (C2 Server).")

    if domain.count('.') > 2:
        findings.append("🎭 تمويه الهوية: استخدام نطاقات فرعية متعددة لإخفاء النطاق الأصلي.")
        impacts.append("⚠️ تخطي فلاتر الحماية التقليدية.")

    if any(ext in domain for ext in ['.xyz', '.top', '.online', '.link', '.pw', '.tk']):
        findings.append("🚩 نطاق منخفض الموثوقية: استخدام امتداد رخيص يُفضل من قبل المهاجمين لسهولة التخلص منه.")
        impacts.append("⚠️ احتمالية عالية لوجود برمجيات خبيثة (Malware Distribution).")

    return findings, impacts, round(entropy, 2)

# --- كود الخلفية والتنسيق (حل مشكلة الخلفية السوداء) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    .stApp {
        background: #05070a !important;
    }

    /* الخلفية السيبرانية الذهبية المتفاعلة */
    #marjan-bg {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1; opacity: 0.35;
    }

    .rtl-container { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .sys-title { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 3.5em; font-weight: 900; margin-bottom: 0px;
        text-shadow: 0 0 20px rgba(212, 175, 85, 0.5);
    }
    
    .metric-card { 
        background: rgba(13, 17, 23, 0.9) !important; border: 1px solid rgba(212, 175, 85, 0.3) !important; 
        border-top: 4px solid #D4AF37 !important; padding: 20px; border-radius: 12px; text-align: center;
        backdrop-filter: blur(10px);
    }

    .report-card {
        background: rgba(10, 25, 47, 0.8) !important; border-radius: 15px; padding: 25px;
        border: 1px solid rgba(212, 175, 85, 0.1); border-right: 6px solid #D4AF37;
        backdrop-filter: blur(10px); margin-top: 15px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; width: 100%; border-radius: 10px;
    }
    </style>

    <div id="marjan-bg"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('marjan-bg', {
            "particles": {
                "number": { "value": 120 },
                "color": { "value": "#D4AF37" },
                "line_linked": { "enable": true, "color": "#D4AF37", "opacity": 0.2 },
                "move": { "enable": true, "speed": 1.5 }
            }
        });
    </script>
    """, unsafe_allow_html=True)

# --- الواجهة البرمجية ---
st.markdown("<h1 class='sys-title'>MARJAN TRACE v5.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white; font-family:Cairo;'>نظام التحقيق الجنائي المتقدم - جامعة المعارف</p>", unsafe_allow_html=True)

url_input = st.text_input("أدخل الرابط المراد تحليله:", placeholder="https://example.com...")

if st.button("بدء بروتوكول الفحص العميق"):
    if url_input:
        findings, impacts, entropy_val = deep_analyze_url(url_input)
        
        is_safe = len(findings) == 0
        status_text = "آمن ظاهرياً" if is_safe else "مشبوه / خطر"
        status_color = "#2ea043" if is_safe else "#ff4b4b"

        # عرض المؤشرات
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f'<div class="metric-card"><h6>الحالة الجنائية</h6><h3 style="color:{status_color}">{status_text}</h3></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="metric-card"><h6>الأدلة المكتشفة</h6><h3>{len(findings)}</h3></div>', unsafe_allow_html=True)
        with col3: st.markdown(f'<div class="metric-card"><h6>معامل العشوائية</h6><h3>{entropy_val}</h3></div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([1.5, 1])
        
        with col_left:
            st.markdown('<div class="report-card rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير التحليل الجنائي المخصص</h4>", unsafe_allow_html=True)
            
            if not is_safe:
                st.markdown("**📌 الأدلة المكتشفة في هذا الرابط:**")
                for f in findings:
                    st.markdown(f"<p style='color:white; font-size:0.9em;'>• {f}</p>", unsafe_allow_html=True)
                
                st.markdown("<hr style='opacity:0.1'>", unsafe_allow_html=True)
                st.markdown("**⚠️ الأضرار المتوقعة (Expected Impacts):**")
                for i in impacts:
                    st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {i}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم العثور على أنماط هجومية معروفة في بنية الرابط.</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:10px; border:1px solid #D4AF37; margin-top:20px;">
                    <h5 style="color:#D4AF37;">💡 توصية المهندس زيد (Zaid's Advisory):</h5>
                    <p>{"هذا الرابط يظهر سلوكاً عدائياً، ننصح بحجبه فوراً." if not is_safe else "الرابط لا يحتوي على مؤشرات خطر واضحة، ولكن توخى الحذر دائماً."}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown("<h4 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox</h4>", unsafe_allow_html=True)
            icon = "🛡️" if is_safe else "🚫"
            st.markdown(f"""
                <div style="border:2px solid #D4AF37; border-radius:15px; height:350px; display:flex; flex-direction:column; align-items:center; justify-content:center; background:rgba(0,0,0,0.5);">
                    <span style="font-size:5em;">{icon}</span>
                    <p style="color:#888; margin-top:20px;">المعاينة محجوبة حمايةً لجهازك</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; color:#D4AF37; font-family:Orbitron; font-size:0.8em;'>Developed by: Eng. Zaid Al-Janabi | University of Al-Maarif | 2026</p>", unsafe_allow_html=True)
