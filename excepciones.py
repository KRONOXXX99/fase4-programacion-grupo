"""Excepciones personalizadas del sistema Software FJ."""


class SistemaFJError(Exception):
    """Excepcion base para errores controlados del sistema."""


class ValidacionError(SistemaFJError):
    """Se lanza cuando un dato no cumple las reglas de validacion."""


class ClienteError(SistemaFJError):
    """Se lanza cuando ocurre un error relacionado con clientes."""


class ServicioError(SistemaFJError):
    """Se lanza cuando ocurre un error relacionado con servicios."""


class ReservaError(SistemaFJError):
    """Se lanza cuando ocurre un error relacionado con reservas."""


class ServicioNoDisponibleError(ServicioError):
    """Se lanza cuando se intenta reservar un servicio no disponible."""


class OperacionNoPermitidaError(SistemaFJError):
    """Se lanza cuando una operacion no es valida para el estado actual."""
