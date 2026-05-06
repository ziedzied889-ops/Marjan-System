import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- 1. إعدادات النظام الأساسية ---
st.set_page_config(page_title="Marjan Trace v9.0", layout="wide")

# --- 2. محرك التحليل الجنائي (المنطق البرمجي) ---
def analyze_target(url):
    findings, actions = [], []
    status, color, entropy = "CLEAN / آمن", "#2ea043", 0
    
    if not url: return findings, actions, status, color, entropy

    domain = urlparse(url).netloc.lower()
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = round(- sum([p * math.log(p) / math.log(2.0) for p in probs]), 2)

    is_danger = False
    # كشف الروابط المشبوهة (مثل التي أرسلتها في الصور)
    if any(x in url.lower() for x in ['sparkasse', 'bank', 'fortnite', 'free', 'login', 'secure']):
        findings.append("🔍 رصد انتحال لعلامة تجارية أو صفحة رسمية (Phishing).")
        actions.append("🔓 سحب البيانات: محاولة الاستيلاء على معلومات الدخول.")
        is_danger = True

    if any(domain.endswith(ext) for ext in ['.top', '.qpon', '.xyz', '.online', '.link']):
        findings.append(f"🚩 امتداد النطاق ({domain.split('.')[-1]}) عالي الخطورة ومستخدم في الهجمات.")
        actions.append("🦠 تحميل خفي: احتمالية تنزيل ملفات تجسس تلقائية.")
        is_danger = True

    if entropy > 3.5:
        findings.append(f"🕵️ عشوائية مرتفعة ({entropy}): النطاق مشفر أو مولد آلياً.")
        actions.append("📡 اتصال C2: محاولة بناء قناة اتصال مع سيرفر تحكم خارجي.")
        is_danger = True

    if is_danger:
        status, color = "CRITICAL / خطر", "#ff4b4b"

    return findings, actions, status, color, entropy

# --- 3. تصميم الواجهة (CSS الثابت لمنع الأخطاء) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@700;900&display=swap');
    .stApp { background-color: #05070a !important; color: white; }
    .rtl { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .title-text { font-family: 'Orbitron', sans-serif; color: #D4AF37; text-align: center; font-size: 3.2rem; margin-bottom: 0px; }
    
    /* إطار المعاينة Sandbox */
    .sandbox-box { 
        border: 2px solid #D4AF37; border-radius: 20px; background: #000;
        min-height: 420px; padding: 20px; position: relative; overflow: hidden;
    }
    
    /* الأيقونات الجانبية المرتبة */
    .side-panel {
        position: absolute; left: 0; top: 0; bottom: 0; width: 50px;
        background: rgba(212, 175, 85, 0.05); display: flex; flex-direction: column;
        align-items: center; justify-content: center; gap: 30px; border-right: 1px solid rgba(212, 175, 85, 0.2);
    }
    
    .report-card {
        background: rgba(10, 25, 47, 0.8); padding: 20px; border-radius: 15px;
        border-right: 6px solid #D4AF37; margin-top: 20px;
    }

    .action-badge {
        background: rgba(255, 75, 75, 0.15); border-right: 4px solid #ff4b4b;
        padding: 12px; margin-bottom: 10px; border-radius: 8px; color: #eee;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. الهيكل البصري ---
st.markdown('<h1 class="title-text">MARJAN TRACE</h1>', unsafe_allow_html=True)
st.markdown('<p class="rtl" style="text-align:center; opacity:0.8;">المنصة الاستخباراتية المتطورة للتحليل الجنائي للروابط</p>', unsafe_allow_html=True)

url_input = st.text_input("أدخل الرابط المستهدف للفحص:", placeholder="https://example.com")

if st.button("تفعيل بروتوكول التشريح"):
    if url_input:
        findings, actions, status, color, entropy = analyze_target(url_input)
        
        # كروت الإحصائيات
        col1, col2, col3 = st.columns(3)
        col1.metric("الحالة الجنائية", status)
        col2.metric("الأدلة المرصودة", len(findings))
        col3.metric("معامل العشوائية", entropy)

        c_left, c_right = st.columns([1.3, 1])

        with c_left:
            st.markdown('<div class="report-card rtl">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>📋 نتائج الفحص الجنائي:</h4>", unsafe_allow_html=True)
            if findings:
                for f in findings: st.markdown(f"<p>• {f}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد مؤشرات جرمية نشطة.</p>", unsafe_allow_html=True)
            
            # توصية المهندس زيد
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:12px; border-left:5px solid #D4AF37; margin-top:20px;">
                    <h6 style="color:#D4AF37; margin-top:0;">🛡️ (Zaid's Advisory):</h6>
                    <p style="font-size:0.9rem;">بناءً على المعطيات، الرابط <b>{"يمثل تهديداً حقيقياً" if len(findings)>0 else "يبدو مستقراً"}</b>. {"يُنصح بحظر النطاق فوراً." if len(findings)>0 else "يمكن المتابعة مع الرقابة."}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_right:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📽️ Sandbox</h3>", unsafe_allow_html=True)
            st.markdown('<div class="sandbox-box rtl">', unsafe_allow_html=True)
            
            # لوحة الأيقونات الجانبية (مرتبة ومنسقة)
            st.markdown("""
                <div class="side-panel">
                    <span title="عزل">🛡️</span>
                    <span title="اتصال">🌐</span>
                    <span title="تشفير">🔐</span>
                </div>
            """, unsafe_allow_html=True)

            # المحتوى الداخلي
            st.markdown('<div style="margin-right:45px;">', unsafe_allow_html=True)
            if actions:
                st.markdown("<h5 style='color:#ff4b4b;'>🚨 الأضرار المتوقعة:</h5>", unsafe_allow_html=True)
                for act in actions:
                    st.markdown(f'<div class="action-badge">{act}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center; padding-top:120px; opacity:0.4;"><h5>البيئة معزولة وآمنة</h5><p>لا يوجد نشاط عدائي</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#D4AF37; font-family:Orbitron; opacity:0.5;'>Eng. Zaid Al-Janabi | 2026</p>", unsafe_allow_html=True)
