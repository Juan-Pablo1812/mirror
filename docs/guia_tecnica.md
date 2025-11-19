
# Guía Técnica – MirrorSync Avanzado

MirrorSync es una herramienta de sincronización de archivos entre dos computadoras (peers), diseñada para ser multiplataforma, segura y eficiente. Esta guía explica su funcionamiento técnico de forma accesible para quienes tienen conocimientos básicos de programación.

---

## Arquitectura General

MirrorSync utiliza una arquitectura **peer-to-peer simétrica**, lo que significa que ambos dispositivos se comportan igual: cada uno puede enviar y recibir archivos.

- **Servidor TLS**: Cada peer ejecuta un servidor que escucha conexiones seguras (TLS).
- **Cliente TCP**: Cada peer también actúa como cliente, conectándose al otro peer para enviar archivos.
- **Detección de cambios**: Se usa la biblioteca `watchdog` para monitorear una carpeta local. Cuando se detecta un cambio (nuevo archivo o modificación), se inicia el proceso de sincronización.

### Ejemplo:
Si modificas un archivo en la carpeta `watched/`, MirrorSync lo detecta y lo envía automáticamente al otro peer.

---

## Protocolo de Comunicación

MirrorSync usa un protocolo personalizado para enviar archivos. Cada transmisión incluye:

```
[8 bytes BE header_len] [header JSON] [8 bytes BE content_len] [contenido del archivo]
```

### ¿Qué significa esto?

- **BE**: Big Endian, una forma de representar números en bytes.
- **header_len**: Tamaño del encabezado (en bytes).
- **header JSON**: Información sobre el archivo.
- **content_len**: Tamaño del contenido del archivo.
- **content bytes**: El archivo en sí.

### Estructura del encabezado (header JSON):

```json
{
  "id": "uuid único",
  "action": "create | update | delete",
  "path": "ruta relativa del archivo",
  "timestamp": "fecha y hora",
  "size": "tamaño en bytes",
  "hash": "hash SHA256 del contenido",
  "sender": "nombre del peer",
  "compressed": true
}
```

---

## Consistencia y Recuperación

Para asegurar que los archivos lleguen correctamente:

- Cada operación espera una respuesta tipo `{"status":"ok"}` como confirmación.
- Si no se recibe el ACK, el archivo se guarda en una tabla llamada `pending` y se reintenta más tarde.
- Los archivos grandes se comprimen con `gzip` antes de enviarse, para ahorrar ancho de banda.

### Ejemplo:
Si el peer remoto está desconectado, el archivo se guarda como pendiente y se reenvía automáticamente cuando se restablece la conexión.

---

## Base de Datos Interna

MirrorSync usa **SQLite**, una base de datos liviana que no requiere instalación adicional.

### Tablas principales:

- **log**: Registra cada archivo enviado o recibido, con su estado y metadatos.
- **pending**: Guarda archivos que no pudieron enviarse, para reintento automático.

Puedes ver la implementación en `src/db.py`.

---

## Mejoras Propuestas (para desarrolladores)

Estas son ideas para mejorar MirrorSync en futuras versiones:

- **Mutual TLS**: Autenticación mutua entre peers usando certificados.
- **Delta binary diffs**: Enviar solo las partes modificadas de un archivo, no el archivo completo.
- **Autenticación de usuario**: Requiere login para usar la herramienta.
- **Compresión por chunks**: Dividir archivos grandes en partes comprimidas.
- **Verificación por bloques**: Validar integridad por secciones, útil para archivos grandes o interrumpidos.

---

## ¿Qué necesitas para usar MirrorSync?

- Python 3.10 o superior
- Entorno virtual (`.venv`) con dependencias instaladas (`watchdog`, `portalocker`, `plyer`, etc.)
- Dos computadoras conectadas por red local o VPN
- Carpetas `watched/` y `synced/` configuradas correctamente


