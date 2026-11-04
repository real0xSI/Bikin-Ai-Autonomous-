
<!-- [ID:26_AUTO_DISCOVERY_DOM_S001] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: DOM, :25, A-ZA-Z0-9_, :15 -->
## Halaman 7

        score = sum(combined_lower.count(kw) for kw in kw_list)​
        if score > 0:​
            scores[dom] = score​
​
    # 4. JIKA TIDAK ADA KATA KUNCI YANG COCOK ATAU SKOR RENDAH -> 
MASUKKAN KE AUTO_DISCOVERY!​
    if not scores:​
        if clean_tags:​
            safe_tag = re.sub(r"[^A-Z0-9_]", "_", clean_tags[0])[:25]​
            return f"26_AUTO_DISCOVERY_{safe_tag}", clean_tags​
        return "26_AUTO_DISCOVERY_UMUM", ["UNLABELED_RAW_DATA"]​
​
    best_dom = max(scores, key=scores.get)​
    return best_dom, clean_tags​
​
def extract_technical_dna(content: str) -> dict:​
    """​
    Mengekstrak daftar fungsi, class, tabel, dan gambar dari sebuah 
seksi​
    untuk dicatat ke dalam 1-3 File Master (Peta Otak AI).​
    """​
    # Cari nama fungsi/class/endpoint di dalam kode​
    funcs_and_classes = 
re.findall(r"(?:def|class|function|interface|type|CREATE 
TABLE)\s+([a-zA-Z0-9_]+)", content)​
    # Cari referensi gambar MinerU / Markdown​
    images = re.findall(r"!\[[^\]]*\]
", content)​
([
)] +)
    # Hitung blok kode & baris tabel​
    code_blocks = len(re.findall(r"```", content)) // 2​
    table_rows = len(re.findall(r"^\|.+\|$", content, re.MULTILINE))​
    ​
    score = (code_blocks * 15) + (table_rows * 2) + 
(len(funcs_and_classes) * 5) + (len(images) * 8)​
    if score >= 40:​
        grade = "PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP"​
    elif score >= 10:​
        grade = "PRIORITAS_2_STRUKTUR_DAN_VISUAL"​
    else:​
        grade = "PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR"​
​
    return {​
        "score": score,​
        "grade": grade,​
        "symbols": list(dict.fromkeys(funcs_and_classes))[:15],​
        "images": images,​
        "code_blocks": code_blocks,​
        "table_rows": table_rows​


