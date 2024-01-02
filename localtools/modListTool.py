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
])

manager.add_mod_childs(a6, "Controlnet_v1_1_SD1.5模型_fp16", [
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

print(manager.get_json())