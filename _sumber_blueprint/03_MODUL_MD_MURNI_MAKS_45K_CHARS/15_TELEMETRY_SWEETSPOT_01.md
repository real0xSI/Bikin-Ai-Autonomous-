
<!-- [ID:15_TELEMETRY_S001] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: NAME, STR -->
## Halaman 385

   async def check_all_health(self) -> dict[str, dict[str, Any]]:
       report: dict[str, dict[str, Any]] = {}
       for name, plug in self._plugins.items():
           if not plug.active:
               report[name] = {
                   "ok": False,
                   "version": plug.version,
                   "status": "DISABLED",
               }
               continue
           try:
               ok = await asyncio.wait_for(plug.health_check(), timeout=2.5)
               report[name] = {
                   "ok": bool(ok),
                   "version": plug.version,
                   "hash": plug.ast_hash,
                   "status": "HEALTHY" if ok else "DEGRADED",
               }
           except Exception as e:
               report[name] = {
                   "ok": False,
                   "version": plug.version,
                   "hash": plug.ast_hash,
                   "status": f"ERROR ({type(e).__name__})",
               }
       return report
   def hot_swap_plugin(
       self, name: str, new_version: str, source_code: str
   ) -> dict[str, Any]:
       """Menyuntikkan / mengganti plugin secara live setelah lulus 6-Gate AST Sterilizer."""
       audit = sterilize_community_script_ast(source_code, script_name=name)
       if not audit["ok"]:
           return {
               "ok": False,
               "reason": f"Ditolak oleh AST Sterilizer: {audit['threats_removed']}",
               "hash": audit["hash"],
           }
       async def _swapped_handler(*args: Any, **kwargs: Any) -> dict[str, Any]:
           return {
               "ok": True,
               "plugin": name,
               "version": new_version,
               "hash": audit["hash"],
           }
       self.register(
           name=name,
           version=new_version,
           handler=_swapped_handler,
           ast_hash=audit["hash"],
       )
       return {
           "ok": True,
           "plugin": name,
           "version": new_version,
           "hash": audit["hash"],
       }
PLUGIN_SURFACE = PluginRegistry()
class AutonomicConvergenceGuard:
   """Anti-Infinite-Loop Guard, Telemetry Window & Shadow-Branch GitOps Controller."""
   def __init__(self) -> None:
       self.verified_ast_hashes: set[str] = set()
       self.incident_remediation_count: dict[str, int] = {}
       self.telemetry_window: deque[tuple[int, str, bool]] = deque(maxlen=80)
   def record_telemetry(self, component: str, success: bool) -> None:
       self.telemetry_window.append((int(time.time()), component, success))



<!-- [ID:15_TELEMETRY_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# LOGGING & RUNTIME CONFIGURATION
