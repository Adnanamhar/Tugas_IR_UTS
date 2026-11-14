# config.py - Konfigurasi Terpusat Proyek UTS Temu Kembali Informasi 2026
# Mahasiswa: Adnan Amhar (NIM: 202310370311001)

import os
from pathlib import Path

# ==============================================================================
# 1. IDENTITAS MAHASISWA & REPOSITORI
# ==============================================================================
STUDENT_NAME = "Adnan Amhar"
STUDENT_NIM = "202310370311001"
NIM_3_DIGIT = "001"
REPO_NAME = f"Dataset-Narkotika_{NIM_3_DIGIT}"
STATUS_PENGERJAAN = "Individu"
MATA_KULIAH = "Temu Kembali Informasi"
DOSEN_PENGAMPU = "Galih W. W"
UNIVERSITAS = "Universitas Muhammadiyah Malang"
FAKULTAS = "Fakultas Teknik"
SEMESTER = "Ganjil 2026/2027"

# ==============================================================================
# 2. PARAMETER TARGET PERADILAN & DATASET
# ==============================================================================
TARGET_PENGADILAN = "PN Jakarta Timur"
LEMBAGA_PERADILAN_RESMI = "Pengadilan Negeri Jakarta Timur"
DIREKTORI = "Pidana Khusus"
KLASIFIKASI = "Narkotika dan Psikotropika"
TAHUN_RANGE = (2023, 2025)

# Target Jumlah Dokumen
JUMLAH_PUTUSAN_TUGAS_2 = 5   # Kurasi 5 dokumen terbaik untuk Tugas 2 (Overview.xlsx & zip)
JUMLAH_PUTUSAN_TUGAS_3 = 50  # Dokumen crawling Tugas 3
TOTAL_KORPUS_MINIMAL   = 55  # Total minimal korpus lengkap untuk Tugas 4

# ==============================================================================
# 3. STRUKTUR DIREKTORI WORKSPACE
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent

DIR_TUGAS_1 = BASE_DIR / "Tugas_1_SOTA"
DIR_TUGAS_2 = BASE_DIR / "Tugas_2_Dataset_GitHub" / REPO_NAME
DIR_TUGAS_3 = BASE_DIR / "Tugas_3_Crawler_Ekstraksi"
DIR_TUGAS_4 = BASE_DIR / "Tugas_4_Preprocessing_Indexing"

DIR_DATA_55_PDF = DIR_TUGAS_3 / "data_putusan_55" / "pdf"
DIR_DATA_55_TXT = DIR_TUGAS_3 / "data_putusan_55" / "txt"
DIR_KORPUS_55   = DIR_TUGAS_4 / "korpus_lengkap_55"

FILE_CSV_EKSTRAKSI = DIR_TUGAS_3 / "hasil_ekstraksi_50_putusan.csv"
FILE_OVERVIEW_XLSX = DIR_TUGAS_2 / "Overview" / "Overview.xlsx"
FILE_ZIP_NARKOTIKA = DIR_TUGAS_2 / "Dataset" / "Narkotika.zip"
FILE_LAPORAN_TUGAS1_PDF = DIR_TUGAS_1 / "Laporan_SOTA_TKI_Hukum.pdf"

# Skema Kolom Ekstraksi (5 Wajib + 4 Bonus Fokus)
KOLOM_EKSTRAKSI = [
    "No",
    "No Putusan",
    "Lembaga Peradilan",
    "Barang Bukti",
    "Amar Putusan",
    "Nama Terdakwa",
    "Tanggal Putusan",
    "Lama Pidana Penjara",
    "Pidana Denda & Subsider"
]

