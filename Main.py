import os
import importlib
import json

# 数据配置
data = {
    "debug": False,                             # 是否开启全局调试  (一般开发者或询问报错时使用)  [True/False]
    "config_file": "/root/autodl-tmp/ui.json",  # 配置文件位置      (一般开发者或询问报错时使用)  [绝对路径]
    "jsonFetcherTimeout": 5,                    # 网络获取超时设置  (一般开发者或询问报错时使用)  [整数(单位秒)]
    "jsonFetcherNetwork": True                  # 是否开启网络获取  (一般开发者或询问报错时使用)  [True/False]
}

# UI 配置字典
project_configs = {
    "autodl_comfyui": {
        "dir": "ComfyUI",
        "module": "xiaolxl_jupyter_controller.ComfyUiMain",
        "default": True
    },
    "autodl_sdwebui": {
        "dir": "stable-diffusion-webui",
        "module": "xiaolxl_jupyter_controller.WebUiMain",
        "default": True
    }
}

def read_project_config():
    try:
        with open("../ServerConfig.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    except Exception as e:
        return None

def check_if_directory_exists(directory_name):
    dir_path = f'../{directory_name}'
    exists = os.path.exists(dir_path) and os.path.isdir(dir_path)
    if data['debug']:
        print(f"检查目录 {directory_name}: {'存在' if exists else '不存在'}")
    return exists

def select_ui(cmd_run):
    project_config = read_project_config()
    if project_config:
        module_path = project_configs[project_config["project_name"]]["module"]
        UiMain = importlib.import_module(module_path)
        UiMain.show(data, cmd_run)
    else:
        for project_name, project_info in project_configs.items():
            if check_if_directory_exists(project_info["dir"]) and project_info["default"]:
                module_path = project_info["module"]
                UiMain = importlib.import_module(module_path)
                UiMain.show(data, cmd_run)
                break
        print("没有找到你需要的UI, 请手动设置或检查项目名字与位置是否正确")

def show(cmd_run):
    select_ui(cmd_run)