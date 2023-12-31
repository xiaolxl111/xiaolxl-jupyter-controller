import ipywidgets as widgets
from ipywidgets import VBox, Button, Layout, HBox

class UIConstructor:
    def __init__(self):
        self.components = []
        # 初始化输出组件
        self.out = widgets.Output(layout={'border': '1px solid black'})

    def add_component(self, component):
        # 直接添加新的组件到列表中
        self.components.append(component)

    def add_hbox_component(self, components):
        components = [components] if not isinstance(components, list) else components
        # 直接添加新的组件到列表中
        self.components.append(HBox(components))
    
    def add_accordion_component(self, components,accordionName,isOpen=False):
        components = [components] if not isinstance(components, list) else components
        accordion = widgets.Accordion(children=components)
        accordion.set_title(0, accordionName)
        accordion.selected_index = 0 if isOpen else None
        self.components.append(accordion)

    def get_ui(self):
        # 在返回之前，将out组件添加到列表的末尾
        return VBox(self.components + [self.out])
    
    def get_ui_no_out(self):
    # 在返回之前，将out组件添加到列表的末尾
        return VBox(self.components)
    
    def get_output_component(self):
        # 返回out组件
        return self.out
    
    def clear_output(self):
        # 清理out
        self.out.clear_output()

class XLButton(Button):
    def __init__(self, 
                 description='', 
                 button_style='', # 'success', 'info', 'warning', 'danger' or '',
                 icon='', 
                 disabled=False, 
                 layout=Layout(width='auto', height='auto'), 
                 style={}):
        super().__init__(description=description,
                         disabled=disabled,
                         button_style=button_style,
                         layout=layout,
                         icon=icon,
                         style=style)
        # 保存初始状态
        self.initial_description = description
        self.initial_button_style = button_style
        self.initial_icon = icon

    def button_start(self, tip='处理中...'):
        """ 更改按钮样式为“正在处理” """
        self.description = tip
        self.button_style = "warning"
        self.icon = "spinner"

    def button_yes_end(self, tip='处理完成'):
        """ 更改按钮样式为“处理完成” """
        self.description = tip
        self.button_style = "success"
        self.icon = "check"

    def button_no_end(self, tip='处理失败'):
        """ 更改按钮样式为“处理失败” """
        self.description = tip
        self.button_style = "danger"
        self.icon = "close"

    def reset_button(self):
        """ 恢复按钮的最初样式和内容 """
        self.description = self.initial_description
        self.button_style = self.initial_button_style
        self.icon = self.initial_icon

    def _package_command(self, command, start_desc, yes_end_desc, no_end_desc):
        self.button_start(start_desc)

        _back = command(self)
        if yes_end_desc != "" and _back:
            self.button_yes_end(start_desc)

        if no_end_desc != "" and not _back:
            self.button_yes_end(start_desc)

        if yes_end_desc == "" and no_end_desc == "":
            self.reset_button()

    def on_click_with_style(self,command, start_desc, yes_end_desc="", no_end_desc=""):
        package_command = self._package_command(command, start_desc, yes_end_desc, no_end_desc)
        self.on_click(package_command)

def get_Dropdown_name_by_key(dropdown,_value):
    return next((name for name, value in dropdown.options if value == _value), None)

# 使用示例
# ui_constructor = UIConstructor()

# 添加一些组件
# name_input = widgets.Text(description='Name:')
# ui_constructor.add_component(name_input)

# 获取并显示UI
# ui = ui_constructor.get_ui()