# Proyek Analisis Data: E-Commerce Public Dataset ✨

Analisis data marketplace Olist (Brasil) periode Januari 2017 – Agustus 2018, mencakup tren penjualan bulanan, kontribusi revenue per kategori produk, dampak keterlambatan pengiriman terhadap review, RFM analysis, dan geospatial analysis. Hasilnya disajikan dalam dashboard interaktif Streamlit.

## Struktur Proyek

```
submission
├── dashboard
│   ├── main_data.csv      # data bersih hasil notebook, dipakai dashboard
│   └── dashboard.py       # aplikasi Streamlit
├── data                   # 9 file CSV dataset asli
├── notebook.ipynb         # proses analisis lengkap
├── README.md
├── requirements.txt
└── url.txt                # link dashboard di Streamlit Cloud
```

## Setup Environment - Anaconda

```
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```
mkdir proyek_analisis_data
cd proyek_analisis_data
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

## Menjalankan Notebook

```
jupyter notebook notebook.ipynb
```

Jalankan notebook dari folder utama proyek agar path `data/` terbaca. Notebook juga akan membuat ulang `dashboard/main_data.csv`.

## Run Streamlit App

```
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka di `http://localhost:8501`. Gunakan filter rentang tanggal dan state di sidebar untuk mengubah seluruh grafik.
