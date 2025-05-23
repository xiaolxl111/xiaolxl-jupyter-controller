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
a1 = "主流模型(大模型)"
manager.add_title(a1)

manager.add_mod_childs(a1, "[Yuno779] Anything-ink (二次元)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/Anything-ink.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "Anything-ink.safetensors"
}
])

manager.add_mod_childs(a1, "[rqdwdw] Counterfeit-V3.0 (二次元)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/Counterfeit-V3.0_fix.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "Counterfeit-V3.0_fix.safetensors"
}
])

manager.add_mod_childs(a1, "[newlifezfztty761] CuteYukiMix-specialchapter (二次元/特化可爱风格)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/cuteyukimixAdorable_specialchapter.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "cuteyukimixAdorable_specialchapter.safetensors"
}
])

manager.add_mod_childs(a1, "[stabilityai] SD_XL (通用)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/sd_xl_base_1.0.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "sd_xl_base_1.0.safetensors"
}
])

manager.add_mod_childs(a1, "[xiaolxl] GuoFeng4.1_2.5D_XL (2.5D/通用)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuoFengCollection/GuoFeng4.1_2.5D.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuoFeng4.1_2.5D.safetensors"
}
])

manager.add_mod_childs(a1, "[_GhostInShell_] GhostMix-V2.0 (2.5D)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/GhostMix-V2.0-fp16-BakedVAE.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GhostMix-V2.0-fp16-BakedVAE.safetensors"
}
])

manager.add_mod_childs(a1, "[s6yx] rev_1.2.2 (2.5D)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/rev_1.2.2-fp16.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "rev_1.2.2-fp16.safetensors"
}
])

manager.add_mod_childs(a1, "[Aitasai] darkSushiMixMix大颗寿司Mix (2.5D/二次元)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/darkSushiMixMix_225D.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "darkSushiMixMix_225D.safetensors"
}
])

# ==========================

a2 = "推荐模型(大模型)"
manager.add_title(a2)

manager.add_mod_childs(a2, "[CagliostroLab] Animagine-XL-V3 (二次元)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/animagineXLV3_v30.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "animagineXLV3_v30.safetensors"
}
])

manager.add_mod_childs(a2, "[playgroundai] playground-v2-XL(13GB) (通用)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/playground-v2.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "playground-v2.safetensors"
}
])

manager.add_mod_childs(a2, "[Yuno779] Anything-V3.0 (二次元)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/Anything-V3.0.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "Anything-V3.0.safetensors"
}
])

manager.add_mod_childs(a2, "[未知] momoko-e (二次元)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/momoko-e.ckpt",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "momoko-e.ckpt"
}
])

manager.add_mod_childs(a2, "[swl-models] PVCGK (手办风格)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/PVCGK.ckpt",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "PVCGK.ckpt"
}
])

manager.add_mod_childs(a2, "[xiaolxl] WestMagic (西幻/2.5D)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/WestMagic_f16.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "WestMagic_f16.safetensors"
}
])

# ==========================

a3 = "经典模型(大模型)"
manager.add_title(a3)

manager.add_mod_childs(a3, "[stabilityai] stable-diffusion-v1-5 (通用)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-models/stable-diffusion-v1-5.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "stable-diffusion-v1-5.safetensors"
}
])

# ==========================

a4 = "国风系列(大模型)"
manager.add_title(a4)

