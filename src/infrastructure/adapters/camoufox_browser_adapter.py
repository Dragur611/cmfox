# src/infrastructure/adapters/camoufox_browser_adapter.py
import time
import logging
from typing import Dict, Any
from camoufox.sync_api import Camoufox
from src.domain.ports import IBrowserPort
from src.domain.entities import BrowserProfile

class CamoufoxBrowserAdapter(IBrowserPort):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def launch_and_hold(self, profile: BrowserProfile) -> None:
        self._logger.info("Configurando motor antidetect Camoufox...")
        
        # Diccionario base de parámetros utilizando opciones nativas 
        launch_params: Dict[str, Any] = {
            # Desactiva el modo headless interno para aprovechar Xvfb del SO [4, 12]
            "headless": False, 
            
            # BrowserForge: Restringe la red probabilística al SO objetivo [4, 12]
            "os": profile.simulated_os,
            
            # Inyecta el arreglo de fuentes para evadir el Canvas Fingerprinting [6]
            "fonts": profile.custom_fonts,
            
            # GeoIP nativo: Ajusta locale, timezone y lat/long basados en la IP externa
            "geoip": profile.enable_geoip,
            
            # Motor C++: Falsificación de WebRTC a nivel de protocolo 
            "block_webrtc": profile.block_webrtc,
            
            # Movimiento natural del cursor portado de HumanCursor [4, 12]
            "humanize": True,
            
            # REQUERIMIENTO 6: No Persistencia absoluta 
            "persistent_context": False,
            "enable_cache": False
        }
        
        # Incorporación condicional de proxy residencial
        if profile.proxy_url:
            launch_params["proxy"] = {"server": profile.proxy_url}
            self._logger.info("Proxy inyectado exitosamente.")
            
        try:
            # Inicialización del navegador a través de Juggler 
            with Camoufox(**launch_params) as browser:
                self._logger.info("Navegador inicializado con éxito y huella rotada.")
                page = browser.new_page()
                
                # Navegar al portal de verificación interno para depuración inicial
                page.goto("https://camoufox.com/tests/webgl")
                
                self._logger.info("Sesión lista para interacción humana vía noVNC.")
                self._logger.info("El contenedor permanecerá abierto. (Ctrl+C para finalizar)")
                
                # REQUERIMIENTO 7: Mantener el proceso vivo para el operador
                while True:
                    time.sleep(30)
                    
        except KeyboardInterrupt:
            self._logger.info("Señal de interrupción recibida. Destruyendo contexto efímero...")
        except Exception as e:
            self._logger.error(f"Error crítico en la ejecución del navegador: {e}")
            raise