# Fase 4 - Programación - Sistema Software FJ

Sistema integral desarrollado en Python para la gestión de clientes, servicios y reservas de la empresa ficticia **Software FJ**, aplicando Programación Orientada a Objetos (POO), manejo de excepciones y registro de eventos mediante logs.

---

## Descripción general

El sistema permite gestionar de forma estructurada:

- Registro de clientes con validaciones
- Administración de servicios (reserva de salas, alquiler de equipos y asesorías)
- Creación, confirmación, cancelación y procesamiento de reservas
- Manejo de errores controlados sin detener la ejecución
- Registro de eventos y errores en archivo de logs
- Interacción mediante consola o interfaz gráfica

---

## Requisitos implementados

- Clase abstracta general `EntidadSistema`
- Clase `Cliente` con encapsulación y validaciones robustas
- Clase abstracta `Servicio`
- Tres servicios especializados:
  - `ReservaSala`
  - `AlquilerEquipo`
  - `AsesoriaEspecializada`
- Clase `Reserva` que integra cliente, servicio, duración y estado
- Confirmación, cancelación y procesamiento de reservas
- Excepciones personalizadas
- Uso de `try/except`, `try/except/else/finally` y encadenamiento de excepciones
- Archivo `logs.txt` para registro de eventos y errores
- Más de 10 operaciones de prueba en `main.py`
- Implementación de interfaz gráfica con Tkinter (`interfaz.py`)
- No se utiliza base de datos

---

## Estructura del proyecto

- `entidad.py` → Clase abstracta base del sistema  
- `cliente.py` → Gestión y validación de clientes  
- `servicio.py` → Servicios abstractos y especializados  
- `reserva.py` → Gestión de reservas  
- `excepciones.py` → Excepciones personalizadas  
- `logger_sistema.py` → Registro de logs  
- `main.py` → Pruebas del sistema en consola  
- `interfaz.py` → Interfaz gráfica del sistema  
- `logs.txt` → Archivo de registro de eventos  

---

## Ejecución

### Modo consola

Permite ejecutar pruebas completas del sistema:

```bash
python main.py