manager.add_mod_childs(a4, "[xiaolxl] GuoFeng4.2XL (国风/通用)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuoFengCollection/Guofeng4.2XL.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "Guofeng4.2XL.safetensors"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuoFeng4.0_Real_Beta (国风/通用)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuoFengCollection/GuoFeng4.0_Real_Beta.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuoFeng4.0_Real_Beta.safetensors"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuoFeng3.4 (2.5D/国风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuoFengCollection/GuoFeng3.4.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuoFeng3.4.safetensors"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuoFeng3.3 (2.5D/国风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuoFengCollection/GuoFeng3.3.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuoFeng3.3.safetensors"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuoFeng3.2_light (2.5D/暗光特化/国风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuoFengCollection/GuoFeng3.2_light.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuoFeng3.2_light.safetensors"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuoFeng3.2 (2.5D/国风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuoFengCollection/GuoFeng3.2.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuoFeng3.2.safetensors"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuoFeng3.1 (2.5D/国风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuoFengCollection/GuoFeng3.1.ckpt",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuoFeng3.1.ckpt"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuoFeng2_MIX (2.5D/国风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuoFengCollection/GuoFeng2MIX.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuoFeng2MIX.safetensors"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuFengXL (二次元/古风/通用)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuFengCollection/GuFengXL_Fp16.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuFengXL_Fp16.safetensors"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuFeng2 (二次元/古风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuFengCollection/GuFeng2.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuFeng2.safetensors"
}
])

manager.add_mod_childs(a4, "[xiaolxl] GuFeng1 (二次元/古风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/GuFengCollection/GuFeng.safetensors",
    "parentPath": "ckpt_dir",
    "sonPath": "/",
    "fileName": "GuFeng.safetensors"
}
])

# ==========================

a5 = "常用Lora(Lora模型)"
manager.add_title(a5)

manager.add_mod_childs(a5, "[xiaolxl] GuFengXL_Lora (古风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-Loras/GuFengXLLora.safetensors",
    "parentPath": "lora_dir",
    "sonPath": "/",
    "fileName": "GuFengXLLora.safetensors"
}
])

manager.add_mod_childs(a5, "[liaoliaojun-了了君] hanfuTang_v41_SDXL (汉服唐风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-Loras/hanfuTang_v41_R_SDXL.safetensors",
    "parentPath": "lora_dir",
    "sonPath": "/",
    "fileName": "hanfuTang_v41_R_SDXL.safetensors"
}
])

manager.add_mod_childs(a5, "[simhuang] MoXinV1 (墨风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-Loras/MoXinV1.safetensors",
    "parentPath": "lora_dir",
    "sonPath": "/",
    "fileName": "MoXinV1.safetensors"
}
])

manager.add_mod_childs(a5, "[AlchemistW] 小人书2.0 (小人书风格)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-Loras/xrs2.0.safetensors",
    "parentPath": "lora_dir",
    "sonPath": "/",
    "fileName": "xrs2.0.safetensors"
}
])

manager.add_mod_childs(a5, "[liaoliaojun-了了君] 汉服3.0 (汉服)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-Loras/hanfu_v30.safetensors",
    "parentPath": "lora_dir",
    "sonPath": "/",
    "fileName": "hanfu_v30.safetensors"
}
])

manager.add_mod_childs(a5, "[CyberAIchemist] add_detail细节调整 (细节调整)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-Loras/add_detail.safetensors",
    "parentPath": "lora_dir",
    "sonPath": "/",
    "fileName": "add_detail.safetensors"
}
])

manager.add_mod_childs(a5, "[samecorner] blindbox_v1_mix (盲盒/手办/可爱)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-Loras/blindbox_v1_mix.safetensors",
    "parentPath": "lora_dir",
    "sonPath": "/",
    "fileName": "blindbox_v1_mix.safetensors"
}
])

manager.add_mod_childs(a5, "[xiaolxl] Dream (梦幻)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-Loras/Dream.safetensors",
    "parentPath": "lora_dir",
    "sonPath": "/",
    "fileName": "Dream.safetensors"
}
])

manager.add_mod_childs(a5, "[xiaolxl] WuMo2 (武墨风)", [
{
    "downloadType": "cg",
    "url": "xiaolxl/stable-diffusion-Loras/WuMo2.safetensors",
    "parentPath": "lora_dir",
    "sonPath": "/",
    "fileName": "WuMo2.safetensors"
}
])

# ==========================

a6 = "插件所需依赖/模型"
manager.add_title(a6)

