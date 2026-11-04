
<!-- [ID:22_HITL_ACTION_S011] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PATCH AUDIT-02, :16 -->
# ==============================================================================
def verify_telegram_webapp_init_data(init_data_raw: str, bot_token: str, max_age_sec: int = 86400) -> dict[str, Any] | None:
    """[PATCH AUDIT-02]: Memverifikasi tanda tangan HMAC-SHA256 Telegram.WebApp.initData."""
    if not init_data_raw or not bot_token:
        return None
    try:
        parsed = dict(parse_qsl(init_data_raw, keep_blank_values=True))
        received_hash = parsed.pop("hash", "")
        if not received_hash:
            return None
        auth_date = int(parsed.get("auth_date", "0"))
        if auth_date > 0 and abs(int(time.time()) - auth_date) > max_age_sec:
            return None
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calculated_hash, received_hash):
            return None
        user_json = parsed.get("user", "{}")
        return json.loads(user_json)
    except Exception:
        return None


_INJECTION_PATTERNS = re.compile(
    r"(ignore\s+(all\s+)?(previous|prior)\s+instructions|system\s*prompt|"
    r"you\s+are\s+now\s+dan|jailbreak|ilja\s*kaerb|drop\s+table|union\s+select|"
    r"<script\b|javascript:|__import__|__subclasses__|__globals__|os\.system|subprocess)",
    re.IGNORECASE,
)


def sanitize_and_deobfuscate_input(raw_text: str) -> tuple[str, bool]:
    if not raw_text:
        return "", False
    normalized = unicodedata.normalize("NFKC", raw_text)
    cleaned = "".join(
        ch for ch in normalized if unicodedata.category(ch) not in ("Cf", "Cc") or ch in ("\n", "\r", "\t")
    ).strip()
    leet_map = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})
    deobfuscated = cleaned.lower().translate(leet_map)
    if _INJECTION_PATTERNS.search(cleaned) or _INJECTION_PATTERNS.search(deobfuscated):
        return cleaned, True
    return cleaned, False


def issue_stateless_ed25519_voucher(user_id: int, compute_units: int = 10, ttl_seconds: int = 86400) -> str:
    now_ts = int(time.time())
    nonce = hashlib.sha256(f"{user_id}:{now_ts}:{os.urandom(8).hex()}".encode()).hexdigest()[:16]
    payload_dict = {"n": nonce, "u": int(user_id), "c": int(compute_units), "exp": now_ts + ttl_seconds}
    payload_bytes = json.dumps(payload_dict, separators=(",", ":")).encode("utf-8")
    priv_key = Ed25519PrivateKey.from_private_bytes(ED25519_PRIV_BYTES)
    signature = priv_key.sign(payload_bytes)
    b64_payload = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
    b64_sig = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
    return f"VCH-{b64_payload}.{b64_sig}"


async def verify_and_redeem_ed25519_voucher(
    db: aiosqlite.Connection, voucher_code: str
) -> tuple[bool, str, int]:
    code = voucher_code.strip()
    if not code.startswith("VCH-") or "." not in code:
        return False, "Format kode voucher tidak valid.", 0
    try:
        body = code[4:]
        b64_payload, b64_sig = body.split(".", 1)
        payload_bytes = base64.urlsafe_b64decode(b64_payload + "=" * (-len(b64_payload) % 4))
        sig_bytes = base64.urlsafe_b64decode(b64_sig + "=" * (-len(b64_sig) % 4))

        pub_key = Ed25519PublicKey.from_public_bytes(ED25519_PUB_BYTES)
        pub_key.verify(sig_bytes, payload_bytes)

        data = json.loads(payload_bytes.decode("utf-8"))
        exp = int(data.get("exp", 0))
        units = int(data.get("c", 10))
        now_ts = int(time.time())
        if exp <= now_ts:
            return False, "Kode voucher sudah kedaluwarsa.", 0

        nullifier_hash = hashlib.sha256(sig_bytes).hexdigest()

        async def _tx(conn: aiosqlite.Connection) -> bool:
            cur = await conn.execute(
                "SELECT 1 FROM redeemed_nullifiers WHERE nullifier_hash = ?;", (nullifier_hash,)
            )
            if await cur.fetchone():
                return False
            await conn.execute(
                "INSERT INTO redeemed_nullifiers (nullifier_hash, expires_at) VALUES (?, ?);",
                (nullifier_hash, exp),
            )
            return True

        ok = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
        if not ok:
            return False, "Kode voucher sudah pernah digunakan sebelumnya.", 0
        return True, f"Kode Voucher Valid (+{units} Unit Kredit Studio Web)!", units
    except Exception as e:
        return False, f"Verifikasi voucher gagal: {e}", 0



<!-- [ID:22_HITL_ACTION_S012] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :-4 -->
## Halaman 398

   )
   row_c = await cur_check.fetchone()
   avail_now = int(row_c[0]) if row_c else 0
   total_prev = int(row_c[1]) if row_c else 0
   if avail_now <= 0:
       return False, 0, total_prev, "NO_PROFIT_YET"
   threshold = int(
       RUNTIME_CONFIG.get("HARVEST_APPROVAL_THRESHOLD_IDR", 500_000)
   )
   if avail_now > threshold and not bypass_threshold_gate:
       ticket = await HUMAN_APPROVAL_GATE.request_approval(
           db,
           action_type="WITHDRAW_ABOVE_THRESHOLD",
           summary=f"Penarikan Laba Bersih Rp {avail_now:,} (> Threshold Rp {threshold:,})",
           payload={"amount_idr": avail_now},
       )
       return False, avail_now, total_prev, ticket["approval_id"]
   async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int]:
       now_ts = int(time.time())
       cur = await conn.execute(
           "SELECT harvestable_profit_vault_idr, total_harvested_by_owner_idr FROM treasury_summary WHERE id 
       )
       row = await cur.fetchone()
       if not row or int(row[0]) <= 0:
           return False, 0, int(row[1]) if row else 0
       avail, new_total = int(row[0]), int(row[1]) + int(row[0])
       await conn.execute(
           "UPDATE treasury_summary SET harvestable_profit_vault_idr = 0, total_harvested_by_owner_idr = ?, u
           (new_total, now_ts),
       )
       return True, avail, new_total
   ok, h_now, tot_h = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
   return ok, h_now, tot_h, "HARVESTED"
