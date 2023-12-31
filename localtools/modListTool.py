import json

class JSONManager:
    def __init__(self):
        self.data = {
            "ts": []
        }

    def add_title(self, title):
        """添加一个新的标题，并附带一个空的模型列表。"""
        self.data["ts"].append({
            "title": title,
            "mods": []
        })

    def add_mod(self, title, modName):
        """向特定标题添加一个模型。"""
        for title_entry in self.data["ts"]:
            if title_entry["title"] == title:
                title_entry["mods"].append({
                    "modName": modName,
                    "modChildren": []
                })
                return
        raise ValueError("未找到标题")

    def add_mod_child(self, title, modName, modChild):
        """向特定标题的特定模型添加一个模型子项。"""
        for title_entry in self.data["ts"]:
            if title_entry["title"] == title:
                for mod in title_entry["mods"]:
                    if mod["modName"] == modName:
                        mod["modChildren"].append(modChild)
                        return
                raise ValueError("未找到模型")
        raise ValueError("未找到标题")

    def add_mod_childs(self, title, modName, modChildren):
        """向特定标题的特定模型添加多个模型子项。"""
        for title_entry in self.data["ts"]:
            if title_entry["title"] == title:
                for mod in title_entry["mods"]:
                    if mod["modName"] == modName:
                        mod["modChildren"].extend(modChildren)
                        return
                raise ValueError("未找到模型")
        raise ValueError("未找到标题")

    def get_json(self):
        """以JSON字符串的形式返回当前数据状态。"""
        return json.dumps(self.data, indent=4, ensure_ascii=False)

manager = JSONManager()
manager.add_title("主流模型")
manager.add_mod("主流模型", "Momoko_e")
manager.add_mod_childs("主流模型", "Momoko_e", [{
    "downloadType": "url",
    "url": "https://hf-mirror.com/xiaolxl/Stable-diffusion-models/resolve/main/momoko-e.ckpt",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "momoko-e.ckpt"
}])
manager.add_mod("主流模型", "res101")
manager.add_mod_childs("主流模型", "res101", [
{
    "downloadType": "cg",
    "url": "tzwm/StableDiffusion-others/res101.pth",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "res101.pth"
},
{
    "downloadType": "cg",
    "url": "tzwm/StableDiffusion-others/res102.pth",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "res102.pth"
}
])
print(manager.get_json())