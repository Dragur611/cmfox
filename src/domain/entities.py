# src/domain/entities.py
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class BrowserProfile:
    """
    Entidad fundamental que representa los requerimientos
    de coherencia para la identidad de un navegador aislado.
    """
    simulated_os: str                 # 'macos', 'windows', o 'linux'
    proxy_url: Optional[str]          # URL del proxy para evasión IP
    enable_geoip: bool                # Automatiza la resolución de zona horaria y locales
    interactive_mode: bool            # Indica si se expondrá la GUI (HITL)
    custom_fonts: List[str]           # Lista de fuentes autorizadas para eludir el canvas
    block_webrtc: bool                # Prevención absoluta de fugas de IP real