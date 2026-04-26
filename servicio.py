"""Servicios ofrecidos por Software FJ."""

from abc import abstractmethod
from entidad import EntidadSistema
from excepciones import ServicioError, ServicioNoDisponibleError, ValidacionError
from logger_sistema import registrar_evento


class Servicio(EntidadSistema):
    """Clase abstracta para servicios con polimorfismo."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(self._validar_texto(codigo, "codigo"))
        self._nombre = self._validar_texto(nombre, "nombre")
        self._tarifa_base = self._validar_numero_positivo(tarifa_base, "tarifa base")
        self._disponible = bool(disponible)

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValidacionError(f"El campo {campo} no puede estar vacio.")
        return valor.strip()

    @staticmethod
    def _validar_numero_positivo(valor: float, campo: str) -> float:
        try:
            numero = float(valor)
        except (TypeError, ValueError) as error:
            raise ValidacionError(f"El campo {campo} debe ser numerico.") from error
        if numero <= 0:
            raise ValidacionError(f"El campo {campo} debe ser mayor que cero.")
        return numero

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    def validar_disponibilidad(self) -> None:
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio {self.nombre} no esta disponible.")

    def cambiar_disponibilidad(self, disponible: bool) -> None:
        self._disponible = bool(disponible)
        registrar_evento("INFO", f"Disponibilidad actualizada para {self.nombre}: {self._disponible}")

    def calcular_costo_final(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Simula sobrecarga usando parametros opcionales de impuesto y descuento."""
        costo = self.calcular_costo(duracion)
        if impuesto < 0 or descuento < 0:
            raise ValidacionError("Impuesto y descuento no pueden ser negativos.")
        if descuento > costo:
            raise ValidacionError("El descuento no puede superar el costo base.")
        return round((costo - descuento) * (1 + impuesto), 2)

    @abstractmethod
    def calcular_costo(self, duracion: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def describir_servicio(self) -> str:
        raise NotImplementedError

    def mostrar_info(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Servicio[{self.identificador}] {self.nombre} - Tarifa: ${self.tarifa_base:,.0f} - {estado}"


class ReservaSala(Servicio):
    """Servicio de reserva de sala por horas."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self.capacidad = int(self._validar_numero_positivo(capacidad, "capacidad"))

    def calcular_costo(self, duracion: float) -> float:
        self.validar_disponibilidad()
        horas = self._validar_numero_positivo(duracion, "duracion")
        recargo_capacidad = 1.15 if self.capacidad > 20 else 1.0
        return round(self.tarifa_base * horas * recargo_capacidad, 2)

    def describir_servicio(self) -> str:
        return f"Reserva de sala con capacidad para {self.capacidad} personas."


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnologicos."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, tipo_equipo: str, cantidad: int, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self.tipo_equipo = self._validar_texto(tipo_equipo, "tipo de equipo")
        self.cantidad = int(self._validar_numero_positivo(cantidad, "cantidad"))

    def calcular_costo(self, duracion: float) -> float:
        self.validar_disponibilidad()
        dias = self._validar_numero_positivo(duracion, "duracion")
        return round(self.tarifa_base * dias * self.cantidad, 2)

    def describir_servicio(self) -> str:
        return f"Alquiler de {self.cantidad} equipo(s) tipo {self.tipo_equipo}."


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria profesional especializada."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, area: str, nivel_experto: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self.area = self._validar_texto(area, "area")
        self.nivel_experto = self._validar_texto(nivel_experto, "nivel experto").lower()
        if self.nivel_experto not in ["basico", "intermedio", "avanzado"]:
            raise ServicioError("El nivel experto debe ser basico, intermedio o avanzado.")

    def calcular_costo(self, duracion: float) -> float:
        self.validar_disponibilidad()
        horas = self._validar_numero_positivo(duracion, "duracion")
        multiplicadores = {"basico": 1.0, "intermedio": 1.25, "avanzado": 1.5}
        return round(self.tarifa_base * horas * multiplicadores[self.nivel_experto], 2)

    def describir_servicio(self) -> str:
        return f"Asesoria en {self.area} con nivel {self.nivel_experto}."