def compute_crc16_ccitt(data_str: str) -> str:
   crc = 0xFFFF
   for ch in data_str.encode("utf-8"):
       crc ^= ch << 8
       for _ in range(8):
           crc = (
               ((crc << 1) ^ 0x1021) & 0xFFFF
               if (crc & 0x8000)
               else (crc << 1) & 0xFFFF
           )
   return f"{crc:04X}"
def generate_dynamic_qris_string(static_qris: str, amount_idr: int) -> str:
   if (
       not static_qris
       or len(static_qris) < 20
       or "5802ID" not in static_qris
   ):
       static_qris = (
           "00020101021126610014ID.CO.GOPAY.WWW01189360091431234567890210G1234567890303UMI"
           "51440014ID.CO.QRIS.WWW0215ID10200000000010303UMI5204581253033605802ID5912BIKINAI STUDIO6007JAKART
       )
   base_qris = static_qris[:-4].replace("010211", "010212", 1)
   if base_qris.endswith("6304"):
       base_qris = base_qris[:-4]
   amt_str = str(int(amount_idr))
   parts = base_qris.split("5802ID", 1)
   reconstructed = (
       f"{parts[0]}54{len(amt_str):02d}{amt_str}5802ID{parts[1]}6304"
   )
   return f"{reconstructed}{compute_crc16_ccitt(reconstructed)}"
async def create_payment_invoice(



<!-- [ID:22_HITL_ACTION_S013] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# Menangkal Token Replay di dalam jendela 60 detik & kompatibel 
protokol Ed25519 TG​
# 
=====================================================================​
class BoundedReplayGuard:​
    def __init__(self, max_size: int = 10000, ttl_seconds: int = 65):​
        self.cache: OrderedDict[str, float] = OrderedDict()​
        self.max_size = max_size​
        self.ttl = ttl_seconds​
​
    def is_replayed_or_register(self, digest_hex: str) -> bool:​
        now = time.time()​
        while self.cache:​
            oldest_key, ts = next(iter(self.cache.items()))​
            if now - ts > self.ttl:​



<!-- [ID:22_HITL_ACTION_S014] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# 3. PERTAHANAN SEC-03: Strict Hostname Whitelist (Anti-SSRF) & HMAC 
Capability Token​
ALLOWED_UPSTREAM_CDN = {"v3.fal.media", "fal.media", 
"replicate.delivery", "cdn.bikinai-gpu.internal"}​
SERVER_SECRET = b"GANTI_DENGAN_32_BYTE_KUNCI_RAHASIA_ANDA"​
​
def verify_safe_upstream_url(url: str) -> bool:​
    parsed = urlparse(url)​
    return parsed.scheme == "https" and parsed.hostname in 
ALLOWED_UPSTREAM_CDN​
​
def generate_webhook_token(job_id: str) -> str:​
    return hmac.new(SERVER_SECRET, job_id.encode(), 
hashlib.sha256).hexdigest()​
​
async def safe_one_time_refund(db: aiosqlite.Connection, job_id: str, 
token: str) -> bool:​
    """Menangkal Webhook Spoofing & Infinite Auto-Refund."""​
    if not hmac.compare_digest(generate_webhook_token(job_id), token):​
        return False​
    cursor = await db.execute(​
        """​
        UPDATE jobs ​



<!-- [ID:22_HITL_ACTION_S015] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :32, :16 -->
## Halaman 391

           "5": "s",
           "7": "t",
           "@": "a",
           "$": "s",
       }
   )
   deobfuscated = cleaned.lower().translate(leet_map)
   for dyn_pat in DYNAMIC_INJECTED_PATTERNS:
       if dyn_pat and (dyn_pat in cleaned.lower() or dyn_pat in deobfuscated):
           return cleaned, True
   is_inj = bool(
       _INJECTION_PATTERNS.search(cleaned)
       or _INJECTION_PATTERNS.search(deobfuscated)
   )
   if is_inj and len(cleaned) >= 12:
       # Self-Evolving Threat Memory: simpan potongan pola serangan baru di memori aktif
       DYNAMIC_INJECTED_PATTERNS.add(deobfuscated[:32])
   return cleaned, is_inj
def sanitize_external_api_response(raw_reply: str) -> str:
   if not raw_reply:
       return ""
   cleaned = re.sub(
       r"<script\b[^>]*>.*?</script>",
       "",
       raw_reply,
       flags=re.IGNORECASE | re.DOTALL,
   )
   cleaned = re.sub(r"javascript\s*:", "", cleaned, flags=re.IGNORECASE)
   return cleaned.replace("|---|", "").strip()
def verify_telegram_webapp_init_data(
   init_data_raw: str, bot_token: str, max_age_sec: int = 3600
) -> dict[str, Any] | None:
   """Menutup VULN-02: Verifikasi kriptografi HMAC-SHA256 timing-safe atas Telegram initData."""
   if not init_data_raw or not bot_token:
       return None
   try:
       parsed = dict(parse_qsl(init_data_raw, keep_blank_values=True))
       received_hash = parsed.pop("hash", "")
       if not received_hash:
           return None
       auth_date = int(parsed.get("auth_date", "0"))
       if auth_date > 0 and abs(int(time.time()) - auth_date) > max_age_sec:
           return None
       data_check_string = "\n".join(
           f"{k}={v}" for k, v in sorted(parsed.items())
       )
       secret_key = hmac.new(
           b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256
       ).digest()
       calculated_hash = hmac.new(
           secret_key, data_check_string.encode("utf-8"), hashlib.sha256
       ).hexdigest()
       return (
           json.loads(parsed.get("user", "{}"))
           if hmac.compare_digest(calculated_hash, received_hash)
           else None
       )
   except Exception:
       return None
def issue_stateless_ed25519_voucher(
   user_id: int, compute_units: int = 15, ttl_seconds: int = 86400
) -> str:
   """
   Menutup VULN-06 (Zero-Identity Linkage):
   TIDAK menyimpan "u": user_id di dalam JSON voucher!
   Diganti dengan Blinded Hash Commitment satu arah H_blind = SHA256(Nonce || Salt)[:16].



<!-- [ID:22_HITL_ACTION_S016] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: DIGEST_HEX -->
# Menutup celah Replay Attack (API-01) & Infinite Voucher Double-Spend​
# 
======================================================================
========​
class BoundedReplayGuard:​
    def __init__(self, max_size: int = 25000, ttl_seconds: int = 65):​
        self.cache: OrderedDict[str, float] = OrderedDict()​
        self.max_size = max_size​
        self.ttl = ttl_seconds​
​
    def is_replayed_or_register(self, digest_hex: str) -> bool:​
        now = time.time()​
        while self.cache:​
            _, ts = next(iter(self.cache.items()))​
            if now - ts > self.ttl:​
                self.cache.popitem(last=False)​
            else:​
                break​
        if digest_hex in self.cache:​
            return True​
        if len(self.cache) >= self.max_size:​
            self.cache.popitem(last=False)​
        self.cache[digest_hex] = now​
        return False​
​
​
REPLAY_GUARD = BoundedReplayGuard(max_size=25000, ttl_seconds=65)​
VOUCHER_NULLIFIER_GUARD = BoundedReplayGuard(max_size=100000, 



<!-- [ID:22_HITL_ACTION_S017] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: DIGEST_HEX -->
## Halaman 217

        self.max_size = max_size​
        self.ttl = ttl_seconds​
​
    def is_replayed_or_register(self, digest_hex: str) -> bool:​
        now = time.time()​
        while self.cache:​
            oldest_key, ts = next(iter(self.cache.items()))​
            if now - ts > self.ttl:​
                self.cache.popitem(last=False)​
            else:​
                break​
        if digest_hex in self.cache:​
            return True​
        if len(self.cache) >= self.max_size:​
            self.cache.popitem(last=False)​
        self.cache[digest_hex] = now​
        return False​
​
REPLAY_GUARD = BoundedReplayGuard()​
​
def verify_telegram_webapp_initdata(init_data_raw: str, bot_token: 
str, max_age_sec: int = 60) -> dict | None:​
    """Verifikasi HMAC-SHA256 initData resmi Telegram + Proteksi 
Anti-Replay."""​
    parsed = dict(parse_qsl(init_data_raw, keep_blank_values=True))​
    received_hash = parsed.pop("hash", None)​
    parsed.pop("signature", None)  # Kecualikan field signature sesuai 
standar protokol terbaru​
    if not received_hash:​
        return None​
​
    auth_date = int(parsed.get("auth_date", 0))​
    if abs(int(time.time()) - auth_date) > max_age_sec:​
        return None​
​
    if REPLAY_GUARD.is_replayed_or_register(received_hash):​
        return None​
​
    data_check_string = "\n".join(f"{k}={v}" for k, v in 
sorted(parsed.items()))​
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), 
hashlib.sha256).digest()​
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), 
hashlib.sha256).hexdigest()​
​
    if not hmac.compare_digest(calculated_hash, received_hash):​
        return None​
    return parsed​



