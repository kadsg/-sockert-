import os
import socket
import zipfile

host = ''  # 监听所有可用的网络接口
port = 8000  # 监听的端口号

# 创建socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定IP地址和端口号
server_socket.bind((host, port))
# 开始监听
server_socket.listen()

print('开始监听...')

while True:
    # 接收Client的连接请求
    client_socket, addr = server_socket.accept()
    print(f'收到来自：{addr} 的请求')

    try:
        # 接收Client发送的文件名
        filename = client_socket.recv(1024).decode()
        path = 'server'

        if not os.path.exists(path):
            os.makedirs(path)

        # 接收Client发送的数据并写入文件（暂存至服务器）
        with open(os.path.join(path, filename), 'wb') as f:
            data = b''
            while True:
                chunk = client_socket.recv(1024)
                # 如果接收到的数据为空，则退出循环
                if not chunk:
                    print(f'接收完毕，共接收{len(data)}字节的数据！')
                    break
                data += chunk
            f.write(data)
            f.close()

        # 压缩文件
        # 创建压缩文件对象
        compressed_data = zipfile.ZipFile(os.path.join(path, filename + '.zip'), mode='w',
                                          compression=zipfile.ZIP_DEFLATED)
        # 将暂存在服务器上的文件写入压缩文件
        compressed_data.write(os.path.join(path, filename))
        compressed_data.close()

        # 读取压缩后的数据，并发送给Client
        with open(os.path.join(path, filename + '.zip'), 'rb') as f:
            compressed_data = f.read()
            client_socket.sendall(compressed_data)
            f.close()
            # 删除服务器临时文件
            os.remove(os.path.join(path, filename + '.zip'))
            os.remove(os.path.join(path, filename))

        # 关闭socket连接
        client_socket.close()
        print(f'服务完毕，已断开对{addr}的连接！')

    except ConnectionResetError as e:
        print(f'与客户端{addr}的连接被终止！')
