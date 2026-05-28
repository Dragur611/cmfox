# main.py
import logging
from dotenv import load_dotenv
from src.infrastructure.adapters.env_config_adapter import EnvConfigAdapter
from src.infrastructure.adapters.camoufox_browser_adapter import CamoufoxBrowserAdapter
from src.application.use_cases.initialize_interactive_session import InitializeInteractiveSession

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    
    # Carga explícita de variables externas (Requerimiento 2)
    load_dotenv()
    
    # Instanciación de Adaptadores (Infraestructura)
    config_adapter = EnvConfigAdapter()
    browser_adapter = CamoufoxBrowserAdapter()
    
    # Inyección de dependencias en el Caso de Uso (Aplicación)
    use_case = InitializeInteractiveSession(
        config_port=config_adapter,
        browser_port=browser_adapter
    )
    
    # Ejecución
    use_case.execute()

if __name__ == "__main__":
    main()