<!-- [ID:22_HITL_ACTION_S018] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :14 -->
## Halaman 383

                   )
       elif isinstance(node, ast.Attribute) and (
           node.attr in forbidden_dunders or node.attr.startswith("__")
       ):
           stripped_threats.append(f"Blocked dunder attribute '{node.attr}'")
       elif isinstance(node, ast.Name) and (
           node.id in forbidden_dunders
           or node.id in forbidden_calls
           or node.id.startswith("__")
       ):
           stripped_threats.append(f"Blocked identifier '{node.id}'")
       elif isinstance(node, ast.Call):
           fn = (
               node.func.id
               if isinstance(node.func, ast.Name)
               else (
                   node.func.attr
                   if isinstance(node.func, ast.Attribute)
                   else ""
               )
           )
           if fn in forbidden_calls:
               stripped_threats.append(f"Blocked call '{fn}()'")
       elif (
           isinstance(node, ast.ExceptHandler)
           and len(node.body) == 1
           and isinstance(node.body[0], ast.Pass)
       ):
           stripped_threats.append("Blocked empty 'except: pass'")
   ast_hash = hashlib.sha256(ast.dump(tree).encode()).hexdigest()[:14]
   if not stripped_threats:
       AUTONOMIC_GUARD.verified_ast_hashes.add(ast_hash)
   return {
       "ok": len(stripped_threats) == 0,
       "script_name": script_name,
       "threats_removed": stripped_threats,
       "hash": ast_hash,
   }
class ModelScanSecurityGate:
   """
   Gate 5: Penegakan Format Tensor Nir-Eksekusi (.safetensors / .gguf)
   dan integrasi pemindai statis protectai/modelscan (Exit Codes 0-4).
   """
   SAFE_EXTENSIONS = (".safetensors", ".gguf")
   RISKY_PICKLE_EXTENSIONS = (".pt", ".pth", ".bin", ".pkl", ".ckpt", ".h5")
   @classmethod
   def verify_model_artifact(cls, model_path_or_repo: str) -> dict[str, Any]:
       target = model_path_or_repo.strip()
       low = target.lower()
       if low.endswith(cls.SAFE_EXTENSIONS) or "gguf" in low or "safetensors" in low:
           return {
               "safe": True,
               "exit_code": 0,
               "format": "SAFETENSORS_OR_GGUF",
               "detail": "Format tensor nir-eksekusi terverifikasi aman (Zero Pickle Execution).",
           }
       # Jika merujuk ke file lokal berisiko Pickle/H5, jalankan CLI modelscan jika tersedia
       if Path(target).exists():
           modelscan_bin = shutil.which("modelscan")
           if modelscan_bin:
               try:
                   proc = subprocess.run(
                       [modelscan_bin, "-p", target],
                       capture_output=True,
                       text=True,
                       timeout=15,
                       check=False,
                   )