manager.add_mod_childs(a6, "Controlnet预处理器(17GB+)", [
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/res101.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/leres",
        "fileName": "res101.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/latest_net_G.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/leres",
        "fileName": "latest_net_G.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/dpt_hybrid-midas-501f0c75.pt",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/midas",
        "fileName": "dpt_hybrid-midas-501f0c75.pt"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/ZoeD_M12_N.pt",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/zoedepth",
        "fileName": "ZoeD_M12_N.pt"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/scannet.pt",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/normal_bae",
        "fileName": "scannet.pt"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/yolox_l.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/openpose",
        "fileName": "yolox_l.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/rtmpose-m_simcc-ap10k_pt-aic-coco_210e-256x256-7a041aa1_20230206.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/openpose",
        "fileName": "rtmpose-m_simcc-ap10k_pt-aic-coco_210e-256x256-7a041aa1_20230206.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/dw-ll_ucoco_384.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/openpose",
        "fileName": "dw-ll_ucoco_384.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/body_pose_model.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/openpose",
        "fileName": "body_pose_model.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/hand_pose_model.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/openpose",
        "fileName": "hand_pose_model.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/facenet.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/openpose",
        "fileName": "facenet.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/mlsd_large_512_fp32.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/mlsd",
        "fileName": "mlsd_large_512_fp32.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/netG.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/lineart_anime",
        "fileName": "netG.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/erika.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/manga_line",
        "fileName": "erika.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/sk_model2.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/lineart",
        "fileName": "sk_model2.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/sk_model.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/lineart",
        "fileName": "sk_model.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/ControlNetHED.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/hed",
        "fileName": "ControlNetHED.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/table5_pidinet.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/pidinet",
        "fileName": "table5_pidinet.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/UNet.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/anime_face_segment",
        "fileName": "UNet.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/250_16_swin_l_oneformer_ade20k_160k.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/oneformer",
        "fileName": "250_16_swin_l_oneformer_ade20k_160k.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/150_16_swin_l_oneformer_coco_100ep.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/oneformer",
        "fileName": "150_16_swin_l_oneformer_coco_100ep.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/upernet_global_small.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/uniformer",
        "fileName": "upernet_global_small.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/ControlNetLama.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/lama",
        "fileName": "ControlNetLama.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/clip_g.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/clip_vision",
        "fileName": "clip_g.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/clip_vitl.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/clip_vision",
        "fileName": "clip_vitl.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/clip_h.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/clip_vision",
        "fileName": "clip_h.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/depth_anything_vitl14.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/depth_anything",
        "fileName": "depth_anything_vitl14.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/graphormer_hand_state_dict.bin",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/hand_refiner/hr16/ControlNet-HandRefiner-pruned",
        "fileName": "graphormer_hand_state_dict.bin"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/hrnetv2_w64_imagenet_pretrained.pth",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/hand_refiner/hr16/ControlNet-HandRefiner-pruned",
        "fileName": "hrnetv2_w64_imagenet_pretrained.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/densepose_r50_fpn_dl.torchscript",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/densepose",
        "fileName": "densepose_r50_fpn_dl.torchscript"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/buffalo_l.zip",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models",
        "fileName": "buffalo_l.zip"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/genderage.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/buffalo_l",
        "fileName": "genderage.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/2d106det.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/buffalo_l",
        "fileName": "2d106det.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/det_10g.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/buffalo_l",
        "fileName": "det_10g.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/1k3d68.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/buffalo_l",
        "fileName": "1k3d68.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/w600k_r50.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/buffalo_l",
        "fileName": "w600k_r50.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/1k3d68.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/antelopev2",
        "fileName": "1k3d68.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/2d106det.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/antelopev2",
        "fileName": "2d106det.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/genderage.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/antelopev2",
        "fileName": "genderage.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/glintr100.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/antelopev2",
        "fileName": "glintr100.onnx"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/controlnet-annotator/scrfd_10g_bnkps.onnx",
        "parentPath": "controlnet_annotator_models_path",
        "sonPath": "/insightface/models/antelopev2",
        "fileName": "scrfd_10g_bnkps.onnx"
    },
])

manager.add_mod_childs(a6, "Controlnet_v1_1_SD1.5模型_fp16(11GB+)", [
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11e_sd15_ip2p_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11e_sd15_ip2p_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11e_sd15_shuffle_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11e_sd15_shuffle_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11f1e_sd15_tile_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11f1e_sd15_tile_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11f1p_sd15_depth_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11f1p_sd15_depth_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15_canny_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15_canny_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15_inpaint_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15_inpaint_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15_mlsd_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15_mlsd_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15_normalbae_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15_normalbae_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15_openpose_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15_openpose_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15_scribble_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15_scribble_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15_seg_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15_seg_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15_softedge_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15_softedge_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15s2_lineart_anime_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15s2_lineart_anime_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11u_sd15_tile_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11u_sd15_tile_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/control_v11p_sd15_lineart_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_v11p_sd15_lineart_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/ioclab_sd15_recolor.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ioclab_sd15_recolor.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_v1_1_fp16/ip-adapter_sd15_plus.pth",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ip-adapter_sd15_plus.pth"
    },
])

