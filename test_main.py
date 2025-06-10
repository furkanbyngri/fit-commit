import unittest
from ml import hareket_oner  # ml.py içindeki fonksiyon

class TestFitness(unittest.TestCase):
    def test_hareket_oner(self):
        sonuc = hareket_oner(kilo=70, yas=25, cinsiyet='erkek')
        self.assertIsInstance(sonuc, list)  # hareketlerin listesi bekleniyor

if __name__ == '__main__':
    unittest.main()