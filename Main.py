import os

# 数据配置
data = {
    "debug": False,                             # 是否开启全局调试  (一般开发者或询问报错时使用)  [True/False]
    "config_file": "/root/autodl-tmp/ui.json",  # 配置文件位置      (一般开发者或询问报错时使用)  [绝对路径]
    "jsonFetcherTimeout": 5,                    # 网络获取超时设置  (一般开发者或询问报错时使用)  [整数(单位秒)]
    "jsonFetcherNetwork": True                  # 是否开启网络获取  (一般开发者或询问报错时使用)  [True/False]
}

class CheckName:
    # 定义UI常量
    AUTO_STYLE = "auto"
    # SdWebUi
    SDWEBUI_STYLE = "WebUi"
    SDWEBUI_DIR = "stable-diffusion-webui"
    # ComfyUi
    COMFYUI_STYLE = "ComfyUi"
    COMFYUI_DIR = "ComfyUI"

def read_use_style_file():
    # 从文件中读取UI样式
    file_path = '../useStyle.txt'
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "-1"

def check_if_directory_exists(directory_name):
    # 检查指定目录是否存在
    dir_path = f'../{directory_name}'
    exists = os.path.exists(dir_path) and os.path.isdir(dir_path)
    if data['debug']:
        print(f"检查目录 {directory_name}: {'存在' if exists else '不存在'}")
    return exists

def get_ui_main(use_style):
    """ 根据UI样式返回相应的主模块 """
    if data['debug']:
        print(f"从文件中读取的UI样式: {use_style}")

    if use_style == CheckName.COMFYUI_STYLE:
        if data['debug']:
            print("加载COMFYUI模块")
        import xiaolxl_jupyter_controller.ComfyUiMain as ComfyUiMain
        return ComfyUiMain
    elif use_style == CheckName.SDWEBUI_STYLE:
        if data['debug']:
            print("加载SDWEBUI模块")
        import xiaolxl_jupyter_controller.WebUiMain as WebUiMain
        return WebUiMain
    else:
        if data['debug']:
            print("未找到匹配的UI模块")
        return None

def select_ui(cmd_run):
    """ 选择合适的UI基于用户配置 """
    use_style = read_use_style_file()

    # 当 use_style 存在且不是 'auto'
    if use_style and use_style != CheckName.AUTO_STYLE:
        UiMain = get_ui_main(use_style)
    else:
        # use_style 为 'auto' 或不存在
        if check_if_directory_exists(CheckName.COMFYUI_DIR):
            UiMain = get_ui_main(CheckName.COMFYUI_STYLE)
        elif check_if_directory_exists(CheckName.SDWEBUI_DIR):
            UiMain = get_ui_main(CheckName.SDWEBUI_STYLE)
        else:
            print("没有找到你需要的UI, 请手动设置或检查项目名字与位置是否正确")
            return

    if UiMain:
        UiMain.show(data, cmd_run)
    else:
        print("没有找到你需要的UI, 请手动设置或检查项目名字与位置是否正确")


def show(cmd_run):
    """ 显示UI界面 """
    select_ui(cmd_run)