# Guía Técnica - Mirror Sync Avanzado

Arquitectura:
- Peer-to-peer simétrico. Cada peer corre un servidor TLS y un cliente que conecta al otro peer.
- Watchdog detecta cambios y envía header+content sobre TCP/TLS.

Protocolo:
- [8 bytes BE header_len] [header json bytes] [8 bytes BE content_len] [content bytes]
- Header JSON contiene: id, action, path, timestamp, size, hash, sender, compressed

Consistencia y recuperación:
- Cada operación espera ACK {"status":"ok"}.
- Si falla, se guarda en tabla 'pending' y se reintenta periódicamente.
- Archivos grandes se comprimen con gzip al enviar.

Bases de datos:
- SQLite con tablas 'log' y 'pending' (ver src/db.py)

Mejoras propuestas:
- Implementar mutual TLS, delta binary diffs, autenticación de usuario, compresión por chunks, y verificación por bloques.
