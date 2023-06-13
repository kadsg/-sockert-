import zipfile

from server.server_business import ServerBusiness


class BusinessZIP(ServerBusiness):
    def compress_file(self, file_path):
        # 压缩文件
        compressed_file_path = file_path + '.zip'
        with zipfile.ZipFile(compressed_file_path, mode='w', compression=zipfile.ZIP_DEFLATED) as compressed_data:
            compressed_data.write(file_path)
        return compressed_file_path