<!-- [ID:22_HITL_ACTION_S019] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 573

ttl_seconds=260000)​
​
​
def verify_telegram_webapp_initdata(​
    init_data_raw: str,​
    bot_token: str,​
    max_age_sec: int = 60,​
    request_nonce: str = "",​
) -> dict | None:​
    parsed = dict(parse_qsl(init_data_raw, keep_blank_values=True))​
    received_hash = parsed.pop("hash", None)​
    parsed.pop("signature", None)​
    if not received_hash:​
        return None​
    try:​
        auth_date = int(parsed.get("auth_date", 0))​
    except ValueError:​
        return None​
    if abs(int(time.time()) - auth_date) > max_age_sec:​
        return None​
​
    replay_key = (​
        f"{received_hash}:{request_nonce}" if request_nonce else 
received_hash​
    )​
    if REPLAY_GUARD.is_replayed_or_register(replay_key):​
        return None​
​
    data_check_string = "\n".join(​
        f"{k}={v}" for k, v in sorted(parsed.items())​
    )​
    secret_key = hmac.new(​
        b"WebAppData", bot_token.encode(), hashlib.sha256​
    ).digest()​
    calc_hash = hmac.new(​
        secret_key, data_check_string.encode(), hashlib.sha256​
    ).hexdigest()​
    return (​
        parsed if hmac.compare_digest(calc_hash, received_hash) else 
None​
    )​
​
​
def mint_stateless_ed25519_voucher(​
    private_key_bytes: bytes,​
    voucher_nonce: str,​
    coin_amount: int,​
    origin_ppp_tier: int,​



<!-- [ID:22_HITL_ACTION_S020] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: DIGEST_HEX -->
## Halaman 598

        self.max_size = max_size​
        self.ttl = ttl_seconds​
​
    def is_replayed_or_register(self, digest_hex: str) -> bool:​
        now = time.time()​
        while self.cache:​
            oldest_key, ts = next(iter(self.cache.items()))​
            if now - ts > self.ttl:​
                self.cache.popitem(last=False)​
            else:​
                break​
        if digest_hex in self.cache:​
            return True​
        if len(self.cache) >= self.max_size:​
            self.cache.popitem(last=False)​
        self.cache[digest_hex] = now​
        return False​
​
REPLAY_GUARD = BoundedReplayGuard()​
​
def verify_telegram_webapp_initdata(init_data_raw: str, bot_token: 
str, max_age_sec: int = 60) -> dict | None:​
    """Verifikasi HMAC-SHA256 initData resmi Telegram + Proteksi 
Anti-Replay."""​
    parsed = dict(parse_qsl(init_data_raw, keep_blank_values=True))​
    received_hash = parsed.pop("hash", None)​
    parsed.pop("signature", None)  # Kecualikan field signature sesuai 
standar protokol terbaru​
    if not received_hash:​
        return None​
​
    auth_date = int(parsed.get("auth_date", 0))​
    if abs(int(time.time()) - auth_date) > max_age_sec:​
        return None​
​
    if REPLAY_GUARD.is_replayed_or_register(received_hash):​
        return None​
​
    data_check_string = "\n".join(f"{k}={v}" for k, v in 
sorted(parsed.items()))​
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), 
hashlib.sha256).digest()​
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), 
hashlib.sha256).hexdigest()​
​
    if not hmac.compare_digest(calculated_hash, received_hash):​
        return None​
    return parsed​



<!-- [ID:22_HITL_ACTION_S021] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: DIGEST_HEX -->
## Halaman 43

                self.cache.popitem(last=False)​
            else:​
                break​
        if digest_hex in self.cache:​
            return True​
        if len(self.cache) >= self.max_size:​
            self.cache.popitem(last=False)​
        self.cache[digest_hex] = now​
        return False​
​
REPLAY_GUARD = BoundedReplayGuard()​
​
def verify_telegram_webapp_initdata(​
    init_data_raw: str, bot_token: str, max_age_sec: int = 60​
) -> dict | None:​
    parsed = dict(parse_qsl(init_data_raw, keep_blank_values=True))​
    received_hash = parsed.pop("hash", None)​
    parsed.pop("signature", None)  # Wajib dikecualikan sesuai standar 
protokol terbaru Telegram​
    if not received_hash:​
        return None​
​
    auth_date = int(parsed.get("auth_date", 0))​
    if abs(int(time.time()) - auth_date) > max_age_sec:​
        return None​
​
    if REPLAY_GUARD.is_replayed_or_register(received_hash):​
        return None​
​
    data_check_string = "\n".join(f"{k}={v}" for k, v in 
sorted(parsed.items()))​
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), 
hashlib.sha256).digest()​
    calculated_hash = hmac.new(​
        secret_key, data_check_string.encode(), hashlib.sha256​
    ).hexdigest()​
​
    if not hmac.compare_digest(calculated_hash, received_hash):​
        return None​
    return parsed​
​
​
# 
=====================================================================​

<!-- [ID:22_HITL_ACTION_S022] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 5 Kategori Operasi Wajib Human Approval Gate (Sesuai Master Contract D2)
MANDATORY_HUMAN_APPROVAL_ACTIONS = (
   "DATA_MIGRATION",
   "PRICE_PLAN_CHANGE",
   "DELETE_FEATURE_PLUGIN",
   "WITHDRAW_ABOVE_THRESHOLD",
   "SECURITY_POLICY_CHANGE",
)
class HumanApprovalGate:
   """
   Human Approval Gate Eksplisit di Level Kode:
   Menahan eksekusi otomatis untuk 5 operasi sensitif sampai disetujui oleh Owner.
   """



