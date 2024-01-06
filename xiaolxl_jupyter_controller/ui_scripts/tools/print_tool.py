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
    
class PrintQueue:
    def __init__(self):
        # 初始化一个空队列
        self.queue = []

    def add_text(self, text):
        """
        向队列中添加文本
        :param text: 要添加到队列的文本
        """
        self.queue.append(text)

    def print_queue(self):
        """
        按队列顺序打印所有文本
        """
        while self.queue:
            print(self.queue.pop(0))

    def print_all(self):
        self.print_queue()

class PrintQueueManager:
    def __init__(self):
        # 初始化一个空的PrintQueue列表
        self.queues = []

    def add_queue(self, print_queue):
        """
        添加一个PrintQueue实例到管理器
        :param print_queue: PrintQueue实例
        """
        self.queues.append(print_queue)

    def print_all(self):
        """
        执行所有队列的打印操作
        """
        for queue in self.queues:
            queue.print_all()

# 使用示例
# pq1 = PrintQueue()
# pq1.add_text("Hello from Queue 1!")
# pq1.add_text("Another message from Queue 1")
# pq2 = PrintQueue()
# pq2.add_text("Hello from Queue 2!")
# manager = PrintQueueManager()
# manager.add_queue(pq1)
# manager.add_queue(pq2)
# 打印所有队列的内容
# manager.print_all()



# 使用示例
# logOut = LogController(enable_output=True)
# logOut.print("这是一条消息。")  # 将打印消息
# logOut.enable_output = False
# logOut.print("这条消息不会被打印。")  # 不会打印任何东西