import tkinter
from tkinter import filedialog
import client_business as business


# 重构后的客户端
class FileCompressorApp:
    def __init__(self, host, port):
        self.host = host  # Server的IP地址或主机名
        self.port = port  # Server监听的端口号
        self.compressor = business.ClientBusiness(self.host, self.port)  # 创建FileCompressor对象

    # 保存压缩文件
    def save_compressed_file(self, compressed_data, options):
        if compressed_data:
            root = tkinter.Tk()
            root.withdraw()
            # 弹出保存文件对话框，获取用户选择的保存路径和文件名
            save_filename = tkinter.filedialog.asksaveasfilename(**options)
            # 保存压缩数据到文件
            with open(save_filename, "wb") as f:
                f.write(compressed_data)
                print("文件保存成功！")

    # 启动客户端
    def run(self):
        try:
            print("选择你要压缩的文件...")
            # 弹出文件选择对话框
            root = tkinter.Tk()
            root.withdraw()
            # 获取用户选择的文件路径
            file_path = filedialog.askopenfilename()

            compressed_data, options = self.compressor.handle(file_path) # 发送文件并接收压缩数据

            self.save_compressed_file(compressed_data, options)  # 保存压缩文件
        except FileNotFoundError:
            print("操作取消！")
        finally:
            if self.compressor.client_socket:
                self.compressor.client_socket.close()


def main():
    host = 'localhost'  # Server的IP地址或主机名
    port = 8000  # Server监听的端口号

    while True:
        app = FileCompressorApp(host, port)  # 创建FileCompressorApp对象
        app.run()  # 启动客户端

        # 询问用户是否继续
        choice = input("是否继续？，按n退出，其他任意键继续：")
        if choice == 'n':
            break
    print("客户端已退出！")


if __name__ == '__main__':
    main()
