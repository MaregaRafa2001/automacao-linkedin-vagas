from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = self.start_script()

    def start_script(self):
        return subprocess.Popen(["python", self.script])

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            print(f"🔄 Arquivo {self.script} modificado. Reiniciando...")
            self.process.kill()
            self.process = self.start_script()

if __name__ == "__main__":
    script = "main.py"  # Altere para o nome do seu script principal
    event_handler = ReloadHandler(script)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
