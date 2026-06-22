# Cafetería - El Rincón

Sistema de gestión para restaurante con reservas en línea, menú dinámico, reseñas y panel de administración.
Desarrollado con Flask, MySQL y JWT.

---

## Estado del Proyecto

El proyecto se encuentra en **fase final**.
Incluye funcionalidades completas de reservas, gestión de menú, moderación de reseñas y un dashboard de estadísticas para el administrador.

---

## Enlaces Útiles

- **Swagger Editor**: Herramienta recomendada para visualizar el contrato swagger.yaml adjunto en el proyecto.

---

## ¿Por qué este proyecto?

El objetivo es ofrecer una solución integral para un restaurante que desee digitalizar la experiencia del cliente, permitiendo:
- **Reservas rápidas** sin necesidad de registro.
- **Consulta de menú** en línea con imágenes y precios.
- **Administración completa** del negocio desde un panel privado.
- **Moderación de reseñas** para mantener la calidad de los comentarios.

---

## Proceso de Uso

- **Reservas**: Un cliente ingresa fecha, horario y cantidad de personas. Recibe un código QR por email para confirmar su asistencia.
- **Menú**: El administrador puede agregar, editar o eliminar platos con imágenes y precios.
- **Reseñas**: Los clientes pueden dejar reseñas después de asistir a una reserva. El administrador las modera antes de publicarlas.
- **Dashboard**: El administrador visualiza estadísticas de reservas, cancelaciones, comensales y valoraciones.

---

## Instalación

Es necesario contar con **Python 3.10+** y **MySQL** instalados en el sistema.

### Clonar el repositorio

```bash
git clone git@github.com:emivaleriano/proyecto_cafeteria.git
cd proyecto_cafeteria
```

### Configurar el entorno

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Variables de entorno

Crear un archivo `.env` en la carpeta `backend/` basado en el `template.env`:

```env
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=cafeteria
MYSQL_USERNAME=root
MYSQL_PASSWORD=root123
MYSQL_HOST=localhost
MYSQL_PORT=3306

BACKEND_PORT=5000
JWT_SECRET=cambiar-a-clave
JWT_EXP_HORAS=1
```

### Levantar la Base de Datos

```bash
mysql -u root -p < db_scheme.sql
```

### Crear usuario administrador (una sola vez)

```bash
python -m backend.scripts.creacion_primer_admin
```

---

## Documentación de Uso

### Iniciar el servidor backend

```bash
python -m backend.app
```

### Iniciar el servidor frontend

```bash
python -m frontend.app
```

### Credenciales del administrador

| Campo | Valor |
|-------|-------|
| **Usuario** | `admin` |
| **Contraseña** | `admin` |

### Ejemplos de Endpoints

#### Login del administrador

```bash
curl -X POST http://localhost:5000/admin/login \
  -H "Content-Type: application/json" \
  -d '{"usuario": "admin", "contrasenia": "admin"}'
```

#### Obtener dashboard

```bash
curl -X GET http://localhost:5000/admin/dashboard \
  -H "Authorization: Bearer <token>"
```

#### Crear una reserva

```bash
curl -X POST http://localhost:5000/reservas \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Ana", "email": "ana@mail.com", "fecha_hora": "2026-06-15 20:00:00", "cantidad_personas": 4}'
```

#### Listar platos del menú

```bash
curl http://localhost:5000/menu
```

---

## Tecnologías utilizadas

| Capa | Tecnología |
|------|------------|
| Backend | Flask, Python |
| Frontend | HTML5, CSS3, Jinja2 |
| Base de datos | MySQL |
| Autenticación | JWT, bcrypt |
| Control de versiones | Git, GitHub |

---

## Licencia

Este proyecto está bajo la Licencia BSD 3-Clause. Consulta el archivo LICENSE.md para más información.

---
