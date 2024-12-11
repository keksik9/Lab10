import os
from dotenv import load_dotenv
import psutil
from http.server import HTTPServer, BaseHTTPRequestHandler

load_dotenv()

EXPORTER_HOST = os.environ.get('EXPORTER_HOST', '0.0.0.0')
EXPORTER_PORT = int(os.environ.get('EXPORTER_PORT', '8081'))

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            cpu_usage = psutil.cpu_percent()

            mem_info = psutil.virtual_memory()
            memory_total = mem_info.total
            memory_used = memory_total - mem_info.available

            disk_info = psutil.disk_usage('/')
            disk_total = disk_info.total
            disk_used = disk_info.used

            metrics = f"""# HELP cpu_usage CPU usage percentage
        # TYPE cpu_usage gauge
        cpu_usage {cpu_usage}
        
        # HELP memory_total Total system memory in bytes
        # TYPE memory_total gauge
        memory_total {memory_total}
        
        # HELP memory_used Used system memory in bytes
        # TYPE memory_used gauge
        memory_used {memory_used}
        
        # HELP disk_total Total disk space in bytes
        # TYPE disk_total gauge
        disk_total {disk_total}
        
        # HELP disk_used Used disk space in bytes
        # TYPE disk_used gauge
        disk_used {disk_used}
        """

            self.send_response(200)
            self.send_header('Content-type', 'text/plain; version=0.0.4')
            self.end_headers()
            self.wfile.write(metrics.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print(f"Starting exporter on {EXPORTER_HOST}:{EXPORTER_PORT}")
    server = HTTPServer((EXPORTER_HOST, EXPORTER_PORT), MetricsHandler)
    print(f"Exporter running on http://{EXPORTER_HOST}:{EXPORTER_PORT}/")
    server.serve_forever()
