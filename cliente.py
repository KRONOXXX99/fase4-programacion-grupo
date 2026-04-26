"""Modulo de clientes del sistema Software FJ."""

import re
from entidad import EntidadSistema
from excepciones import ClienteError, ValidacionError
from logger_sistema import registrar_evento


class Cliente(EntidadSistema):
    """Cliente con encapsulacion y validaciones robustas."""

    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(self._validar_identificador(identificador))
        self.__nombre = ""
        self.__correo = ""
        self.__telefono = ""
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        registrar_evento("INFO", f"Cliente creado correctamente: {self.__nombre}")

    @staticmethod
    def _validar_identificador(identificador: str) -> str:
        if not isinstance(identificador, str) or not identificador.strip():
            raise ClienteError("El identificador del cliente no puede estar vacio.")
        return identificador.strip()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValidacionError("El nombre del cliente no puede estar vacio.")
        if len(valor.strip()) < 3:
            raise ValidacionError("El nombre debe tener al menos 3 caracteres.")
        if any(caracter.isdigit() for caracter in valor):
            raise ValidacionError("El nombre no debe contener numeros.")
        self.__nombre = valor.strip().title()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not isinstance(valor, str) or not re.match(patron, valor.strip()):
            raise ValidacionError("Correo invalido. Ejemplo valido: nombre@dominio.com")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not isinstance(valor, str):
            valor = str(valor)
        valor = valor.strip().replace(" ", "")
        if not valor.isdigit():
            raise ValidacionError("El telefono solo debe contener numeros.")
        if len(valor) < 7 or len(valor) > 12:
            raise ValidacionError("El telefono debe tener entre 7 y 12 digitos.")
        self.__telefono = valor

    def mostrar_info(self) -> str:
        return f"Cliente[{self.identificador}] {self.nombre} - {self.correo} - Tel: {self.telefono}"
