
<!-- [ID:26_AUTO_DISCOVERY_STR_S001] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, TEXT, LINE -->
## Halaman 9

            "domain": dom,​
            "discovered_tags": tags,​
            "dna": extract_technical_dna(raw_text)​
        })​
    return sections​
​
def slice_oversized_section_safely(text: str, max_chars: int) -> 
list[str]:​
    """​
    Jika ada 1 bab tunggal yang panjangnya > 45.000 karakter, potong 
dengan aman​
    di luar blok kode ``` agar setiap file tetap ketat <= 45.000 
karakter!​
    """​
    if len(text) <= max_chars:​
        return [text]​
    ​
    lines = text.splitlines(keepends=True)​
    chunks = []​
    curr = []​
    curr_len = 0​
    in_code = False​
​
    for line in lines:​
        if line.lstrip().startswith("```"):​
            in_code = not in_code​
        ​
        if curr_len + len(line) > max_chars and not in_code and curr:​
            chunks.append("".join(curr))​
            curr = [line]​
            curr_len = len(line)​
        else:​
            curr.append(line)​
            curr_len += len(line)​
            ​
    if curr:​
        chunks.append("".join(curr))​
    return chunks​
​
# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_STR_S002] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: STR, FAKTA, ESTIMASI -->
# ==============================================================================
DYNAMIC_INJECTED_PATTERNS: set[str] = set()
DYNAMIC_SKILL_REGISTRY: dict[str, str] = {
   "UMKM_CATALOG": "Fokus pencahayaan studio komersial, komposisi produk tajam 8K, latar bersih.",
   "CODING_FRONTIER": "Tulis kode modular yang lulus kompilasi AST, bebas except:pass kosong, dan reversible.
   "DEEP_RESEARCH": "Bedah fakta berlabel [FAKTA]/[ESTIMASI], analisis PNL, risiko, dan langkah eksekusi.",
}
def validate_safe_external_url(url: str) -> tuple[bool, str]:
   """Gate 1: Anti-SSRF & Socket IP Validator (Memblokir localhost, IP privat, dan metadata awan)."""
   try:
       parsed = urlparse(url.strip())
       if parsed.scheme != "https":
           return False, "Wajib protokol HTTPS."
       host = (parsed.hostname or "").lower()
       if (
           not host
           or host in ("localhost", "0.0.0.0", "169.254.169.254")
           or host.endswith((".local", ".internal", ".lan"))
       ):
           return False, "Host internal ditolak oleh proteksi Anti-SSRF."
       try:
           ip = ipaddress.ip_address(host)
           if (
               ip.is_private
               or ip.is_loopback
               or ip.is_link_local
               or ip.is_multicast
               or ip.is_reserved
           ):
               return False, f"Alamat IP privat/internal ({ip}) diblokir."
       except ValueError:
           pass
       return True, "URL Aman"



<!-- [ID:26_AUTO_DISCOVERY_STR_S003] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: STR -->
## Halaman 382

   except Exception as e:
       return False, f"URL tidak valid: {e}"
def sterilize_community_script_ast(
   source_code: str, script_name: str = "community_plugin"
) -> dict[str, Any]:
   """Gate 2: Whitelist-First AST & Dunder Traversal Blocker v4.0 (Menutup CVE-2026-40158)."""
   allowed_imports = {
       "json",
       "re",
       "math",
       "time",
       "datetime",
       "base64",
       "hashlib",
       "hmac",
       "typing",
       "dataclasses",
       "collections",
   }
   forbidden_calls = {
       "system",
       "popen",
       "eval",
       "exec",
       "compile",
       "open",
       "input",
       "breakpoint",
       "spawnl",
       "getattr",
       "setattr",
       "delattr",
       "globals",
       "locals",
       "vars",
       "dir",
       "__import__",
   }
   forbidden_dunders = {
       "__subclasses__",
       "__globals__",
       "__builtins__",
       "__self__",
       "__import__",
       "__mro__",
       "__bases__",
       "__code__",
       "__closure__",
       "__dict__",
       "__class__",
       "__getattribute__",
   }
   try:
       tree = ast.parse(source_code)
   except SyntaxError as e:
       return {
           "ok": False,
           "reason": f"SyntaxError: {e}",
           "hash": "",
           "threats_removed": [str(e)],
       }
   stripped_threats: list[str] = []
   for node in ast.walk(tree):
       if isinstance(node, (ast.Import, ast.ImportFrom)):
           mod_names = [alias.name.split(".")[0] for alias in node.names]
           if isinstance(node, ast.ImportFrom) and node.module:
               mod_names.append(node.module.split(".")[0])
           for m in mod_names:
               if m not in allowed_imports:
                   stripped_threats.append(
                       f"Blocked non-whitelisted import '{m}'"



<!-- [ID:26_AUTO_DISCOVERY_STR_S004] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: STR, TEXT, LINE -->
## Halaman 8

judulnya atau fungsinya​
        base_title_clean = re.sub(r"[^a-z0-9]", "", 
base["title"].lower())​
        base_syms = set(base["dna"]["symbols"])​
​
        for j in range(i + 1, n):​
            if visited[j]:​
                continue​
            cand = secs[j]​
            cand_title_clean = re.sub(r"[^a-z0-9]", "", 
cand["title"].lower())​
            title_sim = SequenceMatcher(None, base_title_clean, 
cand_title_clean).ratio() if base_title_clean and cand_title_clean 
else 0​
            sym_overlap = 
len(base_syms.intersection(cand["dna"]["symbols"])) > 0​
​
            if title_sim >= 0.65 or sym_overlap:​
                visited[j] = True​
                base["audit_flag"] = f"⚠️ 
KEMBAR_PARSIAL_DENGAN_VERSI_LAIN (Rekomendasi Otomatis: PILIH INI 
karena Skor={base['dna']['score']})"​
                cand["audit_flag"] = f"⚠️ 
KEMBAR_PARSIAL_VERSI_ALTERNATIF (Skor={cand['dna']['score']} - Hapus 
blok ini saat audit jika sudah diwakili versi atas, atau gabungkan)"​
                cluster.append(cand)​
​
        ordered.extend(cluster)​
    return ordered​
​
def slice_oversized_safely(text: str, max_chars: int) -> list[str]:​
    if len(text) <= max_chars:​
        return [text]​
    lines = text.splitlines(keepends=True)​
    chunks, curr, curr_len, in_code = [], [], 0, False​
    for line in lines:​
        if line.lstrip().startswith("```"):​
            in_code = not in_code​
        if curr_len + len(line) > max_chars and not in_code and curr:​
            chunks.append("".join(curr))​
            curr, curr_len = [line], len(line)​
        else:​
            curr.append(line)​
            curr_len += len(line)​
    if curr:​
        chunks.append("".join(curr))​
    return chunks​
​


