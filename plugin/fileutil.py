import os
import sys


class FileUtil:
    # 全局储存目录
    storage_path = os.path.join(os.getcwd(), "data")
    system_name = sys.platform
    # 默认win环境
    catalog_symbol = "\\"

    def __init__(self):
        if "win" in self.system_name:
            self.catalog_symbol = "\\"
        else:
            self.catalog_symbol = "/"

    def write(self, file_path, file_name, msg):
        # 去除首位空格
        path = self.storage_path + self.catalog_symbol + str(file_path)
        path = path.strip()
        # 去除尾部 目录分割 符号
        path = path.rstrip(self.catalog_symbol)
        is_exists = os.path.exists(path)
        if is_exists:
            file = open(path + self.catalog_symbol + file_name, "w+", encoding="utf-8")
            file.write(msg)
            file.close()
        else:
            # 创建多文件夹 创建自定义目录则 -> mkdir
            os.makedirs(path)
            file = open(path + self.catalog_symbol + file_name, "w+", encoding="utf-8")
            file.write(msg)
            file.close()

    def read(self, file_path, file_name):
        path = self.storage_path + self.catalog_symbol + str(file_path)
        path = path.strip()
        # 去除尾部 目录分割 符号
        path = path.rstrip(self.catalog_symbol)
        # 判断文件夹是否存在
        is_exists = os.path.exists(path)
        if is_exists:
            # 判断文件是否存在
            if os.path.exists(path + self.catalog_symbol + file_name):
                file = open(path + self.catalog_symbol + file_name, "r", encoding="utf-8")
                msg = file.read()
                print(msg)
                file.close()
                if msg == "":
                    return 'null'
                else:
                    return msg
            else:
                return 'null'
        else:
            return 'null'
