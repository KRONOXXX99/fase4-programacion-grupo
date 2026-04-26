"""Interfaz grafica Tkinter para el Sistema Integral Software FJ."""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import SistemaFJError
from logger_sistema import registrar_evento, limpiar_logs, LOG_FILE


class SoftwareFJApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Gestion de Clientes, Servicios y Reservas")
        self.root.geometry("1050x680")
        self.root.minsize(980, 620)

        self.clientes = []
        self.servicios = []
        self.reservas = []

        self.contador_clientes = 1
        self.contador_servicios = 1
        self.contador_reservas = 1

        limpiar_logs()
        registrar_evento("INFO", "Inicio de ejecucion de interfaz grafica Software FJ")

        self.configurar_estilos()
        self.crear_layout()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f6f8")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Title.TLabel", background="#f4f6f8", foreground="#14213d", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background="#f4f6f8", foreground="#4b5563", font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background="#ffffff", foreground="#14213d", font=("Segoe UI", 12, "bold"))
        style.configure("TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Accent.TButton", background="#2563eb", foreground="white")
        style.configure("Success.TButton", background="#16a34a", foreground="white")
        style.configure("Danger.TButton", background="#dc2626", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=27)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def crear_layout(self):
        contenedor = ttk.Frame(self.root, padding=18)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(contenedor, text="Sistema Integral de Gestion - Software FJ", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Clientes, servicios, reservas, excepciones controladas y registro de logs.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(0, 12))

        self.tabs = ttk.Notebook(contenedor)
        self.tabs.pack(fill="both", expand=True)

        self.tab_clientes = ttk.Frame(self.tabs)
        self.tab_servicios = ttk.Frame(self.tabs)
        self.tab_reservas = ttk.Frame(self.tabs)
        self.tab_logs = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_clientes, text="Clientes")
        self.tabs.add(self.tab_servicios, text="Servicios")
        self.tabs.add(self.tab_reservas, text="Reservas")
        self.tabs.add(self.tab_logs, text="Logs")

        self.crear_tab_clientes()
        self.crear_tab_servicios()
        self.crear_tab_reservas()
        self.crear_tab_logs()

    def crear_card(self, parent, titulo):
        card = ttk.Frame(parent, style="Card.TFrame", padding=16)
        ttk.Label(card, text=titulo, style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))
        return card

    def crear_tab_clientes(self):
        frame = ttk.Frame(self.tab_clientes, padding=14)
        frame.pack(fill="both", expand=True)

        form = self.crear_card(frame, "Registrar cliente")
        form.pack(side="left", fill="y", padx=(0, 12))

        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.telefono_var = tk.StringVar()

        self.crear_input(form, "Nombre", self.nombre_var)
        self.crear_input(form, "Correo", self.correo_var)
        self.crear_input(form, "Telefono", self.telefono_var)

        ttk.Button(form, text="Registrar cliente", style="Success.TButton", command=self.registrar_cliente).pack(fill="x", pady=(8, 0))
        ttk.Button(form, text="Limpiar campos", command=self.limpiar_cliente).pack(fill="x", pady=(8, 0))

        listado = self.crear_card(frame, "Clientes registrados")
        listado.pack(side="left", fill="both", expand=True)

        columnas = ("id", "nombre", "correo", "telefono")
        self.tabla_clientes = ttk.Treeview(listado, columns=columnas, show="headings")
        for col in columnas:
            self.tabla_clientes.heading(col, text=col.capitalize())
        self.tabla_clientes.pack(fill="both", expand=True)

    def crear_tab_servicios(self):
        frame = ttk.Frame(self.tab_servicios, padding=14)
        frame.pack(fill="both", expand=True)

        form = self.crear_card(frame, "Crear servicio")
        form.pack(side="left", fill="y", padx=(0, 12))

        self.tipo_servicio_var = tk.StringVar(value="ReservaSala")
        self.nombre_servicio_var = tk.StringVar()
        self.tarifa_var = tk.StringVar()
        self.extra1_var = tk.StringVar()
        self.extra2_var = tk.StringVar()

        ttk.Label(form, text="Tipo de servicio").pack(anchor="w")
        tipo_combo = ttk.Combobox(
            form,
            textvariable=self.tipo_servicio_var,
            values=["ReservaSala", "AlquilerEquipo", "AsesoriaEspecializada"],
            state="readonly",
        )
        tipo_combo.pack(fill="x", pady=(0, 8))
        tipo_combo.bind("<<ComboboxSelected>>", lambda _: self.actualizar_labels_servicio())

        self.crear_input(form, "Nombre del servicio", self.nombre_servicio_var)
        self.crear_input(form, "Tarifa base", self.tarifa_var)

        self.extra1_label = ttk.Label(form, text="Capacidad")
        self.extra1_label.pack(anchor="w")
        ttk.Entry(form, textvariable=self.extra1_var).pack(fill="x", pady=(0, 8))

        self.extra2_label = ttk.Label(form, text="Campo adicional")
        self.extra2_label.pack(anchor="w")
        self.extra2_entry = ttk.Entry(form, textvariable=self.extra2_var)
        self.extra2_entry.pack(fill="x", pady=(0, 8))
        self.actualizar_labels_servicio()

        ttk.Button(form, text="Crear servicio", style="Success.TButton", command=self.crear_servicio).pack(fill="x", pady=(8, 0))
        ttk.Button(form, text="Limpiar campos", command=self.limpiar_servicio).pack(fill="x", pady=(8, 0))

        listado = self.crear_card(frame, "Servicios creados")
        listado.pack(side="left", fill="both", expand=True)

        columnas = ("id", "tipo", "nombre", "tarifa", "estado")
        self.tabla_servicios = ttk.Treeview(listado, columns=columnas, show="headings")
        for col in columnas:
            self.tabla_servicios.heading(col, text=col.capitalize())
        self.tabla_servicios.pack(fill="both", expand=True)

    def crear_tab_reservas(self):
        frame = ttk.Frame(self.tab_reservas, padding=14)
        frame.pack(fill="both", expand=True)

        form = self.crear_card(frame, "Gestionar reserva")
        form.pack(side="left", fill="y", padx=(0, 12))

        self.combo_cliente_var = tk.StringVar()
        self.combo_servicio_var = tk.StringVar()
        self.duracion_var = tk.StringVar()
        self.impuesto_var = tk.StringVar(value="0.19")
        self.descuento_var = tk.StringVar(value="0")

        ttk.Label(form, text="Cliente").pack(anchor="w")
        self.combo_clientes = ttk.Combobox(form, textvariable=self.combo_cliente_var, state="readonly")
        self.combo_clientes.pack(fill="x", pady=(0, 8))

        ttk.Label(form, text="Servicio").pack(anchor="w")
        self.combo_servicios = ttk.Combobox(form, textvariable=self.combo_servicio_var, state="readonly")
        self.combo_servicios.pack(fill="x", pady=(0, 8))

        self.crear_input(form, "Duracion", self.duracion_var)
        self.crear_input(form, "Impuesto (ej: 0.19)", self.impuesto_var)
        self.crear_input(form, "Descuento", self.descuento_var)

        ttk.Button(form, text="Crear reserva", style="Accent.TButton", command=self.crear_reserva).pack(fill="x", pady=(8, 0))
        ttk.Button(form, text="Confirmar seleccionada", style="Success.TButton", command=self.confirmar_reserva).pack(fill="x", pady=(8, 0))
        ttk.Button(form, text="Procesar seleccionada", command=self.procesar_reserva).pack(fill="x", pady=(8, 0))
        ttk.Button(form, text="Cancelar seleccionada", style="Danger.TButton", command=self.cancelar_reserva).pack(fill="x", pady=(8, 0))

        listado = self.crear_card(frame, "Reservas")
        listado.pack(side="left", fill="both", expand=True)

        columnas = ("codigo", "cliente", "servicio", "duracion", "estado", "costo")
        self.tabla_reservas = ttk.Treeview(listado, columns=columnas, show="headings")
        for col in columnas:
            self.tabla_reservas.heading(col, text=col.capitalize())
        self.tabla_reservas.pack(fill="both", expand=True)

    def crear_tab_logs(self):
        frame = ttk.Frame(self.tab_logs, padding=14)
        frame.pack(fill="both", expand=True)

        card = self.crear_card(frame, "Registro de eventos y errores")
        card.pack(fill="both", expand=True)

        botones = ttk.Frame(card)
        botones.pack(fill="x", pady=(0, 8))
        ttk.Button(botones, text="Actualizar logs", command=self.cargar_logs).pack(side="left")
        ttk.Button(botones, text="Limpiar logs", command=self.limpiar_y_cargar_logs).pack(side="left", padx=8)

        self.text_logs = tk.Text(card, wrap="word", font=("Consolas", 10), height=20)
        self.text_logs.pack(fill="both", expand=True)
        self.cargar_logs()

    def crear_input(self, parent, label, variable):
        ttk.Label(parent, text=label).pack(anchor="w")
        ttk.Entry(parent, textvariable=variable).pack(fill="x", pady=(0, 8))

    def actualizar_labels_servicio(self):
        tipo = self.tipo_servicio_var.get()
        if tipo == "ReservaSala":
            self.extra1_label.config(text="Capacidad")
            self.extra2_label.config(text="No usado")
            self.extra2_entry.config(state="disabled")
        elif tipo == "AlquilerEquipo":
            self.extra1_label.config(text="Tipo de equipo")
            self.extra2_label.config(text="Cantidad")
            self.extra2_entry.config(state="normal")
        else:
            self.extra1_label.config(text="Area")
            self.extra2_label.config(text="Nivel: basico, intermedio o avanzado")
            self.extra2_entry.config(state="normal")

    def registrar_cliente(self):
        try:
            codigo = f"C{self.contador_clientes:03d}"
            cliente = Cliente(codigo, self.nombre_var.get(), self.correo_var.get(), self.telefono_var.get())
            self.clientes.append(cliente)
            self.contador_clientes += 1
            self.refrescar_clientes()
            self.limpiar_cliente()
            messagebox.showinfo("Exito", "Cliente registrado correctamente.")
        except Exception as error:
            self.manejar_error("No fue posible registrar el cliente", error)

    def crear_servicio(self):
        try:
            codigo = f"S{self.contador_servicios:03d}"
            tipo = self.tipo_servicio_var.get()
            nombre = self.nombre_servicio_var.get()
            tarifa = self.tarifa_var.get()

            if tipo == "ReservaSala":
                servicio = ReservaSala(codigo, nombre, tarifa, self.extra1_var.get())
            elif tipo == "AlquilerEquipo":
                servicio = AlquilerEquipo(codigo, nombre, tarifa, self.extra1_var.get(), self.extra2_var.get())
            else:
                servicio = AsesoriaEspecializada(codigo, nombre, tarifa, self.extra1_var.get(), self.extra2_var.get())

            self.servicios.append(servicio)
            self.contador_servicios += 1
            self.refrescar_servicios()
            self.limpiar_servicio()
            messagebox.showinfo("Exito", "Servicio creado correctamente.")
        except Exception as error:
            self.manejar_error("No fue posible crear el servicio", error)

    def crear_reserva(self):
        try:
            cliente = self.obtener_cliente_seleccionado()
            servicio = self.obtener_servicio_seleccionado()
            codigo = f"R{self.contador_reservas:03d}"
            reserva = Reserva(codigo, cliente, servicio, self.duracion_var.get())
            self.reservas.append(reserva)
            self.contador_reservas += 1
            self.refrescar_reservas()
            messagebox.showinfo("Exito", "Reserva creada en estado pendiente.")
        except Exception as error:
            self.manejar_error("No fue posible crear la reserva", error)

    def confirmar_reserva(self):
        reserva = self.obtener_reserva_tabla()
        if not reserva:
            return
        try:
            reserva.confirmar()
            self.refrescar_reservas()
            messagebox.showinfo("Exito", "Reserva confirmada correctamente.")
        except Exception as error:
            self.manejar_error("No fue posible confirmar la reserva", error)

    def procesar_reserva(self):
        reserva = self.obtener_reserva_tabla()
        if not reserva:
            return
        try:
            impuesto = float(self.impuesto_var.get() or 0)
            descuento = float(self.descuento_var.get() or 0)
            total = reserva.procesar(impuesto=impuesto, descuento=descuento)
            self.refrescar_reservas()
            messagebox.showinfo("Reserva procesada", f"Costo total: ${total:,.0f}")
        except Exception as error:
            self.manejar_error("No fue posible procesar la reserva", error)

    def cancelar_reserva(self):
        reserva = self.obtener_reserva_tabla()
        if not reserva:
            return
        try:
            reserva.cancelar()
            self.refrescar_reservas()
            messagebox.showinfo("Exito", "Reserva cancelada correctamente.")
        except Exception as error:
            self.manejar_error("No fue posible cancelar la reserva", error)

    def obtener_cliente_seleccionado(self):
        valor = self.combo_cliente_var.get()
        if not valor:
            raise ValueError("Debe seleccionar un cliente.")
        codigo = valor.split(" - ")[0]
        return next(c for c in self.clientes if c.identificador == codigo)

    def obtener_servicio_seleccionado(self):
        valor = self.combo_servicio_var.get()
        if not valor:
            raise ValueError("Debe seleccionar un servicio.")
        codigo = valor.split(" - ")[0]
        return next(s for s in self.servicios if s.identificador == codigo)

    def obtener_reserva_tabla(self):
        item = self.tabla_reservas.selection()
        if not item:
            messagebox.showwarning("Seleccion requerida", "Seleccione una reserva en la tabla.")
            return None
        codigo = self.tabla_reservas.item(item[0], "values")[0]
        return next((r for r in self.reservas if r.codigo == codigo), None)

    def refrescar_clientes(self):
        self.tabla_clientes.delete(*self.tabla_clientes.get_children())
        for c in self.clientes:
            self.tabla_clientes.insert("", "end", values=(c.identificador, c.nombre, c.correo, c.telefono))
        self.combo_clientes["values"] = [f"{c.identificador} - {c.nombre}" for c in self.clientes]
        self.cargar_logs()

    def refrescar_servicios(self):
        self.tabla_servicios.delete(*self.tabla_servicios.get_children())
        for s in self.servicios:
            estado = "Disponible" if s.disponible else "No disponible"
            self.tabla_servicios.insert("", "end", values=(s.identificador, s.__class__.__name__, s.nombre, f"${s.tarifa_base:,.0f}", estado))
        self.combo_servicios["values"] = [f"{s.identificador} - {s.nombre}" for s in self.servicios]
        self.cargar_logs()

    def refrescar_reservas(self):
        self.tabla_reservas.delete(*self.tabla_reservas.get_children())
        for r in self.reservas:
            self.tabla_reservas.insert(
                "",
                "end",
                values=(r.codigo, r.cliente.nombre, r.servicio.nombre, r.duracion, r.estado, f"${r.costo_total:,.0f}"),
            )
        self.cargar_logs()

    def limpiar_cliente(self):
        self.nombre_var.set("")
        self.correo_var.set("")
        self.telefono_var.set("")

    def limpiar_servicio(self):
        self.nombre_servicio_var.set("")
        self.tarifa_var.set("")
        self.extra1_var.set("")
        self.extra2_var.set("")

    def cargar_logs(self):
        try:
            contenido = Path(LOG_FILE).read_text(encoding="utf-8")
        except FileNotFoundError:
            contenido = "No se ha generado el archivo logs.txt."
        self.text_logs.delete("1.0", "end")
        self.text_logs.insert("1.0", contenido)

    def limpiar_y_cargar_logs(self):
        limpiar_logs()
        registrar_evento("INFO", "Logs reiniciados desde la interfaz grafica")
        self.cargar_logs()

    def manejar_error(self, contexto, error):
        registrar_evento("ERROR", f"{contexto}: {error}")
        self.cargar_logs()
        messagebox.showerror("Error controlado", f"{contexto}:\n{error}\n\nEl sistema continua activo.")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = SoftwareFJApp(ventana)
    ventana.mainloop()
