import os, random, string

def _get_runConfig(ui_config):
    """
    获取系统所设置的默认配置
    """
    run_config_index = ui_config.get_config_value("runConfigIndex")
    run_configs = ui_config.get_config_value("runConfigs")

    return run_configs.get(run_config_index, {})

def update_run_config_index(ui_config, new_index):
    """
    修改系统默认配置
    """
    ui_config.set_config_value('runConfigIndex', new_index)

def remove_run_config(ui_config, config_name):
    """
    删除某个运行配置
    """
    run_config_index = ui_config.get_config_value("runConfigIndex")
    if config_name == run_config_index:
        update_run_config_index(ui_config,"xiaolxlDefault")
        key = f'runConfigs.{config_name}'
        ui_config.remove_config_value(key)
    else:
        key = f'runConfigs.{config_name}'
        ui_config.remove_config_value(key)

def get_run_config_value(ui_config, key, config_name=None):
    """
    获取运行配置的值
    
    不存在将使用runConfigIndex所指向的配置
    """
    try:
        # 尝试使用提供的或当前的config_name获取值
        if config_name is None:
            config_name = ui_config.get_config_value('runConfigIndex')
        full_key = f"runConfigs.{config_name}.{key}"
        return ui_config.get_config_value(full_key)
    except Exception as e:
        # 如果出错，则尝试使用默认的config_name
        default_config_name = "xiaolxlDefault"
        full_key = f"runConfigs.{default_config_name}.{key}"
        return ui_config.get_config_value(full_key)

def set_run_config_value(ui_config, key, value, config_name=None):
    """
    设置运行配置的值
    
    config_name不存在将修改runConfigIndex所指向的配置
    """
    if config_name is None:
        config_name = ui_config.get_config_value('runConfigIndex')
    full_key = f"runConfigs.{config_name}.{key}"
    ui_config.set_config_value(full_key, value)

def get_run_configs_formatted(ui_config):
    """
    获取格式化的全部运行配置
    
    (配置名字, 配置key)
    """
    run_configs = ui_config.get_config_value('runConfigs')
    current_run_config_index = ui_config.get_config_value('runConfigIndex')
    configs_info = []

    for key, config in run_configs.items():
        name = config.get('name', '')
        if key == current_run_config_index:
            name += " (默认)"
        configs_info.append((name, key))

    return configs_info

def create_directories_from_config(ui_config):
    """
    对指定的路径key的值确认是否存在路径, 不存在则创建

    如果没有找到key会从内置配置获取(防止更新失效)
    """
    # 指定要检查的 key
    keys_to_check = ["ckpt_dir", 
                     "embeddings_dir", 
                     "hypernetwork_dir",
                     "lora_dir", 
                     "vae_dir", 
                     "controlnet_dir",
                     "controlnet_annotator_models_path", 
                     "temp_dir",
                     "sdWebUi_dir", 
                     "sdWebUiExtensions_dir", 
                     "animatediff_dir",
                     "dreambooth_models_path"]

    run_config = _get_runConfig(ui_config)

    for key in keys_to_check:
        path = run_config.get(key)
        # 如果key不在run_config中，尝试从get_run_config_value获取
        if path is None:
            path = get_run_config_value(ui_config, key)

        # 检查路径是否存在，并根据需要创建目录
        if path and not os.path.exists(path):
            os.makedirs(path)
            # print(f"Created directory: {path}")
        elif path:
            # print(f"Directory already exists: {path}")
            pass
        else:
            # print(f"Key '{key}' not found in configuration or has no value.")
            pass

def get_config_dirs(ui_config):
    """
    获取带中文注释的, 指定的几个路径
    
    (路径注释, 路径key)
    如果没有找到key会从内置配置获取(防止更新失效)
    """
    def add_directory(key, display_name, path):
        custom_names[key] = display_name
        config[key] = path

    config = _get_runConfig(ui_config)

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

    # 使用 add_directory 方法添加新的目录项
    # add_directory("temp_dir", "数据盘目录", "/root/autodl-tmp")

    dir_info = []
    for key in custom_names:
        if key in config:
            dir_path = config[key]
        else:
            # 如果key不在config中，则尝试通过get_run_config_value获取
            dir_path = get_run_config_value(ui_config, key)
            config[key] = dir_path  # 更新config字典

        # Check if the directory exists, if not create it
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        dir_info.append((custom_names[key], key))

    return dir_info

def get_config_path(ui_config, key):
    """
    获取系统所设置的默认配置中的某个key对应的值
    """
    try:
        config = _get_runConfig(ui_config)
        return config.get(key)
    except Exception as e:
        run_config_index = "xiaolxlDefault"
        run_configs = ui_config.get_config_value("runConfigs")
        config = run_configs.get(run_config_index, {})
        return config.get(key)
    
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


def get_xiaolxl_jupyter_controller_path():
    """
    获取xiaolxl_jupyter_controller项目路径
    """
    # 获取当前文件的绝对路径
    current_file = os.path.abspath(__file__)

    # 获取当前文件所在的目录
    current_dir = os.path.dirname(current_file)

    # 获取当前目录的上一级目录
    parent_dir = os.path.dirname(current_dir)

    return parent_dir
    
def generate_random_letters(length=20):
    """
    随机指定数量生成字母
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))