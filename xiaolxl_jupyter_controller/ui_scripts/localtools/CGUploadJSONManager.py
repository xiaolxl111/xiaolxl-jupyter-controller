import os
import json
import tarfile

class CGUploadJSONManager:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = self._load_json()

    def _load_json(self):
        """加载现有的JSON数据，如果文件不存在，则创建一个新的结构。"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"ts": []}

    def _save_json(self):
        """将当前的数据状态保存到JSON文件中。"""
        with open(self.json_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def _upload_file_cg(self, file_path, token, cloud_url):
        """上传文件到CG服务器。这里只是一个示意，实际上传代码需替换。"""
        !cg upload {file_path} --token {token}
        print(f"正在上传文件：{file_path} 到 {cloud_url} 使用token {token}")

    def _create_targz_file(self, source_dir, output_file):
        """创建tar.gz压缩文件。如果文件已存在，则跳过打包。"""
        if not os.path.exists(output_file):
            with tarfile.open(output_file, 'w:gz') as tar:
                tar.add(source_dir, arcname=os.path.basename(source_dir))
            print(f"成功创建tar.gz文件：{output_file}")
        else:
            print(f"tar.gz文件已存在：{output_file}，跳过创建。")

    def _check_duplicates_cg(self, mod_children, file_name):
        """检查cg上传方式下的重复文件。"""
        for child in mod_children:
            if child['fileName'] == file_name:
                print(f"警告：文件名重复 - {file_name}。上传被取消。")
                return True
        return False

    def _check_duplicates_cg_targz(self, metadata, son_path, file_name):
        """检查cg_targz上传方式下的重复文件。"""
        for item in metadata:
            if item['sonPath'] == son_path and item['fileName'] == file_name:
                print(f"警告：在相同子路径下发现重复文件 - {son_path}/{file_name}。上传被取消。")
                return True
        return False

    def add_to_json_cg(self, category, title, model_name, file_dict):
        """将新的模型信息添加到JSON数据中，专为cg方式设计。"""
        title_entry = next((t for t in self.data["ts"] if t["title"] == title), None)
        if not title_entry:
            title_entry = {"title": title, "mods": []}
            self.data["ts"].append(title_entry)

        mod_entry = next((m for m in title_entry["mods"] if m["modName"] == model_name), None)
        if not mod_entry:
            mod_entry = {"modName": model_name, "modChildren": []}
            title_entry["mods"].append(mod_entry)

        if not self._check_duplicates_cg(mod_entry["modChildren"], file_dict['fileName']):
            mod_entry["modChildren"].append(file_dict)
            return True

    def add_to_json_cg_targz(self, category, title, model_name, file_dict):
        """将新的模型信息添加到JSON数据中，专为cg_targz方式设计。"""
        title_entry = next((t for t in self.data["ts"] if t["title"] == title), None)
        if not title_entry:
            title_entry = {"title": title, "mods": []}
            self.data["ts"].append(title_entry)

        mod_entry = next((m for m in title_entry["mods"] if m["modName"] == model_name), None)
        if not mod_entry:
            mod_entry = {"modName": model_name, "modChildren": [file_dict]}  # 直接将file_dict作为modChildren的一部分
            title_entry["mods"].append(mod_entry)
        else:  # 如果模型条目已存在
            if mod_entry["modChildren"]:  # 检查是否已有条目
                existing_tar_gz = mod_entry["modChildren"][0]  # cg_targz模式下应只有一个条目
                if not self._check_duplicates_cg_targz(existing_tar_gz['metadata'], file_dict['sonPath'], file_dict['fileName']):
                    # 更新metadata而不是重新添加modEntry
                    existing_tar_gz['metadata'].append({"sonPath": file_dict['sonPath'], "fileName": file_dict['fileName']})
            else:  # 如果modChildren为空
                mod_entry["modChildren"].append(file_dict)  # 直接添加新的file_dict

    def gen_and_upload_cg(self, category, title, model_name, directory, token, cloud_url, local_parent_path):
        """通过cg方式上传文件并更新JSON。"""
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                # 计算文件相对于扫描目录的相对路径
                relative_path = os.path.relpath(root, directory)
                if relative_path == '.':
                    son_path = '/'
                else:
                    # 确保sonPath以'/'开始
                    son_path = '/' + relative_path.replace('\\', '/')
                    # 如果sonPath不仅仅是'/'，则确保它不以'/'结尾
                    if son_path != '/' and son_path.endswith('/'):
                        son_path = son_path[:-1]

                file_dict = {
                    "downloadType": "cg",
                    "url": f"{cloud_url}/{file}",
                    "parentPath": local_parent_path,
                    "sonPath": son_path,
                    "fileName": file
                }

                if self.add_to_json_cg(category, title, model_name, file_dict):
                    self._upload_file_cg(file_path, token, cloud_url)


        self._save_json()

# 实例化 CGUploadJSONManager
# manager = CGUploadJSONManager('/root/autodl-tmp/jsontest/json.json')

# 设置上传的参数
# category = "a2"
# title = "测试模型(大模型)"
# model_name = "[hhhh] test (二次元)"
# directory = "/root/autodl-tmp/jsontest/abc"
# token = "your_upload_token_here"  # 替换为实际的上传令牌
# cloud_url = "xiaolxl/stable-diffusion-models"
# local_parent_path = "ckpt_dir"

# 执行上传并更新 JSON
# manager.gen_and_upload_cg(category, title, model_name, directory, token, cloud_url, local_parent_path)

# 实例化 CGUploadJSONManager
# manager = CGUploadJSONManager('/root/autodl-tmp/jsontest/json.json')

# 设置上传的参数
# category = "a3"
# title = "依赖(大模型)"
# model_name = "[hhhh2] pack (二次元)"
# directory = "/root/autodl-tmp/jsontest/abc2"
# token = "your_upload_token_here"  # 替换为实际的上传令牌
# cloud_url = "xiaolxl/stable-diffusion-models"
# local_parent_path = "ckpt_dir"
# package_name = "pakcname_test"

# 执行打包上传并更新 JSON
# manager.gen_and_upload_cg_targz(category, title, model_name, directory, token, cloud_url, local_parent_path, package_name)