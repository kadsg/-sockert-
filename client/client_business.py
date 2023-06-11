import os
import socket


# 客户端业务逻辑
class ClientBusiness:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_connected = False
        self.client_socket = None

    # 连接到服务器
    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.is_connected = True

    # 关闭连接
    def close_connection(self):
        self.client_socket.close()
        self.is_connected = False

    # 发送文件
    def send_file(self, file_path):
        send_flag = False
        # 打开文件并发送
        with open(file_path, 'rb') as f:
            # 如果连接没有建立
            if not self.is_connected:
                self.connect_to_server()

            # 首先发送文件名，让server创建临时文件
            if not send_flag:
                # 发送文件名
                filename = os.path.basename(file_path)
                self.client_socket.sendall(filename.encode())
                send_flag = True

            # 发送文件数据
            length = 0
            chunk = b''
            while True:
                # 一次读取1024字节的数据
                data = f.read(1024)
                # 追加到chunk中
                chunk += data
                length += len(data)
                if not data:  # 读完了文件，退出循环
                    print(f"{length} 字节的数据将发送至客户端...")
                    self.client_socket.sendall(chunk)  # 发送数据
                    # 关闭写入通道，告诉Server数据已经发送完毕
                    self.client_socket.shutdown(socket.SHUT_WR)
                    break

    # 返回接收压缩后的文件和文件类型过滤器
    def receive_compressed_file(self):
        # 接收Server返回的数据
        compressed_data = b""
        while True:
            data = self.client_socket.recv(1024)
            if not data:  # 数据接收完毕，退出循环
                break
            compressed_data += data

        # TODO: 暂时写定文件类型过滤器为ZIP文件
        # 文件类型过滤器
        options = {
            'defaultextension': '.zip',
            'filetypes': [('ZIP files', '*.zip'), ('All files', '*.*')],
        }

        return compressed_data, options  # 返回压缩后的数据

    # 发送文件并返回压缩后的文件
    def handle(self, file_name):
        self.send_file(file_name)
        return self.receive_compressed_file()
