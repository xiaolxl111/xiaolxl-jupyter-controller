import json
import os

class JsonConfigManager:
    def __init__(self, user_config_path, default_config_path, debug=False):
        self.debug = debug
        self.user_config_path = user_config_path
        self.default_config_path = default_config_path
        self.user_config = self.read_config(user_config_path)
        self.default_config = self.read_config(default_config_path)
        
        self.debug_print("配置管理器以调试模式初始化。")

    def debug_print(self, *msgs):
        if self.debug:
            for msg in msgs:
                print(msg)

    def read_config(self, path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            self.debug_print(f"未找到位于 {path} 的配置文件。")
            return {}

    def obtain_run_config_index(self):
        # 获取运行配置索引
        if self.user_config.get('runConfigIndex'):
            return self.user_config.get('runConfigIndex')
        else:
            return "xiaolxlDefault"

    def obtain_default_run_config(self):
        # 获取默认运行配置
        return self.user_config.get('runConfigs', {}).get('xiaolxlDefault')

    def obtain_run_config_index_config(self):
        # 获取指定索引的运行配置
        index = self.obtain_run_config_index()
        return self.user_config.get('runConfigs', {}).get(index)

    def obtain_run_configs_list(self):
        # 获取所有运行配置的列表
        return self.user_config.get('runConfigs', {})

    def get_config_item(self, config_id, item):
        # 尝试获取指定ID的用户配置项
        config = self.user_config.get('runConfigs', {}).get(config_id, {})
        if item in config:
            return config[item]

        # 若未找到，尝试获取用户默认配置项
        default_config = self.obtain_default_run_config()
        if default_config and item in default_config:
            return default_config[item]

        # 若仍未找到，尝试获取默认配置的默认项
        default_default_config = self.default_config.get('runConfigs', {}).get('xiaolxlDefault', {})
        default_value = default_default_config.get(item)

        # 若在默认配置中找到默认值，将其设置在用户配置中并保存
        if default_value is not None:
            self.set_and_save_config_item(config_id, item, default_value)
            self.debug_print(f"在 '{config_id}' 中设置 '{item}' 的默认值，并保存用户配置。")
        return default_value

    def get_default_config_item(self, item):
        # 获取默认配置项
        return self.get_config_item('xiaolxlDefault', item)

    def get_run_config_index_item(self, item):
        # 获取运行配置索引项
        index = self.obtain_run_config_index()
        if index:
            return self.get_config_item(index, item)
        return self.get_default_config_item(item)

    def save_config(self):
        # 保存用户配置
        with open(self.user_config_path, 'w') as file:
            json.dump(self.user_config, file, indent=4)
            self.debug_print(f"用户配置已保存至 {self.user_config_path}。")

    def set_and_save_config_item(self, config_id, item, value):
        # 设置并保存配置项
        self.user_config.setdefault('runConfigs', {}).setdefault(config_id, {})[item] = value
        self.debug_print(f"已设置 {item} 在 {config_id} 中的值为 {value} 并保存。")
            
    def set_run_config_index(self, new_index):
        # 设置新的运行配置索引
        self.user_config['runConfigIndex'] = new_index
        self.debug_print(f"运行配置索引已更新为 {new_index} 并保存。")

    def remove_config(self, config_id):
        # 检查配置ID是否存在于用户配置中
        if config_id in self.user_config.get('runConfigs', {}):
            # 从用户配置中删除指定的配置ID
            del self.user_config['runConfigs'][config_id]
            # 保存更新后的用户配置
            self.save_config()
            self.debug_print(f"配置 '{config_id}' 已从用户配置中删除并保存。")
        else:
            self.debug_print(f"未找到配置 '{config_id}'，无法删除。")

    def get_directory_mapper_items(self):
        # 初始化最终的目录映射项列表，首先使用用户配置
        merged_directory_mapper_items = self.user_config.get('directoryMapperItems', [])
        
        # 将用户配置项转换为键值对的形式，以便检查默认配置项是否已存在
        user_config_keys = {list(item.keys())[0]: list(item.values())[0] for item in merged_directory_mapper_items}

        # 遍历默认配置中的每个目录映射项
        for default_item in self.default_config.get('directoryMapperItems', []):
            default_key = list(default_item.keys())[0]
            
            # 如果默认配置项的键不在用户配置键中，则添加到最终列表中
            if default_key not in user_config_keys:
                merged_directory_mapper_items.append(default_item)

        return merged_directory_mapper_items

    def set_directory_mapper_items(self, directory_mapper_items):
        # 设置 directoryMapperItems 的值，并仅保存这部分到用户配置文件中
        self.user_config['directoryMapperItems'] = directory_mapper_items
        self.save_specific_config('directoryMapperItems')

    def save_specific_config(self, config_key):
        # 读取当前用户配置文件的内容
        current_config = {}
        try:
            with open(self.user_config_path, 'r') as file:
                current_config = json.load(file)
        except FileNotFoundError:
            self.debug_print(f"未找到位于 {self.user_config_path} 的配置文件，将创建新文件。")

        # 更新特定配置项
        current_config[config_key] = self.user_config[config_key]

        # 确保目录存在
        directory = os.path.dirname(self.user_config_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            self.debug_print(f"目录 {directory} 不存在，已创建。")

        # 将更新后的配置写回文件
        with open(self.user_config_path, 'w') as file:
            json.dump(current_config, file, indent=4)
            self.debug_print(f"{config_key} 配置已更新并保存至 {self.user_config_path}。")

    def print_config(self):
        self.debug_print(
            "============配置内容开始===========",
            "当前用户配置:",
            json.dumps(self.user_config, indent=4),
            "默认配置:",
            json.dumps(self.default_config, indent=4),
            "============配置内容结束==========="
        )
