
<!-- [ID:26_AUTO_DISCOVERY_A_Z0_9_S001] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: A-Z0-9, ::-1 -->
## Halaman 571

​
​
def _contains_adversarial_pattern(candidate_text: str) -> bool:​
    """Memeriksa teks normal, leetspeak, kata terbalik, dan anagram 
suku kata ('ilja kaerb')."""​
    lowered = candidate_text.lower()​
    collapsed = re.sub(r"\b([a-z0-9])\s+(?=[a-z0-9]\b)", r"\1", 
lowered)​
​
    for variant in (collapsed, collapsed.translate(LEETSPEAK_MAP)):​
        alnum_only = re.sub(r"[^a-z0-9]", "", variant)​
        reversed_full = alnum_only[::-1]​
        word_reversed = "".join(​
            re.sub(r"[^a-z0-9]", "", w)[::-1] for w in variant.split()​
        )​
​
        for root in ADVERSARIAL_ROOTS:​
            if (​
                root in alnum_only​
                or root in reversed_full​
                or root in word_reversed​
            ):​
                return True​
​
        n_chars = len(alnum_only)​
        for root, (r_len, r_sig) in 
ADVERSARIAL_SORTED_SIGNATURES.items():​
            if n_chars >= r_len:​
                for i in range(n_chars - r_len + 1):​
                    window = alnum_only[i : i + r_len]​
                    if "".join(sorted(window)) == r_sig:​
                        if set(window) == set(root):​
                            return True​
    return False​
​
​
def sanitize_and_deobfuscate_input(raw_text: str) -> tuple[str, bool]:​
    """Melucuti karakter hantu Unicode (SEC-01), 'ilja kaerb', 
leetspeak, & Base64."""​
    normalized = unicodedata.normalize("NFKC", raw_text)​
    clean_chars = [​
        c​
        for c in normalized​
        if unicodedata.category(c) not in ("Cf", "Cc", "Cs")​
    ]​
    sanitized = "".join(clean_chars).strip()​
​
    if _contains_adversarial_pattern(sanitized):​


