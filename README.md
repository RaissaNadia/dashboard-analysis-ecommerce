# 📊  Analysis E-Commerce Data dengan Dashboard

## 📌 Deskripsi Project
Project ini bertujuan untuk menganalisis data e-commerce guna memahami perilaku pelanggan, performa produk, serta faktor yang memengaruhi revenue dan kepuasan pelanggan.

Analisis dilakukan menggunakan pendekatan data analytics mulai dari data wrangling, exploratory data analysis (EDA), hingga explanatory analysis dan visualisasi interaktif menggunakan Streamlit.

---

## 🎯 Tujuan Analisis
- Mengidentifikasi segmentasi pelanggan menggunakan metode RFM (Recency, Frequency, Monetary)
- Menganalisis tren revenue dari waktu ke waktu
- Menentukan kategori produk dengan performa terbaik
- Menganalisis pengaruh keterlambatan pengiriman terhadap kepuasan pelanggan
- Mengidentifikasi faktor yang memengaruhi revenue

---

## 📊 Insight Utama

### 1. Segmentasi Pelanggan (RFM)
Sebagian kecil pelanggan dalam segmen "Top Customer" memberikan kontribusi revenue terbesar. Hal ini menunjukkan bahwa bisnis sangat bergantung pada pelanggan bernilai tinggi.

### 2. Tren Revenue
Terjadi fluktuasi revenue bulanan yang dipengaruhi oleh periode tertentu seperti musim belanja, promosi, atau event khusus.

### 3. Performa Produk
Produk dengan jumlah transaksi tinggi tidak selalu menghasilkan revenue terbesar. Hal ini menunjukkan adanya perbedaan antara popularitas dan profitabilitas.

### 4. Keterlambatan Pengiriman
Keterlambatan pengiriman memiliki dampak signifikan terhadap penurunan review score pelanggan, yang berpotensi memengaruhi loyalitas pelanggan.

### 5. Distribusi Wilayah
Beberapa state memberikan kontribusi revenue yang jauh lebih besar dibandingkan wilayah lainnya, menunjukkan adanya ketimpangan pasar.

---

## 📈 Kesimpulan

Analisis menunjukkan bahwa segmentasi pelanggan dan performa produk merupakan faktor utama yang memengaruhi revenue. Selain itu, keterlambatan pengiriman terbukti berdampak signifikan terhadap kepuasan pelanggan, sehingga menjadi aspek penting yang perlu diperhatikan untuk meningkatkan loyalitas dan performa bisnis secara keseluruhan.

---

## 🖥️ Dashboard
Dashboard interaktif dibuat menggunakan Streamlit dan menampilkan:
- KPI utama (Revenue, Order, Review, Delivery)
- Tren revenue
- Top produk
- Segmentasi pelanggan (RFM)
- Analisis keterlambatan pengiriman
- Performa seller
- Analisis wilayah

---

## ⚙️ Cara Menjalankan Dashboard

1. Install dependencies:
```
pip install -r requirements.txt

---

jalankan streamlit dengan
streamlit run dashboard/dashboard.py

---

masuk melalui broser untuk akses dashboard melalui link yang didapat setelah run streamlit
http://localhost:8501

---

### 📁 Struktur Folder

submission
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt

---
##🚀 Deploy

Dashboard dapat diakses melalui link berikut:

https://dashboard-analysis-ecommerce-goeuakluep969a2q3u3kjd.streamlit.app/


## 👤 Author

Nadia Raissa R

---