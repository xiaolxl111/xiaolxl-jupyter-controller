import subprocess
import os
import ipywidgets as widgets


class DirectoryMapper:
    def __init__(self, original_path):
        # 初始化时，保存原始目录路径
        self.original_path = original_path
        self.mapped = False
        self.mapped_path = None

        # 检查目录是否已经被映射
        self.check_mapping()

    def run_command(self, command):
        # 运行命令并返回输出
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()

    def check_mapping(self):
        # 检查原始目录是否已经映射到其他目录
        if os.path.islink(self.original_path):
            self.mapped = True
            self.mapped_path = os.readlink(self.original_path)
        else:
            self.mapped = False
            self.mapped_path = None

    def create_mapping(self, new_path):
        if new_path == '':
            print("新目录不能为空!")
            return
        # 修复目录不存在bug
        os.makedirs(new_path, exist_ok=True)
        # 如果原始目录没有映射到其他目录，则创建新的映射
        if not self.mapped:
            os.makedirs(new_path, exist_ok=True)  # 创建自定义绝对路径
            self.run_command(f'mv {self.original_path}/* {new_path}')  # 转移文件
            self.run_command(f'rm -rf {self.original_path}')  # 删除原目录
            os.symlink(new_path, self.original_path)  # 创建符号链接
        elif self.mapped_path != new_path:
            os.makedirs(new_path, exist_ok=True)  # 创建自定义绝对路径
            self.run_command(f'mv {self.mapped_path}/* {new_path}')  # 转移文件
            self.run_command(f'rm -rf {self.original_path}')  # 删除原目录
            os.symlink(new_path, self.original_path)  # 创建符号链接

        # 检查目录是否已经被映射
        self.check_mapping()
        
    def remove_mapping(self):
        # 如果有映射，则删除映射
        if self.mapped:
            os.unlink(self.original_path)  # 删除符号链接
            os.makedirs(self.original_path)  # 创建同名目录
            self.run_command(f'mv {self.mapped_path}/* {self.original_path}')  # 转移文件
        else:
            print("此目录没有链接的目录,无需取消链接!")
            return

        # 检查目录是否已经被映射
        self.check_mapping()


