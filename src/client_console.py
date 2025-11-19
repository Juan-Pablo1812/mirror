import socket
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from locker import lock_file, unlock_file

WATCHED_DIR = "watched"
HOST = "127.0.0.1"
PORT = 9001

class SyncHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"[MODIFIED] {event.src_path}")
            send_file(event.src_path)

def send_file(path):
    try:
        lock_file(path)
        with open(path, "rb") as f:
            data = f.read()
        unlock_file(path)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(os.path.basename(path).encode() + b"\n" + data)
            print(f"[SENT] {path}")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    print(f"[START] Watching {WATCHED_DIR} → {HOST}:{PORT}")
    event_handler = SyncHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()