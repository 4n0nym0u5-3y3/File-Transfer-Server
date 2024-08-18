import http.server
import socketserver
import socket
import ssl
import os
import cgi
import shutil
import logging
from urllib.parse import unquote

# Configurazione
PORT = 4433
UPLOAD_DIR = "uploads"
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"
LOG_FILE = "file_sharing.log"

# Creazione della cartella di upload se non esiste
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Configurazione del logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

class FileSharingHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        # Gestisce il caricamento dei file
        content_type, _ = cgi.parse_header(self.headers['Content-Type'])
        if content_type == 'multipart/form-data':
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            filename = form['file'].filename
            file_data = form['file'].file.read()

            with open(os.path.join(UPLOAD_DIR, filename), 'wb') as f:
                f.write(file_data)

            # Log dell'evento
            logging.info(f"File caricato: {filename}")

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Upload completato con successo")
        else:
            self.send_response(400)
            self.end_headers()

    def list_directory(self, path):
        # Lista sicura dei file nella directory
        try:
            file_list = os.listdir(path)
        except OSError:
            self.send_error(404, "Directory non trovata")
            return None
        file_list.sort(key=lambda a: a.lower())
        display_path = unquote(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        out = []
        out.append(f'<html><head><title>File in {display_path}</title></head>')
        out.append('<body><h2>Lista dei file disponibili</h2>')
        out.append('<ul>')
        for name in file_list:
            fullname = os.path.join(path, name)
            display_name = name
            out.append(f'<li><a href="{display_name}">{display_name}</a></li>')
        out.append('</ul>')
        out.append('</body></html>')
        self.wfile.write("".join(out).encode('utf-8'))
        return None

    def translate_path(self, path):
        # Prevenzione degli attacchi di directory traversal
        path = super().translate_path(path)
        if os.path.commonpath([os.path.abspath(UPLOAD_DIR), os.path.abspath(path)]) != os.path.abspath(UPLOAD_DIR):
            return UPLOAD_DIR
        return path

# Generazione del QR code per l'accesso
def generate_qr_code(ip):
    import pyqrcode
    url = f"https://{ip}:{PORT}"
    qr_code = pyqrcode.create(url)
    qr_code.png("server_qr.png", scale=6)
    return url

# Configurazione del server
with socketserver.TCPServer(("", PORT), FileSharingHandler) as httpd:
    # Wrap SSL
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=CERT_FILE, keyfile=KEY_FILE, server_side=True)

    # Ottenere l'indirizzo IP del server
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    server_url = generate_qr_code(ip_address)

    # Informazioni sul server
    print(f"Server attivo su {server_url}")
    print("Scansiona il QR code nel file 'server_qr.png' per accedere.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server in chiusura...")
    finally:
        httpd.server_close()
