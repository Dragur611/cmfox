# src/application/use_cases/initialize_interactive_session.py
from src.domain.ports import IConfigReaderPort, IBrowserPort
import logging

class InitializeInteractiveSession:
    def __init__(self, config_port: IConfigReaderPort, browser_port: IBrowserPort):
        self._config_port = config_port
        self._browser_port = browser_port
        self._logger = logging.getLogger(__name__)

    def execute(self) -> None:
        self._logger.info("Iniciando la lectura del perfil de configuración...")
        profile = self._config_port.retrieve_profile()
        
        valid_os = ["macos", "windows", "linux"]
        if profile.simulated_os not in valid_os:
            raise ValueError(f"El SO simulado '{profile.simulated_os}' es inválido. "
                             f"Valores permitidos: {valid_os}")
        
        self._logger.info(f"Perfil validado. Sistema Operativo a simular: {profile.simulated_os}")
        self._logger.info("Delegando inicialización al adaptador del navegador.")
        
        # Ejecuta la instanciación y mantiene la sesión abierta
        self._browser_port.launch_and_hold(profile)