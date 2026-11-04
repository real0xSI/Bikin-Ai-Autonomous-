
<!-- [ID:26_AUTO_DISCOVERY_LINE_S001] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: LINE, DICT, AUDIT_MANUAL_PILIH_SATU, FALSE, BASE -->
## Halaman 7

        if line.lstrip().startswith("```"):​
            in_code = not in_code​
        if not in_code and re.match(r"^#{1,3}\s+.+", line):​
            if curr_lines:​
                raw = "".join(curr_lines)​
                dom, tags, dna = classify_and_extract_dna(curr_title, 
raw)​
                sections.append({"source": source_tag, "title": 
curr_title.strip(), "content": raw, "domain": dom, "tags": tags, 
"dna": dna})​
            curr_title = line​
            curr_lines = [line]​
        else:​
            curr_lines.append(line)​
​
    if curr_lines:​
        raw = "".join(curr_lines)​
        dom, tags, dna = classify_and_extract_dna(curr_title, raw)​
        sections.append({"source": source_tag, "title": 
curr_title.strip(), "content": raw, "domain": dom, "tags": tags, 
"dna": dna})​
    return sections​
​
def mark_similar_sections_for_human_audit(secs: list[dict]):​
    """​
    Mendeteksi bab dari PDF vs MD yang judul/isinya mirip (tapi tidak 
100% kembar),​
    lalu menaruhnya BERDAMPINGAN dan memberi bendera 
[AUDIT_MANUAL_PILIH_SATU]​
    agar Anda mudah mengaudit mana yang mau dipakai sebelum disuapkan 
ke AI!​
    """​
    n = len(secs)​
    visited = [False] * n​
    ordered = []​
​
    # Urutkan awal berdasarkan skor tertinggi​
    secs.sort(key=lambda x: x["dna"]["score"], reverse=True)​
​
    for i in range(n):​
        if visited[i]:​
            continue​
        visited[i] = True​
        base = secs[i]​
        base["audit_flag"] = "MANDIRI_UNIK"​
        cluster = [base]​
​
        # Cari apakah ada seksi lain di domain yang sama yang mirip 


