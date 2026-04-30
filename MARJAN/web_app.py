import customtkinter as ctk
import requests
import base64

# إعدادات الألوان للهوية الرقمية
GOLD_ELITE = "#D4AF37"
CYBER_DARK = "#05070a"
DETECTION_BLUE = "#00d2ff"

ctk.set_appearance_mode("dark")

class CyberForensicShield(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        
        self.title("Cyber Shield Forensic Edition | Eng. Zaid Al-Janabi")
        self.geometry("950x850")
        self.configure(fg_color=CYBER_DARK)

        self.main_container = ctk.CTkFrame(self, fg_color="#0a0c10", border_width=2, 
                                           border_color=GOLD_ELITE, corner_radius=30)
        self.main_container.pack(pady=(40, 10), padx=40, fill="both", expand=True)

        self.draw_cyber_security_shield()

        self.title_label = ctk.CTkLabel(self.main_container, text="ULTIMATE CYBER SHIELD", 
                                        font=("Orbitron", 35, "bold"), text_color=GOLD_ELITE)
        self.title_label.pack(pady=(10, 20))

        self.url_entry = ctk.CTkEntry(self.main_container, width=580, height=60, 
                                      placeholder_text="أدخل الرابط المستهدف للتحليل الجنائي...",
                                      font=("Arial", 16), justify="right",
                                      fg_color="#010409", border_color=GOLD_ELITE, corner_radius=15)
        self.url_entry.pack(pady=10)

        self.scan_btn = ctk.CTkButton(self.main_container, text="تشغيل الفحص الجنائي الرقمي", 
                                      command=self.run_cyber_forensics,
                                      fg_color=GOLD_ELITE, hover_color="#B8860B", text_color="black",
                                      height=60, font=("Arial", 20, "bold"), corner_radius=15)
        self.scan_btn.pack(pady=20)

        self.result_frame = ctk.CTkFrame(self.main_container, fg_color="#000000", border_width=1, border_color="#1f2937")
        self.result_frame.pack(pady=(0, 20), padx=60, fill="both", expand=True)

        # تعديل الكونسول ليدعم المحاذاة لليمين
        self.console = ctk.CTkTextbox(self.result_frame, font=("Arial", 17), 
                                      fg_color="transparent", text_color="#00FF41", border_width=0)
        self.console.pack(pady=15, padx=25, fill="both", expand=True)
        self.update_console("> درع الحماية: [نشط]\n> بانتظار تحديد الهدف للتحليل...", "#00FF41")

        self.footer = ctk.CTkLabel(self, text="Eng. Zaid Al-Janabi", 
                                   font=("Orbitron", 18, "bold"), text_color=GOLD_ELITE)
        self.footer.pack(pady=(5, 20))

    def draw_cyber_security_shield(self):
        canvas = ctk.CTkCanvas(self.main_container, width=160, height=180, bg="#0a0c10", highlightthickness=0)
        canvas.pack(pady=(30, 0))
        shield_pts = [80, 10, 150, 45, 150, 105, 80, 170, 10, 105, 10, 45]
        canvas.create_polygon(shield_pts, fill="#0d1117", outline=GOLD_ELITE, width=3)
        canvas.create_oval(65, 65, 95, 95, outline=DETECTION_BLUE, width=2)
        canvas.create_line(80, 20, 80, 65, fill=DETECTION_BLUE, width=1)
        canvas.create_line(80, 95, 80, 160, fill=DETECTION_BLUE, width=1)
        canvas.create_text(80, 80, text="🛡️", font=("Arial", 45))

    def run_cyber_forensics(self):
        url = self.url_entry.get().strip()
        if not url:
            self.update_console("!!! تنبيه: يرجى تحديد هدف للفحص الجنائي !!!", GOLD_ELITE)
            return

        self.update_console("> جاري جلب البصمات الأمنية وتحليل السلوك السحابي...", DETECTION_BLUE)
        self.update()

        try:
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            headers = {"x-apikey": self.API_KEY}
            response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
            
            if response.status_code == 200:
                stats = response.json()['data']['attributes']['last_analysis_stats']
                malicious = stats['malicious']
                
                if malicious > 0:
                    report = f"!!! رصد تهديد جنائي عالي الخطورة !!!\n" + "-"*35 + f"\nالحالة: خبيث (Malicious)\nعدد التنبيهات الأمنية: {malicious}"
                    self.update_console(report, "#f85149")
                else:
                    report = "✔ شهادة أمان رقمية صادرة\n" + "-"*35 + "\nالحالة: نظيف (Clean)\nلم يتم العثور على نشاط مشبوه."
                    self.update_console(report, "#3fb950")
            else:
                self.update_console("> الرابط غير مسجل. تم إرساله للمختبر للتحليل...\nيرجى إعادة الفحص بعد لحظات.", GOLD_ELITE)
                requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": url})

        except Exception as e:
            self.update_console(f"فشل فني في النظام: {str(e)}", "#f85149")

    def update_console(self, text, color):
        self.console.delete("0.0", "end")
        self.console.insert("0.0", text)
        self.console.configure(text_color=color)
        # محاكاة المحاذاة لليمين عبر إضافة مسافات برمجية أو استخدام الخطوط المناسبة
        self.main_container.configure(border_color=color)

if __name__ == "__main__":
    app = CyberForensicShield()
    app.mainloop()