<!-- [ID:22_HITL_ACTION_S023] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: DIGEST_HEX -->
## Halaman 642

                self.cache.popitem(last=False)​
            else:​
                break​
        if digest_hex in self.cache:​
            return True​
        if len(self.cache) >= self.max_size:​
            self.cache.popitem(last=False)​
        self.cache[digest_hex] = now​
        return False​
​
REPLAY_GUARD = BoundedReplayGuard()​
​
def verify_telegram_webapp_initdata(​
    init_data_raw: str, bot_token: str, max_age_sec: int = 60​
) -> dict | None:​
    parsed = dict(parse_qsl(init_data_raw, keep_blank_values=True))​
    received_hash = parsed.pop("hash", None)​
    parsed.pop("signature", None)  # Wajib dikecualikan sesuai standar 
protokol terbaru Telegram​
    if not received_hash:​
        return None​
​
    auth_date = int(parsed.get("auth_date", 0))​
    if abs(int(time.time()) - auth_date) > max_age_sec:​
        return None​
​
    if REPLAY_GUARD.is_replayed_or_register(received_hash):​
        return None​
​
    data_check_string = "\n".join(f"{k}={v}" for k, v in 
sorted(parsed.items()))​
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), 
hashlib.sha256).digest()​
    calculated_hash = hmac.new(​
        secret_key, data_check_string.encode(), hashlib.sha256​
    ).hexdigest()​
​
    if not hmac.compare_digest(calculated_hash, received_hash):​
        return None​
    return parsed​
​
​
# 
=====================================================================​

<!-- [ID:22_HITL_ACTION_S024] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER -->
## Halaman 16

sistem menghentikan retry berisiko, mengarantina komponen, mencatat insiden ke tabel 
human_escalation_queue, dan mengirim notifikasi darurat ke DM Owner. 
3.​ [FAKTA] [Bersumber] Human Approval Gate Eksplisit di Kode (HumanApprovalGate): 
○​ Menambahkan tabel pending_human_approvals dan fungsi pengunci di level kode untuk 5 aksi 
wajib persetujuan Owner: 
1.​ DATA_MIGRATION (migrasi skema/ekspor database). 
2.​ PRICE_PLAN_CHANGE (perubahan tarif koin/paket PPP). 
3.​ DELETE_FEATURE_PLUGIN (penghapusan/penonaktifan plugin atau fitur). 
4.​ WITHDRAW_ABOVE_THRESHOLD (penarikan/harvest laba bersih di atas ambang batas 
HARVEST_APPROVAL_THRESHOLD_IDR). 
5.​ SECURITY_POLICY_CHANGE (perubahan mode produksi, whitelist AST, atau penguncian 
Owner). 
○​ Setiap aksi di atas menghasilkan tiket persetujuan dengan tombol [✅ Setujui Eksekusi] dan [❌ 
Batalkan] di DM Owner. 
4.​ [FAKTA] [Bersumber] Penambalan Penuh VULN-01 s.d. VULN-08 & Ekosistem Sumber Daya: 
○​ Staggered Speculative Hedging (τ=1,2s) + RouteLLM Complexity Scorer (τ=0,11593): 
Menembak penyedia primer tercepat pada t=0 dan hanya memicu gelombang cadangan jika 
belum ada respons dalam 1,2 detik, ditambah dukungan rute Chutes AI (Bittensor Serverless), 
Groq, Cerebras, OpenRouter, Gemini 2.5/3.8 Flash, Pollinations, serta Puter.js Client Bridge di 
Web Studio. 
○​ Blinded Ed25519 Voucher + Atomic Escrow Burn: Menghapus user_id dari payload JSON 
voucher (diganti komitmen hash buta Hblind​) dan memotong koin secara atomik. 
○​ Bittensor Subnet 27 & ModelScan/Safetensors Gate: Menyediakan adaptor kesiapan node 
Bittensor Compute (rumus skor Stotal​=SGPU​+Balloc​ dengan timeout, retry, dan circuit breaker) serta 
pemindai ekstensi bobot model (.safetensors / .gguf & integrasi CLI modelscan) di panel 
/bansos & /admin. 
 
D3. RENCANA BERTAHAP (Kriteria Sukses & Rollback Trigger) 
 
1.​ Fase 1 — Rekonstruksi Sintaksis Bersih, Fondasi SQLite Singleton WAL & Human Approval Gate: 
○​ Target: Membersihkan seluruh artefak OCR dari kode v3.7.0, menambahkan tabel 
pending_human_approvals & human_escalation_queue, menerapkan koneksi SQLite WAL 
terkelola, serta mengunci is_verified_owner_dm (Fail-Closed + Bootstrap Token) dan 
HumanApprovalGate. 
○​ Kriteria Sukses: python3 -m py_compile app.py menghasilkan exit code 0 (0 syntax error) dan 
pemeriksaan skema database menciptakan 13 tabel utuh. 
○​ Rollback Trigger: Kegagalan kompilasi AST atau kegagalan transaksi 
SingleWriterSQLiteDaemon. 
2.​ Fase 2 — Integrasi Plugin Surface, Self-Healing Loop (Max 3x Retry → Escalate), Staggered 
Router & Bittensor/ModelScan Adapter: 
○​ Target: Memasang PluginRegistry (register, health, hot_swap), SelfHealingOrchestrator, 
Two-Tier Staggered Hedging (τ=1,2s), RouteLLM Matrix Classifier, 4-Gate Bansos Sterilizer, 
ModelScan/Safetensors Validator, dan Bittensor Compute Adapter. 
○​ Kriteria Sukses: Uji simulasi matikan dependency memicu tepat 3x percobaan perbaikan lalu 
otomatis masuk ke human_escalation_queue tanpa infinite loop; pemeriksaan 
sterilize_community_script_ast memblokir traversi dunder (__subclasses__, __import__) 100%. 
○​ Rollback Trigger: Retry melebihi 3x atau lolosnya atribut dunder pada pengujian AST. 



