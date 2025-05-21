import os, random, string
from xiaolxl_jupyter_controller import RootDir

def update_run_config_index(ui_config, new_index):
    """
    修改系统默认配置
    """
    ui_config.set_run_config_index(new_index)

def remove_run_config(ui_config, config_name):
    """
    删除某个运行配置
    """
    run_config_index = ui_config.obtain_run_config_index()
    if config_name == run_config_index:
        update_run_config_index(ui_config,"xiaolxlDefault")
        ui_config.remove_config(config_name)
    else:
        ui_config.remove_config(config_name)

def get_run_config_value(ui_config, key, config_name=None):
    """
    获取运行配置的值
    
    不存在将使用runConfigIndex所指向的配置
    """
    if config_name is None:
        return ui_config.get_run_config_index_item(key)
    else:
        return ui_config.get_config_item(config_name,key)

def set_run_config_value(ui_config, key, value, config_name=None):
    """
    设置运行配置的值
    
    config_name不存在将修改runConfigIndex所指向的配置
    """
    if config_name is None:
        ui_config.set_and_save_config_item(ui_config.obtain_run_config_index(),key,value)
    else:
        ui_config.set_and_save_config_item(config_name,key,value)

def get_run_configs_formatted(ui_config):
    """
    获取格式化的全部运行配置
    
    [todo:用户没有保存配置时,这个列表是空,但不影响运行]
    (配置名字, 配置key)
    """
    run_configs = ui_config.obtain_run_configs_list()
    current_run_config_index = ui_config.obtain_run_config_index()
    configs_info = []

    for key, config in run_configs.items():
        name = config.get('name', '')
        if key == current_run_config_index:
            name += " (默认)"
        configs_info.append((name, key))

    return configs_info

def get_config_dirs(ui_config):
    """
    获取带中文注释的, 指定的几个路径
    
    (路径注释, 路径key)
    如果没有找到key会从内置配置获取(防止更新失效)
    """
    custom_names = {
        "ckpt_dir": "大模型目录",
        "embeddings_dir": "Embeddings目录",
        "hypernetwork_dir": "Hypernetwork目录",
        "lora_dir": "LoRA目录",
        "vae_dir": "VAE目录",
        "controlnet_dir": "ControlNet模型目录",
        "controlnet_annotator_models_path": "ControlNet Annotator预处理模型目录",
        "animatediff_dir": "animatediff模型目录",
        "temp_dir": "数据盘目录",
    }

    # 新增列表，用于指定需要创建但不返回的目录
    dirs_to_create = {
        "dreambooth_models_path": "dreambooth目录初始化",
    }

    # 遍历新列表，为每个键创建目录
    for key in dirs_to_create:
        dir_path = ui_config.get_run_config_index_item(key)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
            # 注意: 这些目录信息不被添加到dir_info列表中，因此不会被返回

    dir_info = []
    for key in custom_names:
        dir_path = ui_config.get_run_config_index_item(key)
        if dir_path:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            dir_info.append((custom_names[key], key))

    return dir_info

def get_config_path(ui_config, key):
    """
    获取系统所设置的默认配置中的某个key对应的值
    """
    return ui_config.get_run_config_index_item(key)
    
def has_files(directory_path):
    """
    判断指定文件夹下是否有文件

    :param directory_path: 需要检查的文件夹路径
    :return: 如果文件夹存在且至少包含一个文件，则返回True，否则返回False
    """
    import os

    # 检查指定路径是否存在且为文件夹
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return False

    # 遍历文件夹内的内容
    for entry in os.listdir(directory_path):
        # 如果发现是文件，则返回True
        if os.path.isfile(os.path.join(directory_path, entry)):
            return True

    # 如果没有找到文件，返回False
    return False
# 使用示例
# result = has_files("指定的文件夹路径")
# print(result)

def has_mods_files(directory_path):
    # 检查指定路径是否存在且为文件夹
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return False

    # 遍历文件夹内的内容
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        # 检查文件扩展名是否为.safetensors或.ckpt
        if os.path.isfile(full_path) and (full_path.endswith('.safetensors') or full_path.endswith('.ckpt')):
            return True

    # 如果没有找到符合条件的文件，返回False
    return False
# 使用示例
# result = has_specific_files("指定的文件夹路径")
# print(result)

def has_vae_files(directory_path):
    # 检查指定路径是否存在且为文件夹
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return False

    # 遍历文件夹内的内容
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        # 检查文件扩展名是否为.vae.pt或.safetensors
        if os.path.isfile(full_path) and (full_path.endswith('.vae.pt') or full_path.endswith('.safetensors')):
            return True

    # 如果没有找到符合条件的文件，返回False
    return False
# 使用示例
# result = has_vae_or_safetensors_files("指定的文件夹路径")
# print(result)



def get_xiaolxl_jupyter_controller_path():
    """
    获取xiaolxl_jupyter_controller项目路径
    """
    return str(RootDir.get_project_root_dir())
    
def generate_random_letters(length=20):
    """
    随机指定数量生成字母
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))