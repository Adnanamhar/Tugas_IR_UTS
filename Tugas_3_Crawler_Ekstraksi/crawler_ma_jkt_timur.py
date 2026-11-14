# crawler_ma_jkt_timur.py
# Pipeline Pengunduhan dan Ekstraksi Putusan PN Jakarta Timur
# Mendukung mode otomatis dan mode pemrosesan batch dari folder SumberData

import os
import sys
import time
import glob
import pandas as pd
from pathlib import Path
import pypdf
import fitz # PyMuPDF

# Import modul konfigurasi dan extractor
sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent))
import config
try:
    from regex_extractor import ekstrak_semua_fitur
except ImportError:
    from Tugas_3_Crawler_Ekstraksi.regex_extractor import ekstrak_semua_fitur

def ekstrak_teks_dari_pdf(pdf_path: str) -> str:
    """Mengekstrak teks penuh dari berkas PDF menggunakan PyMuPDF."""
    teks_total = []
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            teks_total.append(page.get_text())
        doc.close()
    except Exception as e:
        print(f"Error membaca {pdf_path} dengan PyMuPDF: {e}. Mencoba pypdf...")
        try:
            reader = pypdf.PdfReader(pdf_path)
            for page in reader.pages:
                teks_total.append(page.extract_text() or "")
        except Exception as e2:
            print(f"Gagal mengekstrak teks dari {pdf_path}: {e2}")
            return ""
            
    return "\n".join(teks_total)

def proses_batch_putusan(input_pdf_dir: Path, output_txt_dir: Path, output_csv: Path) -> pd.DataFrame:
    """
    Memproses seluruh PDF putusan yang ada di input_pdf_dir:
    1. Ekstraksi teks penuh menjadi file .txt
    2. Ekstraksi 9 fitur terstruktur menggunakan Regex
    3. Ekspor ke file CSV
    """
    output_txt_dir.mkdir(parents=True, exist_ok=True)
    asli_pdfs = sorted(list(input_pdf_dir.glob("Putusan_Asli_MA_JktTim_*.pdf")))
    if len(asli_pdfs) >= 55:
        pdf_files = asli_pdfs[:55]
    elif len(asli_pdfs) > 0:
        pdf_files = asli_pdfs
    else:
        pdf_files = sorted([p for p in input_pdf_dir.glob("*.pdf") if "Analisis" not in p.name and "Putusan Pengadilan" not in p.name])[:55]
    
    print(f"Ditemukan {len(pdf_files)} berkas PDF di {input_pdf_dir}")
    if not pdf_files:
        print("Tidak ada berkas PDF untuk diproses.")
        return pd.DataFrame()

    data_hasil = []
    for idx, pdf_file in enumerate(pdf_files, start=1):
        print(f"[{idx}/{len(pdf_files)}] Memproses: {pdf_file.name}")
        
        # Ekstrak teks
        teks_putusan = ekstrak_teks_dari_pdf(str(pdf_file))
        
        # Simpan teks ke file .txt
        txt_filename = output_txt_dir / f"{pdf_file.stem}.txt"
        with open(txt_filename, "w", encoding="utf-8") as f_out:
            f_out.write(teks_putusan)
            
        # Ekstraksi fitur regex (9 kolom)
        fitur = ekstrak_semua_fitur(no_urut=idx, teks_putusan=teks_putusan, nama_file=pdf_file.name)
        data_hasil.append(fitur)

    df = pd.DataFrame(data_hasil)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"Berhasil menyimpan {len(df)} data ke {output_csv}")
    return df

if __name__ == "__main__":
    # Cek apakah ada PDF di SumberData atau data_putusan_55/pdf
    dir_sumber = config.BASE_DIR / "SumberData"
    dir_target_pdf = config.DIR_DATA_55_PDF
    dir_target_txt = config.DIR_DATA_55_TXT
    
    # Salin atau proses langsung
    if any(dir_sumber.glob("*.pdf")):
        print(f"Memproses PDF dari {dir_sumber}...")
        proses_batch_putusan(dir_sumber, dir_target_txt, config.FILE_CSV_EKSTRAKSI)
    elif any(dir_target_pdf.glob("*.pdf")):
        print(f"Memproses PDF dari {dir_target_pdf}...")
        proses_batch_putusan(dir_target_pdf, dir_target_txt, config.FILE_CSV_EKSTRAKSI)
    else:
        print("Direktori PDF masih kosong. Silakan sediakan atau unduh PDF putusan ke folder SumberData/")

