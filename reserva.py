"""Modulo de reservas del sistema Software FJ."""

from cliente import Cliente
from servicio import Servicio
from excepciones import OperacionNoPermitidaError, ReservaError, ValidacionError
from logger_sistema import registrar_evento


class Reserva:
    """Integra cliente, servicio, duracion y estado de la reserva."""

    ESTADOS_VALIDOS = ["pendiente", "confirmada", "cancelada", "procesada"]

    def __init__(self, codigo: str, cliente: Cliente, servicio: Servicio, duracion: float):
        self.codigo = self._validar_codigo(codigo)
        self.cliente = self._validar_cliente(cliente)
        self.servicio = self._validar_servicio(servicio)
        self.duracion = self._validar_duracion(duracion)
        self.estado = "pendiente"
        self.costo_total = 0.0
        registrar_evento("INFO", f"Reserva creada en estado pendiente: {self.codigo}")

    @staticmethod
    def _validar_codigo(codigo: str) -> str:
        if not isinstance(codigo, str) or not codigo.strip():
            raise ReservaError("El codigo de reserva no puede estar vacio.")
        return codigo.strip().upper()

    @staticmethod
    def _validar_cliente(cliente: Cliente) -> Cliente:
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva debe asociarse a un cliente valido.")
        return cliente

    @staticmethod
    def _validar_servicio(servicio: Servicio) -> Servicio:
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva debe asociarse a un servicio valido.")
        return servicio

    @staticmethod
    def _validar_duracion(duracion: float) -> float:
        try:
            valor = float(duracion)
        except (TypeError, ValueError) as error:
            raise ValidacionError("La duracion debe ser numerica.") from error
        if valor <= 0:
            raise ValidacionError("La duracion debe ser mayor que cero.")
        return valor

    def confirmar(self) -> None:
        try:
            if self.estado != "pendiente":
                raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
            self.servicio.validar_disponibilidad()
        except Exception as error:
            registrar_evento("ERROR", f"No se pudo confirmar la reserva {self.codigo}: {error}")
            raise
        else:
            self.estado = "confirmada"
            registrar_evento("INFO", f"Reserva confirmada: {self.codigo}")
        finally:
            registrar_evento("INFO", f"Finalizo intento de confirmacion para reserva {self.codigo}")

    def cancelar(self) -> None:
        if self.estado == "procesada":
            registrar_evento("ERROR", f"Intento de cancelar reserva procesada: {self.codigo}")
            raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada.")
        if self.estado == "cancelada":
            registrar_evento("ERROR", f"Intento de cancelar dos veces la reserva: {self.codigo}")
            raise OperacionNoPermitidaError("La reserva ya estaba cancelada.")
        self.estado = "cancelada"
        registrar_evento("INFO", f"Reserva cancelada: {self.codigo}")

    def procesar(self, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        try:
            if self.estado != "confirmada":
                raise OperacionNoPermitidaError("La reserva debe estar confirmada antes de procesarse.")
            self.costo_total = self.servicio.calcular_costo_final(self.duracion, impuesto, descuento)
        except Exception as error:
            registrar_evento("ERROR", f"Error procesando reserva {self.codigo}: {error}")
            raise ReservaError("No fue posible procesar la reserva correctamente.") from error
        else:
            self.estado = "procesada"
            registrar_evento("INFO", f"Reserva procesada: {self.codigo}. Costo total: {self.costo_total}")
            return self.costo_total
        finally:
            registrar_evento("INFO", f"Finalizo intento de procesamiento para reserva {self.codigo}")

    def mostrar_info(self) -> str:
        return (
            f"Reserva {self.codigo} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duracion: {self.duracion} | "
            f"Estado: {self.estado} | Costo: ${self.costo_total:,.0f}"
        )
