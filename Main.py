import os
import importlib

# 数据配置
data = {
    "debug": False,                             # 是否开启全局调试  (一般开发者或询问报错时使用)  [True/False]
    "config_file": "/root/autodl-tmp/ui.json",  # 配置文件位置      (一般开发者或询问报错时使用)  [绝对路径]
    "jsonFetcherTimeout": 5,                    # 网络获取超时设置  (一般开发者或询问报错时使用)  [整数(单位秒)]
    "jsonFetcherNetwork": True                  # 是否开启网络获取  (一般开发者或询问报错时使用)  [True/False]
}

# UI 配置字典
ui_configs = {
    "ComfyUi": {
        "dir": "ComfyUI",
        "module": "xiaolxl_jupyter_controller.ComfyUiMain"
    },
    "WebUi": {
        "dir": "stable-diffusion-webui",
        "module": "xiaolxl_jupyter_controller.WebUiMain"
    }
}

def read_use_style_file():
    file_path = '../useStyle.txt'
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None

def check_if_directory_exists(directory_name):
    dir_path = f'../{directory_name}'
    exists = os.path.exists(dir_path) and os.path.isdir(dir_path)
    if data['debug']:
        print(f"检查目录 {directory_name}: {'存在' if exists else '不存在'}")
    return exists

def select_ui(cmd_run):
    use_style = read_use_style_file()

    if use_style == "auto" or not use_style:
        for style, config in ui_configs.items():
            if check_if_directory_exists(config["dir"]):
                use_style = style
                break

    if use_style in ui_configs:
        module_path = ui_configs[use_style]["module"]
        UiMain = importlib.import_module(module_path)
        UiMain.show(data, cmd_run)
    else:
        print("没有找到你需要的UI, 请手动设置或检查项目名字与位置是否正确")

def show(cmd_run):
    select_ui(cmd_run)