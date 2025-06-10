import pandas as pd
import numpy as np
import os
import re
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors
import joblib

# 1. Ana GIF veri kümesini yükle
df_main = pd.read_csv("datas/exercises.csv")
print(f"Ana veri: {df_main.shape[0]} satır, {df_main.shape[1]} sütun")

# 2. Video klasör yapısını tara ve egzersiz adıyla eşleştirecek sözlük oluştur
video_dir = "datas/hareketler"
video_dict = {}
# Her klasör adı egzersiz adı, içinden ilk .mp4 dosyasını alıyoruz
for dirname in os.listdir(video_dir):
    dirpath = os.path.join(video_dir, dirname)
    if os.path.isdir(dirpath):
        # Normalize: lowercase + remove non-alphanumeric
        key = re.sub(r'[^a-z0-9]', '', dirname.lower())
        # .mp4 dosyalarını bul
        videos = [f for f in os.listdir(dirpath) if f.lower().endswith('.mp4')]
        if videos:
            video_dict[key] = os.path.join(dirpath, videos[0])
print(f"Video sözlüğü: {len(video_dict)} egzersiz kaydı")

# 3. Ana veri setinde her hareketin 'name' sütununu normalize ederek anahtara çevirince
#    video_dict içindeki anahtarlardan hangisi adı içine alıyor kontrol ederek videoPath ekle

def normalize_name(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

df_main['nameKey'] = df_main['name'].apply(normalize_name)
# Eşleşen video yolunu ata

df_main['videoPath'] = df_main['nameKey'].apply(
    lambda nk: next((path for key, path in video_dict.items() if key in nk), np.nan)
)
# Video bulunanları filtrele
df = df_main[df_main['videoPath'].notna()].reset_index(drop=True)
print(f"Eşleşen video bulunan hareket sayısı: {df.shape[0]}")

# 4. Metin özelliklerini birleştir (isim + tüm instruction sütunları)
instr_cols = [c for c in df.columns if 'instruction' in c.lower()]
df['text'] = df['name'].astype(str)
for c in instr_cols:
    df['text'] += ' ' + df[c].astype(str)

# 5. Özellik mühendisliği (one-hot + TF-IDF)
categorical_cols = [c for c in ['bodyPart','equipment','target'] if c in df.columns]
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), categorical_cols),
    ('txt', TfidfVectorizer(max_features=1000, stop_words='english'), 'text')
], remainder='drop')

# 6. Özellik matrisi oluştur
X = preprocessor.fit_transform(df)
print(f"Özellik matrisi: {X.shape}")

# 7. NearestNeighbors modelini eğit
dist_model = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute')
dist_model.fit(X)

# 8. Model ve ön işlem adımlarını kaydet
joblib.dump({'preprocessor': preprocessor, 'model': dist_model, 'data': df}, 'fitness_recommender_combined.joblib')
print("Model ve ön işlemler kaydedildi: fitness_recommender_combined.joblib")

# 9. Öneri fonksiyonu (kullanıcı girdisi üzerinden)
def recommend(record: dict, top_n: int = 5):
    qdf = pd.DataFrame([record])
    # normalize ve text oluşturma
    qdf['text'] = qdf['name'].astype(str)
    for c in instr_cols:
        if c in qdf.columns:
            qdf['text'] += ' ' + qdf[c].astype(str)
    # ön işleme ve benzerlik
    qX = preprocessor.transform(qdf)
    distances, indices = dist_model.kneighbors(qX, n_neighbors=top_n)
    # önerilen videolar dahil
    return df.iloc[indices[0]][['name','bodyPart','equipment','videoPath']]

# 10. Örnek test
example = {
    'name': 'push-up',  # örnek olarak push-up
    'bodyPart': 'chest',
    'equipment': 'body weight',
    'target': 'pectorals'
}
print("Örnek öneriler:")
print(recommend(example))
