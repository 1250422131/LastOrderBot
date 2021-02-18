import os
class FileUtil:

    # 全局储存目录
    storage_path = os.path.join(os.getcwd(), "data")

    def write(self, file_path,file_name , msg):
        # 去除首位空格
        path = self.storage_path + "\\" + str(file_path)
        path = path.strip()
        # 去除尾部 \ 符号
        path= path.rstrip("\\")
        isExists = os.path.exists(path)
        if isExists:
            file = open(path + "\\" + file_name, "w+", encoding="utf-8")
            file.write(msg)
            file.close
        else:
            #创建多文件夹 创建自定义目录则 -> mkdir
            os.makedirs(path)
            file = open(path + "\\" + file_name, "w+", encoding="utf-8")
            file.write(msg)
            file.close


    def read(self, file_path,file_name):
        path = self.storage_path + "\\" + str(file_path)
        path = path.strip()
        # 去除尾部 \ 符号
        path= path.rstrip("\\")
        #判断文件夹是否存在
        isExists = os.path.exists(path)
        if isExists:
            #判断文件是否存在
            if os.path.exists(path + "\\" + file_name):
                file = open(path + "\\" + file_name, "r", encoding="utf-8")
                msg = file.read()
                print(msg)
                file.close
                if msg == "":
                    return 'null'
                else:
                    return msg
            else:
                return 'null'
        else:
            return 'null'
