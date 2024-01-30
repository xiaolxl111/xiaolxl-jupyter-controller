import os

def extract_base_filename(filename):
    # Split the filename by '.' and take the first part
    base_name = filename.split('.')[0]
    return base_name

def get_download_command(download_link, download_path, filename, download_method, download_type="url"):
    command = "echo 未找到下载方式，请更新启动器！"
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

    if download_type == "cg_targz":
        folder_name = download_link.split('/')[-2]  # 链接格式为 .../folder_name/filename
        # 构建下载命令
        command = "mkdir -p " + download_path + " && cd " + download_path + " && "
        # 根据下载方法添加下载命令
        command += "cg down " + download_link + " && "
        # 移动文件到正确位置
        command += "mv " + folder_name + "/" + filename + " ./ && "
        # 删除多余文件夹
        command += "rm -rf " + folder_name + " && "
        # 解压文件到对应目录
        command += "tar xzvf " + filename + " -C " + download_path + " && "
        # 删除压缩包
        command += "rm -f " + filename + " && "
        # 完成提示
        command += "echo 下载完毕!文件已解压到:" + download_path

    
    return command


def check_downloaded(downloadType, filename, download_path, mod_child):
    if downloadType == "cg_targz":
        # cg_targz类型需要检查所有metadata中列出的文件
        for file_info in mod_child['metadata']:
            # 构建每个文件的完整路径
            file_path = os.path.join(download_path, extract_base_filename(filename), file_info['sonPath'], file_info['fileName'])
            # 如果任何文件不存在，则返回False
            if not os.path.exists(file_path):
                return False
        # 如果所有文件都存在，则返回True
        return True
    else:
        # 其他类型的检查方法保持不变
        file_path = os.path.join(download_path, filename)
        aria2_file = file_path + ".aria2"
        return os.path.exists(file_path) and not os.path.exists(aria2_file)
