from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/changeip":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("Request received on /changeip\n")
            global index, danhsach, port
            if index < len(danhsach):
                os.system(f'bash upstream.sh "{danhsach[index].split(":")[:1]}" "{danhsach[index].split(":")[2:]}" "{port}"')
                index += 1
            else:
                index = 0
                os.system(f'bash upstream.sh "{danhsach[index].split(":")[:1]}" "{danhsach[index].split(":")[2:]}" "{port}"')
                index += 1
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("404 Not Found\n")
index = 0
if __name__ == "__main__":
    danhsach = []
    path = input("Nhập đường dẫn file danh sách proxy (ip:port:user:pass): ")
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                danhsach.append(line.strip())
    else:
        print("File không tồn tại")
        quit()
    port = input("Nhập port cố định: ")
    os.system(f'bash upstream.sh "{danhsach[index].split(":")[:1]}" "{danhsach[index].split(":")[2:]}" "{port}"')
    index += 1
    server_address = ('0.0.0.0', 1234)
    httpd = HTTPServer(server_address, SimpleHandler)

    print("Server running at http://127.0.0.1:1234...")
    httpd.serve_forever()
