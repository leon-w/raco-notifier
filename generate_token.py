import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import api


def get_user_code(client_id, port=12983):
    global code

    webbrowser.open(f'https://api.fib.upc.edu/v2/o/authorize?client_id={client_id}'
                    f'&redirect_uri=http://localhost:{port}&response_type=code&scope=read&approval_prompt=auto')

    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            global code
            code = parse_qs(urlparse(self.path).query)['code'][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Code registered')

        def log_message(self, *args):
            return

    httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    httpd.handle_request()
    return code


def generate_token():
    user_code = get_user_code(api.secrets["client_id"])
    token = api.Token.from_user_code(user_code)
    token.save_to_file(api.TOKEN_FILE)


if __name__ == '__main__':
    generate_token()
