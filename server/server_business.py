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
    @staticmethod
    def receive_file_name(client_socket):
        filename = client_socket.recv(1024).decode()
        return filename

    # 接收客户端发送的文件
    @staticmethod
    def receive_file(client_socket, file_path):
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
    @staticmethod
    def compress_file(file_path):
        # 压缩文件
        pass  # 由子类实现

    # 向客户端发送压缩后的文件
    @staticmethod
    def send_compressed_file(client_socket, file_path):
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
