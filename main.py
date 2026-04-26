"""Pruebas principales del Sistema Integral Software FJ."""

from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import SistemaFJError
from logger_sistema import limpiar_logs, registrar_evento


def ejecutar_operacion(numero: int, descripcion: str, funcion):
    """Ejecuta una operacion controlada para demostrar robustez del sistema."""
    print(f"\nOperacion {numero}: {descripcion}")
    print("-" * 70)
    try:
        resultado = funcion()
    except SistemaFJError as error:
        print(f"Error controlado: {error}")
        registrar_evento("ERROR", f"Operacion {numero} fallo de forma controlada: {error}")
    except Exception as error:
        print(f"Error inesperado controlado: {error}")
        registrar_evento("CRITICO", f"Operacion {numero} genero error inesperado: {error}")
    else:
        if resultado is not None:
            print(resultado)
        registrar_evento("INFO", f"Operacion {numero} ejecutada correctamente.")
    finally:
        print("Operacion finalizada. El sistema continua activo.")


def main():
    limpiar_logs()
    registrar_evento("INFO", "Inicio de ejecucion del Sistema Software FJ")

    datos = {"clientes": {}, "servicios": {}, "reservas": {}}

    def op1_cliente_valido():
        cliente = Cliente("C001", "Jose Alejandro", "jose@example.com", "3115965432")
        datos["clientes"]["jose"] = cliente
        return cliente.mostrar_info()

    def op2_cliente_correo_invalido():
        return Cliente("C002", "Laura Medina", "correo-sin-arroba", "3202786625").mostrar_info()

    def op3_cliente_telefono_invalido():
        return Cliente("C003", "Carlos Rojas", "carlos@example.com", "31A596").mostrar_info()

    def op4_crear_sala():
        servicio = ReservaSala("S001", "Sala de juntas principal", 45000, capacidad=25)
        datos["servicios"]["sala"] = servicio
        return servicio.mostrar_info() + "\n" + servicio.describir_servicio()

    def op5_crear_alquiler_equipo():
        servicio = AlquilerEquipo("S002", "Alquiler de computadores", 30000, "Computador portatil", 3)
        datos["servicios"]["equipo"] = servicio
        return servicio.mostrar_info() + "\n" + servicio.describir_servicio()

    def op6_crear_asesoria():
        servicio = AsesoriaEspecializada("S003", "Asesoria en Python", 60000, "programacion", "avanzado")
        datos["servicios"]["asesoria"] = servicio
        return servicio.mostrar_info() + "\n" + servicio.describir_servicio()

    def op7_servicio_tarifa_invalida():
        return ReservaSala("S004", "Sala error", -10000, capacidad=10).mostrar_info()

    def op8_reserva_valida_confirmar_procesar():
        reserva = Reserva("R001", datos["clientes"]["jose"], datos["servicios"]["sala"], 2)
        reserva.confirmar()
        total = reserva.procesar(impuesto=0.19, descuento=5000)
        datos["reservas"]["r1"] = reserva
        return reserva.mostrar_info() + f"\nTotal calculado con impuesto y descuento: ${total:,.0f}"

    def op9_reserva_duracion_invalida():
        return Reserva("R002", datos["clientes"]["jose"], datos["servicios"]["equipo"], 0).mostrar_info()

    def op10_servicio_no_disponible():
        servicio = datos["servicios"]["asesoria"]
        servicio.cambiar_disponibilidad(False)
        reserva = Reserva("R003", datos["clientes"]["jose"], servicio, 3)
        reserva.confirmar()
        return reserva.mostrar_info()

    def op11_cancelar_reserva_pendiente():
        reserva = Reserva("R004", datos["clientes"]["jose"], datos["servicios"]["equipo"], 1)
        reserva.cancelar()
        datos["reservas"]["r4"] = reserva
        return reserva.mostrar_info()

    def op12_procesar_sin_confirmar():
        reserva = Reserva("R005", datos["clientes"]["jose"], datos["servicios"]["equipo"], 1)
        return f"Costo: {reserva.procesar()}"

    operaciones = [
        (1, "Registro valido de cliente", op1_cliente_valido),
        (2, "Registro invalido de cliente por correo", op2_cliente_correo_invalido),
        (3, "Registro invalido de cliente por telefono", op3_cliente_telefono_invalido),
        (4, "Creacion correcta de servicio ReservaSala", op4_crear_sala),
        (5, "Creacion correcta de servicio AlquilerEquipo", op5_crear_alquiler_equipo),
        (6, "Creacion correcta de servicio AsesoriaEspecializada", op6_crear_asesoria),
        (7, "Creacion incorrecta de servicio con tarifa negativa", op7_servicio_tarifa_invalida),
        (8, "Reserva exitosa, confirmada y procesada", op8_reserva_valida_confirmar_procesar),
        (9, "Reserva fallida por duracion invalida", op9_reserva_duracion_invalida),
        (10, "Reserva fallida por servicio no disponible", op10_servicio_no_disponible),
        (11, "Cancelacion correcta de reserva pendiente", op11_cancelar_reserva_pendiente),
        (12, "Procesamiento fallido de reserva sin confirmar", op12_procesar_sin_confirmar),
    ]

    print("SISTEMA INTEGRAL DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS")
    print("Empresa: Software FJ")
    print("=" * 70)

    for numero, descripcion, funcion in operaciones:
        ejecutar_operacion(numero, descripcion, funcion)

    print("\nResumen: se ejecutaron operaciones validas e invalidas sin detener el sistema.")
    print("Revise el archivo logs.txt para ver eventos y errores registrados.")
    registrar_evento("INFO", "Fin de ejecucion del Sistema Software FJ")


if __name__ == "__main__":
    main()
