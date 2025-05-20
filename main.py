import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read and decode form data
        data = self.rfile.read(int(self.headers["Content-Length"]))
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        print(data_dict)
        # Path to the directory and file
        storage_dir = pathlib.Path("storage")
        storage_dir.mkdir(exist_ok=True)
        data_file = storage_dir / "data.json"

        # Get current timestamp as key
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Read existing data
        if data_file.exists():
            try:
                with open(data_file, "r", encoding="utf-8") as f:
                    all_data = json.load(f)
                    if not isinstance(all_data, dict):
                        all_data = {}
            except json.JSONDecodeError:
                all_data = {}
        else:
            all_data = {}

        # Add new record with timestamp
        all_data[timestamp] = data_dict

        # Save data to JSON file
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

        # Redirect back to "/"
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        elif pr_url.path == "/read":
            self.render_messages_page()
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def render_messages_page(self):
        data_file = pathlib.Path("storage") / "data.json"

        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        # Set up Jinja2 template enviroment
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("messages.html")

        # Render HTML using template
        html = template.render(data=data)

        # Send HTTP response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        print("Server started! On http://localhost:3000")
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
