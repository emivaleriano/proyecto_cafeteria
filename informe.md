# Informe de Proyecto: Sistema de Reservas para Cafetería
Objetivo
El proyecto consiste en una aplicación web para la gestión de reservas de una cafetería. Permite a los clientes hacer reservas online y a los administradores del local gestionar el flujo completo del negocio desde un panel de control.
La aplicación está dividida en dos partes que se comunican mediante una API RESTful: un backend desarrollado en Flask que expone los endpoints, y un frontend también en Flask que consume esa API y renderiza las vistas con Jinja2.

**Integrantes:**
- Pablo Valentin Fraga, 115934
- Marco Pascual Grizzo Martinez, 114241
- Sofía Toledo, 114940
- Nadia Alejandra Romero Arvire, 115495

## Funciones principales

- Registro de usuarios a partir de la creación de reservas con selección de servicios adicionales
- Generación y envío de código QR por email para el check-in en el local
- Panel de administración para visualizar, confirmar, cancelar y actualizar reservas
- Gestión del menú (crear, editar, activar/desactivar platos)
- Gestión de servicios adicionales ofrecidos por el local
- Configuración de franjas horarias por día de la semana
- Sistema de reseñas post-visita enviado por email luego del check-in
- Estadísticas básicas en el dashboard (total de reservas, reservas del día, cancelaciones, reseñas)

## Tecnologías utilizadas

- Flask – framework principal tanto para el backend (API RESTful) como para el frontend (rutas y renderizado de templates)
- MySQL – base de datos relacional gestionada con mysql-connector-python
- Jinja2 – motor de templates para el renderizado HTML en el frontend
- Flask-Mail – envío de emails con templates HTML (confirmación de reserva, post check-in)
- qrcode + Pillow – generación de códigos QR adjuntos en los emails
- PyJWT + bcrypt – autenticación del administrador con tokens JWT y contraseñas hasheadas
- python-dotenv – gestión de variables de entorno

## Base de datos
La base de datos se llama *cafeteria* y contiene las siguientes tablas:
|  **Tabla**       |    **Descripción**                                                       |
|------------------|--------------------------------------------------------------------------|
| usuarios         | Datos de los clientes que realizan reservas (nombre, email, teléfono)|
| reservas         | Reservas registradas, con estado, cantidad de personas, servicios elegidos y código QR único|
| franjas_horarias | Horarios de apertura y cierre configurables por día de la semana|
| servicios        | Servicios adicionales ofrecidos por el local (pueden activarse o desactivarse)|
| menu             | Platos del menú con nombre, descripción, precio, categoría, tags e imagen|
| resenas          | Reseñas vinculadas a una reserva completada, con puntaje y comentario|
| administrador    | Credenciales del administrador del sistema|
| info_local       | Datos generales del local (nombre, dirección, capacidad máxima, contacto)|


**Endpoints desarrollados**: declarados en el archivo *swagger.yaml*

## Dificultades presentadas:

## Aprendizajes:

## Mejoras:

## Conclusion:
