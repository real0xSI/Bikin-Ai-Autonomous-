
<!-- [ID:26_AUTO_DISCOVERY_DICT_S001] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: DICT, LINE -->
# 5. PEMECAH SEMANTIK AMAN (TIDAK MEMOTONG TENGAH BLOK KODE & TABEL)​
# 
======================================================================
========​
def split_lossless_sections(md_text: str, source_tag: str) -> 
list[dict]:​
    lines = md_text.splitlines(keepends=True)​
    sections = []​
    curr_title = "BAGIAN_AWAL_DOKUMEN"​
    curr_lines = []​
    in_code_block = False​
​
    for line in lines:​
        if line.lstrip().startswith("```"):​
            in_code_block = not in_code_block​
​
        # Pisahkan di Heading (#, ##, ###) hanya jika sedang tidak di 
dalam blok kode​
        if not in_code_block and re.match(r"^#{1,3}\s+.+", line):​
            if curr_lines:​
                raw_text = "".join(curr_lines)​
                dom, tags = classify_with_auto_discovery(curr_title, 
raw_text)​
                sections.append({​
                    "source": source_tag,​
                    "title": curr_title.strip(),​
                    "content": raw_text,​
                    "domain": dom,​
                    "discovered_tags": tags,​
                    "dna": extract_technical_dna(raw_text)​
                })​
            curr_title = line​
            curr_lines = [line]​
        else:​
            curr_lines.append(line)​
​
    if curr_lines:​
        raw_text = "".join(curr_lines)​
        dom, tags = classify_with_auto_discovery(curr_title, raw_text)​
        sections.append({​
            "source": source_tag,​
            "title": curr_title.strip(),​
            "content": raw_text,​


