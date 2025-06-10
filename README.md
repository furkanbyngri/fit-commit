# Fit-Commit - Sağlık Yaşam Koçu

Fit-Commit, kilo, yaş, cinsiyet gibi kişisel bilgilerinizi kullanarak size yapay zeka destekli, kişiselleştirilmiş fitness hareketleri ve video anlatımlı egzersiz programları sunan bir sağlık yaşam koçudur. Python ile geliştirilmiş olup, kullanıcıya en uygun egzersizleri önerirken yapay zeka ile eğitilmiş modelleri kullanır.

---

## Özellikler

- Kullanıcıdan kilo, yaş ve cinsiyet bilgilerini alır.
- Yapay zeka tabanlı model ile kişiye özel fitness hareketleri önerir.
- Egzersizlerin video anlatımları ile kullanıcıya rehberlik eder.
- Kolay kullanılabilir arayüz ile sağlıklı yaşamı destekler.
- Modüler yapısı ile kolay genişletilebilir.

---

## Teknolojiler

- Python (veri işleme ve model eğitimi)
- Yapay Zeka / Makine Öğrenimi (egzersiz öneri modeli)
- Video oynatma desteği
- Git & GitHub ile versiyon kontrol ve iş birliği
- Jira ile proje yönetimi ve task takibi

---

# Kurulum
1. Projeyi klonlayın:  
   `git clone https://github.com/kullaniciadi/fit-commit.git`
2. Proje klasörüne girin:  
   `cd fit-commit`
3. Gerekli paketleri yükleyin:  
   `pip install -r requirements.txt`
4. Programı çalıştırın:  
   `python src/main_window.py`

   # Kullanım
Program açıldığında kilo, yaş ve cinsiyet bilgilerinizi giriniz. Sistem yapay zeka modelini kullanarak size en uygun egzersiz programını sunacaktır. Her hareketin yanında video anlatımı bulunur, bu videoları izleyerek doğru hareketi yapabilirsiniz.

# Testler
Projede temel işlevlerin doğruluğunu sağlamak için unit testler yazılmıştır.  
Testleri çalıştırmak için:  
`python -m unittest discover tests`

# Proje Yönetimi
Bu proje GitHub’da versiyon kontrolü altında tutulmakta ve Jira ile Kanban yöntemi kullanılarak yönetilmektedir. Her yeni özellik veya hata düzeltmesi için ayrı bir branch açılır ve kod inceleme (code review) süreçleri uygulanır.

# Tasarım Deseni
Projede Strategy Pattern kullanılarak farklı egzersiz öneri algoritmaları kolayca entegre edilebilmektedir.

# Katkıda Bulunanlar
- Furkan Boynueğri— Proje Yönetimi, Git & Jira entegrasyonu  
- Eren Güzel — Python kodlama, Yapay zeka modeli geliştirme
- Eren Albayrak- Test ve Tasarım modelleme
