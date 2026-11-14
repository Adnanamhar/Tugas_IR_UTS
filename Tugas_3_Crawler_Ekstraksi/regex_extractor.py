# regex_extractor.py
# Modul Ekstraksi Informasi Putusan Narkotika Pengadilan Negeri Jakarta Timur
# Mengekstrak 9 Kolom (5 Wajib + 4 Bonus Fokus) sesuai pedoman pengerjaan UTS

import re
from typing import Dict, Any

def bersihkan_teks(teks: str) -> str:
    """Membersihkan spasi berlebih dan karakter noise dari teks PDF."""
    if not teks:
        return ""
    # Ganti non-breaking space
    teks = teks.replace('\xa0', ' ')
    # Rapikan baris kosong berturut-turut
    teks = re.sub(r'\r\n', '\n', teks)
    teks = re.sub(r'\n{3,}', '\n\n', teks)
    return teks.strip()

def ekstrak_nomor_putusan(teks: str) -> str:
    """Mengekstrak nomor registrasi putusan peradilan."""
    # Pola: Nomor 123/Pid.Sus/2024/PN Jkt.Tim atau variasinya
    match = re.search(r'(?:Nomor|NOMOR)\s*:?\s*([0-9]+/[Pp]id\.[A-Za-z0-9\.]+(?:/[A-Za-z0-9\.]+)?/[0-9]{4}/PN\s*[A-Za-z\.]+)', teks)
    if match:
        return match.group(1).strip()
    
    # Alternatif pola umum putusan PN
    match_alt = re.search(r'([0-9]+/[Pp]id\.[A-Za-z0-9\.]+/[0-9]{4}/PN\s*[A-Za-z\.]+)', teks)
    if match_alt:
        return match_alt.group(1).strip()
        
    return "Tidak Ditemukan"

def ekstrak_nama_terdakwa(teks: str) -> str:
    """Mengekstrak nama lengkap terdakwa dari bagian identitas atau pembuka amar."""
    # Pola 1: Bagian identitas formal
    match_id = re.search(r'Nama\s+lengkap\s*:?\s*([^\n\r;]+)', teks, re.IGNORECASE)
    if match_id:
        nama = match_id.group(1).strip()
        # Bersihkan alias / bin / binti
        nama = re.sub(r'\s{2,}', ' ', nama)
        return nama.strip(',.')

    # Pola 2: Bagian awal amar putusan (Menyatakan Terdakwa X terbukti...)
    match_amar = re.search(r'Menyatakan\s+Terdakwa\s+([A-Z\s\.\',]+?)(?:\s+tersebut|\s+telah|\s+terbukti|,)', teks)
    if match_amar:
        nama = match_amar.group(1).strip()
        if len(nama) > 3 and not nama.isupper() == False:
            return nama.strip(',.')
            
    return "Tidak Teridentifikasi"

