# Fase 4 - Programacion - Sistema Software FJ

Sistema integral orientado a objetos para gestionar clientes, servicios y reservas de la empresa ficticia Software FJ.

## Requisitos implementados

- Clase abstracta general `EntidadSistema`.
- Clase `Cliente` con encapsulacion y validaciones robustas.
- Clase abstracta `Servicio`.
- Tres servicios especializados:
  - `ReservaSala`
  - `AlquilerEquipo`
  - `AsesoriaEspecializada`
- Clase `Reserva` que integra cliente, servicio, duracion y estado.
- Confirmacion, cancelacion y procesamiento de reservas.
- Excepciones personalizadas.
- Uso de `try/except`, `try/except/else/finally` y encadenamiento de excepciones.
- Archivo `logs.txt` para eventos y errores.
- Mas de 10 operaciones de prueba en `main.py`.
- No utiliza bases de datos.

## Como ejecutar

```bash
python main.py
```

## Archivos principales

- `entidad.py`: clase abstracta general.
- `cliente.py`: gestion y validacion de clientes.
- `servicio.py`: servicios abstractos y especializados.
- `reserva.py`: gestion de reservas.
- `excepciones.py`: excepciones personalizadas.
- `logger_sistema.py`: registro de logs.
- `main.py`: pruebas de ejecucion.

## Enlace del repositorio

https://github.com/KRONOXXX99/fase4-programacion-grupo.git
