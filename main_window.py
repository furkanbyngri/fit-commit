import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd
import os, re, random
from tkvideo import tkvideo  # pip install tkvideo

# --- Makine Öğrenmesi Öneri Sınıfı ---
class MLRecommender:
    def __init__(self, model_path="fitness_recommender_combined.joblib", video_dir="datas/hareketler"):
        obj = joblib.load(model_path)
        self.df = obj['data']
        self.video_dict = {}
        for dirname in os.listdir(video_dir):
            dirpath = os.path.join(video_dir, dirname)
            if os.path.isdir(dirpath):
                key = re.sub(r'[^a-z0-9]', '', dirname.lower())
                vids = [os.path.join(dirpath, f)
                        for f in os.listdir(dirpath)
                        if f.lower().endswith('.mp4')]
                if vids:
                    self.video_dict[key] = list(dict.fromkeys(vids))

    def recommend_person(self, age, height, weight, hours, top_n=5):
        bmi = weight / ((height/100)**2)
        if bmi < 18.5:
            muscles = ['pectorals','quadriceps','glutes']
        elif bmi < 25:
            muscles = ['cardio']
        else:
            muscles = ['abdominals','obliques']
        if hours < 2:
            muscles.append('shoulders')
        filtered = self.df[self.df['target'].isin(muscles)]
        if filtered.empty:
            filtered = self.df
        recs = []
        for _, row in filtered.drop_duplicates('name').head(top_n).iterrows():
            name_key = re.sub(r'[^a-z0-9]', '', row['name'].lower())
            paths = []
            for k, p_list in self.video_dict.items():
                if k in name_key:
                    paths.extend(p_list)
            unique_paths = list(dict.fromkeys(paths))
            random.shuffle(unique_paths)
            recs.append({'row': row, 'videoPaths': unique_paths})
        return recs

# --- Ana Uygulama ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
class FitApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FitApp")
        self.geometry("360x640")
        self.resizable(False, False)
        try:
            self.recommender = MLRecommender()
        except Exception as e:
            messagebox.showerror("Hata", f"Model yüklenirken hata: {e}")
            self.destroy()
            return
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        self.frames = {}
        for Page in (InputPage, ResultPage, DetailPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(InputPage)
    def show_frame(self, cls):
        self.frames[cls].tkraise()

# --- Giriş Sayfası ---
class InputPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.CTkLabel(self, text="🏃 FitApp", font=(None, 20, "bold")).pack(pady=10)
        form = ctk.CTkFrame(self)
        form.pack(pady=20)
        self.entries = {}
        fields = [("İsim","name"),("Yaş","age"),("Boy (cm)","height"),
                  ("Kilo (kg)","weight"),("Haftalık Egzersiz (saat)","hours")]
        for i,(label,key) in enumerate(fields):
            row = ctk.CTkFrame(form)
            row.grid(row=i, column=0, pady=5, padx=10)
            ctk.CTkLabel(row, text=label, width=120, anchor="w").pack(side="left")
            ent = ctk.CTkEntry(row, width=150)
            ent.pack(side="right")
            self.entries[key] = ent
        ctk.CTkButton(self, text="HESAPLA", command=self.on_calculate).pack(pady=10)
    def on_calculate(self):
        try:
            name = self.entries['name'].get().strip()
            age = int(self.entries['age'].get())
            height = float(self.entries['height'].get())
            weight = float(self.entries['weight'].get())
            hours = float(self.entries['hours'].get())
            if not name: raise ValueError
        except:
            messagebox.showerror("Hata", "Lütfen tüm alanları doğru doldurun.")
            return
        recs = self.controller.recommender.recommend_person(age, height, weight, hours)
        self.controller.frames[ResultPage].show_results(name, recs)
        self.controller.show_frame(ResultPage)

# --- Sonuçlar Sayfası ---
class ResultPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.players = []
        ctk.CTkLabel(self, text="🔍 Öneriler", font=(None,18,"bold")).pack(pady=10)
        self.user_lbl = ctk.CTkLabel(self, text="")
        self.user_lbl.pack(pady=5)
        self.scroll = ctk.CTkScrollableFrame(self, width=340, height=400)
        self.scroll.pack(pady=10)
        ctk.CTkButton(self, text="Geri", command=lambda:self.controller.show_frame(InputPage)).pack(pady=5)
    def show_results(self, user_name, recs):
        for pl in self.players:
            try: pl.stop()
            except: pass
        self.players.clear()
        self.user_lbl.configure(text=f"Merhaba {user_name}, önerilerim:")
        for w in self.scroll.winfo_children():
            w.destroy()
        for rec in recs:
            row = rec['row']
            vids = rec['videoPaths']
            frame = ctk.CTkFrame(self.scroll, corner_radius=8)
            frame.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(frame, text=f"{row['name']} ({row['bodyPart']})").pack(anchor="w", padx=10)
            if vids:
                vid = vids[0]
                rec['previewVid'] = vid  # store chosen preview video
                lbl = tk.Label(frame, bg="black")
                lbl.pack(pady=5)
                player = tkvideo(vid, lbl, loop=0, size=(300,160))
                player.play()
                self.players.append(player)
            ctk.CTkButton(frame, text="Detay", width=60,
                          command=lambda r=rec: self.open_detail(r)).pack(pady=2)
    def open_detail(self, rec):
        for pl in self.players:
            try: pl.stop()
            except: pass
        self.players.clear()
        self.controller.frames[DetailPage].show_detail(rec)
        self.controller.show_frame(DetailPage)

# --- Detay Sayfası ---
class DetailPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.CTkButton(self, text="← Geri", command=lambda: controller.show_frame(ResultPage)).pack(anchor="w", pady=5, padx=5)
        self.video_frame = tk.Frame(self, bg="black", width=340, height=240)
        self.video_frame.pack(pady=10)
        self.lbl_info = ctk.CTkLabel(self, text="", justify="left")
        self.lbl_info.pack(padx=10)
        self.detail_player = None
    def show_detail(self, rec):
        if self.detail_player:
            try: self.detail_player.stop()
            except: pass
        for w in self.video_frame.winfo_children():
            w.destroy()
        vid = rec.get('previewVid')
        if vid:
            lbl = tk.Label(self.video_frame, bg="black")
            lbl.place(relwidth=1, relheight=1)
            self.detail_player = tkvideo(vid, lbl, loop=1, size=(340,240))
            self.detail_player.play()
        else:
            ctk.CTkLabel(self.video_frame, text="Video bulunamadı").pack(expand=True)
        r = rec['row']
        info = (
            f"Hareket: {r['name']}\n"
            f"Bölge: {r['bodyPart']}\n"
            f"Ekipman: {r['equipment']}"
        )
        self.lbl_info.configure(text=info)

if __name__ == "__main__":
    app = FitApp()
    app.mainloop()