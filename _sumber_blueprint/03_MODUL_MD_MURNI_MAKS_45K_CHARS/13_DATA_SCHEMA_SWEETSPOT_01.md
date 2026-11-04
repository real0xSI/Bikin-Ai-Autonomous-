
<!-- [ID:13_DATA_SCHEMA_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# ==============================================================================
class SingleWriterSQLiteDaemon:
    """
    Single-Writer SQLite WAL Daemon untuk menjamin bebas `database is locked`
    di bawah beban konkurensi tinggi, dilengkapi antrean tulis sekuensial
    dan koneksi baca terpisah.
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self._write_lock: Optional[asyncio.Lock] = None
        self._conn: Optional[sqlite3.Connection] = None
        self._initialized: bool = False

    def _get_lock(self) -> asyncio.Lock:
        if self._write_lock is None:
            self._write_lock = asyncio.Lock()
        return self._write_lock

    def connect_sync(self) -> sqlite3.Connection:
        if self._conn is None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self.db_path), timeout=30.0, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            try:
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute("CREATE TABLE IF NOT EXISTS _wal_probe (id INT);")
            except sqlite3.OperationalError:
                conn.close()
                fallback_dir = Path("/tmp/.bikinai_vault")
                fallback_dir.mkdir(parents=True, exist_ok=True)
                self.db_path = fallback_dir / "bikinai_master_vault.db"
                conn = sqlite3.connect(str(self.db_path), timeout=30.0, check_same_thread=False)
                conn.row_factory = sqlite3.Row
                conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA foreign_keys=ON;")
            conn.execute("PRAGMA busy_timeout=15000;")
            conn.execute("PRAGMA temp_store=MEMORY;")
            self._conn = conn
        assert self._conn is not None
        return self._conn

    def init_schema_sync(self) -> None:
        conn = self.connect_sync()
        now_ts = int(time.time())
        schema_statements = [
            # (1) users
            """
            CREATE TABLE IF NOT EXISTS users (
                internal_user_id INTEGER PRIMARY KEY,
                username TEXT DEFAULT '',
                first_name TEXT DEFAULT '',
                language_code TEXT DEFAULT 'id',
                koin_utama INTEGER DEFAULT 0 CHECK(koin_utama >= 0),
                koin_bonus INTEGER DEFAULT 15 CHECK(koin_bonus >= 0 AND koin_bonus <= 25),
                has_topped_up INTEGER DEFAULT 0,
                ppp_zone INTEGER DEFAULT 4,
                last_claim_date TEXT DEFAULT '',
                chat_used_today INTEGER DEFAULT 0,
                free_img_used_today INTEGER DEFAULT 0,
                quota_day_epoch INTEGER DEFAULT 0,
                personal_memory_notes TEXT DEFAULT '',
                active_canvas_content TEXT DEFAULT '',
                referred_by INTEGER DEFAULT 0,
                affiliate_stars_balance INTEGER DEFAULT 0,
                affiliate_idr_pending INTEGER DEFAULT 0,
                created_at INTEGER DEFAULT 0
            );
            """,
            # (2) identity_history
            """
            CREATE TABLE IF NOT EXISTS identity_history (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                old_username TEXT DEFAULT '',
                new_username TEXT DEFAULT '',
                changed_at INTEGER NOT NULL
            );
            """,
            # (3) jobs
            """
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                internal_user_id INTEGER NOT NULL,
                cost INTEGER NOT NULL DEFAULT 0,
                deducted_bonus INTEGER NOT NULL DEFAULT 0,
                deducted_utama INTEGER NOT NULL DEFAULT 0,
                is_watermarked INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'PENDING',
                refunded_lock INTEGER NOT NULL DEFAULT 0,
                prompt_text TEXT DEFAULT '',
                engine_used TEXT DEFAULT '',
                telegram_file_id TEXT DEFAULT '',
                created_at INTEGER NOT NULL
            );
            """,
            # (4) payment_invoices
            """
            CREATE TABLE IF NOT EXISTS payment_invoices (
                invoice_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                tier_key TEXT NOT NULL,
                amount_idr INTEGER NOT NULL,
                coins_credited INTEGER NOT NULL,
                provider TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                followup_sent INTEGER NOT NULL DEFAULT 0,
                created_at INTEGER NOT NULL
            );
            """,
            # (5) redeemed_nullifiers
            """
            CREATE TABLE IF NOT EXISTS redeemed_nullifiers (
                nullifier_hash TEXT PRIMARY KEY,
                expires_at INTEGER NOT NULL
            );
            """,
            # (6) treasury_summary
            """
            CREATE TABLE IF NOT EXISTS treasury_summary (
                id INTEGER PRIMARY KEY CHECK(id = 1),
                gross_revenue_idr INTEGER NOT NULL DEFAULT 0,
                working_capital_vault_idr INTEGER NOT NULL DEFAULT 0,
                harvestable_profit_vault_idr INTEGER NOT NULL DEFAULT 0,
                total_harvested_by_owner_idr INTEGER NOT NULL DEFAULT 0,
                total_jobs_completed INTEGER NOT NULL DEFAULT 0,
                updated_at INTEGER NOT NULL DEFAULT 0
            );
            """,
            # (7) bot_bindings
            """
            CREATE TABLE IF NOT EXISTS bot_bindings (
                binding_key TEXT PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                topic_id INTEGER NOT NULL DEFAULT 0,
                topic_title TEXT DEFAULT ''
            );
            """,
            # (8) system_settings
            """
            CREATE TABLE IF NOT EXISTS system_settings (
                setting_key TEXT PRIMARY KEY,
                setting_val TEXT NOT NULL DEFAULT ''
            );
            """,
            # (9) user_feedback
            """
            CREATE TABLE IF NOT EXISTS user_feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT DEFAULT '',
                feedback_text TEXT NOT NULL,
                created_at INTEGER NOT NULL
            );
            """,
            # (10) omni_resource_registry
            """
            CREATE TABLE IF NOT EXISTS omni_resource_registry (
                resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                resource_name TEXT NOT NULL,
                endpoint_url TEXT NOT NULL,
                secret_or_meta TEXT DEFAULT '',
                is_live_verified INTEGER NOT NULL DEFAULT 1,
                expires_at INTEGER NOT NULL DEFAULT 0
            );
            """,
            # (11) syndicated_assets
            """
            CREATE TABLE IF NOT EXISTS syndicated_assets (
                asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_signature TEXT UNIQUE NOT NULL,
                engine_name TEXT NOT NULL,
                media_url TEXT DEFAULT '',
                telegram_file_id TEXT DEFAULT '',
                times_reused INTEGER NOT NULL DEFAULT 0,
                created_at INTEGER NOT NULL
            );
            """,
            # (12) api_keys
            """
            CREATE TABLE IF NOT EXISTS api_keys (
                api_key TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                tier_name TEXT NOT NULL DEFAULT 'VIBE_CODER',
                token_quota_remaining INTEGER NOT NULL DEFAULT 500000,
                expires_at INTEGER NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at INTEGER NOT NULL
            );
            """,
            # (13) adaptive_threat_rules
            """
            CREATE TABLE IF NOT EXISTS adaptive_threat_rules (
                rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_regex TEXT UNIQUE NOT NULL,
                source_attack_sample TEXT DEFAULT '',
                hits_count INTEGER NOT NULL DEFAULT 1,
                created_at INTEGER NOT NULL
            );
            """,
            # (14) human_escalation_queue
            """
            CREATE TABLE IF NOT EXISTS human_escalation_queue (
                incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
                component TEXT NOT NULL,
                error_class TEXT NOT NULL,
                error_detail TEXT NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 3,
                status TEXT NOT NULL DEFAULT 'OPEN',
                created_at INTEGER NOT NULL
            );
            """,
            # (15) pending_approvals
            """
            CREATE TABLE IF NOT EXISTS pending_approvals (
                approval_id TEXT PRIMARY KEY,
                action_type TEXT NOT NULL,
                summary TEXT NOT NULL,
                payload_json TEXT NOT NULL DEFAULT '{}',
                status TEXT NOT NULL DEFAULT 'PENDING',
                created_at INTEGER NOT NULL
            );
            """,
            # (16) social_autopost_queue
            """
            CREATE TABLE IF NOT EXISTS social_autopost_queue (
                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_type TEXT NOT NULL,
                platform TEXT NOT NULL,
                caption_text TEXT NOT NULL,
                media_ref TEXT DEFAULT '',
                affiliate_url TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'QUEUED',
                created_at INTEGER NOT NULL
            );
            """,
        ]
        with conn:
            for stmt in schema_statements:
                conn.execute(stmt)
            conn.execute(
                """
                INSERT OR IGNORE INTO treasury_summary
                (id, gross_revenue_idr, working_capital_vault_idr, harvestable_profit_vault_idr,
                 total_harvested_by_owner_idr, total_jobs_completed, updated_at)
                VALUES (1, 0, 0, 0, 0, 0, ?);
                """,
                (now_ts,),
            )
            default_settings = {
                "owner_id": str(OWNER_ID_RUNTIME),
                "miniapp_url": f"{PUBLIC_WEB_BASE_URL}/",
                "freedom_portal_name": "NOCTURNE FREEDOM STUDIO v4.0",
                "bansos_mode": "NORMAL",
                "qris_universal_file_id": "",
                "qris_gopay_file_id": "",
                "qris_shopeepay_file_id": "",
                "qris_dana_file_id": "",
                "last_milestone_notified": "0",
                "security_policy_level": "STRICT_ZERO_TRUST_6GATE",
            }
            for k, v in default_settings.items():
                conn.execute(
                    "INSERT OR IGNORE INTO system_settings (setting_key, setting_val) VALUES (?, ?);",
                    (k, v),
                )
        self._initialized = True

    async def execute_write(self, sql: str, params: Tuple[Any, ...] = ()) -> int:
        if not self._initialized:
            self.init_schema_sync()
        async with self._get_lock():
            conn = self.connect_sync()
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            return cur.lastrowid or cur.rowcount

    async def execute_script_tx(self, operations: List[Tuple[str, Tuple[Any, ...]]]) -> None:
        if not self._initialized:
            self.init_schema_sync()
        async with self._get_lock():
            conn = self.connect_sync()
            with conn:
                for sql, params in operations:
                    conn.execute(sql, params)

    async def fetch_one(self, sql: str, params: Tuple[Any, ...] = ()) -> Optional[Dict[str, Any]]:
        if not self._initialized:
            self.init_schema_sync()
        conn = self.connect_sync()
        cur = conn.execute(sql, params)
        row = cur.fetchone()
        return dict(row) if row is not None else None

    async def fetch_all(self, sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        if not self._initialized:
            self.init_schema_sync()
        conn = self.connect_sync()
        cur = conn.execute(sql, params)
        return [dict(r) for r in cur.fetchall()]

    async def get_setting(self, key: str, default: str = "") -> str:
        row = await self.fetch_one(
            "SELECT setting_val FROM system_settings WHERE setting_key = ?;",
            (key,),
        )
        return str(row["setting_val"]) if row and row.get("setting_val") is not None else default

    async def set_setting(self, key: str, val: str) -> None:
        await self.execute_write(
            """
            INSERT INTO system_settings (setting_key, setting_val)
            VALUES (?, ?)
            ON CONFLICT(setting_key) DO UPDATE SET setting_val = excluded.setting_val;
            """,
            (str(key), str(val)),
        )


_DB_DAEMON_SINGLETON: Optional[SingleWriterSQLiteDaemon] = None


def get_db() -> SingleWriterSQLiteDaemon:
    """Mengembalikan instance tunggal SingleWriterSQLiteDaemon."""
    global _DB_DAEMON_SINGLETON
    if _DB_DAEMON_SINGLETON is None:
        _DB_DAEMON_SINGLETON = SingleWriterSQLiteDaemon(DB_PATH)
        _DB_DAEMON_SINGLETON.init_schema_sync()
    return _DB_DAEMON_SINGLETON



<!-- [ID:13_DATA_SCHEMA_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# 2. DATABASE SCHEMA (11 TABLES) & 3-TIER PPP MATRIX
MAX_KOIN_BONUS_CAP = 25
PPP_EFFECTIVE_COIN_IDR = {1: 580, 2: 260, 3: 84}

PPP_PRICING_PACKAGES = {
    "ID": {
        "HEMAT": {"name": "⚡ Paket Hemat Kreator", "idr": 5000, "coins": 60},
        "PRO": {"name": "🔥 Paket Studio Pro (+16% Bonus)", "idr": 25000, "coins": 350},
        "SULTAN": {"name": "👑 Paket Sultan / Executive VIP (+33% Bonus & Jalur Prioritas)", "idr": 250000, "coins": 4000},
    },
    "GLOBAL": {
        "HEMAT": {"name": "⚡ Starter Creator Pack", "usd": "$1.99", "stars": 110, "idr_eq": 31000, "coins": 60},
        "PRO": {"name": "🔥 Studio Pro Pack", "usd": "$9.99", "stars": 550, "idr_eq": 155000, "coins": 350},
        "SULTAN": {"name": "👑 Sovereign Executive VIP", "usd": "$49.99", "stars": 2750, "idr_eq": 775000, "coins": 2500},
    },
}


async def init_master_db(db: aiosqlite.Connection) -> None:
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            internal_user_id INTEGER PRIMARY KEY, username TEXT DEFAULT 'Kreator', first_name TEXT DEFAULT '',
            language_code TEXT DEFAULT 'id', koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),
            koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND koin_bonus <= 25),
            has_topped_up INTEGER NOT NULL DEFAULT 0, ppp_zone INTEGER NOT NULL DEFAULT 3, last_claim_date TEXT,
            chat_used_today INTEGER NOT NULL DEFAULT 0, free_img_used_today INTEGER NOT NULL DEFAULT 0,
            quota_day_epoch INTEGER NOT NULL DEFAULT 0, personal_memory_notes TEXT DEFAULT '',
            active_canvas_content TEXT DEFAULT '', created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS identity_history (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            old_username TEXT, new_username TEXT, changed_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY, internal_user_id INTEGER NOT NULL, cost INTEGER NOT NULL,
            deducted_bonus INTEGER NOT NULL DEFAULT 0, deducted_utama INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'PROCESSING', refunded_lock INTEGER NOT NULL DEFAULT 0,
            prompt_text TEXT DEFAULT '', engine_used TEXT DEFAULT '', created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS payment_invoices (
            invoice_id TEXT PRIMARY KEY, user_id INTEGER NOT NULL, amount_idr INTEGER NOT NULL,
            coins_credited INTEGER NOT NULL DEFAULT 60, provider TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING', created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS redeemed_nullifiers (nullifier_hash TEXT PRIMARY KEY, expires_at INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS treasury_summary (
            id INTEGER PRIMARY KEY CHECK (id = 1), gross_revenue_idr INTEGER NOT NULL DEFAULT 0,
            working_capital_vault_idr INTEGER NOT NULL DEFAULT 0, harvestable_profit_vault_idr INTEGER NOT NULL DEFAULT 0,
            total_harvested_by_owner_idr INTEGER NOT NULL DEFAULT 0, total_jobs_completed INTEGER NOT NULL DEFAULT 0,
            updated_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS bot_bindings (
            binding_key TEXT PRIMARY KEY, chat_id INTEGER NOT NULL, topic_id INTEGER NOT NULL DEFAULT 0, topic_title TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS system_settings (setting_key TEXT PRIMARY KEY, setting_val TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS user_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            username TEXT, feedback_text TEXT NOT NULL, created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS omni_resource_registry (
            resource_id TEXT PRIMARY KEY, category TEXT NOT NULL, resource_name TEXT NOT NULL,
            endpoint_url TEXT NOT NULL, secret_or_meta TEXT NOT NULL, is_live_verified INTEGER NOT NULL DEFAULT 0,
            expires_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS syndicated_assets (
            asset_id TEXT PRIMARY KEY, prompt_signature TEXT NOT NULL, engine_name TEXT NOT NULL,
            media_url TEXT NOT NULL, times_reused INTEGER NOT NULL DEFAULT 1, created_at INTEGER NOT NULL
        );
        """
    )
    await db.commit()
    cur = await db.execute("SELECT setting_key, setting_val FROM system_settings;")
    for k, v in await cur.fetchall():
        if k == "MINIAPP_URL" and v.startswith("https://"):
            RUNTIME_CONFIG["MINIAPP_URL"] = v
        elif k == "OWNER_ID_RUNTIME" and v.isdigit() and int(v) > 0:
            RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = int(v)
        elif k == "PILIHAN_MESIN_MEDIA" and v.isdigit():
            RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] = int(v)
        elif k in ("LAUNCH_PRODUCTION_MODE", "HAPPY_HOUR_MODE", "AUTO_APPROVE_SANDBOX_TOPUP"):
            RUNTIME_CONFIG[k] = v == "1"
        elif k in (
            "ID_ACTIVE_CATEGORY", "ID_ACTIVE_PROVIDER", "GLOBAL_ACTIVE_PROVIDER",
            "BANSOS_OPERATION_MODE", "PRIMARY_ROLLING_AGENT", "WEB_BRAND_NAME", "CUSTOM_WEB_DOMAIN",
        ):
            RUNTIME_CONFIG[k] = v


