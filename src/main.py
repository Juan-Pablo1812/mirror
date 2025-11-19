# main.py - PyQt5 GUI for Mirror Sync
import sys, os, threading, hashlib
from PyQt5 import QtWidgets, QtCore
from plyer import notification
from sync_core import SyncCore
from db import init_db

DEFAULT_WATCH = os.path.abspath(os.path.join(os.getcwd(), '..', 'watched'))
if not os.path.exists(DEFAULT_WATCH):
    os.makedirs(DEFAULT_WATCH, exist_ok=True)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MirrorSync - Avanzado')
        self.resize(800, 600)
        layout = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QHBoxLayout()
        self.dir_edit = QtWidgets.QLineEdit(DEFAULT_WATCH)
        btn_browse = QtWidgets.QPushButton('Cambiar')
        btn_browse.clicked.connect(self.browse)
        form.addWidget(self.dir_edit)
        form.addWidget(btn_browse)
        layout.addLayout(form)

        h2 = QtWidgets.QHBoxLayout()
        self.peer_edit = QtWidgets.QLineEdit('127.0.0.1')
        self.port_edit = QtWidgets.QLineEdit('9001')
        h2.addWidget(QtWidgets.QLabel('Peer IP:'))
        h2.addWidget(self.peer_edit)
        h2.addWidget(QtWidgets.QLabel('Port:'))
        h2.addWidget(self.port_edit)
        layout.addLayout(h2)

        btns = QtWidgets.QHBoxLayout()
        self.start_btn = QtWidgets.QPushButton('Iniciar')
        self.stop_btn = QtWidgets.QPushButton('Detener')
        self.syncall_btn = QtWidgets.QPushButton('Forzar resync')
        btns.addWidget(self.start_btn)
        btns.addWidget(self.stop_btn)
        btns.addWidget(self.syncall_btn)
        layout.addLayout(btns)

        self.log_view = QtWidgets.QPlainTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)

        self.start_btn.clicked.connect(self.start_sync)
        self.stop_btn.clicked.connect(self.stop_sync)
        self.syncall_btn.clicked.connect(self.sync_all)

        self.core = None
        self.db = init_db(os.path.join(os.getcwd(), 'sync.db'))

        # timer to refresh logs
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh_logs)
        self.timer.start(1000)

    def browse(self):
        d = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder', self.dir_edit.text())
        if d:
            self.dir_edit.setText(d)

    def start_sync(self):
        watch = self.dir_edit.text().strip()
        peer = self.peer_edit.text().strip()
        try:
            port = int(self.port_edit.text().strip())
        except:
            port = 9001
        if self.core and self.core.running:
            self.append_log('Ya está corriendo')
            return
        self.core = SyncCore(
            watch, peer, port, port,
            certfile=None,
            keyfile=None,
            db_path=os.path.join(os.getcwd(), 'sync.db'),
            log_path=os.path.join(os.getcwd(), 'sync.log'),
            on_file_received=self.handle_file_received  # callback para notificación
        )
        t = threading.Thread(target=self.core.start, daemon=True)
        t.start()
        self.append_log('Iniciado SyncCore')

    def stop_sync(self):
        if self.core:
            self.core.stop()
            self.append_log('Detenido SyncCore')

    def sync_all(self):
        root = self.dir_edit.text().strip()
        for rootdir, dirs, files in os.walk(root):
            for fn in files:
                path = os.path.join(rootdir, fn)
                try:
                    os.utime(path, None)
                except:
                    pass
        self.append_log('Forzado resync (touch)')

    def append_log(self, s):
        self.log_view.appendPlainText(s)

    def refresh_logs(self):
        path = os.path.join(os.getcwd(), 'sync.log')
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
                self.log_view.setPlainText(data)
            except:
                pass

    def handle_file_received(self, filename, data):
        path = os.path.join(os.getcwd(), 'synced', filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    existing = f.read()
                if hashlib.sha256(existing).digest() == hashlib.sha256(data).digest():
                    self.append_log(f"[SKIP] {filename} ya existe y es idéntico")
                    return
            except:
                pass

        with open(path, 'wb') as f:
            f.write(data)

        notification.notify(
            title="Archivo sincronizado",
            message=f"{filename} guardado correctamente.",
            timeout=5
        )
        self.append_log(f"[SYNC] {filename} guardado")

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()