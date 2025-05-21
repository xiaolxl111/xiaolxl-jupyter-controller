class ComponentRegistry:
    def __init__(self, debug=False):
        """
        初始化 ComponentRegistry 类。

        :param debug: 是否开启调试模式，默认为 False。
        """
        self.registry = {}
        self.debug = debug

    def log(self, message):
        """
        输出调试信息。

        :param message: 需要输出的消息。
        """
        if self.debug:
            print(f"[ComponentRegistry]: {message}")

    def register(self, key, component):
        """
        注册一个组件。

        :param key: 组件的键。
        :param component: 组件对象。
        :return: 如果注册成功返回 True,如果键已存在则返回 False。
        """
        if key in self.registry:
            self.log(f"注册失败：键 '{key}' 已存在。")
            return False
        else:
            self.registry[key] = component
            self.log(f"组件 '{key}' 已注册。")
            return True

    def unregister(self, key):
        """
        注销一个组件。

        :param key: 组件的键。
        :return: 如果注销成功返回 True,如果键不存在则返回 False。
        """
        if key in self.registry:
            del self.registry[key]
            self.log(f"组件 '{key}' 已注销。")
            return True
        else:
            self.log(f"注销失败：键 '{key}' 不存在。")
            return False

# 示例用法
# registry = ComponentRegistry(debug=True) # 创建组件注册表实例
# registry.register('button1', 'SomeComponent') # 注册组件
# registry.unregister('button1') # 取消注册组件