def ekstrak_tanggal_putusan(teks: str) -> str:
    """Mengekstrak tanggal pembacaan putusan musyawarah hakim."""
    # Pola: pada hari Rabu, tanggal 15 Mei 2024 atau tanggal 15 Mei 2024
    bulan_regex = r'(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)'
    match = re.search(rf'tanggal\s+([0-9]{{1,2}}\s+{bulan_regex}\s+[0-9]{{4}})', teks, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Pola alternatif di akhir dokumen
    match_alt = re.search(rf'([0-9]{{1,2}}\s+{bulan_regex}\s+[0-9]{{4}})', teks[-1500:], re.IGNORECASE)
    if match_alt:
        return match_alt.group(1).strip()
        
    return "Tidak Tertera"

def ekstrak_amar_putusan(teks: str) -> str:
    """Mengekstrak teks amar putusan lengkap setelah kata kunci MENGADILI:"""
    pola_mengadili = r'(?:M\s*E\s*N\s*G\s*A\s*D\s*I\s*L\s*I\s*:?|MENGADILI\s*:?)(.*?)(?:Demikianlah|Demikian\s+diputuskan|Panitera\s+Pengganti|$)'
    match = re.search(pola_mengadili, teks, re.DOTALL | re.IGNORECASE)
    if match:
        amar = match.group(1).strip()
        # Bersihkan nomor halaman atau footer yang mungkin terbawa
        amar_clean = re.sub(r'Halaman\s+[0-9]+\s+dari\s+[0-9]+\s+Putusan[^\n]*', '', amar)
        amar_clean = re.sub(r'Disclaimer[^\n]*', '', amar_clean)
        amar_clean = re.sub(r'\s{2,}', ' ', amar_clean).strip()
        return amar_clean
    return "Amar putusan tidak dapat diekstraksi secara otomatis"

def ekstrak_barang_bukti(teks: str) -> str:
    """Mengekstrak daftar barang bukti tindak pidana narkotika."""
    # Pola 1: Bagian penetapan barang bukti dalam amar putusan
    pola_bb_amar = r'Menetapkan\s+barang\s+bukti\s+berupa\s*:?\s*(.*?)(?:Dirampas|Dikembalikan|Dimusnahkan|Membebankan|Menetapkan\s+agar|6\.)'
    match = re.search(pola_bb_amar, teks, re.DOTALL | re.IGNORECASE)
    if match:
        bb = match.group(1).strip()
        bb_clean = re.sub(r'\s{2,}', ' ', bb).strip(' -:;')
        if len(bb_clean) > 10:
            return bb_clean

    # Pola 2: Bagian barang bukti di uraian dakwaan/tuntutan
    pola_bb_tuntutan = r'barang\s+bukti\s+berupa\s*:?\s*(.*?)(?:sebagaimana\s+diatur|dirampas\s+untuk|dikembalikan\s+kepada)'
    match_tuntutan = re.search(pola_bb_tuntutan, teks, re.DOTALL | re.IGNORECASE)
    if match_tuntutan:
        bb = match_tuntutan.group(1).strip()
        bb_clean = re.sub(r'\s{2,}', ' ', bb).strip(' -:;')
        return bb_clean

    return "Barang bukti tidak terperinci"

def ekstrak_lama_penjara(teks_amar: str) -> str:
    """Mengekstrak lama hukuman pidana penjara."""
    # Pola: pidana penjara selama 6 (enam) tahun dan 3 (tiga) bulan
    pola_penjara = r'penjara\s+selama\s+([0-9]+\s*(?:\([^\)]+\))?\s*(?:tahun|bulan)(?:\s+(?:dan\s+)?[0-9]+\s*(?:\([^\)]+\))?\s*bulan)?)'
    match = re.search(pola_penjara, teks_amar, re.IGNORECASE)
    if match:
        return match.group(1).strip()
        
    match_singkat = re.search(r'selama\s+([0-9]+\s*(?:tahun|bulan)(?:\s+(?:dan\s+)?[0-9]+\s*bulan)?)', teks_amar, re.IGNORECASE)
    if match_singkat:
        return match_singkat.group(1).strip()
        
    return "Tidak Ditemukan"

def ekstrak_denda_subsider(teks_amar: str) -> str:
    """Mengekstrak besaran pidana denda dan kurungan subsider pengganti."""
    # Pola denda nominal dan subsider
    pola_denda = r'(denda\s+(?:sejumlah|sebesar)\s+Rp\.?\s*[0-9\.,]+[^\.;]+(?:dengan\s+ketentuan|apabila|jika|subsider|diganti)[^\.;]+)'
    match = re.search(pola_denda, teks_amar, re.IGNORECASE)
    if match:
        res = match.group(1).strip()
        return re.sub(r'\s{2,}', ' ', res)
        
    # Pola sederhana: Rp X,-
    match_rp = re.search(r'Rp\.?\s*([0-9\.,]+(?:;|\s*\(?[^\)]+\)?))', teks_amar)
    if match_rp:
        return f"Denda Rp {match_rp.group(1).strip()}"
        
    return "Nihil / Tidak Dikenakan Denda"

def ekstrak_semua_fitur(no_urut: int, teks_putusan: str, nama_file: str = "") -> Dict[str, Any]:
    """
    Mengekstrak 9 kolom terstruktur dari dokumen putusan.
    5 Kolom Wajib + 4 Kolom Bonus.
    """
    teks_clean = bersihkan_teks(teks_putusan)
    
    no_putusan = ekstrak_nomor_putusan(teks_clean)
    if no_putusan == "Tidak Ditemukan" and nama_file:
        no_putusan = nama_file.replace('.txt', '').replace('.pdf', '')
        
    amar_putusan = ekstrak_amar_putusan(teks_clean)
    
    return {
        # 5 Kolom Wajib
        "No": no_urut,
        "No Putusan": no_putusan,
        "Lembaga Peradilan": "PN Jakarta Timur",
        "Barang Bukti": ekstrak_barang_bukti(teks_clean),
        "Amar Putusan": amar_putusan,
        # 4 Kolom Bonus
        "Nama Terdakwa": ekstrak_nama_terdakwa(teks_clean),
        "Tanggal Putusan": ekstrak_tanggal_putusan(teks_clean),
        "Lama Pidana Penjara": ekstrak_lama_penjara(amar_putusan if len(amar_putusan) > 20 else teks_clean),
        "Pidana Denda & Subsider": ekstrak_denda_subsider(amar_putusan if len(amar_putusan) > 20 else teks_clean),
    }

