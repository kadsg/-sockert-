import os
import shutil
import server_business as business
from server.business_zip import BusinessZIP


# 服务端
class Server:
    def __init__(self, host, port):
        self.host = host  # 监听的IP地址，为空则表示监听本机所有IP
        self.port = port  # 监听的端口号
        self.server_socket = None  # 服务端socket
        # 此处可更换压缩策略
        self.business = BusinessZIP(self.host, self.port)  # 服务端业务逻辑

    def start(self):
        self.server_socket = self.business.open_server()  # 启动服务
        print('开始监听...')

        while True:
            client_socket, addr = self.server_socket.accept()  # 接收客户端连接
            print(f'收到来自：{addr} 的请求！')

            path = f'serverFor/{addr}'  # 临时文件夹路径
            # 如果临时文件夹不存在，则创建
            if not os.path.exists(path):
                os.makedirs(path)

            try:
                filename = self.business.receive_file_name(client_socket)  # 接收文件名
                file_path = os.path.join(path, filename)  # 设置保存到服务器上的临时文件路径
                self.business.receive_file(client_socket, file_path)  # 接收并写入客户端发送的文件
                compressed_file_path = self.business.compress_file(file_path)  # 压缩文件并返回压缩后的文件路径
                self.business.send_compressed_file(client_socket, compressed_file_path)  # 向客户端发送压缩后的文件

                # 删除服务器临时文件夹
                shutil.rmtree(path)
                print(f'为客户端{addr}的请求提供服务完毕！')
            except ConnectionResetError:
                print(f'与客户端{addr}的连接被终止！')

            client_socket.close()  # 关闭客户端连接


def main():
    host = ''  # 监听的IP地址，为空则表示监听本机所有IP
    port = 8000  # 监听的端口号

    server = Server(host, port)
    server.start()


if __name__ == '__main__':
    main()
