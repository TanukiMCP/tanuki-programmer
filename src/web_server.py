import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "web_ui"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    # Change to the directory where web_ui is located
    # This assumes web_ui is in the same directory as src/web_server.py's parent
    # For this project structure, it means going up one level from src/
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving Tanuki-Programmer UI at http://localhost:{PORT}/")
        print(f"Serving files from directory: {DIRECTORY}")
        httpd.serve_forever()
