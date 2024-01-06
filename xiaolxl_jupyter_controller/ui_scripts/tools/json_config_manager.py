import json
import os

class JsonConfigManager:
    def __init__(self, file_path, default_config_path, debug=False):
        self.file_path = file_path
        self.default_config_path = default_config_path
        self.debug = debug
        self.default_data = self._read_default_config()
        self.data = self._read_or_create()
        self.print_config()

    def _read_default_config(self):
        if os.path.exists(self.default_config_path):
            with open(self.default_config_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            self._debug_print(f"默认配置文件 {self.default_config_path} 不存在")
            return {}

    def _read_or_create(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}

    def _debug_print(self, message):
        if self.debug:
            print(f"[JsonConfigManager]: {message}")

    def get_config_value(self, key):
        self._debug_print(f"尝试获取配置项 '{key}'")
        keys = key.split('.')
        value = self.data
        try:
            for k in keys:
                value = self._get_value_with_key(value, k)
            return value
        except KeyError:
            self._debug_print(f"配置项 '{key}' 不存在，从默认配置中获取")
            default_value = self.default_data
            for k in keys:
                default_value = self._get_value_with_key(default_value, k)
            self.set_config_value(key, default_value)
            return default_value

    def _get_value_with_key(self, value, key):
        if '[' in key and ']' in key:
            key, index = key[:-1].split('[')
            index = int(index)
            if key not in value or not isinstance(value[key], list) or index >= len(value[key]):
                raise KeyError("配置项不存在或索引超出范围")
            return value[key][index]
        else:
            if key not in value:
                raise KeyError(f"配置项 '{key}' 不存在")
            return value[key]

    def set_config_value(self, key, value):
        self._debug_print(f"设置配置项 '{key}' 的值为 '{value}'")
        keys = key.split('.')
        temp = self.data
        for k in keys[:-1]:
            if '[' in k and ']' in k:
                k, index = k[:-1].split('[')
                index = int(index)
                while len(temp.setdefault(k, [])) <= index:
                    temp[k].append({})
                temp = temp[k][index]
            else:
                temp = temp.setdefault(k, {})
        last_key = keys[-1]
        if '[' in last_key and ']' in last_key:
            last_key, index = last_key[:-1].split('[')
            index = int(index)
            while len(temp.setdefault(last_key, [])) <= index:
                temp[last_key].append(None)
            temp[last_key][index] = value
        else:
            temp[last_key] = value

    def remove_config_value(self, key):
        self._debug_print(f"尝试删除配置项 '{key}'")
        keys = key.split('.')
        temp = self.data
        for k in keys[:-1]:
            if '[' in k and ']' in k:
                k, index = k[:-1].split('[')
                index = int(index)
                if k not in temp or not isinstance(temp[k], list) or index >= len(temp[k]):
                    raise KeyError("配置项不存在或索引超出范围")
                temp = temp[k][index]
            else:
                if k not in temp:
                    raise KeyError("配置项不存在")
                temp = temp[k]

        last_key = keys[-1]
        if '[' in last_key and ']' in last_key:
            last_key, index = last_key[:-1].split('[')
            index = int(index)
            if last_key in temp and isinstance(temp[last_key], list) and index < len(temp[last_key]):
                temp[last_key].pop(index)
            else:
                raise KeyError("配置项不存在或索引超出范围")
        else:
            if last_key in temp:
                del temp[last_key]
            else:
                raise KeyError("配置项不存在")

    def save_config(self):
        self._debug_print(f"保存配置到文件 {self.file_path}")
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def print_config(self):
        self._debug_print("============配置内容开始===========")
        if self.debug:
            print(json.dumps(self.data, ensure_ascii=False, indent=4))
        self._debug_print("============配置内容结束===========")

# 使用示例
# defconfig_file = '/root/autodl-tmp/cs.json'
# config_file = '/root/autodl-tmp/cs2.json'  # 配置文件路径
# config_manager = JsonConfigManager(config_file, defconfig_file, debug=True)  # 开启调试模式

# 获取并显示配置项的值，如果不存在则显示默认值并更新
# value = config_manager.get_config_value('runSetting[0].name')
# value = config_manager.get_config_value('abc[0].name.list[0]')
# value = config_manager.get_config_value('abc[0].name.list[1]')

# config_manager.print_config()
# config_manager.save_config()
# print(value)
