import os, socket, threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from locker import lock_file, unlock_file

class SyncCore:
    def __init__(self, watch_dir, peer_ip, peer_port, listen_port,
                 certfile=None, keyfile=None, db_path=None, log_path=None,
                 on_file_received=None):
        self.watch_dir = watch_dir
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.listen_port = listen_port
        self.running = False
        self.observer = None
        self.on_file_received = on_file_received

    def start(self):
        self.running = True
        self._start_watcher()
        self._start_server()

    def stop(self):
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()

    def _start_watcher(self):
        class Handler(FileSystemEventHandler):
            def __init__(self, outer):
                self.outer = outer

            def on_modified(self, event):
                if not event.is_directory:
                    self.outer._send_file(event.src_path)

        self.observer = Observer()
        self.observer.schedule(Handler(self), self.watch_dir, recursive=True)
        self.observer.start()

    def _send_file(self, path):
        try:
            lock_file(path)
            with open(path, 'rb') as f:
                data = f.read()
            unlock_file(path)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.peer_ip, self.peer_port))
                s.sendall(os.path.basename(path).encode() + b'\n' + data)
        except Exception as e:
            print(f"[ERROR] Envío fallido: {e}")

    def _start_server(self):
        def server_thread():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', self.listen_port))
                s.listen()
                while self.running:
                    try:
                        conn, addr = s.accept()
                        threading.Thread(target=self._handle_client, args=(conn,), daemon=True).start()
                    except:
                        break
        threading.Thread(target=server_thread, daemon=True).start()

    def _handle_client(self, conn):
        with conn:
            try:
                filename = b""
                while True:
                    byte = conn.recv(1)
                    if byte == b'\n':
                        break
                    filename += byte
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk

                if self.on_file_received:
                    self.on_file_received(filename.decode(), data)
                else:
                    self._default_save(filename.decode(), data)

            except Exception as e:
                print(f"[ERROR] Al recibir archivo: {e}")

    def _default_save(self, filename, data):
        path = os.path.join(os.getcwd(), 'synced', filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data)
        print(f"[SYNC] {filename} guardado")