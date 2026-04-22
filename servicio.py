from datetime import date, timedelta


class Servicio:
    def __init__(self, cliente, descripcion, fecha=None):
        if not cliente or not isinstance(cliente, str):
            raise ValueError("El cliente debe ser un texto no vacío.")
        if not descripcion or not isinstance(descripcion, str):
            raise ValueError("La descripción debe ser un texto no vacío.")

        self.cliente = cliente.strip()
        self.descripcion = descripcion.strip()
        self.fecha = fecha or date.today()

    def calcular_costo(self):
        raise NotImplementedError("Debes implementar calcular_costo()")

    def aplicar_impuesto(self, porcentaje=0.19):
        return self.calcular_costo() * (1 + porcentaje)

    def resumen(self):
        costo = self.calcular_costo()
        costo_con_iva = self.aplicar_impuesto()
        return (
            f"\n{'─' * 45}\n"
            f"  Servicio   : {self.__class__.__name__}\n"
            f"  Cliente    : {self.cliente}\n"
            f"  Descripción: {self.descripcion}\n"
            f"  Fecha      : {self.fecha}\n"
            f"  Subtotal   : ${costo:>12,.0f}\n"
            f"  IVA (19%)  : ${costo_con_iva - costo:>12,.0f}\n"
            f"  Total      : ${costo_con_iva:>12,.0f}\n"
            f"{'─' * 45}"
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(cliente='{self.cliente}', costo=${self.calcular_costo():,.0f})"


# AlquilerEquipo

EQUIPOS = {
    "1": {"nombre": "taladro",          "tarifa": 25_000},
    "2": {"nombre": "andamio",          "tarifa": 50_000},
    "3": {"nombre": "generador",        "tarifa": 80_000},
    "4": {"nombre": "compresor",        "tarifa": 40_000},
    "5": {"nombre": "retroexcavadora",  "tarifa": 300_000},
}


class AlquilerEquipo(Servicio):
    def __init__(self, cliente, descripcion, equipo, fecha_inicio, fecha_fin, cantidad=1):
        super().__init__(cliente, descripcion, fecha_inicio)

        equipo = equipo.strip().lower()
        nombres = [e["nombre"] for e in EQUIPOS.values()]
        if equipo not in nombres:
            raise ValueError(f"Equipo '{equipo}' no existe. Disponibles: {', '.join(nombres)}.")

        if not isinstance(fecha_inicio, date) or not isinstance(fecha_fin, date):
            raise TypeError("Las fechas deben ser objetos date.")
        if fecha_fin < fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio.")

        if not isinstance(cantidad, int) or cantidad < 1:
            raise ValueError("La cantidad debe ser un entero mayor a 0.")

        self.equipo = equipo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.dias = (fecha_fin - fecha_inicio).days + 1
        self.cantidad = cantidad

    def _tarifa(self):
        for e in EQUIPOS.values():
            if e["nombre"] == self.equipo:
                return e["tarifa"]

    def _descuento(self):
        if self.dias >= 30:
            return 0.15
        elif self.dias >= 15:
            return 0.10
        elif self.dias >= 7:
            return 0.05
        return 0.0

    def calcular_costo(self):
        subtotal = self._tarifa() * self.dias * self.cantidad
        return subtotal * (1 - self._descuento())

    def resumen(self):
        descuento_pct = self._descuento() * 100
        base = super().resumen()
        detalle = (
            f"  · Equipo   : {self.equipo}\n"
            f"  · Período  : {self.fecha_inicio} → {self.fecha_fin} ({self.dias} días)\n"
            f"  · Cantidad : {self.cantidad} unidad(es)\n"
            f"  · Descuento: {descuento_pct:.0f}%"
        )
        return base.rstrip("─" * 45).rstrip() + "\n" + detalle + "\n" + "─" * 45


# Asesoria

MODALIDADES = {"virtual", "presencial", "hibrida"}

PREGUNTAS = [
    {
        "pregunta": "¿Qué tipo de trabajo va a realizar?",
        "opciones": {
            "1": "Construcción en altura (fachadas, techos)",
            "2": "Perforación o instalación",
            "3": "Generación de energía o iluminación",
            "4": "Pintura, limpieza o trabajos con aire",
            "5": "Movimiento de tierra o excavación",
        }
    },
    {
        "pregunta": "¿En qué entorno va a trabajar?",
        "opciones": {
            "1": "Exterior / obra grande",
            "2": "Interior / espacio reducido",
        }
    },
]

# clave: (resp_pregunta1, resp_pregunta2)
RECOMENDACIONES = {
    ("1", "1"): "andamio",
    ("1", "2"): "andamio",
    ("2", "1"): "taladro",
    ("2", "2"): "taladro",
    ("3", "1"): "generador",
    ("3", "2"): "generador",
    ("4", "1"): "compresor",
    ("4", "2"): "compresor",
    ("5", "1"): "retroexcavadora",
    ("5", "2"): "retroexcavadora",
}


class Asesoria(Servicio):

    TARIFA_HORA = 90_000
    MAX_HORAS = 200

    def __init__(self, cliente, descripcion, horas, modalidad="virtual", urgente=False, asesor="Por asignar"):
        super().__init__(cliente, descripcion)

        try:
            horas = float(horas)
        except (TypeError, ValueError):
            raise ValueError("Las horas deben ser un número.")

        if not (1 <= horas <= self.MAX_HORAS):
            raise ValueError(f"Las horas deben estar entre 1 y {self.MAX_HORAS} (recibido: {horas}).")

        modalidad = modalidad.strip().lower()
        if modalidad not in MODALIDADES:
            raise ValueError(f"Modalidad '{modalidad}' no válida. Opciones: {', '.join(MODALIDADES)}.")

        if not isinstance(urgente, bool):
            raise TypeError("El parámetro 'urgente' debe ser True o False.")

        self.horas = horas
        self.modalidad = modalidad
        self.urgente = urgente
        self.asesor = asesor.strip() if asesor else "Por asignar"

    def _recargo(self):
        recargo = 0.0
        if self.urgente:
            recargo += 0.30
        if self.modalidad == "presencial":
            recargo += 0.15
        return recargo

    def calcular_costo(self):
        return self.TARIFA_HORA * self.horas * (1 + self._recargo())

    def resumen(self):
        recargo_pct = self._recargo() * 100
        base = super().resumen()
        detalle = (
            f"  · Modalidad: {self.modalidad}\n"
            f"  · Urgente  : {'Sí' if self.urgente else 'No'}\n"
            f"  · Recargo  : {recargo_pct:.0f}%\n"
            f"  · Asesor   : {self.asesor}"
        )
        return base.rstrip("─" * 45).rstrip() + "\n" + detalle + "\n" + "─" * 45


# Menús interactivos

def leer_opcion(opciones_validas, mensaje="  Opción: "):
    while True:
        entrada = input(mensaje).strip()
        if entrada in opciones_validas:
            return entrada
        print(f"  ✗ Opción inválida. Elige entre: {', '.join(opciones_validas)}")


def leer_entero(mensaje, minimo=1, maximo=9999):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if minimo <= valor <= maximo:
                return valor
            print(f"  ✗ Debe ser un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  ✗ Ingresa un número entero válido.")


def menu_asesoria():
    print("\n" + "═" * 45)
    print("         ASESORÍA DE EQUIPOS")
    print("═" * 45)

    cliente = ""
    while not cliente:
        cliente = input("  Nombre del cliente: ").strip()
        if not cliente:
            print("  ✗ El nombre no puede estar vacío.")

    respuestas = []
    for p in PREGUNTAS:
        print(f"\n  {p['pregunta']}")
        for cod, desc in p["opciones"].items():
            print(f"    [{cod}] {desc}")
        respuestas.append(leer_opcion(list(p["opciones"].keys())))

    clave = tuple(respuestas)
    equipo_recomendado = RECOMENDACIONES.get(clave, "andamio")

    print(f"\n  ✔ Equipo recomendado: {equipo_recomendado.upper()}")
    for cod, datos in EQUIPOS.items():
        if datos["nombre"] == equipo_recomendado:
            print(f"     Tarifa diaria: ${datos['tarifa']:,.0f}")
            break

    print("\n  ── Datos de la asesoría ──")
    print("  Modalidad:")
    print("    [1] Virtual")
    print("    [2] Presencial")
    print("    [3] Híbrida")
    mod_map = {"1": "virtual", "2": "presencial", "3": "hibrida"}
    modalidad = mod_map[leer_opcion(["1", "2", "3"])]

    print("  ¿Es urgente?  [1] Sí   [2] No")
    urgente = leer_opcion(["1", "2"]) == "1"

    asesor = input("  Nombre del asesor (Enter para omitir): ").strip() or "Por asignar"

    asesoria = Asesoria(
        cliente=cliente,
        descripcion=f"Asesoría para alquiler de {equipo_recomendado}",
        horas=1,
        modalidad=modalidad,
        urgente=urgente,
        asesor=asesor,
    )

    print(asesoria.resumen())
    return cliente, equipo_recomendado


def menu_alquiler(cliente_default="", equipo_sugerido=""):
    print("\n" + "═" * 45)
    print("         ALQUILER DE EQUIPOS")
    print("═" * 45)

    if cliente_default:
        print(f"  Cliente: {cliente_default}")
        cliente = cliente_default
    else:
        cliente = ""
        while not cliente:
            cliente = input("  Nombre del cliente: ").strip()

    alquileres = []

    while True:
        print("\n  ── Catálogo de equipos ──")
        for cod, datos in EQUIPOS.items():
            sugerido = " ◄ recomendado" if datos["nombre"] == equipo_sugerido else ""
            print(f"    [{cod}] {datos['nombre']:<18} ${datos['tarifa']:>10,.0f}/día{sugerido}")
        print("    [0] Finalizar y ver resumen")

        cod = leer_opcion(["0"] + list(EQUIPOS.keys()))
        if cod == "0":
            break

        equipo = EQUIPOS[cod]["nombre"]
        cantidad = leer_entero(f"  Cantidad de '{equipo}' a alquilar: ", 1, 50)
        dias = leer_entero("  ¿Cuántos días lo necesita? ", 1, 365)

        fecha_inicio = date.today()
        fecha_fin = fecha_inicio + timedelta(days=dias - 1)

        alquiler = AlquilerEquipo(
            cliente=cliente,
            descripcion=f"Alquiler de {equipo}",
            equipo=equipo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cantidad=cantidad,
        )
        alquileres.append(alquiler)
        print(f"  ✔ Agregado: {cantidad}x {equipo} por {dias} día(s)")

    if not alquileres:
        print("\n  No se agregó ningún equipo.")
        return

    print("\n" + "═" * 45)
    print("         RESUMEN DE ALQUILER")
    print("═" * 45)

    total_general = 0
    for a in alquileres:
        print(a.resumen())
        total_general += a.aplicar_impuesto()

    if len(alquileres) > 1:
        print(f"\n  {'TOTAL A PAGAR':.<30} ${total_general:>12,.0f}")


# Punto de entrada

if __name__ == "__main__":
    while True:
        print("\n" + "═" * 45)
        print("   SISTEMA DE SERVICIOS Y ALQUILER")
        print("═" * 45)
        print("  [1] Iniciar con asesoría (recomendado)")
        print("  [2] Ir directo al alquiler")
        print("  [0] Salir")

        opcion = leer_opcion(["0", "1", "2"])

        if opcion == "0":
            print("\n  Hasta luego.\n")
            break
        elif opcion == "1":
            cliente, equipo_recomendado = menu_asesoria()
            print("\n  ¿Desea proceder al alquiler?  [1] Sí   [2] No")
            if leer_opcion(["1", "2"]) == "1":
                menu_alquiler(cliente, equipo_recomendado)
        elif opcion == "2":
            menu_alquiler()
