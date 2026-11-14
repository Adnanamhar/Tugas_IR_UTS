# pipeline_ir.py
# Pipeline Lengkap Temu Kembali Informasi (TKI) Dokumen Putusan Pengadilan
# Meliputi: Text Preprocessing (Sastrawi + Memoization Cache), Inverted Index, TF-IDF, BM25, & Cosine Similarity

import os
import re
import math
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Any
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Inisialisasi Sastrawi
_stemmer_factory = StemmerFactory()
_stemmer = _stemmer_factory.create_stemmer()

_stopword_factory = StopWordRemoverFactory()
_default_stopwords = set(_stopword_factory.get_stop_words())

# Daftar Stopwords Khusus Domain Hukum (Administratif Peradilan)
# Catatan: Kata substantif penting seperti nama zat (sabu, ganja, ekstasi),
# kata vonis (penjara, denda, subsider), dan ukuran (gram) TETAP dipertahankan.
CUSTOM_LEGAL_STOPWORDS = {
    'halaman', 'dari', 'putusan', 'nomor', 'mahkamah', 'agung', 'republik', 'indonesia',
    'direktori', 'pengadilan', 'negeri', 'panitera', 'pengganti', 'hakim', 'ketua', 'anggota',
    'jaksa', 'penuntut', 'umum', 'tersebut', 'atas', 'bahwa', 'oleh', 'karena', 'itu', 'maka',
    'kepada', 'dalam', 'pada', 'untuk', 'dengan', 'dan', 'atau', 'sebagaimana', 'dimaksud',
    'berdasarkan', 'surat', 'tertanggal', 'tahun', 'bulan', 'hari', 'tanggal', 'persidangan',
    'sidang', 'musyawarah', 'dihadiri', 'dibacakan', 'terbuka', 'disampaikan', 'berita', 'acara',
    'register', 'salinan', 'catatan', 'perkara', 'memeriksa', 'mengadili', 'menimbang',
    'mengingat', 'memperhatikan', 'pasal', 'undang', 'ayat', 'kitab', 'hukum', 'acara', 'pidana',
    'kuhap', 'biaya', 'sejumlah', 'rupiah', 'demikian', 'demikianlah', 'ditetapkan', 'diucapkan'
}

SEMUA_STOPWORDS = _default_stopwords.union(CUSTOM_LEGAL_STOPWORDS)

# Global Cache untuk Stemming (Menghemat waktu eksekusi dari menit menjadi detik)
STEM_CACHE: Dict[str, str] = {}

def fast_stem(word: str) -> str:
    """Melakukan stemming dengan memoization cache agar cepat."""
    if word not in STEM_CACHE:
        STEM_CACHE[word] = _stemmer.stem(word)
    return STEM_CACHE[word]

def bersihkan_dan_tokenisasi(teks: str) -> List[str]:
    """
    Tahap 1: Case Folding & Cleaning
    Tahap 2: Tokenizing
    """
    if not teks:
        return []
        
    # Case Folding
    teks_lower = teks.lower()
    
    # Cleaning noise khusus format putusan (watermark, disclaimer, angka acak)
    teks_clean = re.sub(r'disclaimer\s+kepaniteraan\s+mahkamah\s+agung[^\n]*', ' ', teks_lower)
    teks_clean = re.sub(r'halaman\s+\d+\s+dari\s+\d+[^\n]*', ' ', teks_clean)
    teks_clean = re.sub(r'https?://\S+', ' ', teks_clean)
    
    # Hapus karakter selain huruf alfabet dan spasi
    teks_clean = re.sub(r'[^a-z\s]', ' ', teks_clean)
    
    # Tokenizing sederhana (pemecahan kata)
    tokens = [t.strip() for t in teks_clean.split() if len(t.strip()) > 1]
    return tokens

def preprocess_teks(teks: str, gunakan_stemming: bool = True) -> List[str]:
    """
    Pipeline Preprocessing Lengkap:
    1. Cleaning & Case Folding
    2. Tokenizing
    3. Stopword Removal (Umum + Legal)
    4. Stemming dengan Cache (PySastrawi)
    """
    tokens = bersihkan_dan_tokenisasi(teks)
    
    # Stopword Removal
    tokens_filtered = [t for t in tokens if t not in SEMUA_STOPWORDS]
    
    # Stemming
    if gunakan_stemming:
        tokens_final = [fast_stem(t) for t in tokens_filtered if len(fast_stem(t)) > 1]
    else:
        tokens_final = tokens_filtered
        
    return tokens_final

