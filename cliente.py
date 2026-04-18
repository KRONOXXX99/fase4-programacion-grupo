class Cliente:
    def __init__(self, nombre, correo, telefono):
        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)

    # VALIDACIONES
    def set_nombre(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío")
        self.nombre = nombre

    def set_correo(self, correo):
        if "@" not in correo or "." not in correo:
            raise ValueError("Correo inválido")
        self.correo = correo

    def set_telefono(self, telefono):
        if not telefono.isdigit():
            raise ValueError("El teléfono debe contener solo números")
        self.telefono = telefono

    # MÉTODO
    def mostrar_info(self):
        return f"Cliente: {self.nombre}, Correo: {self.correo}, Tel: {self.telefono}"
