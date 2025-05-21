import os
import importlib
import json
from xiaolxl_jupyter_controller.RootDir import get_import_root_dir

# 数据配置
data = {
    "debug": False,                             # 是否开启全局调试  (一般开发者或询问报错时使用)  [True/False]
    "jsonFetcherTimeout": 5,                    # 网络获取超时设置  (一般开发者或询问报错时使用)  [整数(单位秒)]
    "jsonFetcherNetwork": True,                 # 是否开启网络获取  (一般开发者或询问报错时使用)  [True/False]
    "branch": "main"                            # 当前分支         (一般开发者或询问报错时使用)  [分支名字(main/dev)]
}

# UI 配置字典
# project_configs = { ... } # Removed and loaded from JSON file

def load_project_configs() -> dict:
    """Loads project configurations from the JSON file."""
    # Construct path using get_import_root_dir from RootDir.py
    import_root_dir = get_import_root_dir()
    config_path = os.path.join(import_root_dir, 'launcher_projects_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The project configuration file was not found at {config_path}")
        # Depending on requirements, could raise error, return default, or exit
        raise  # Re-raise the exception as this file is crucial
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {config_path}")
        raise # Re-raise

project_configs = load_project_configs()

def read_project_config() -> dict | None:
    try:
        with open("../ServerConfig.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        if data['debug']:
            print(f"读取镜像配置文件ServerConfig.json时,未找到文件")
        return None
    except json.JSONDecodeError:
        if data['debug']:
            print(f"读取镜像配置文件ServerConfig.json时,json转换失败")
        return None
    except Exception as e:
        if data['debug']:
            print(f"读取镜像配置文件ServerConfig.json时,发生未知错误: {e}")
        return None

def check_if_directory_exists(directory_name: str) -> bool:
    dir_path = f'../{directory_name}'
    exists = os.path.exists(dir_path) and os.path.isdir(dir_path)
    if data['debug']:
        print(f"检查镜像中项目目录 {directory_name}: {'存在' if exists else '不存在'}")
    return exists

def select_ui(cmd_run: object) -> None:
    # Ensure project_configs is loaded, could be done globally as above or here
    # if 'project_configs' not in globals() or project_configs is None:
    #     global project_configs
    #     project_configs = load_project_configs()
    #     if project_configs is None: # Handle case where loading failed and returned None
    #         print("Failed to load project configurations. Cannot select UI.")
    #         return

    project_config = read_project_config()
    if project_config:
        project_name = project_config.get("project_name")
        if project_name and project_name in project_configs:
            config_file_path = project_configs[project_name]["config_file"]
            data['config_file'] = config_file_path  # 设置config_file的路径
            module_path = project_configs[project_name]["module"]
            UiMain = importlib.import_module(module_path)
            UiMain.show(data, cmd_run)
        else:
            print(f"Project name '{project_name}' not found in launcher_projects_config.json or project_name is missing. Falling back to default.")
            # Fallback logic from original else block
            for proj_name, project_info in project_configs.items(): # Use a different variable name
                if check_if_directory_exists(project_info["dir"]) and project_info["default"]:
                    config_file_path = project_info["config_file"]
                    data['config_file'] = config_file_path
                    module_path = project_info["module"]
                    UiMain = importlib.import_module(module_path)
                    UiMain.show(data, cmd_run)
                    return
            UiMain = importlib.import_module("xiaolxl_jupyter_controller.AutoDlMain")
            data['config_file'] = "/root/autodl-tmp/default_ui.json"
            UiMain.show(data, cmd_run)
            print("No default project found in config or directory check failed. Loaded AutoDlMainUI.")
    else:
        for project_name, project_info in project_configs.items():
            if check_if_directory_exists(project_info["dir"]) and project_info["default"]:
                config_file_path = project_info["config_file"]
                data['config_file'] = config_file_path  # 设置config_file的路径
                module_path = project_info["module"]
                UiMain = importlib.import_module(module_path)
                UiMain.show(data, cmd_run)
                return
        # 如果没有找到匹配的项目，使用默认的UI并设置默认的config_file路径
        UiMain = importlib.import_module("xiaolxl_jupyter_controller.AutoDlMain") # 无对应UI的默认UI
        data['config_file'] = "/root/autodl-tmp/default_ui.json"  # 无对应UI的默认配置路径
        UiMain.show(data, cmd_run)
        print("没有找到你需要的UI, 已加载默认的AutoDlMainUI")

def show(cmd_run: object) -> None:
    select_ui(cmd_run)