# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ssl
import os
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/changeip":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            global index, danhsach, port, chaylai
            if index < len(danhsach):
                self.wfile.write("Request received on /changeip\n")
                os.system('bash upstream.sh "{}" "{}" "{}"'.format(":".join(danhsach[index].split(":")[:2]),":".join(danhsach[index].split(":")[2:]), port))
                index += 1
            elif not chaylai:
                self.wfile.write("Cannot change (out of proxy)\n")
            else:
                self.wfile.write("Request received on /changeip\n")
                index = 0
                os.system('bash upstream.sh "{}" "{}" "{}"'.format(":".join(danhsach[index].split(":")[:2]),":".join(danhsach[index].split(":")[2:]), port))
                index += 1
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("404 Not Found\n")
index = 0
if __name__ == "__main__":
    danhsach = []
    path = raw_input("Nhập đường dẫn file danh sách proxy (ip:port:user:pass): ")
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                danhsach.append(line.strip())
    else:
        print("File không tồn tại")
        quit()
    port = raw_input("Nhập port cố định: ")
    chaylai = raw_input("Chạy lại từ đầu sau khi hết danh sách proxy? (y/n): ")
    if chaylai.lower() == 'y':
        chaylai = True
    else:
        chaylai = False
    os.system('bash upstream.sh "{}" "{}" "{}"'.format(":".join(danhsach[index].split(":")[:2]),":".join(danhsach[index].split(":")[2:]), port))
    index += 1
    server_address = ('0.0.0.0', 1234)
    httpd = HTTPServer(server_address, SimpleHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile="server.key",    # Đường dẫn đến khóa riêng
                                   certfile="server.crt",   # Đường dẫn đến chứng chỉ SSL
                                   server_side=True)

    print("Server running at http://127.0.0.1:1234...")
    print("LINK CHANGE IP: http://IP:1234/changeip")
    httpd.serve_forever()