manager.add_mod_childs(a6, "Controlnet_XL模型_fp16(25GB+)", [
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/t2i-adapter_diffusers_xl_depth_zoe.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "t2i-adapter_diffusers_xl_depth_zoe.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/t2i-adapter_diffusers_xl_openpose.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "t2i-adapter_diffusers_xl_openpose.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/t2i-adapter_xl_canny.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "t2i-adapter_xl_canny.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/t2i-adapter_xl_openpose.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "t2i-adapter_xl_openpose.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/thibaud_xl_openpose.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "thibaud_xl_openpose.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/diffusers_xl_canny_full.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "diffusers_xl_canny_full.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/diffusers_xl_canny_mid.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "diffusers_xl_canny_mid.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/diffusers_xl_canny_small.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "diffusers_xl_canny_small.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/diffusers_xl_depth_full.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "diffusers_xl_depth_full.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/diffusers_xl_depth_mid.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "diffusers_xl_depth_mid.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/diffusers_xl_depth_small.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "diffusers_xl_depth_small.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/ip-adapter_xl.pth",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ip-adapter_xl.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_blur.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_blur.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_blur_anime.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_blur_anime.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_blur_anime_beta.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_blur_anime_beta.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_canny.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_canny.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_canny_anime.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_canny_anime.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_depth.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_depth.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_depth_anime.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_depth_anime.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_openpose_anime.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_openpose_anime.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_openpose_anime_v2.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_openpose_anime_v2.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/kohya_controllllite_xl_scribble_anime.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "kohya_controllllite_xl_scribble_anime.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sai_xl_canny_128lora.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sai_xl_canny_128lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sai_xl_canny_256lora.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sai_xl_canny_256lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sai_xl_depth_128lora.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sai_xl_depth_128lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sai_xl_depth_256lora.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sai_xl_depth_256lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sai_xl_recolor_128lora.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sai_xl_recolor_128lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sai_xl_recolor_256lora.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sai_xl_recolor_256lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sai_xl_sketch_128lora.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sai_xl_sketch_128lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sai_xl_sketch_256lora.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sai_xl_sketch_256lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sargezt_xl_depth.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sargezt_xl_depth.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sargezt_xl_depth_faid_vidit.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sargezt_xl_depth_faid_vidit.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sargezt_xl_depth_zeed.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sargezt_xl_depth_zeed.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/sargezt_xl_softedge.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "sargezt_xl_softedge.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/t2i-adapter_diffusers_xl_canny.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "t2i-adapter_diffusers_xl_canny.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/t2i-adapter_diffusers_xl_depth_midas.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "t2i-adapter_diffusers_xl_depth_midas.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/t2i-adapter_diffusers_xl_lineart.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "t2i-adapter_diffusers_xl_lineart.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/t2i-adapter_diffusers_xl_sketch.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "t2i-adapter_diffusers_xl_sketch.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/t2i-adapter_xl_sketch.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "t2i-adapter_xl_sketch.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_XL_fp16/thibaud_xl_openpose_256lora.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "thibaud_xl_openpose_256lora.safetensors"
    },
])

manager.add_mod_childs(a6, "Controlnet新增模型合集(20GB+)", [
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/control_sd15_depth_anything.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_sd15_depth_anything.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/control_sd15_animal_openpose_fp16.pth",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_sd15_animal_openpose_fp16.pth"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/control_sd15_inpaint_depth_hand_fp16.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_sd15_inpaint_depth_hand_fp16.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/controlnet_for_densepose.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "controlnet_for_densepose.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/loose_controlnet.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "loose_controlnet.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/control_instant_id_sdxl.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "control_instant_id_sdxl.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/controlnet-sd-xl-1.0-softedge-dexined.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "controlnet-sd-xl-1.0-softedge-dexined.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/ip-adapter_instant_id_sdxl.bin",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ip-adapter_instant_id_sdxl.bin"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/ip-adapter-faceid_sd15.bin",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid_sd15.bin"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/ip-adapter-faceid-plusv2_sdxl.bin",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid-plusv2_sdxl.bin"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/ip-adapter-faceid_sdxl.bin",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid_sdxl.bin"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/ip-adapter-faceid-plus_sd15.bin",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid-plus_sd15.bin"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/ip-adapter-faceid-portrait_sd15.bin",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid-portrait_sd15.bin"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Mods_Update/ip-adapter-faceid-plusv2_sd15.bin",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid-plusv2_sd15.bin"
    },
])