<!-- [ID:22_HITL_ACTION_S025] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER, CITE: 85 -->
## Halaman 24

●​ [FAKTA] [Bersumber] Seluruh kode v3.4.0 (App.py) dan v3.7.0 (audit update 1.pdf) tetap 
dipertahankan 100% tanpa ada fitur yang dihapus[cite: 37, 161, 191], dan diperluas dengan 10 
spesifikasi baru pada A4. 
D2. Arsitektur Target v4.0 (Modular, Suntik-Siap, & 3-Step UX) 
1.​ Lapisan Keamanan "Suntik" (HotPatchEngine + PluginRegistry + HumanApprovalGate): 
○​ app.py bertindak sebagai orchestrator tipis dengan PluginRegistry (register, health(), 
hot_swap()) dan perintah /suntik di DM /admin untuk menyuntikkan aturan keamanan, model 
baru, atau plugin tanpa restart. 
○​ HumanApprovalGate mengunci 5 operasi sensitif di kode: migrasi data, ubah harga/plan, 
hapus fitur/plugin, tarik saldo di atas threshold, dan ubah kebijakan keamanan. 
2.​ Interaksi 3-Langkah (3-Step Progressive Disclosure) & Auto-Bahasa (ID vs EN): 
○​ Deteksi otomatis language_code pengguna sejak detik pertama[cite: 72, 161]: 
■​ Langkah 1: Hanya menampilkan 3 Tombol Etalase Utama (1. Studio Visual/Video/Suara, 
2. Riset, Koding & Chat, 3. Dompet, Eceran/Sub, Afiliasi & API Mandiri) + peluncur Mini 
App[cite: 85]. 
■​ Langkah 2: Jika pengguna berbahasa Indonesia (id) mengklik kategori, muncul 
sub-menu rapi Preset Orang Awam (UMKM, Studio, Foto Jadi Video, Hapus BG). Untuk 
pengguna Global (en), antarmuka langsung menampilkan kontrol studio profesional yang 
bersih dalam bahasa Inggris. 
■​ Langkah 3: Eksekusi disertai Animasi Tunggu & Live Progress Bar (⏳ [25%]... → ⚡ 
[60%]... → ✨ [95%]...) + send_chat_action agar pengguna tahu persis proses berjalan 
lancar dan tidak mengira bot error. 
3.​ Auto-Grup Komunitas Lintas Negara (Ambang Batas ≥100 Pengguna): 
○​ Tabel geo_community_clusters mencatat jumlah pengguna per negara/bahasa. Saat suatu 
negara mencapai 100 pengguna, bot otomatis menyiapkan klaster/topik komunitas bahasa 
tersebut dan mengirim tombol aktivasi 1-klik ke Owner (lengkap dengan fitur /setup_grup 
otomatis 6 kamar topik dalam bahasa lokal mereka)[cite: 123, 185]. 
4.​ Self-Healing Loop & Router Cerdas (Combo Grading + Staggered Hedging 1.2s + 
Anti-Soft-Refusal): 
○​ Mengikuti alur: classify_error → pilih handler → apply_fix → verify → gagal 3x → escalate ke 
log + human_escalation_queue. 
○​ Menyediakan endpoint /v1/chat/completions dan /v1/images/generations dengan autentikasi 
sk-bikinai-... untuk melayani pasar vibecoders / pengguna mandiri. 
 
D3. Rencana Bertahap Revisi v4.0 (Kriteria Sukses & Rollback Trigger) 
 
1.​ Fase 1 — Fondasi 15 Tabel SQLite WAL, HotPatchEngine (/suntik), HumanApprovalGate, & 
SelfHealingOrchestrator: 
○​ Kriteria Sukses: python3 -m py_compile app.py lulus 100% (exit code 0), uji suntik aturan baru 
berhasil tanpa restart, dan simulasi matikan dependency berhenti tepat pada retry ke-3 lalu 
masuk ke human_escalation_queue[cite: 40, 191]. 
○​ Rollback Trigger: Kegagalan kompilasi AST atau kegagalan isolasi plugin[cite: 47, 191]. 
2.​ Fase 2 — Router Combo Grading, Staggered Hedging, Anti-Soft-Refusal, & 
AutonomousResourceHarvester (Auto-Test vs Owner Control): 
○​ Kriteria Sukses: Endpoint gratis diuji mandiri (<2,0s) sebelum masuk antrean aktif, sedangkan 



<!-- [ID:22_HITL_ACTION_S026] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER -->
## Halaman 130

sistem menghentikan retry berisiko, mengarantina komponen, mencatat insiden ke tabel 
human_escalation_queue, dan mengirim notifikasi darurat ke DM Owner. 
3.​ [FAKTA] [Bersumber] Human Approval Gate Eksplisit di Kode (HumanApprovalGate): 
○​ Menambahkan tabel pending_human_approvals dan fungsi pengunci di level kode untuk 5 aksi 
wajib persetujuan Owner: 
1.​ DATA_MIGRATION (migrasi skema/ekspor database). 
2.​ PRICE_PLAN_CHANGE (perubahan tarif koin/paket PPP). 
3.​ DELETE_FEATURE_PLUGIN (penghapusan/penonaktifan plugin atau fitur). 
4.​ WITHDRAW_ABOVE_THRESHOLD (penarikan/harvest laba bersih di atas ambang batas 
HARVEST_APPROVAL_THRESHOLD_IDR). 
5.​ SECURITY_POLICY_CHANGE (perubahan mode produksi, whitelist AST, atau penguncian 
Owner). 
○​ Setiap aksi di atas menghasilkan tiket persetujuan dengan tombol [✅ Setujui Eksekusi] dan [❌ 
Batalkan] di DM Owner. 
4.​ [FAKTA] [Bersumber] Penambalan Penuh VULN-01 s.d. VULN-08 & Ekosistem Sumber Daya: 
○​ Staggered Speculative Hedging (τ=1,2s) + RouteLLM Complexity Scorer (τ=0,11593): 
Menembak penyedia primer tercepat pada t=0 dan hanya memicu gelombang cadangan jika 
belum ada respons dalam 1,2 detik, ditambah dukungan rute Chutes AI (Bittensor Serverless), 
Groq, Cerebras, OpenRouter, Gemini 2.5/3.8 Flash, Pollinations, serta Puter.js Client Bridge di 
Web Studio. 
○​ Blinded Ed25519 Voucher + Atomic Escrow Burn: Menghapus user_id dari payload JSON 
voucher (diganti komitmen hash buta Hblind​) dan memotong koin secara atomik. 
○​ Bittensor Subnet 27 & ModelScan/Safetensors Gate: Menyediakan adaptor kesiapan node 
Bittensor Compute (rumus skor Stotal​=SGPU​+Balloc​ dengan timeout, retry, dan circuit breaker) serta 
pemindai ekstensi bobot model (.safetensors / .gguf & integrasi CLI modelscan) di panel 
/bansos & /admin. 
 
