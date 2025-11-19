
# Manual de Usuario – MirrorSync Avanzado

MirrorSync es una herramienta de sincronización de archivos entre dos computadoras (peers), diseñada para ser multiplataforma, segura y fácil de usar. Este manual te guiará paso a paso para instalar, configurar y ejecutar el sistema, incluso si tienes poca experiencia con programación.

---

## Requisitos previos

Antes de comenzar, asegúrate de tener lo siguiente instalado en tu computadora:

- **Python 3.9 o superior**  
  Puedes verificarlo con:
  ```bash
  python --version
  ```

- **pip** (el gestor de paquetes de Python)  
  Verifica con:
  ```bash
  pip --version
  ```

- **Visual Studio (opcional)**  
  Solo si deseas compilar o depurar desde un entorno gráfico. No es obligatorio.

- **Dependencias del proyecto**  
  Están listadas en el archivo `src/requirements.txt`. Se instalarán automáticamente más adelante.

---

## Instalación paso a paso

### 1. Crear un entorno virtual

Esto aísla las dependencias del proyecto para evitar conflictos con otros programas.

- En **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- En **Linux o WSL**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

> Si ves que el prompt cambia (por ejemplo, aparece `(venv)` al inicio), ¡todo está listo!

---

### 2. Instalar las dependencias

Con el entorno virtual activado, instala los paquetes necesarios:

```bash
pip install -r src/requirements.txt
```

Esto instalará bibliotecas como `watchdog`, `portalocker`, `plyer`, entre otras.

---

### 3. Configurar el sistema

Abre el archivo `src/main.py` en tu editor favorito (por ejemplo, VS Code o Notepad++) y busca las siguientes líneas:

```python
watch_dir = "watched"
peer_ip = "192.168.1.100"
peer_port = 9000
listen_port = 9001
```

Modifica según tu red local:

- `watch_dir`: carpeta que deseas sincronizar
- `peer_ip`: dirección IP del otro equipo
- `peer_port`: puerto al que se conecta tu cliente
- `listen_port`: puerto en el que tu servidor escucha

> Asegúrate de que ambos peers tengan configuraciones complementarias (el puerto de escucha de uno debe coincidir con el puerto de conexión del otro).

---

### 4. Ejecutar el sistema

Con todo configurado, ejecuta el programa:

```bash
python src/main.py
```

Si todo está bien, verás mensajes en consola indicando que el servidor está escuchando y que el sistema está monitoreando la carpeta.

---

## Notas sobre seguridad (TLS)

MirrorSync puede usar conexiones seguras (TLS) si lo deseas. Para ello:

1. Genera un certificado y una clave privada (por ejemplo, usando `openssl`)
2. Pasa las rutas como parámetros al crear `SyncCore`:
   ```python
   certfile="cert.pem", keyfile="key.pem"
   ```

Esto cifra la comunicación entre peers para mayor seguridad.

---

## Registro de eventos

MirrorSync guarda un archivo de log llamado `sync.log` en la misma carpeta desde donde ejecutas el programa. Allí se registran:

- Archivos enviados y recibidos
- Errores o conflictos
- Reintentos por desconexión

Puedes revisar este archivo para depurar o auditar el comportamiento del sistema.

---

## Consejos adicionales

- Usa carpetas como `watched/` y `synced/` para mantener tu estructura organizada
- Si usas WSL, puedes editar archivos desde Windows y ver los cambios reflejados en tiempo real
- Puedes ejecutar MirrorSync en modo consola o con interfaz gráfica (`main.py` vs `client_console.py`)

