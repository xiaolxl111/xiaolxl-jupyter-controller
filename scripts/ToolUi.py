import os
import ipywidgets as widgets
from ipywidgets import Layout,Label,HBox,VBox,GridBox

from ui_tool import * 
from print_tool import * 
from config_tool import * 

def getUi(data,cmd_run,controllers):
    ui_constructor = UIConstructor()
    rootOut = ui_constructor.get_output_component()

    logOut = controllers['logOut']
    uiConfig = controllers['uiConfig']

    with rootOut:

        official_help = widgets.HTML(
            value="<h1>官方常用帮助文档</h1>\
                <h3>1.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/arc/'>压缩与解压</a></font></h3>\
                <h3>2.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/netdisk/'>公网网盘上传下载</a></font></h3>\
                <h3>3.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/migrate_instance_2/'>迁移实例(同地区)</a></font></h3>\
                <h3>3.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/migrate_instance/'>迁移实例(不同地区)</a></font></h3>\
                <h3>4.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/ssh_proxy/'>SSH远程连接(无法使用自定义服务的时候使用)</a></font></h3>\
                <h3>5.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/network_turbo/'>学术加速</a></font></h3>\
                <h3>5.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/price/'>充值与计费</a></font></h3>",
        )

        #===========


        extensions_install_ui = UIConstructor()

        extensions_input = widgets.Text(
            value='',
            placeholder='请输入扩展插件的git链接(例如: https://jihulab.com/xiaolxl_pub/sd-webui-animatediff.git)',
            style={'description_width': 'initial'},
            layout=Layout(width='1000px', height='auto'),
            description='扩展插件git链接(安装完毕后记得重启webui):',
            disabled=False
        )
        extensions_install_ui.add_component(extensions_input)
        
        extensions_buttom = widgets.Button(
                description='点击安装',
                style={'description_width': 'initial'},
                layout=Layout(width='400px', height='auto'),
                button_style='success'
        )
        def extensions_buttom_click(self):
            ui_constructor.clear_output()
            ext_dir = get_config_path(uiConfig,"sdWebUiExtensions_dir")
            with rootOut:
                cmd_run("echo 请稍等，正在安装! && cd " + ext_dir + " && git clone " + extensions_input.value + " && echo 插件已安装在" + ext_dir + " && echo 安装完成!")
        extensions_buttom.on_click(extensions_buttom_click)
        extensions_install_ui.add_component(extensions_buttom)


        #===========

        class FileDeletionUI:
            def __init__(self):
                self.ui_components = []

                # Image component
                file = open(get_xiaolxl_jupyter_controller_path() + "/img/删除.png", "rb")
                image = file.read()
                del_img = widgets.Image(
                    value=image,
                    format='png',
                    width=300,
                    height=300
                )
                self.ui_components.append(del_img)

                # Text input component
                self.del_input = widgets.Text(
                    value='',
                    placeholder='请直接粘贴，无需添加/root/',
                    style={'description_width': 'initial'},
                    layout=Layout(width='1000px', height='auto'),
                    description='请输入复制好的文件路径(请直接粘贴，无需添加/root/):',
                    disabled=False
                )
                self.ui_components.append(self.del_input)

                # Delete button
                del_button = widgets.Button(
                    description='点击删除(注意！一定要在上方输入路径！不然会全部删除！)',
                    style={'description_width': 'initial'},
                    layout=Layout(width='400px', height='auto'),
                    button_style='success'
                )

                # Clear path button
                clear_dir_button = widgets.Button(
                    description='点击清空路径',
                    style={'description_width': 'initial'},
                    layout=Layout(width='150px', height='auto'),
                    button_style='danger'
                )

                # Setup button actions
                del_button.on_click(self.del_button_click)
                clear_dir_button.on_click(self.clear_dir_button_click)

                self.ui_components.append(HBox([del_button, clear_dir_button]))

                self.last_path = ""

            def del_button_click(self, _):
                ui_constructor.clear_output()
            
                current_path = self.del_input.value.strip()

                if current_path == "":
                    with rootOut:
                        print(red_text("错误：路径不能为空！"))
                    return

                if self.last_path == "":
                    self.last_path = current_path
                    with rootOut:
                        print("你要删除的路径是:\n" + "/root/" + current_path + "\n" + red_text("请再次点击删除按钮以确认删除"))
                    return

                if current_path != self.last_path:
                    with rootOut:
                        print("你要删除的路径是:\n" + "/root/" + current_path + "\n" + red_text("请再次点击删除按钮以确认删除"))
                    self.last_path = current_path  # 更新 self.last_path
                    return
                
                with rootOut:
                    cmd_run("echo 请稍等，正在删除! && rm -rf /root/" + current_path + " && echo 删除完成!")
                
                self.last_path = ""

            def clear_dir_button_click(self, _):
                self.last_path = ""
                self.del_input.value = ""

            def get_ui_components(self):
                return self.ui_components

        del_ui = UIConstructor()

        file_deletion_ui = FileDeletionUI()
        components = file_deletion_ui.get_ui_components()

        # 遍历数组并添加每个组件
        for component in components:
            del_ui.add_component(component)


        #===========


        other_ui = UIConstructor()

        clear_buttom = widgets.Button(
            description='清理系统盘',
            style={'description_width': 'initial'},
            layout=Layout(width='300px', height='auto'),
            button_style='primary'
        )
        def clear_buttom_click(self):
            ui_constructor.clear_output()
            with rootOut:
                cmd_run("du -sh /root/miniconda3/pkgs/ && rm -rf /root/miniconda3/pkgs/*")
                cmd_run("du -sh /root/.local/share/Trash && rm -rf /root/.local/share/Trash")
                cmd_run("rm -rf ~/.cache/pip")
                cmd_run("echo 清理完成!")
        #绑定加速函数
        clear_buttom.on_click(clear_buttom_click)
        other_ui.add_component(clear_buttom)


        #===========

    
        accordion = widgets.Accordion(children=[official_help,extensions_install_ui.get_ui_no_out(),del_ui.get_ui_no_out(),other_ui.get_ui_no_out()])
        accordion.set_title(0, '官方帮助文档')
        accordion.set_title(1, '扩展/插件安装')
        accordion.set_title(2, '文件/目录删除')
        accordion.set_title(3, '其它工具')
        accordion.selected_index = None
        ui_constructor.add_component(accordion)

    return ui_constructor.get_ui()