D3. RENCANA BERTAHAP (Kriteria Sukses & Rollback Trigger) 
 
1.​ Fase 1 — Rekonstruksi Sintaksis Bersih, Fondasi SQLite Singleton WAL & Human Approval Gate: 
○​ Target: Membersihkan seluruh artefak OCR dari kode v3.7.0, menambahkan tabel 
pending_human_approvals & human_escalation_queue, menerapkan koneksi SQLite WAL 
terkelola, serta mengunci is_verified_owner_dm (Fail-Closed + Bootstrap Token) dan 
HumanApprovalGate. 
○​ Kriteria Sukses: python3 -m py_compile app.py menghasilkan exit code 0 (0 syntax error) dan 
pemeriksaan skema database menciptakan 13 tabel utuh. 
○​ Rollback Trigger: Kegagalan kompilasi AST atau kegagalan transaksi 
SingleWriterSQLiteDaemon. 
2.​ Fase 2 — Integrasi Plugin Surface, Self-Healing Loop (Max 3x Retry → Escalate), Staggered 
Router & Bittensor/ModelScan Adapter: 
○​ Target: Memasang PluginRegistry (register, health, hot_swap), SelfHealingOrchestrator, 
Two-Tier Staggered Hedging (τ=1,2s), RouteLLM Matrix Classifier, 4-Gate Bansos Sterilizer, 
ModelScan/Safetensors Validator, dan Bittensor Compute Adapter. 
○​ Kriteria Sukses: Uji simulasi matikan dependency memicu tepat 3x percobaan perbaikan lalu 
otomatis masuk ke human_escalation_queue tanpa infinite loop; pemeriksaan 
sterilize_community_script_ast memblokir traversi dunder (__subclasses__, __import__) 100%. 
○​ Rollback Trigger: Retry melebihi 3x atau lolosnya atribut dunder pada pengujian AST. 



<!-- [ID:22_HITL_ACTION_S027] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER, CITE: 85 -->
## Halaman 138

●​ [FAKTA] [Bersumber] Seluruh kode v3.4.0 (App.py) dan v3.7.0 (audit update 1.pdf) tetap 
dipertahankan 100% tanpa ada fitur yang dihapus[cite: 37, 161, 191], dan diperluas dengan 10 
spesifikasi baru pada A4. 
D2. Arsitektur Target v4.0 (Modular, Suntik-Siap, & 3-Step UX) 
1.​ Lapisan Keamanan "Suntik" (HotPatchEngine + PluginRegistry + HumanApprovalGate): 
○​ app.py bertindak sebagai orchestrator tipis dengan PluginRegistry (register, health(), 
hot_swap()) dan perintah /suntik di DM /admin untuk menyuntikkan aturan keamanan, model 
baru, atau plugin tanpa restart. 
○​ HumanApprovalGate mengunci 5 operasi sensitif di kode: migrasi data, ubah harga/plan, 
hapus fitur/plugin, tarik saldo di atas threshold, dan ubah kebijakan keamanan. 
2.​ Interaksi 3-Langkah (3-Step Progressive Disclosure) & Auto-Bahasa (ID vs EN): 
○​ Deteksi otomatis language_code pengguna sejak detik pertama[cite: 72, 161]: 
■​ Langkah 1: Hanya menampilkan 3 Tombol Etalase Utama (1. Studio Visual/Video/Suara, 
2. Riset, Koding & Chat, 3. Dompet, Eceran/Sub, Afiliasi & API Mandiri) + peluncur Mini 
App[cite: 85]. 
■​ Langkah 2: Jika pengguna berbahasa Indonesia (id) mengklik kategori, muncul 
sub-menu rapi Preset Orang Awam (UMKM, Studio, Foto Jadi Video, Hapus BG). Untuk 
pengguna Global (en), antarmuka langsung menampilkan kontrol studio profesional yang 
bersih dalam bahasa Inggris. 
■​ Langkah 3: Eksekusi disertai Animasi Tunggu & Live Progress Bar (⏳ [25%]... → ⚡ 
[60%]... → ✨ [95%]...) + send_chat_action agar pengguna tahu persis proses berjalan 
lancar dan tidak mengira bot error. 
3.​ Auto-Grup Komunitas Lintas Negara (Ambang Batas ≥100 Pengguna): 
○​ Tabel geo_community_clusters mencatat jumlah pengguna per negara/bahasa. Saat suatu 
negara mencapai 100 pengguna, bot otomatis menyiapkan klaster/topik komunitas bahasa 
tersebut dan mengirim tombol aktivasi 1-klik ke Owner (lengkap dengan fitur /setup_grup 
otomatis 6 kamar topik dalam bahasa lokal mereka)[cite: 123, 185]. 
4.​ Self-Healing Loop & Router Cerdas (Combo Grading + Staggered Hedging 1.2s + 
Anti-Soft-Refusal): 
○​ Mengikuti alur: classify_error → pilih handler → apply_fix → verify → gagal 3x → escalate ke 
log + human_escalation_queue. 
○​ Menyediakan endpoint /v1/chat/completions dan /v1/images/generations dengan autentikasi 
sk-bikinai-... untuk melayani pasar vibecoders / pengguna mandiri. 
 
