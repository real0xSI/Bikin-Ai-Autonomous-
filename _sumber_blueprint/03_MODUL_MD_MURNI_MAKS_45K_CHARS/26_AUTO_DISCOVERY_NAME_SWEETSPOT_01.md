
<!-- [ID:26_AUTO_DISCOVERY_NAME_S001] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: NAME -->
# ==============================================================================
@dataclass
class RegisteredPlugin:
   name: str
   version: str
   ast_hash: str
   handler: Callable[..., Coroutine[Any, Any, Any]]
   health_check: Callable[[], Coroutine[Any, Any, bool]]
   active: bool = True
   updated_at: int = field(default_factory=lambda: int(time.time()))
class PluginRegistry:
   """
   Plugin Surface Level Orchestrator:
   Mendukung self-registration, pemeriksaan health(), dan Hot-Swap tanpa restart.
   """
   def __init__(self) -> None:
       self._plugins: dict[str, RegisteredPlugin] = {}
   def register(
       self,
       name: str,
       version: str,
       handler: Callable[..., Coroutine[Any, Any, Any]],
       health_check: Callable[[], Coroutine[Any, Any, bool]] | None = None,
       ast_hash: str = "builtin_verified",
   ) -> None:
       async def _default_health() -> bool:
           return True
       self._plugins[name] = RegisteredPlugin(
           name=name,
           version=version,
           ast_hash=ast_hash,
           handler=handler,
           health_check=health_check or _default_health,
           active=True,
       )


