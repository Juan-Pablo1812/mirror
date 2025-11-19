# Manual de Usuario - Mirror Sync Avanzado

Requisitos:
- Python 3.9+
- pip
- Visual Studio (opcional) o ejecutar con Python directamente
- Dependencias: ver src/requirements.txt

Instalación:
1. Crear entorno virtual:
   python -m venv venv
   venv\Scripts\activate   (Windows) OR source venv/bin/activate (Linux)
2. Instalar dependencias:
   pip install -r src/requirements.txt
3. Configurar:
   - Editar src/main.py si lo deseas (IP del peer, puerto, carpeta a sincronizar)
4. Ejecutar:
   python src/main.py

Notas:
- Para TLS puedes generar certificados y apuntar a ellos en SyncCore (parámetros certfile/keyfile).
- El proyecto registra eventos en sync.log en la carpeta donde ejecutes.
