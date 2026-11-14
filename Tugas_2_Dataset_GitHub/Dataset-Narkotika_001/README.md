# Dataset Putusan Pidana Narkotika — Pengadilan Negeri Jakarta Timur

[![Mata Kuliah](https://img.shields.io/badge/Mata%20Kuliah-Temu%20Kembali%20Informasi-007ACC?style=flat-square)](#)
[![Institusi](https://img.shields.io/badge/Institusi-Universitas%20Muhammadiyah%20Malang-B31B1B?style=flat-square)](#)
[![Tahun Putusan](https://img.shields.io/badge/Tahun%20Putusan-2023--2025-success?style=flat-square)](#)
[![Klasifikasi](https://img.shields.io/badge/Klasifikasi-Pidana%20Khusus%20Narkotika-orange?style=flat-square)](#)
[![Lisensi](https://img.shields.io/badge/Lisensi-Public%20Domain%20(Open%20Data%20MA%20RI)-blue?style=flat-square)](#)

Repositori ini memuat dataset kurasi putusan pengadilan perkara **Pidana Khusus Narkotika dan Psikotropika** dari **Pengadilan Negeri Jakarta Timur** rentang tahun **2023 hingga 2025**. Dataset ini dikumpulkan dan dikelola untuk memenuhi penugasan Ujian Tengah Semester (UTS) mata kuliah **Temu Kembali Informasi (Information Retrieval)** pada Program Studi Teknik Informatika, Fakultas Teknik, Universitas Muhammadiyah Malang.

Dokumen putusan pengadilan Mahkamah Agung RI merupakan dokumen publik terbuka yang tidak terikat Hak atas Kekayaan Intelektual (HaKI), sehingga dapat dimanfaatkan secara legal sebagai korpus pengujian sistem *Information Retrieval*, ekstraksi entitas (*Information Extraction*), dan pemodelan pencarian dokumen hukum.

---

## Struktur Direktori Repositori

Sesuai ketentuan penugasan (SUBCPMK-2), struktur direktori repositori disusun sebagai berikut:

```text
Dataset-Narkotika_001/
├── Dataset/
│   └── Narkotika.zip          # Arsip berkas putusan pengadilan berekstensi .pdf
├── Overview/
│   └── Overview.xlsx          # Ringkasan data putusan terstruktur (Excel format)
└── README.md                  # Dokumentasi teknis dataset
```

---

## Metadata & Skema Atribut Data

Ringkasan metadata perkara pada `Overview/Overview.xlsx` mencakup atribut wajib dan rincian putusan peradilan:

| No | Nama Kolom | Tipe Data | Deskripsi |
| :---: | :--- | :---: | :--- |
| 1 | `No` | Integer | Nomor urut dokumen putusan dalam dataset (1 s.d. 55). |
| 2 | `No Putusan` | String | Nomor registrasi perkara resmi pada PN Jakarta Timur (contoh: `.../Pid.Sus/2024/PN Jkt.Tim`). |
| 3 | `Lembaga Peradilan` | String | Instansi peradilan yang memutus perkara (`PN Jakarta Timur`). |
| 4 | `Barang Bukti` | Text | Rincian barang bukti narkotika (jenis narkotika, jumlah bungkus plastik klip, berat kotor/bersih dalam gram, timbangan digital, gawai/HP, dan alat hisap). |
| 5 | `Amar Putusan` | Text | Teks putusan lengkap Majelis Hakim setelah klausul `MENGADILI:` mencakup penetapan kesalahan terdakwa, vonis masa penjara, denda, serta status barang bukti. |
| 6 | `Nama Terdakwa` | String | Identitas nama lengkap terdakwa perkara narkotika. |
| 7 | `Tanggal Putusan` | String | Tanggal pembacaan putusan musyawarah oleh Majelis Hakim. |
| 8 | `Lama Pidana Penjara` | String | Durasi hukuman vonis kurungan penjara (tahun dan bulan). |
| 9 | `Pidana Denda & Subsider` | String | Besaran denda nominal (Rupiah) beserta lama kurungan pengganti (subsider). |

> **Catatan Format:** Sesuai rubrik evaluasi penugasan, seluruh 9 atribut (5 kolom wajib + 4 kolom bonus ekstraksi) disatukan secara elegan ke dalam **1 Single Tab (Sheet Tunggal)** bernama **`Overview`** dengan total tepat 56 baris (1 baris header + 55 baris data perkara).

---

## Kriteria Pemilihan Data

1. **Lembaga Peradilan**: Seluruh putusan berasal dari yurisdiksi **Pengadilan Negeri Jakarta Timur (PN Jkt.Tim)** sesuai alokasi NIM `001`.
2. **Kategori Perkara**: Direktori **Pidana Khusus**, klasifikasi **Narkotika dan Psikotropika** (pelanggaran UU RI No. 35 Tahun 2009).
3. **Rentang Waktu**: Putusan yang dibacakan pada periode **2023 s.d. 2025**.
4. **Keaslian & Keunikan Dokumen**: Seluruh 55 berkas merupakan dokumen putusan resmi multi-halaman berstempel Mahkamah Agung RI (total 1.607 halaman), tanpa adanya duplikasi perkara (100% unik).

---

## Cara Menggunakan Dataset

### 1. Mengekstrak Arsip PDF
```bash
unzip Dataset/Narkotika.zip -d extracted_pdf/
```

### 2. Membaca Metadata dengan Python (Pandas)
```python
import pandas as pd

# Membaca tab tunggal Overview (55 data x 9 kolom)
df_overview = pd.read_excel("Overview/Overview.xlsx", sheet_name="Overview")
print(f"Total Data: {len(df_overview)} baris, {len(df_overview.columns)} kolom")
print(df_overview[["No Putusan", "Nama Terdakwa", "Lama Pidana Penjara", "Pidana Denda & Subsider"]].head())
```

---

## Identitas Mahasiswa

* **Nama Mahasiswa** : Adnan Amhar
* **NIM** : 202310370311001 (3 Digit Terakhir: `001`)
* **Mata Kuliah** : Temu Kembali Informasi (TKI)
* **Dosen Pengampu** : Galih W. W
* **Fakultas / Prodi** : Fakultas Teknik / Informatika
* **Universitas** : Universitas Muhammadiyah Malang