manager.add_mod_childs(a6, "Controlnet新增Lora合集(1GB+-)", [
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Loras_Update/ip-adapter-faceid_sd15_lora.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid_sd15_lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Loras_Update/ip-adapter-faceid_sdxl_lora.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid_sdxl_lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Loras_Update/ip-adapter-faceid-plus_sd15_lora.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid-plus_sd15_lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Loras_Update/ip-adapter-faceid-plusv2_sd15_lora.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid-plusv2_sd15_lora.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/ControlNet_Loras_Update/ip-adapter-faceid-plusv2_sdxl_lora.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/",
        "fileName": "ip-adapter-faceid-plusv2_sdxl_lora.safetensors"
    },
])

manager.add_mod_childs(a6, "AnimateDiff动画模型(2GB+)", [
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111/mm_sd15_v2.safetensors",
        "parentPath": "animatediff_dir",
        "sonPath": "/",
        "fileName": "mm_sd15_v2.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111/mm_sd15_v3.safetensors",
        "parentPath": "animatediff_dir",
        "sonPath": "/",
        "fileName": "mm_sd15_v3.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111/mm_sdxl_v10_beta.safetensors",
        "parentPath": "animatediff_dir",
        "sonPath": "/",
        "fileName": "mm_sdxl_v10_beta.safetensors"
    },
])

manager.add_mod_childs(a6, "常用VAE模型", [
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

manager.add_mod_childs(a6, "AnimateDifV2的motionLoRA和v3AdapterLora(350MB)", [
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-MotionLoRA/mm_sd15_v2_lora_PanLeft.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/AnimateDiffMotionLoRA",
        "fileName": "mm_sd15_v2_lora_PanLeft.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-MotionLoRA/mm_sd15_v2_lora_TiltDown.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/AnimateDiffMotionLoRA",
        "fileName": "mm_sd15_v2_lora_TiltDown.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-MotionLoRA/mm_sd15_v2_lora_TiltUp.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/AnimateDiffMotionLoRA",
        "fileName": "mm_sd15_v2_lora_TiltUp.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-MotionLoRA/mm_sd15_v2_lora_PanRight.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/AnimateDiffMotionLoRA",
        "fileName": "mm_sd15_v2_lora_PanRight.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-MotionLoRA/mm_sd15_v2_lora_RollingClockwise.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/AnimateDiffMotionLoRA",
        "fileName": "mm_sd15_v2_lora_RollingClockwise.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-MotionLoRA/mm_sd15_v2_lora_RollingAnticlockwise.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/AnimateDiffMotionLoRA",
        "fileName": "mm_sd15_v2_lora_RollingAnticlockwise.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-MotionLoRA/mm_sd15_v2_lora_ZoomIn.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/AnimateDiffMotionLoRA",
        "fileName": "mm_sd15_v2_lora_ZoomIn.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-MotionLoRA/mm_sd15_v2_lora_ZoomOut.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/AnimateDiffMotionLoRA",
        "fileName": "mm_sd15_v2_lora_ZoomOut.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-MotionLoRA/mm_sd15_v3_adapter.safetensors",
        "parentPath": "lora_dir",
        "sonPath": "/AnimateDiffMotionLoRA",
        "fileName": "mm_sd15_v3_adapter.safetensors"
    },
])

manager.add_mod_childs(a6, "AnimateDifV3的SparseControlNet模型(2GB)", [
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-ControlNetMod/mm_sd15_v3_sparsectrl_rgb.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "mm_sd15_v3_sparsectrl_rgb.safetensors"
    },
    {
        "downloadType": "cg",
        "url": "xiaolxl/AnimateDiff-A1111-ControlNetMod/mm_sd15_v3_sparsectrl_scribble.safetensors",
        "parentPath": "controlnet_dir",
        "sonPath": "/",
        "fileName": "mm_sd15_v3_sparsectrl_scribble.safetensors"
    },
])