class InvertedIndexSystem:
    """Sistem Indexing & Temu Kembali Informasi Berbasis Korpus Dokumen Putusan."""
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1  # Parameter BM25
        self.b = b    # Parameter BM25
        self.dokumen_asli: Dict[str, str] = {}
        self.dokumen_tokens: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.vocab: set = set()
        self.idf_cache: Dict[str, float] = {}

    def tambahkan_dokumen(self, doc_id: str, teks: str):
        """Menambahkan dokumen ke korpus dan membangun inverted index."""
        self.dokumen_asli[doc_id] = teks
        tokens = preprocess_teks(teks, gunakan_stemming=True)
        self.dokumen_tokens[doc_id] = tokens
        self.doc_lengths[doc_id] = len(tokens)
        
        # Hitung Term Frequency (TF)
        tf_counts = Counter(tokens)
        for term, freq in tf_counts.items():
            self.inverted_index[term][doc_id] = freq
            self.vocab.add(term)

    def bangun_index(self):
        """Finalisasi indeks dan perhitungan rata-rata panjang dokumen serta IDF."""
        n_docs = len(self.dokumen_tokens)
        if n_docs == 0:
            return
            
        self.avg_doc_length = sum(self.doc_lengths.values()) / n_docs
        
        # Hitung IDF untuk seluruh term di vocabulary
        for term, postings in self.inverted_index.items():
            df_term = len(postings)
            # Standar formula IDF dengan smoothing
            self.idf_cache[term] = math.log((n_docs - df_term + 0.5) / (df_term + 0.5) + 1.0)
            
        print(f"Index selesai dibangun:")
        print(f"  - Total Dokumen : {n_docs}")
        print(f"  - Total Vocabulary: {len(self.vocab)} term unik")
        print(f"  - Rata-rata Panjang Dokumen: {self.avg_doc_length:.1f} token")

    def cari_bm25(self, query: str, top_k: int = 5) -> List[Tuple[str, float, str]]:
        """
        Melakukan pencarian berbasis algoritma Okapi BM25.
        Mengembalikan list of (doc_id, score, snippet).
        """
        query_tokens = preprocess_teks(query, gunakan_stemming=True)
        scores = defaultdict(float)
        
        for term in query_tokens:
            if term not in self.inverted_index:
                continue
                
            idf = self.idf_cache.get(term, 0.0)
            postings = self.inverted_index[term]
            
            for doc_id, tf in postings.items():
                doc_len = self.doc_lengths[doc_id]
                # Formula Okapi BM25
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_length))
                scores[doc_id] += idf * (numerator / denominator)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        hasil = []
        for doc_id, score in ranked:
            snippet = self._buat_snippet(self.dokumen_asli[doc_id], query_tokens)
            hasil.append((doc_id, round(score, 4), snippet))
        return hasil

    def cari_cosine_sim(self, query: str, top_k: int = 5) -> List[Tuple[str, float, str]]:
        """
        Melakukan pencarian berbasis Vector Space Model (VSM) dengan Cosine Similarity.
        """
        query_tokens = preprocess_teks(query, gunakan_stemming=True)
        if not query_tokens:
            return []
            
        # Vektor query TF-IDF
        query_tf = Counter(query_tokens)
        query_vec = {}
        for term, freq in query_tf.items():
            idf = self.idf_cache.get(term, 0.0)
            query_vec[term] = (1 + math.log(freq)) * idf if freq > 0 else 0
            
        q_norm = math.sqrt(sum(v**2 for v in query_vec.values()))
        if q_norm == 0:
            return []

        scores = defaultdict(float)
        doc_norms = defaultdict(float)

        for term, q_val in query_vec.items():
            if term not in self.inverted_index:
                continue
            for doc_id, tf in self.inverted_index[term].items():
                idf = self.idf_cache.get(term, 0.0)
                d_val = (1 + math.log(tf)) * idf
                scores[doc_id] += q_val * d_val
                
        # Hitung norm dokumen dan normalisasi cosine
        ranked = []
        for doc_id, dot_prod in scores.items():
            # Estimasi norm dokumen
            d_norm = math.sqrt(sum(((1 + math.log(tf)) * self.idf_cache.get(t, 0.0))**2 
                                  for t, tf in Counter(self.dokumen_tokens[doc_id]).items()))
            if d_norm > 0:
                sim = dot_prod / (q_norm * d_norm)
                ranked.append((doc_id, sim))

        ranked = sorted(ranked, key=lambda x: x[1], reverse=True)[:top_k]
        
        hasil = []
        for doc_id, score in ranked:
            snippet = self._buat_snippet(self.dokumen_asli[doc_id], query_tokens)
            hasil.append((doc_id, round(score, 4), snippet))
        return hasil

    def _buat_snippet(self, teks_asli: str, kata_kunci: List[str], max_len: int = 180) -> str:
        """Menemukan cuplikan teks yang paling relevan dengan kueri."""
        kalimat_list = re.split(r'[\.\n;]+', teks_asli)
        for kalimat in kalimat_list:
            kalimat_clean = kalimat.strip()
            kalimat_lower = kalimat_clean.lower()
            if any(k in kalimat_lower for k in kata_kunci if len(k) > 2):
                if len(kalimat_clean) > max_len:
                    return kalimat_clean[:max_len] + "..."
                return kalimat_clean
        # Default cuplikan awal
        return teks_asli[:max_len].strip() + "..."

