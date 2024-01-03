import os

def get_download_command(download_link, download_path, filename, download_method, download_type="url"):
    command = ""
    if download_type == "url":
        if download_method == "more":
            command = "mkdir -p " + download_path + " && cd " + download_path + " && aria2c -s 16 -x 8 --seed-time=0 '" + download_link + "' -o " + filename + " && echo 下载完毕!文件已保存到" + download_path
        if download_method == "one":
            command = "mkdir -p " + download_path + " && cd " + download_path + " && aria2c --seed-time=0 '" + download_link + "' -o " + filename + " && echo 下载完毕!文件已保存到" + download_path
    
    if download_type == "cg":
        folder_name = download_link.split('/')[-2]  # 链接格式为 .../folder_name/filename
        # 构建下载命令
        command = "mkdir -p " + download_path + " && cd " + download_path + " && "
        # 根据下载方法添加下载命令
        command += "cg down " + download_link + " && "
        # 移动文件到正确位置
        command += "mv " + folder_name + "/" + filename + " ./ && "
        # 删除多余文件夹
        command += "rm -rf " + folder_name + " && "
        # 完成提示
        command += "echo 下载完毕!文件已保存到:" + os.path.join(download_path, filename)
    
    return command


def check_downloaded(filename, download_path):
        # 检查文件是否已下载
        file_path = os.path.join(download_path, filename)
        aria2_file = file_path + ".aria2"
        return os.path.exists(file_path) and not os.path.exists(aria2_file)