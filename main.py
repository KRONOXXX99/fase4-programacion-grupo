from cliente import Cliente

def main():
    try:
        cliente1 = Cliente("Juan", "juan@mail.com", "123456789")
        print(cliente1.mostrar_info())

        # prueba error
        cliente2 = Cliente("", "correo_malo", "abc")

    except Exception as e:
        print(f"Error detectado: {e}")

if __name__ == "__main__":
    main()
