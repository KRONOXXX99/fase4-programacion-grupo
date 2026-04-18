from cliente import Cliente
from reserva import Reserva

def main():
    print("Sistema iniciado\n")

    # Lista para guardar resultados
    operaciones = []

    # 1. Cliente válido
    try:
        cliente1 = Cliente("Juan", "juan@mail.com", "123456789")
        operaciones.append(cliente1.mostrar_info())
    except Exception as e:
        operaciones.append(f"Error cliente1: {e}")

    # 2. Cliente inválido
    try:
        cliente2 = Cliente("", "correo_malo", "abc")
        operaciones.append(cliente2.mostrar_info())
    except Exception as e:
        operaciones.append(f"Error cliente2: {e}")

    # 3. Reserva básica (sin servicio aún)
    try:
        reserva1 = Reserva(cliente1, None, 2)
        operaciones.append("Reserva creada (sin servicio aún)")
    except Exception as e:
        operaciones.append(f"Error reserva1: {e}")

    # Mostrar resultados
    print("Resultados:\n")
    for op in operaciones:
        print(op)


if __name__ == "__main__":
    main()
