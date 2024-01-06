# ANSI颜色代码
RED = '\033[91m'  # 红色
GREEN = '\033[92m'  # 绿色
YELLOW = '\033[93m'  # 黄色
BLUE = '\033[94m'  # 蓝色
MAGENTA = '\033[95m'  # 品红色
CYAN = '\033[96m'  # 青色
RESET = '\033[0m'  # 用于重置颜色设置

def red_text(text):
    return RED + text + RESET  # 返回红色文本

def green_text(text):
    return GREEN + text + RESET  # 返回绿色文本

def yellow_text(text):
    return YELLOW + text + RESET  # 返回黄色文本

def blue_text(text):
    return BLUE + text + RESET  # 返回蓝色文本

def magenta_text(text):
    return MAGENTA + text + RESET  # 返回品红色文本

def cyan_text(text):
    return CYAN + text + RESET  # 返回青色文本

class LogController:
    def __init__(self, enable_output=False):
        self.enable_output = enable_output

    def print(self, *args, **kwargs):
        if self.enable_output:
            print(*args, **kwargs)

    # 抛出错误
    def exp(self,error):
        raise ValueError(error)
    
def html_blue_text(text, single_line=True):
    if single_line:
        return "<p style='color: #000080;'>" + text + "</p>"
    else:
        return "<span style='color: #000080;'>" + text + "</span>"

def html_red_text(text, single_line=True):
    if single_line:
        return "<p style='color: #ff0000;'>" + text + "</p>"
    else:
        return "<span style='color: #ff0000;'>" + text + "</span>"


# 使用示例
# logOut = LogController(enable_output=True)
# logOut.print("这是一条消息。")  # 将打印消息

# logOut.enable_output = False
# logOut.print("这条消息不会被打印。")  # 不会打印任何东西