D3. Rencana Bertahap Revisi v4.0 (Kriteria Sukses & Rollback Trigger) 
 
1.​ Fase 1 — Fondasi 15 Tabel SQLite WAL, HotPatchEngine (/suntik), HumanApprovalGate, & 
SelfHealingOrchestrator: 
○​ Kriteria Sukses: python3 -m py_compile app.py lulus 100% (exit code 0), uji suntik aturan baru 
berhasil tanpa restart, dan simulasi matikan dependency berhenti tepat pada retry ke-3 lalu 
masuk ke human_escalation_queue[cite: 40, 191]. 
○​ Rollback Trigger: Kegagalan kompilasi AST atau kegagalan isolasi plugin[cite: 47, 191]. 
2.​ Fase 2 — Router Combo Grading, Staggered Hedging, Anti-Soft-Refusal, & 
AutonomousResourceHarvester (Auto-Test vs Owner Control): 
○​ Kriteria Sukses: Endpoint gratis diuji mandiri (<2,0s) sebelum masuk antrean aktif, sedangkan 



<!-- [ID:22_HITL_ACTION_S028] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_18, SPAN_19, SPAN_23 -->
## Halaman 231

terlampaui. | | 15 | pending_approvals | approval_id, action_type, summary, payload_json, 
statu[span_18](start_span)[span_18](end_span)s, created_at | Mengunci 5 kategori tindakan 
kritis hingga mendapatkan persetujuan eksplisit pemilik. | | 16 | social_autopost_queue | post_id, 
track_type, platform, caption_text, media[span_19](start_span)[span_19](end_span)_ref, 
affiliate_url, status, created_at | Mengelola antrean publikasi otomatis ke TikTok dan Shopee 
dengan pemisahan jalur promosi. | 
Orkestrator Tipis, 6-Gate Zero-Trust Sterilizer, dan 
Loop Pemulihan Mandiri 
Desain arsitektural V4.0.txt memisahkan logika inti dari permukaan ekstensi melalui 
PluginRegistry yang mendukung pendaftaran mandiri (register), pemeriksaan kesehatan 
berkala (check_all_health), serta penggantian modul secara langsung saat sistem berjalan 
(hot_swap_plugin) melalui perintah /suntik. Karena kemampuan injeksi kode dinamis dan 
integrasi sumber daya komunitas membawa risiko eksekusi kode jarak jauh (Remote Code 
Execution) maupun pemalsuan permintaan sisi server (Server-Side Request Forgery), setiap 
muatan eksternal wajib melewati pipa penyaringan berlapis 6-Gate Zero-Trust Sterilizer secara 
berurutan sebelum diizinkan berinteraksi dengan memori utama maupun basis data. 
Gerbang pertama (AntiSSRFValidator) mengurai nama host tujuan menjadi alamat IP melalui 
resolusi DNS dan memblokir seluruh rentang jaringan privat, loopback, serta link-local baik 
pada IPv4 (127.0.0.0/8, 10.0.0.0/8, 100.64.0.0/10, 169.254.0.0/16, 172.16.0.0/12, 
192.168.0.0/16) maupun IPv6 (::1/128, fc00::/7, fe80::/10). Gerbang kedua 
(WhitelistASTSterilizer v4.0) membedah pohon sintaks abstrak dari setiap kode plugin yang 
disuntikkan untuk memblokir akses atribut dunder berbahaya (__subclasses__, __globals__, 
__builtins__, __class__, __bases__, __mro__, __code__), pemanggilan fungsi eksekusi (eval, 
exec, compile, __import__, open), serta modul sistem (os, subprocess, sys, shutil, socket, pty). 
Gerbang ketiga (PayloadMalwareScrubber) memverifikasi magic bytes biner untuk memastikan 
kesesuaian header berkas media (PNG, JPEG, WEBP, MP4, PDF, MP3) dan menolak berkas 
eksekusi (MZ, \x7fELF, #!). 
Selanjutnya, gerbang keempat (LivePingChecker) mewajibkan uji koneksi soket TCP asinkron 
dengan batas waktu ketat di bawah 2,5 detik sebelum sebuah titik akhir diaktifkan di 
omni_resource_registry. Gerbang kelima (ProtectAIModelScanEnforcer) melindungi pipeline 
inferensi dari serangan deserialisasi bobot model dengan hanya mengizinkan format 
.safetensors dan .gguf (disertai pemeriksaan header biner GGUF), serta memblokir secara 
mutlak ekstensi berbasis Pickle/PyTorch (.pkl, .pt, .bin, .pickle, .pth, .ckpt). Gerbang keenam 
(AdaptiveThreatMemory) mengekstraksi pola serangan yang terdeteksi menjadi ekspresi 
reguler otomatis di tabel adaptive_t[span_23](start_span)[span_23](end_span)hreat_rules, 
sehingga sistem memiliki kekebalan adaptif terhadap variasi serangan serupa di masa 
mendatang. 
Pada saat eksekusi berjalan, SelfHealingOrchestrator mengawasi setiap komponen melalui 
siklus klasifikasi kesalahan (NETWORK_TIMEOUT, RATE_LIMIT, DB_CONCURRENCY, 
AUTH_FAILURE, GENERAL_FAULT), pemilihan penangan, penerapan jeda eksponensial, dan 
verifikasi ulang. Apabila suatu tugas masih gagal setelah tiga kali percobaan berturut-turut, 
orkestrator menghentikan percobaan ulang yang berisiko menghabiskan kuota, mencatat 
insiden ke dalam human_escalation_queue, dan mengirimkan peringatan ke ruang pesan 
pemilik. Di samping itu, kelas HumanApprovalGate mengunci lima kategori tindakan kritis di 
tingkat kode—meliputi DATA_MIGRATION, PRICE_PLAN_CHANGE, 


