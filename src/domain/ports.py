# src/domain/ports.py
from abc import ABC, abstractmethod
from src.domain.entities import BrowserProfile

class IConfigReaderPort(ABC):
    """Puerto de entrada para la obtención de parámetros de configuración."""
    @abstractmethod
    def retrieve_profile(self) -> BrowserProfile:
        pass

class IBrowserPort(ABC):
    """Puerto de salida para el control del motor de renderizado antidetect."""
    @abstractmethod
    def launch_and_hold(self, profile: BrowserProfile) -> None:
        pass