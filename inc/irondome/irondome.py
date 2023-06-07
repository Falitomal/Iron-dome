import os
import sys
import time
import argparse
import psutil
import logging
import resource
from daemon import DaemonContext
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuración del registro de logs.
log_file = "/var/log/irondome/irondome.log"
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO)

class FileChangeHandler(FileSystemEventHandler):
    """Clase que maneja los eventos del sistema de archivos."""

    def __init__(self, extensions):
        self.extensions = extensions

    def on_created(self, event):
        """Método que se activa cuando se detecta la creación de un archivo."""
        if not event.is_directory and any(event.src_path.endswith(ext) for ext in self.extensions):
            logging.info(f'Archivo creado: {event.src_path}')

    def on_deleted(self, event):
        """Método que se activa cuando se detecta la eliminación de un archivo."""
        if not event.is_directory and any(event.src_path.endswith(ext) for ext in self.extensions):
            logging.info(f'Archivo eliminado: {event.src_path}')

    def on_modified(self, event):
        """Método que se activa cuando se detecta un cambio en un archivo."""
        if not event.is_directory and any(event.src_path.endswith(ext) for ext in self.extensions):
            logging.info(f'Archivo modificado: {event.src_path}')


def get_args():
    parser = argparse.ArgumentParser(
        prog='Iron Dome',
        description='This program will monitor a critical zone in perpetuity.',
    )
    parser.add_argument('route', type=str, metavar='ROUTE')
    parser.add_argument('extensions', type=str, nargs='*', metavar='FILE_EXTENSION')
    parser.add_argument('-i', '--interval', type=int, default=1)
    return parser.parse_args()


def run_daemon(route, extensions, interval):
    # Crear el observador de eventos.
    observer = Observer()

    # Configurar el observador para que use nuestro manejador de eventos,
    # y para que vigile el directorio que se especificó.
    event_handler = FileChangeHandler(extensions)
    observer.schedule(event_handler, route, recursive=True)

    # Iniciar el observador.
    observer.start()
    try:
        while True:
            # Reportar el uso de CPU, memoria y disco.
            cpu_usage = psutil.cpu_percent(interval=interval)
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            logging.info(f'Uso de CPU: {cpu_usage}%, Uso de memoria: {memory_usage}%, Uso de disco: {disk_usage}%')

            # Comprobar el uso de la memoria cada 10 segundos.
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > 100000000:
                logging.info('Uso de memoria superior a 100 MB, terminando...')
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Este programa solo puede ser ejecutado por el usuario root.")
        sys.exit(1)
        
    args = get_args()
    with DaemonContext(stdout=sys.stdout, stderr=sys.stderr):
        print(f'PID:{os.getpid()}')
        run_daemon(args.route, args.extensions, args.interval)
