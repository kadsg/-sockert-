import socket
import tkinter
from tkinter import filedialog
import os

host = 'localhost'  # Server的IP地址或主机名
port = 8000  # Server监听的端口号

# 创建socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接Server
client_socket.connect((host, port))

# 打开文件选择对话框
print("连接成功！选择你要压缩的文件...")
root = tkinter.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# 发送文件名
filename = os.path.basename(file_path)
client_socket.sendall(filename.encode())

# 打开文件并发送
with open(file_path, 'rb') as f:
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
            client_socket.sendall(chunk)  # 发送数据
            # 关闭写入通道，告诉Server数据已经发送完毕
            client_socket.shutdown(socket.SHUT_WR)
            break

# 接收Server返回的数据
compressed_data = b""
while True:
    data = client_socket.recv(1024)
    if not data:  # 数据接收完毕，退出循环
        break
    compressed_data += data

# 打开文件保存对话框
root = tkinter.Tk()
root.withdraw()
# 弹出保存文件对话框，获取用户选择的保存路径和文件名
# 文件类型过滤器
options = {
    'defaultextension': '.zip',
    'filetypes': [('ZIP files', '*.zip'), ('All files', '*.*')],
}
save_filename = tkinter.filedialog.asksaveasfilename(**options)

try:
    # 保存压缩数据到文件
    with open(save_filename, "wb") as f:
        f.write(compressed_data)
        f.close()
except FileNotFoundError:
    print("用户取消保存！")

# 关闭socket连接
client_socket.close()