manager.add_mod_childs(a6, 'TAG插件反推依赖模型包(3GB+-)', [
{
  'downloadType': 'cg_targz',
  'url': 'xiaolxl/tagger_interrogators/interrogators.tar.gz',
  'parentPath': 'models_dir',
  'sonPath': '/',
  'fileName': 'interrogators.tar.gz',
  'metadata': [
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-moat-tagger-v2/blobs',
      'fileName': 'b8cef913be4c9e8d93f9f903e74271416502ce0b4b04df0ff1e2f00df488aa03'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-moat-tagger-v2/blobs',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-moat-tagger-v2/snapshots/8452cddf280b952281b6e102411c50e981cb2908',
      'fileName': 'model.onnx'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-moat-tagger-v2/snapshots/8452cddf280b952281b6e102411c50e981cb2908',
      'fileName': 'selected_tags.csv'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-moat-tagger-v2/refs',
      'fileName': 'main'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-moat-tagger-v2',
      'fileName': 'b8cef913be4c9e8d93f9f903e74271416502ce0b4b04df0ff1e2f00df488aa03.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-moat-tagger-v2',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-vit-tagger-v2',
      'fileName': '8a21cadd1f88a095094cafbffe3028c3cc3d97f4d58c54344c5994bcf48e24ac.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-vit-tagger-v2',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-vit-tagger',
      'fileName': '22e88a3226e427998fdf669bdbd035ee7040f3229796dd66ec35b8dd90e852b5.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-vit-tagger',
      'fileName': '33ab5e6f93fe352338b6837f32849e9815c3bd08.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-swinv2-tagger-v2',
      'fileName': '67740df7ede9a53e50d6e29c6a5c0d6c862f1876c22545d810515bad3ae17bb1.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-swinv2-tagger-v2',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-convnextv2-tagger-v2',
      'fileName': 'e91daa19cd9e8725125b7d70702d1560855fb687f8d8c4218eddaa821f41834a.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-convnextv2-tagger-v2',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-convnext-tagger-v2',
      'fileName': '71f06ecb7b9df81d8f271da4d43997ea2ed363cdac29aa64fcb256c9631e656a.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-convnext-tagger-v2',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-convnext-tagger',
      'fileName': 'b7d7c9923e0056a2def0f4418df01a1274467b3da8480f146b851289257734de.lock'
    },
    {
      'sonPath': '/.locks/models--SmilingWolf--wd-v1-4-convnext-tagger',
      'fileName': '33ab5e6f93fe352338b6837f32849e9815c3bd08.lock'
    },
    {
      'sonPath': '/.locks/models--deepghs--ml-danbooru-onnx',
      'fileName': '594c26e2cb72637c343f0492ba9d76b642e751201bcf61ff43f02ddeab3abcb9.lock'
    },
    {
      'sonPath': '/.locks/models--deepghs--ml-danbooru-onnx',
      'fileName': '70051a40fcc09a1d420d77beb78366c648d293d2.lock'
    },
    {
      'sonPath': '/.locks/models--deepghs--ml-danbooru-onnx',
      'fileName': '4ea7aa66df59632c71e036cd9eda9c89e0eaf58bcd39bf9718e63583378cba75.lock'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger-v2/blobs',
      'fileName': '8a21cadd1f88a095094cafbffe3028c3cc3d97f4d58c54344c5994bcf48e24ac'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger-v2/blobs',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger-v2/snapshots/1f3f3e8ae769634e31e1ef696df11ec37493e4f2',
      'fileName': 'model.onnx'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger-v2/snapshots/1f3f3e8ae769634e31e1ef696df11ec37493e4f2',
      'fileName': 'selected_tags.csv'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger-v2/snapshots/1f3f3e8ae769634e31e1ef696df11ec37493e4f2/.ipynb_checkpoints',
      'fileName': 'selected_tags-checkpoint.csv'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger-v2/refs',
      'fileName': 'main'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger/blobs',
      'fileName': '22e88a3226e427998fdf669bdbd035ee7040f3229796dd66ec35b8dd90e852b5'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger/blobs',
      'fileName': '33ab5e6f93fe352338b6837f32849e9815c3bd08'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger/snapshots/213a7bd66d93407911b8217e806a95edc3593eed',
      'fileName': 'model.onnx'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger/snapshots/213a7bd66d93407911b8217e806a95edc3593eed',
      'fileName': 'selected_tags.csv'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-vit-tagger/refs',
      'fileName': 'main'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-swinv2-tagger-v2/blobs',
      'fileName': '67740df7ede9a53e50d6e29c6a5c0d6c862f1876c22545d810515bad3ae17bb1'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-swinv2-tagger-v2/blobs',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-swinv2-tagger-v2/snapshots/e8a736126633b7e60d0ce59930ee8b70642d7560',
      'fileName': 'model.onnx'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-swinv2-tagger-v2/snapshots/e8a736126633b7e60d0ce59930ee8b70642d7560',
      'fileName': 'selected_tags.csv'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-swinv2-tagger-v2/refs',
      'fileName': 'main'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnextv2-tagger-v2/blobs',
      'fileName': 'e91daa19cd9e8725125b7d70702d1560855fb687f8d8c4218eddaa821f41834a'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnextv2-tagger-v2/blobs',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnextv2-tagger-v2/snapshots/dbd4dbe553ee51feb3bc745b614fb762080e3912',
      'fileName': 'model.onnx'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnextv2-tagger-v2/snapshots/dbd4dbe553ee51feb3bc745b614fb762080e3912',
      'fileName': 'selected_tags.csv'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnextv2-tagger-v2/refs',
      'fileName': 'main'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger-v2/blobs',
      'fileName': '71f06ecb7b9df81d8f271da4d43997ea2ed363cdac29aa64fcb256c9631e656a'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger-v2/blobs',
      'fileName': '71796801c13109547bc017d40fc6f5b89bfd9cc0'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger-v2/snapshots/4b34d1b07bdd8e95494072648960b8a6adcbc0ff',
      'fileName': 'model.onnx'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger-v2/snapshots/4b34d1b07bdd8e95494072648960b8a6adcbc0ff',
      'fileName': 'selected_tags.csv'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger-v2/refs',
      'fileName': 'main'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger/blobs',
      'fileName': 'b7d7c9923e0056a2def0f4418df01a1274467b3da8480f146b851289257734de'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger/blobs',
      'fileName': '33ab5e6f93fe352338b6837f32849e9815c3bd08'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger/snapshots/4036ca51f1c082b0e7c4496890bbf9eadad5764a',
      'fileName': 'model.onnx'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger/snapshots/4036ca51f1c082b0e7c4496890bbf9eadad5764a',
      'fileName': 'selected_tags.csv'
    },
    {
      'sonPath': '/models--SmilingWolf--wd-v1-4-convnext-tagger/refs',
      'fileName': 'main'
    },
    {
      'sonPath': '/models--deepghs--ml-danbooru-onnx/blobs',
      'fileName': '594c26e2cb72637c343f0492ba9d76b642e751201bcf61ff43f02ddeab3abcb9'
    },
    {
      'sonPath': '/models--deepghs--ml-danbooru-onnx/blobs',
      'fileName': '70051a40fcc09a1d420d77beb78366c648d293d2'
    },
    {
      'sonPath': '/models--deepghs--ml-danbooru-onnx/blobs',
      'fileName': '4ea7aa66df59632c71e036cd9eda9c89e0eaf58bcd39bf9718e63583378cba75'
    },
    {
      'sonPath': '/models--deepghs--ml-danbooru-onnx/snapshots/60009d1a5989970203364a2b27c887e0fa2747f2',
      'fileName': 'TResnet-D-FLq_ema_6-30000.onnx'
    },
    {
      'sonPath': '/models--deepghs--ml-danbooru-onnx/snapshots/60009d1a5989970203364a2b27c887e0fa2747f2',
      'fileName': 'classes.json'
    },
    {
      'sonPath': '/models--deepghs--ml-danbooru-onnx/snapshots/60009d1a5989970203364a2b27c887e0fa2747f2',
      'fileName': 'ml_caformer_m36_dec-5-97527.onnx'
    },
    {
      'sonPath': '/models--deepghs--ml-danbooru-onnx/refs',
      'fileName': 'main'
    }
  ]
}
  ]
)

print(manager.get_json())