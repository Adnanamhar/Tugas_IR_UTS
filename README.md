# Ujian Tengah Semester (UTS) Temu Kembali Informasi

Repositori ini memuat seluruh kode program, dataset, dokumen laporan, dan pipeline temu kembali informasi untuk pemenuhan tugas Ujian Tengah Semester (UTS) mata kuliah **Temu Kembali Informasi (Information Retrieval)** pada Program Studi Teknik Informatika, Fakultas Teknik, Universitas Muhammadiyah Malang.

## Identitas Mahasiswa
* **Nama** : Adnan Amhar
* **NIM** : 202310370311001 (Alokasi Digit: `001`)
* **Kelas** : 7A
* **Dosen Pengampu** : Galih W. W
* **Target Yurisdiksi Peradilan** : Pengadilan Negeri Jakarta Timur
* **Klasifikasi Perkara** : Pidana Khusus — Narkotika dan Psikotropika (UU RI No. 35 Tahun 2009)
* **Tahun Putusan** : 2023 – 2025

---

## Struktur Direktori Repositori

```text
Tugas_IR_UTS/
├── Tugas_1_SOTA/
│   └── Laporan_SOTA_TKI_Hukum.pdf            # Laporan SOTA 5 paper Scopus/IEEE (format landscape 7 kolom)
├── Tugas_2_Dataset_GitHub/
│   └── Dataset-Narkotika_001/
│       ├── Dataset/
│       │   └── Narkotika.zip                 # Arsip 55 file PDF putusan resmi PN Jakarta Timur (10 MB)
│       ├── Overview/
│       │   └── Overview.xlsx                 # Metadata 55 putusan (1 sheet tunggal 'Overview', 9 kolom)
│       └── README.md                         # Dokumentasi spesifik dataset kurasi
├── Tugas_3_Crawler_Ekstraksi/
│   ├── Tugas_3_Web_Crawler_dan_Ekstraksi.ipynb # Google Colab crawler & ekstraksi 9 fitur
│   ├── crawler_ma_jkt_timur.py               # Skrip pipeline ekstraksi teks batch
│   ├── regex_extractor.py                    # Modul ekstraksi RegEx 9 fitur peradilan
│   ├── hasil_ekstraksi_50_putusan.csv        # Tabel hasil ekstraksi 55 putusan dalam format CSV
│   └── data_putusan_55/
│       ├── pdf/                              # 55 berkas PDF putusan resmi Mahkamah Agung RI
│       └── txt/                              # 55 berkas teks full-text hasil konversi
├── Tugas_4_Preprocessing_Indexing/
│   ├── Tugas_4_Preprocessing_dan_Indexing.ipynb # Google Colab pipeline temu kembali informasi
│   └── pipeline_ir.py                        # Modul preprocessing, inverted index, TF-IDF, BM25, Cosine Sim
├── docs/
│   └── checklist_pengumpulan.md              # Lembar verifikasi kelengkapan komponen UTS
├── config.py                                 # Konfigurasi terpusat path dan parameter proyek
├── requirements.txt                          # Daftar dependensi pustaka Python
└── README.md                                 # Dokumentasi utama proyek
```

---

## Ringkasan Capaian Penugasan

### 1. Tugas 1: Studi State-of-the-Art (Bobot 10%)
Kajian komparatif terhadap 5 artikel ilmiah bereputasi internasional (Scopus Q1/Q2 dan IEEE Xplore rentang tahun 2021–2026) mengenai arsitektur *Legal Information Retrieval*. Disajikan dalam matriks 7 kolom (Judul, Penulis & Tahun, Nama Jurnal/Konferensi, Problem, Metode/Arsitektur, Dataset/Korpus, dan Hasil Evaluasi).

### 2. Tugas 2: Kurasi Dataset & Format Repositori (Bobot 10%)
Pengelolaan dataset peradilan perkara Narkotika PN Jakarta Timur yang dikemas dalam repositori berstruktur baku. File `Overview/Overview.xlsx` diformat strictly **1 sheet tunggal** bernama `Overview` memuat 55 baris data perkara dan 9 kolom atribut (5 kolom wajib + 4 kolom bonus ekstraksi). Berkas `Dataset/Narkotika.zip` berisi 55 PDF putusan asli yang 100% unik tanpa duplikasi.

### 3. Tugas 3: Web Crawler & Ekstraksi Entitas Peradilan (Bobot 15%)
Pembangunan web crawler direktori resmi Mahkamah Agung RI untuk menghimpun dokumen putusan dan ekstraksi 9 entitas hukum utama menggunakan ekspresi reguler (Nomor Putusan, Lembaga Peradilan, Barang Bukti, Amar Putusan, Nama Terdakwa, Tanggal Putusan, Lama Pidana Penjara, dan Pidana Denda & Subsider).

### 4. Tugas 4: Pipeline Preprocessing & Inverted Indexing (Bobot 15%)
Implementasi temu kembali informasi teks hukum multi-tahap:
* *Case folding*, *tokenization*, dan pembersihan teks hukum.
* *Stopwords removal* khusus peradilan (mempertahankan istilah substansial narkotika).
* *Stemming* Bahasa Indonesia menggunakan PySastrawi dengan mekanisme *memoization caching*.
* Pembangunan struktur data *Inverted Index* (menghasilkan 4.004 *vocabulary* kata unik).
* Pembobotan dokumen berbasis *Term Frequency - Inverse Document Frequency* (TF-IDF) dan BM25.
* Perhitungan relevansi dokumen terhadap kueri pencarian menggunakan *Cosine Similarity*.

---

## Petunjuk Menjalankan Program

### 1. Pemasangan Dependensi
Pastikan Python versi 3.10 atau yang lebih baru telah terpasang, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 2. Menjalankan Ekstraksi Batch Data Putusan (Tugas 3)
Untuk menjalankan ekstraksi data teks dan memperbarui tabel ringkasan CSV:
```bash
python3 Tugas_3_Crawler_Ekstraksi/crawler_ma_jkt_timur.py
```

### 3. Menguji Pipeline Temu Kembali Informasi (Tugas 4)
Untuk menguji fungsi penelusuran dokumen dengan metode TF-IDF dan BM25:
```bash
python3 -c "
import config
from Tugas_4_Preprocessing_Indexing.pipeline_ir import InvertedIndexSystem

ir = InvertedIndexSystem()
for t in sorted(config.DIR_DATA_55_TXT.glob('*.txt')):
    with open(t, 'r', encoding='utf-8') as f:
        ir.tambahkan_dokumen(t.stem, f.read())
ir.bangun_index()
hasil = ir.cari_bm25('narkotika jenis sabu', top_k=3)
for doc, skor, snippet in hasil:
    print(f'Dokumen: {doc} | Skor BM25: {skor:.4f}')
"
```
