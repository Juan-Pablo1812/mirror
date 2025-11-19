# locker.py - simple portalocker wrapper
import portalocker, os

def lock_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    f = open(path, 'a+b')
    portalocker.lock(f, portalocker.LOCK_EX)
    return f

def unlock_file(f):
    try:
        portalocker.unlock(f)
        f.close()
    except Exception:
        pass