async def save_persistent_setting(db: aiosqlite.Connection, key: str, val: str) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("INSERT OR REPLACE INTO system_settings (setting_key, setting_val) VALUES (?, ?);", (key, str(val)))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def set_topic_binding(db: aiosqlite.Connection, key: str, chat_id: int, topic_id: int, title: str = "") -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("INSERT OR REPLACE INTO bot_bindings (binding_key, chat_id, topic_id, topic_title) VALUES (?, ?, ?, ?);", (key, chat_id, topic_id, title))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def get_topic_binding(db: aiosqlite.Connection, key: str) -> tuple[int, int] | None:
    cur = await db.execute("SELECT chat_id, topic_id FROM bot_bindings WHERE binding_key = ?;", (key,))
    row = await cur.fetchone()
    return (int(row[0]), int(row[1])) if row else None


async def get_all_topic_bindings(db: aiosqlite.Connection) -> dict[str, tuple[int, int, str]]:
    cur = await db.execute("SELECT binding_key, chat_id, topic_id, topic_title FROM bot_bindings;")
    return {r[0]: (int(r[1]), int(r[2]), str(r[3] or r[0])) for r in await cur.fetchall()}



<!-- [ID:13_DATA_SCHEMA_S003] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# 2. DATABASE SCHEMA ABADI v3.7.0 (11 TABEL MASTER & 3-TIER PPP MATRIX)
MAX_KOIN_BONUS_CAP = 25
PPP_EFFECTIVE_COIN_IDR = {1: 580, 2: 260, 3: 84}

