import zipfile
import socket


class ServerBusiness:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    # 开始监听
    def open_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        return self.server_socket

    # 接收客户端发送的文件名
    def receive_file_name(self, client_socket):
        filename = client_socket.recv(1024).decode()
        return filename

    # 接收客户端发送的文件
    def receive_file(self, client_socket, file_path):
        with open(file_path, 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)

    # 关闭服务端的连接
    def close(self):
        self.server_socket.close()

    # 对文件进行压缩后保存到临时目录中
    # 返回压缩后的文件路径
    def compress_file(self, file_path):
        # 压缩文件
        # TODO: 写定为zip压缩，后续可以考虑使用其他压缩算法
        compressed_file_path = file_path + '.zip'
        with zipfile.ZipFile(compressed_file_path, mode='w', compression=zipfile.ZIP_DEFLATED) as compressed_data:
            compressed_data.write(file_path)

        return compressed_file_path

    # 向客户端发送压缩后的文件
    def send_compressed_file(self, client_socket, file_path):
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
