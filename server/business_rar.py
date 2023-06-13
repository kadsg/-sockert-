from server.server_business import ServerBusiness

import rarfile  # pip install rarfile


class BusinessRAR(ServerBusiness):
    def compress_file(self, file_path):  # 重写父类的方法，实现rar压缩
        # 压缩文件
        compressed_file_path = file_path + '.rar'
        with rarfile.RarFile(compressed_file_path, mode='w') as compressed_data:
            compressed_data.write(file_path)
        return compressed_file_path
