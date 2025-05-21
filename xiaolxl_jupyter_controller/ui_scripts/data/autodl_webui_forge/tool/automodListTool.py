import json

class JSONManager:
    def __init__(self):
        self.data = {}

    def add_mod_childs(self, title, modChildren):
        """向特定标题添加多个模型子项。"""
        if title not in self.data:
            self.data[title] = {"modChildren": []}
        self.data[title]["modChildren"].extend(modChildren)

    def get_json(self):
        """以JSON字符串的形式返回当前数据状态。"""
        return json.dumps(self.data, indent=4, ensure_ascii=False)

manager = JSONManager()

manager.add_mod_childs("mod", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/Anything-ink.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "Anything-ink.safetensors"
}
])

manager.add_mod_childs("vae", [
    {
        "downloadType": "cg",
        "url": "xiaolxl/stable-diffusion-vaes/model.vae.pt",
        "parentPath": "vae_dir",
        "sonPath": "/",
        "fileName": "model.vae.pt"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/stable-diffusion-vaes/sdxl_vae.safetensors",
        "parentPath": "vae_dir",
        "sonPath": "/",
        "fileName": "sdxl_vae.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/stable-diffusion-vaes/vae-ft-mse-840000-ema-pruned.safetensors",
        "parentPath": "vae_dir",
        "sonPath": "/",
        "fileName": "vae-ft-mse-840000-ema-pruned.safetensors"
    },
])

manager.add_mod_childs("core", [
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/ESRGAN_4x.pth',
  'parentPath': 'models_dir',
  'sonPath': '/ESRGAN',
  'fileName': 'ESRGAN_4x.pth',
},
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/detection_Resnet50_Final.pth',
  'parentPath': 'models_dir',
  'sonPath': '/GFPGAN',
  'fileName': 'detection_Resnet50_Final.pth',
},
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/parsing_bisenet.pth',
  'parentPath': 'models_dir',
  'sonPath': '/GFPGAN',
  'fileName': 'parsing_bisenet.pth',
},
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/model.ckpt',
  'parentPath': 'models_dir',
  'sonPath': '/LDSR',
  'fileName': 'model.ckpt',
},
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/project.yaml',
  'parentPath': 'models_dir',
  'sonPath': '/LDSR',
  'fileName': 'project.yaml',
},
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/RealESRGAN_x4plus.pth',
  'parentPath': 'models_dir',
  'sonPath': '/RealESRGAN',
  'fileName': 'RealESRGAN_x4plus.pth',
},
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/RealESRGAN_x4plus_anime_6B.pth',
  'parentPath': 'models_dir',
  'sonPath': '/RealESRGAN',
  'fileName': 'RealESRGAN_x4plus_anime_6B.pth',
},
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/ScuNET.pth',
  'parentPath': 'models_dir',
  'sonPath': '/ScuNET',
  'fileName': 'ScuNET.pth',
},
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/SwinIR_4x.pth',
  'parentPath': 'models_dir',
  'sonPath': '/SwinIR',
  'fileName': 'SwinIR_4x.pth',
},
{
  'downloadType': 'cg',
  'url': 'xiaolxl/sdwebui_core/codeformer-v0.1.0.pth',
  'parentPath': 'models_dir',
  'sonPath': '/Codeformer',
  'fileName': 'codeformer-v0.1.0.pth',
}
  ]
)

print(manager.get_json())