class DirectoryMapperUI:
    def __init__(self, directory_link_items, uiConfig, out):
        self.directory_link_items = directory_link_items
        self.directory_mappers = []  # 存储DirectoryMapper对象的数组
        self.main_vbox = widgets.VBox()
        self.uiConfig = uiConfig
        self.out = out
        self.mapping_ui_elements = {}  # 存储每个映射的UI组件
        self.create_directory_mappers()
        self.init_ui()

    def two_step_confirmation(prompt="请再次点击确认您的操作"):
        def decorator(func):
            def wrapper(self, *args, skip_confirmation=False, **kwargs):
                if skip_confirmation:
                    return func(self, *args, **kwargs)

                if not hasattr(func, '_first_call'):
                    func._first_call = True
                    func._prev_args = None
                    func._prev_kwargs = None

                args_changed = args != func._prev_args or kwargs != func._prev_kwargs

                if func._first_call or args_changed:
                    formatted_prompt = prompt.format(*args, **kwargs)
                    self.out.clear_output()
                    with self.out:
                        print(formatted_prompt)
                    func._prev_args = args
                    func._prev_kwargs = kwargs
                    func._first_call = False
                else:
                    func._first_call = True
                    return func(self, *args, **kwargs)

            return wrapper
        return decorator

    def create_directory_mappers(self):
        self.directory_mappers = [DirectoryMapper(original_path) for mapping in self.directory_link_items for original_path, _ in mapping.items()]
        for mapper, mapping in zip(self.directory_mappers, self.directory_link_items):
            for _, mapped_path in mapping.items():
                mapper.create_mapping(mapped_path)
        self.save_directory_link_items()

    def init_ui(self):
        self.tip = widgets.HTML(value="如果你是开发者请注意，为了用户更好的使用，这里内置的设置无法删除，但是可以修改和添加<br>")

        self.new_original_path = widgets.Text(description="原目录:")
        self.new_mapped_path = widgets.Text(description="链接到的目录:")
        create_button = widgets.Button(description="新建")
        create_button.on_click(self.create_mapping_new)
        new_mapping_hbox = widgets.HBox([self.new_original_path, self.new_mapped_path, create_button])

        self.main_vbox.children = [self.tip,new_mapping_hbox]

        for mapping in self.directory_link_items:
            for original_path, mapped_path in mapping.items():
                self.add_mapping_ui(original_path, mapped_path)

    def add_mapping_ui(self, original_path, mapped_path):
        hbox = self.create_mapping_ui(original_path, mapped_path)
        self.mapping_ui_elements[original_path] = hbox
        self.main_vbox.children += (hbox,)

    def remove_mapping_ui(self, original_path):
        hbox = self.mapping_ui_elements.pop(original_path, None)
        if hbox:
            self.main_vbox.children = tuple(child for child in self.main_vbox.children if child != hbox)

    def create_mapping_ui(self, original_path, mapped_path):
        original_path_widget = widgets.Text(value=original_path, description="原目录:", disabled=True)
        mapped_path_widget = widgets.Text(value=mapped_path, description="链接到的目录:", disabled=False)
        modify_button = widgets.Button(description="修改",button_style='warning')
        delete_button = widgets.Button(description="删除",button_style='danger')

        modify_button.on_click(lambda btn: self.modify_mapping(original_path, mapped_path_widget.value))
        delete_button.on_click(lambda btn: self.delete_mapping(original_path))

        return widgets.HBox([original_path_widget, mapped_path_widget, modify_button, delete_button])

    @two_step_confirmation(prompt="您的目录 {0} 将被链接到 {1},并且会转移 原目录或原链接目录 中的文件到 {1},请再次点击进行确认!")
    def modify_mapping(self, original_path, new_mapped_path):
        for mapper, mapping in zip(self.directory_mappers, self.directory_link_items):
            if original_path in mapping:
                mapping[original_path] = new_mapped_path
                mapper.create_mapping(new_mapped_path)
                self.update_single_ui(original_path, new_mapped_path)
                break
        self.out.clear_output()
        with self.out:
            print("链接完成!")
            self.save_directory_link_items()

    @two_step_confirmation(prompt="您的目录 {0} 将被取消链接,并且会转移 链接目录 中的文件到 {0},请再次点击进行确认!")
    def delete_mapping(self, original_path):
        for i, (mapper, mapping) in enumerate(zip(self.directory_mappers, self.directory_link_items)):
            if original_path in mapping:
                del self.directory_link_items[i]
                mapper.remove_mapping()
                del self.directory_mappers[i]
                self.remove_mapping_ui(original_path)
                break
        self.out.clear_output()
        with self.out:
            print("删除链接完成!")
            self.save_directory_link_items()

    @two_step_confirmation(prompt="您的目录将被链接,并且会转移 原目录 中的文件到 被链接目录,请再次点击进行确认!")
    def create_mapping_new(self, btn):
        original_path = self.new_original_path.value
        mapped_path = self.new_mapped_path.value

        # 检查原始路径是否已存在于现有映射中
        if any(original_path in mapping for mapping in self.directory_link_items):
            self.out.clear_output()
            with self.out:
                print(f"原始路径 {original_path} 已存在，请选择不同的原始路径。")
            return

        self.out.clear_output()
        with self.out:
            if original_path and mapped_path:
                self.directory_link_items.append({original_path: mapped_path})
                mapper = DirectoryMapper(original_path)
                mapper.create_mapping(mapped_path)
                self.directory_mappers.append(mapper)
                self.add_mapping_ui(original_path, mapped_path)
                print("链接完成!")
                self.save_directory_link_items()
            else:
                print("输入数据有空值")

    def update_single_ui(self, original_path, mapped_path):
        hbox = self.mapping_ui_elements[original_path]
        hbox.children[1].value = mapped_path  # 更新映射路径的UI显示

    def save_directory_link_items(self):
        self.uiConfig.set_directory_mapper_items(self.directory_link_items)

    def get_ui(self):
        return self.main_vbox

# 初始化WidgetsUI
# directory_link_items = [
#     {"/root/test2": "/root/autodl-tmp/test9"},
#     {"/root/test1": "/root/autodl-tmp/test10"},
# ]

# directory_mapper_ui = DirectoryMapperUI(directory_link_items)
# ui = directory_mapper_ui.get_ui()
# display(ui)  # 使用IPython.display.display来展示UI