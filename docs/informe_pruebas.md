
# Informe de Pruebas – MirrorSync

Este informe documenta pruebas básicas realizadas para verificar el correcto funcionamiento del sistema de sincronización MirrorSync. Cada prueba simula una acción común (crear, modificar, borrar archivos) y observa si el cambio se replica correctamente en el otro equipo (peer).

---

## Entorno de prueba

- **Peer A**: Cliente en WSL (Linux), carpeta `watched/`
- **Peer B**: Servidor en Windows, carpeta `synced/`
- Ambos dispositivos están conectados en red local
- MirrorSync está ejecutándose en ambos extremos

---

## Caso 1: Crear un archivo nuevo

**Objetivo:** Verificar que un archivo nuevo creado en A se sincroniza automáticamente en B.

### Pasos:
1. En Peer A (WSL), crear un archivo:
   ```bash
   echo "Hola desde A" > watched/archivo1.txt
   ```

2. Esperar unos segundos.

### Resultado esperado:
- En Peer B, aparece `archivo1.txt` dentro de la carpeta `synced/`
- El contenido del archivo es idéntico
- Se muestra una notificación visual (si GUI está activa)
- Se registra en el log o base de datos

---

## Caso 2: Modificar un archivo existente

**Objetivo:** Verificar que los cambios en un archivo ya sincronizado se actualizan en el peer remoto.

### Pasos:
1. En Peer A:
   ```bash
   echo "Línea nueva" >> watched/archivo1.txt
   ```

2. Esperar unos segundos.

### Resultado esperado:
- En Peer B, el archivo `archivo1.txt` se actualiza con el nuevo contenido
- Se muestra una notificación de actualización
- Se registra un nuevo evento en el log

---

## Caso 3: Borrar un archivo

**Objetivo:** Verificar que la eliminación de un archivo en A se refleja en B.

### Pasos:
1. En Peer A:
   ```bash
   rm watched/archivo1.txt
   ```

2. Esperar unos segundos.

### Resultado esperado:
- En Peer B, el archivo `archivo1.txt` también se elimina
- Se registra un evento de tipo `"action": "delete"` en el log
- Se muestra una notificación (si está habilitada)

> Nota: Esta funcionalidad depende de que el sistema esté configurado para replicar eliminaciones. Si no está implementada, el archivo en B permanecerá.

---

## Caso 4: Desconexión de red

**Objetivo:** Verificar que si el peer remoto está desconectado, las operaciones se guardan y se reintentan automáticamente.

### Pasos:
1. Apagar temporalmente el servidor (Peer B) o desconectar la red
2. En Peer A:
   ```bash
   echo "Archivo offline" > watched/offline.txt
   ```

3. Esperar unos segundos y luego volver a conectar el servidor

### Resultado esperado:
- El archivo `offline.txt` no se puede enviar de inmediato
- Se guarda en la tabla `pending` de la base de datos
- Cuando el servidor se reconecta, el archivo se reenvía automáticamente
- Se elimina de `pending` y se registra como sincronizado

---

## Observaciones adicionales

- Todos los eventos deben generar un log interno (en consola, archivo o base de datos)
- Si el archivo ya existe y es idéntico (mismo hash), no se reenvía
- Si hay errores (por ejemplo, archivo bloqueado), deben registrarse sin detener el sistema

