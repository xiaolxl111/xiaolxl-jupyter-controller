class VersionController:
    def __init__(self, debug=False):
        import json
        import os

        self._debug = debug  # 新增的私有属性，用于控制调试输出

        # 设置JSON文件的路径
        current_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(current_dir, '..', 'data', 'xiaolxl_jupyter_controller_version.json')

        # 读取JSON文件
        try:
            with open(json_file_path, 'r') as file:
                self.data = json.load(file)
                self._debug_print(f"JSON文件加载成功: {json_file_path}")
        except FileNotFoundError:
            self._debug_print(f"文件未找到: {json_file_path}")
            self.data = {}

    def _debug_print(self, message):
        """如果启用了调试模式，打印调试信息。"""
        if self._debug:
            print("[VersionController]: ", message)

    def get_version(self):
        """从JSON文件返回版本号。"""
        version = self.data.get("xiaolxl_jupyter_controller_version", "Unknown")
        self._debug_print(f"获取的版本号: {version}")
        return version
    
    def get_data(self):
        return self.data
    
    def get_version_from_json(self, json_data):
        """从提供的JSON数据中获取版本号。"""
        if not isinstance(json_data, dict):
            self._debug_print("提供的数据不是有效的JSON对象")
            return "Invalid data"

        version = json_data.get("xiaolxl_jupyter_controller_version", "Unknown")
        self._debug_print(f"从指定的JSON数据中获取的版本号: {version}")
        return version
    
    def get_update_time(self):
        """从JSON文件返回更新时间。"""
        update_time = self.data.get("update_time", "Unknown")
        self._debug_print(f"获取的更新时间: {update_time}")
        return update_time

    def is_version_lower(self, compare_version):
        """
        将当前版本与给定版本进行比较。
        如果当前版本较低，则返回True，否则返回False。
        """
        current_version = self.get_version()
        if current_version == "Unknown":
            self._debug_print("当前版本未知，无法比较")
            return False

        # 将版本号分割成各部分并比较每一部分
        current_version_parts = [int(part) for part in current_version.split('.')]
        compare_version_parts = [int(part) for part in compare_version.split('.')]
        
        is_lower = current_version_parts < compare_version_parts
        self._debug_print(f"当前版本 {current_version_parts} 是否低于 {compare_version_parts}: {is_lower}")
        return is_lower


# 创建一个开启了调试模式的 VersionController 实例
# versionController = VersionController(debug=True)
# 获取当前的版本号
# current_version = versionController.get_version()
# 比较当前版本和另一个版本
# compare_version = "1.0.0"
# is_lower = versionController.is_version_lower(compare_version)