PPP_PRICING_PACKAGES = {
    "ID": {
        "HEMAT": {"name": "⚡ Paket Hemat Kreator", "idr": 5000, "coins": 60},
        "PRO": {"name": "🔥 Paket Studio Pro (+16% Bonus)", "idr": 25000, "coins": 350},
        "SULTAN": {"name": "👑 Paket Sultan / Executive VIP (+33% Bonus & Jalur Prioritas)", "idr": 250000, "coins": 4000},
    },
    "GLOBAL": {
        "HEMAT": {"name": "⚡ Starter Creator Pack", "usd": "$1.99", "stars": 110, "idr_eq": 31000, "coins": 60},
        "PRO": {"name": "🔥 Studio Pro Pack", "usd": "$9.99", "stars": 550, "idr_eq": 155000, "coins": 350},
        "SULTAN": {"name": "👑 Sovereign Executive VIP", "usd": "$49.99", "stars": 2750, "idr_eq": 775000, "coins": 2500},
    },
}


async def init_master_db(db: aiosqlite.Connection) -> None:
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            internal_user_id INTEGER PRIMARY KEY, username TEXT DEFAULT 'Kreator', first_name TEXT DEFAULT '',
            language_code TEXT DEFAULT 'id', koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),
            koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND koin_bonus <= 25),
            has_topped_up INTEGER NOT NULL DEFAULT 0, ppp_zone INTEGER NOT NULL DEFAULT 3, last_claim_date TEXT,
            chat_used_today INTEGER NOT NULL DEFAULT 0, free_img_used_today INTEGER NOT NULL DEFAULT 0,
            quota_day_epoch INTEGER NOT NULL DEFAULT 0, personal_memory_notes TEXT DEFAULT '',
            active_canvas_content TEXT DEFAULT '', created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS identity_history (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            old_username TEXT, new_username TEXT, changed_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY, internal_user_id INTEGER NOT NULL, cost INTEGER NOT NULL,
            deducted_bonus INTEGER NOT NULL DEFAULT 0, deducted_utama INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'PROCESSING', refunded_lock INTEGER NOT NULL DEFAULT 0,
            prompt_text TEXT DEFAULT '', engine_used TEXT DEFAULT '', created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS payment_invoices (
            invoice_id TEXT PRIMARY KEY, user_id INTEGER NOT NULL, amount_idr INTEGER NOT NULL,
            coins_credited INTEGER NOT NULL DEFAULT 60, provider TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING', created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS redeemed_nullifiers (nullifier_hash TEXT PRIMARY KEY, expires_at INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS treasury_summary (
            id INTEGER PRIMARY KEY CHECK (id = 1), gross_revenue_idr INTEGER NOT NULL DEFAULT 0,
            working_capital_vault_idr INTEGER NOT NULL DEFAULT 0, harvestable_profit_vault_idr INTEGER NOT NULL DEFAULT 0,
            total_harvested_by_owner_idr INTEGER NOT NULL DEFAULT 0, total_jobs_completed INTEGER NOT NULL DEFAULT 0,
            updated_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS bot_bindings (
            binding_key TEXT PRIMARY KEY, chat_id INTEGER NOT NULL, topic_id INTEGER NOT NULL DEFAULT 0, topic_title TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS system_settings (setting_key TEXT PRIMARY KEY, setting_val TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS user_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            username TEXT, feedback_text TEXT NOT NULL, created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS omni_resource_registry (
            resource_id TEXT PRIMARY KEY, category TEXT NOT NULL, resource_name TEXT NOT NULL,
            endpoint_url TEXT NOT NULL, secret_or_meta TEXT NOT NULL, is_live_verified INTEGER NOT NULL DEFAULT 0,
            expires_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS syndicated_assets (
            asset_id TEXT PRIMARY KEY, prompt_signature TEXT NOT NULL, engine_name TEXT NOT NULL,
            media_url TEXT NOT NULL, times_reused INTEGER NOT NULL DEFAULT 1, created_at INTEGER NOT NULL
        );
        """
    )
    await db.commit()
    cur = await db.execute("SELECT setting_key, setting_val FROM system_settings;")
    for k, v in await cur.fetchall():
        if k == "MINIAPP_URL" and v.startswith("https://"):
            RUNTIME_CONFIG["MINIAPP_URL"] = v
        elif k == "OWNER_ID_RUNTIME" and v.isdigit() and int(v) > 0:
            RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = int(v)
        elif k == "PILIHAN_MESIN_MEDIA" and v.isdigit():
            RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] = int(v)
        elif k in ("LAUNCH_PRODUCTION_MODE", "HAPPY_HOUR_MODE", "AUTO_APPROVE_SANDBOX_TOPUP"):
            RUNTIME_CONFIG[k] = v == "1"
        elif k in (
            "ID_ACTIVE_CATEGORY", "ID_ACTIVE_PROVIDER", "GLOBAL_ACTIVE_PROVIDER",
            "BANSOS_OPERATION_MODE", "PRIMARY_ROLLING_AGENT", "WEB_BRAND_NAME", "CUSTOM_WEB_DOMAIN",
        ):
            RUNTIME_CONFIG[k] = v


async def save_persistent_setting(db: aiosqlite.Connection, key: str, val: str) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("INSERT OR REPLACE INTO system_settings (setting_key, setting_val) VALUES (?, ?);", (key, str(val)))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def set_topic_binding(db: aiosqlite.Connection, key: str, chat_id: int, topic_id: int, title: str = "") -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("INSERT OR REPLACE INTO bot_bindings (binding_key, chat_id, topic_id, topic_title) VALUES (?, ?, ?, ?);", (key, chat_id, topic_id, title))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def get_topic_binding(db: aiosqlite.Connection, key: str) -> tuple[int, int] | None:
    cur = await db.execute("SELECT chat_id, topic_id FROM bot_bindings WHERE binding_key = ?;", (key,))
    row = await cur.fetchone()
    return (int(row[0]), int(row[1])) if row else None


async def get_all_topic_bindings(db: aiosqlite.Connection) -> dict[str, tuple[int, int, str]]:
    cur = await db.execute("SELECT binding_key, chat_id, topic_id, topic_title FROM bot_bindings;")
    return {r[0]: (int(r[1]), int(r[2]), str(r[3] or r[0])) for r in await cur.fetchall()}



<!-- [ID:13_DATA_SCHEMA_S004] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# ==============================================================================
MAX_KOIN_BONUS_CAP = 25
PPP_EFFECTIVE_COIN_IDR = {1: 580, 2: 260, 3: 84}


async def init_master_db(db: aiosqlite.Connection) -> None:
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            internal_user_id INTEGER PRIMARY KEY,
            username TEXT DEFAULT 'Kreator',
            first_name TEXT DEFAULT '',
            language_code TEXT DEFAULT 'id',
            koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),
            koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND koin_bonus <= 25),
            has_topped_up INTEGER NOT NULL DEFAULT 0,
            ppp_zone INTEGER NOT NULL DEFAULT 3,
            last_claim_date TEXT,
            chat_used_today INTEGER NOT NULL DEFAULT 0,
            free_img_used_today INTEGER NOT NULL DEFAULT 0,
            quota_day_epoch INTEGER NOT NULL DEFAULT 0,
            personal_memory_notes TEXT DEFAULT '',
            active_canvas_content TEXT DEFAULT '',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS identity_history (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            old_username TEXT,
            new_username TEXT,
            changed_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            internal_user_id INTEGER NOT NULL,
            cost INTEGER NOT NULL,
            deducted_bonus INTEGER NOT NULL DEFAULT 0,
            deducted_utama INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'PROCESSING',
            refunded_lock INTEGER NOT NULL DEFAULT 0,
            prompt_text TEXT DEFAULT '',
            engine_used TEXT DEFAULT '',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS payment_invoices (
            invoice_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount_idr INTEGER NOT NULL,
            coins_credited INTEGER NOT NULL DEFAULT 60,
            provider TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS redeemed_nullifiers (
            nullifier_hash TEXT PRIMARY KEY,
            expires_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS treasury_summary (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            gross_revenue_idr INTEGER NOT NULL DEFAULT 0,
            working_capital_vault_idr INTEGER NOT NULL DEFAULT 0,
            harvestable_profit_vault_idr INTEGER NOT NULL DEFAULT 0,
            total_harvested_by_owner_idr INTEGER NOT NULL DEFAULT 0,
            total_jobs_completed INTEGER NOT NULL DEFAULT 0,
            updated_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bot_bindings (
            binding_key TEXT PRIMARY KEY,
            chat_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL DEFAULT 0,
            topic_title TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS system_settings (
            setting_key TEXT PRIMARY KEY,
            setting_val TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            feedback_text TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS omni_resource_registry (
            resource_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            resource_name TEXT NOT NULL,
            endpoint_url TEXT NOT NULL,
            secret_or_meta TEXT NOT NULL,
            is_live_verified INTEGER NOT NULL DEFAULT 0,
            expires_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS syndicated_assets (
            asset_id TEXT PRIMARY KEY,
            prompt_signature TEXT NOT NULL,
            engine_name TEXT NOT NULL,
            media_url TEXT NOT NULL,
            times_reused INTEGER NOT NULL DEFAULT 1,
            created_at INTEGER NOT NULL
        );
        """
    )
    await db.commit()

    cur = await db.execute("SELECT setting_key, setting_val FROM system_settings;")
    for k, v in await cur.fetchall():
        if k == "MINIAPP_URL" and v.startswith("https://"):
            RUNTIME_CONFIG["MINIAPP_URL"] = v
        elif k == "OWNER_ID_RUNTIME" and v.isdigit() and int(v) > 0:
            RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = int(v)
        elif k == "PILIHAN_MESIN_MEDIA" and v.isdigit():
            RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] = int(v)
        elif k in ("LAUNCH_PRODUCTION_MODE", "HAPPY_HOUR_MODE", "AUTO_APPROVE_SANDBOX_TOPUP"):
            RUNTIME_CONFIG[k] = v == "1"
        elif k in (
            "ID_ACTIVE_CATEGORY",
            "ID_ACTIVE_PROVIDER",
            "GLOBAL_ACTIVE_PROVIDER",
            "BANSOS_OPERATION_MODE",
            "PRIMARY_ROLLING_AGENT",
        ):
            RUNTIME_CONFIG[k] = v


async def save_persistent_setting(db: aiosqlite.Connection, key: str, val: str) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            "INSERT OR REPLACE INTO system_settings (setting_key, setting_val) VALUES (?, ?);",
            (key, str(val)),
        )

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def set_topic_binding(
    db: aiosqlite.Connection, key: str, chat_id: int, topic_id: int, title: str = ""
) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            "INSERT OR REPLACE INTO bot_bindings (binding_key, chat_id, topic_id, topic_title) VALUES (?, ?, ?, ?);",
            (key, chat_id, topic_id, title),
        )

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def get_topic_binding(db: aiosqlite.Connection, key: str) -> tuple[int, int] | None:
    cur = await db.execute("SELECT chat_id, topic_id FROM bot_bindings WHERE binding_key = ?;", (key,))
    row = await cur.fetchone()
    return (int(row[0]), int(row[1])) if row else None


async def get_all_topic_bindings(db: aiosqlite.Connection) -> dict[str, tuple[int, int, str]]:
    cur = await db.execute("SELECT binding_key, chat_id, topic_id, topic_title FROM bot_bindings;")
    rows = await cur.fetchall()
    return {r[0]: (int(r[1]), int(r[2]), str(r[3] or r[0])) for r in rows}


