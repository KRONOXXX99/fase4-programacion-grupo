"""Clase abstracta general para las entidades del sistema."""

from abc import ABC, abstractmethod


class EntidadSistema(ABC):
    """Representa una entidad general dentro del sistema Software FJ."""

    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self) -> str:
        """Devuelve el identificador de la entidad."""
        return self._identificador

    @abstractmethod
    def mostrar_info(self) -> str:
        """Obliga a las clases hijas a mostrar su informacion principal."""
        raise NotImplementedError
