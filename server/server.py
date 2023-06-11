import os
import shutil
import socket
import zipfile

host = ''  # 监听的IP地址，为空则表示监听本机所有IP
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
    print(f'收到来自：{addr} 的请求！')

    try:
        # 接收Client发送的文件名
        filename = client_socket.recv(1024).decode()
        path = f'serverFor/{addr}'  # 临时文件夹路径

        # 如果临时文件夹不存在，则创建
        if not os.path.exists(path):
            os.makedirs(path)

        # 接收Client发送的数据并写入文件（暂存至服务器）
        with open(os.path.join(path, filename), 'wb') as f:
            data = b''  # 用于存储接收到的数据
            while True:  # 循环接收数据
                chunk = client_socket.recv(1024)  # 一次接收1024字节的数据
                # 如果接收到的数据为空，则退出循环
                if not chunk:
                    print(f'接收完毕，共接收{len(data)}字节的数据！')
                    break
                data += chunk  # 将接收到的数据追加到data中
            f.write(data)  # 将data写入文件
            f.close()  # 关闭文件

        # 压缩文件
        # 创建压缩文件对象
        compressed_data = zipfile.ZipFile(os.path.join(path, filename + '.zip'), mode='w',
                                          compression=zipfile.ZIP_DEFLATED)
        compressed_data.write(os.path.join(path, filename))  # 将暂存在服务器上的文件写入压缩文件
        compressed_data.close()  # 关闭压缩文件对象

        # 读取压缩后的数据，并发送给Client
        with open(os.path.join(path, filename + '.zip'), 'rb') as f:
            compressed_data = f.read()
            client_socket.sendall(compressed_data)
            f.close()

            # 删除服务器临时文件夹
            shutil.rmtree(path)

        # 关闭Client连接
        client_socket.shutdown(socket.SHUT_WR)
        print(f'为客户端{addr}的请求提供服务完毕！')

    except ConnectionResetError as e:  # 如果连接被重置
        print(f'与客户端{addr}的连接被终止！')
