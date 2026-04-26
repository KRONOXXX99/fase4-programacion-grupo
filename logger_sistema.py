"""Modulo de registro de eventos y errores del sistema."""

from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent / "logs.txt"


def registrar_evento(tipo: str, mensaje: str) -> None:
    """Registra eventos relevantes y errores en un archivo de texto."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{fecha}] [{tipo.upper()}] {mensaje}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as archivo:
            archivo.write(linea)
    except OSError as error:
        # Si el log falla, no debe detener el sistema principal.
        print(f"No fue posible escribir en logs.txt: {error}")


def limpiar_logs() -> None:
    """Limpia el archivo de logs al iniciar una nueva ejecucion de pruebas."""
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as archivo:
            archivo.write("REGISTRO DE EVENTOS Y ERRORES - SOFTWARE FJ\n")
            archivo.write("=" * 55 + "\n")
    except OSError as error:
        print(f"No fue posible limpiar logs.txt: {error}")
