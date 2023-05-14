from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self):
        return self.data

def build_semantic_tree(expression):
    root = TreeNode("EXPR")
    current = root
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isdigit():
            current.add_child(TreeNode("INT:" + char))
            i += 1
        elif char in ["+", "-", "*", "/"]:
            current.add_child(TreeNode("OP:" + char))
            current = current.children[-1]
            i += 1
        elif char == "(":
            current.add_child(TreeNode("EXPR"))
            current = current.children[-1]
            i += 1
        elif char == ")":
            current = current.parent
            i += 1
    return root

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("index.html", "r") as f:
                html = f.read()
                self.wfile.write(bytes(html, "utf-8"))
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode())
            inputString = post_data['inputString'][0]
            root = build_semantic_tree(inputString)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("output.html", "r") as f:
                html = f.read().format(inputString, str(root))
                self.wfile.write(bytes(html, "utf-8"))
        else:
            self.send_error(404)

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('Starting server...')
    httpd.serve_forever()
