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

    def add_mod_childs(self, title, modName, modChildren):
        """向特定标题的特定模型添加多个模型子项。"""
        mod_exists = False
        for title_entry in self.data["ts"]:
            if title_entry["title"] == title:
                for mod in title_entry["mods"]:
                    if mod["modName"] == modName:
                        mod_exists = True
                        mod["modChildren"].extend(modChildren)
                        return
                if not mod_exists:
                    self.add_mod(title, modName)
                    self.add_mod_childs(title, modName, modChildren)
                    return
        raise ValueError("未找到标题")

    def get_json(self):
        """以JSON字符串的形式返回当前数据状态。"""
        return json.dumps(self.data, indent=4, ensure_ascii=False)

manager = JSONManager()
manager.add_title("主流模型")

manager.add_mod_childs("主流模型", "[Yuno779] Anything-ink (二次元)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/Anything-ink.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "Anything-ink.safetensors"
}
])

manager.add_mod_childs("主流模型", "[rqdwdw] Counterfeit-V3.0 (二次元)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/Counterfeit-V3.0_fix.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "Counterfeit-V3.0_fix.safetensors"
}
])

manager.add_mod_childs("主流模型", "[newlifezfztty761] CuteYukiMix-specialchapter (二次元,特化可爱风格)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/cuteyukimixAdorable_specialchapter.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "cuteyukimixAdorable_specialchapter.safetensors"
}
])

# manager.add_mod_childs("主流模型", "Momoko_e", [{
#     "downloadType": "url",
#     "url": "https://hf-mirror.com/xiaolxl/Stable-diffusion-models/resolve/main/momoko-e.ckpt",
#     "parentPath": "ckpt_dir",
#     "sonPath": "/",
#     "fileName": "momoko-e.ckpt"
# }])

# manager.add_mod_childs("主流模型", "res101", [
# {
#     "downloadType": "cg",
#     "url": "tzwm/StableDiffusion-others/res101.pth",
#     "parentPath": "ckpt_dir",
#     "sonPath": "/",
#     "fileName": "res101.pth"
# },
# {
#     "downloadType": "cg",
#     "url": "tzwm/StableDiffusion-others/res102.pth",
#     "parentPath": "ckpt_dir",
#     "sonPath": "/",
#     "fileName": "res102.pth"
# }
# ])

print(manager.get_json())