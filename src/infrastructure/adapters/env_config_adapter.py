# src/infrastructure/adapters/env_config_adapter.py
import os
from src.domain.ports import IConfigReaderPort
from src.domain.entities import BrowserProfile

class EnvConfigAdapter(IConfigReaderPort):
    def retrieve_profile(self) -> BrowserProfile:
        # Se asume que load_dotenv() se ejecuta en el punto de entrada (main.py)
        os_target = os.getenv("SIMULATED_OS", "linux").lower()
        
        # Mapeo estricto para asegurar la coherencia biométrica tipográfica 
        coherence_font_map = {
            "macos":[],
            "windows":[],
            "linux":[]
        }
        
        return BrowserProfile(
            simulated_os=os_target,
            proxy_url=os.getenv("PROXY_URL"),
            enable_geoip=os.getenv("ENABLE_GEOIP", "true").lower() == "true",
            interactive_mode=True, # Forzado en 'True' para Interacción Humana (Req 7)
            custom_fonts=coherence_font_map.get(os_target, coherence_font_map["linux"]),
            block_webrtc=os.getenv("BLOCK_WEBRTC", "true").lower() == "true"
        )