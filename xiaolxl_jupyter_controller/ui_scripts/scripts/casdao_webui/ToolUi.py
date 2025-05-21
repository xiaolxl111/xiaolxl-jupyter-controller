import os
import ipywidgets as widgets
from ipywidgets import Layout,Label,HBox,VBox,GridBox

from ...tools.component.ui_tool import * 
from ...tools.utils.print_tool import * 
from ...tools.utils.config_tool import * 

def getUi(data,cmd_run,controllers):
    ui_constructor = UIConstructor()
    rootOut = ui_constructor.get_output_component()

    logOut = controllers['logOut']
    uiConfig = controllers['uiConfig']

    with rootOut:

        official_help = widgets.HTML(
            value="<h1>官方常用帮助文档</h1>\
                <h3>1.<font color='#0fa3ff'><a target='_blank' href='https://console.casdao.com:9006/#/gpu/instructions'>GPU容器云使用说明</a></font></h3>",
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
                file = open(get_xiaolxl_jupyter_controller_path() + "/xiaolxl_jupyter_controller/ui_scripts/img/删除.png", "rb")
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
                    placeholder='请直接粘贴，无需添加/home/tom/',
                    style={'description_width': 'initial'},
                    layout=Layout(width='1000px', height='auto'),
                    description='请输入复制好的文件路径(请直接粘贴，无需添加/home/tom/):',
                    disabled=False
                )
                self.ui_components.append(self.del_input)

                # Delete button
                del_button = widgets.Button(
                    description='点击删除(注意！一定要在上方输入路径！不然会全部删除！)',
                    style={'description_width': 'initial'},
                    layout=Layout(width='400px', height='auto'),
                    button_style='danger'
                )

                # Clear path button
                clear_dir_button = widgets.Button(
                    description='点击清空路径',
                    style={'description_width': 'initial'},
                    layout=Layout(width='150px', height='auto'),
                    button_style='warning'
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
                        print("你要删除的路径是:\n" + "/home/tom/" + current_path + "\n" + red_text("请再次点击删除按钮以确认删除"))
                    return

                if current_path != self.last_path:
                    with rootOut:
                        print("你要删除的路径是:\n" + "/home/tom/" + current_path + "\n" + red_text("请再次点击删除按钮以确认删除"))
                    self.last_path = current_path  # 更新 self.last_path
                    return
                
                with rootOut:
                    cmd_run("echo 请稍等，正在删除! && rm -rf /home/tom/" + current_path + " && echo 删除完成!")
                
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


        class FileMoveCopyUI:
            def __init__(self):
                self.ui_components = []

                file = open(get_xiaolxl_jupyter_controller_path() + "/xiaolxl_jupyter_controller/ui_scripts/img/删除.png", "rb")
                image = file.read()
                move_copy_img = widgets.Image(
                    value=image,
                    format='png',
                    width=300,
                    height=300
                )
                self.ui_components.append(move_copy_img)

                # Single choice for move or copy
                self.move_or_copy = widgets.RadioButtons(
                    options=['复制', '移动'],
                    description='操作类型:',
                    disabled=False
                )
                self.ui_components.append(self.move_or_copy)

                # Source path input
                self.src_input = widgets.Text(
                    value='',
                    placeholder='请输入源文件路径，无需添加/home/tom/',
                    style={'description_width': 'initial'},
                    layout=Layout(width='1000px', height='auto'),
                    description='请输入复制好的源文件路径(无需添加/home/tom/):',
                    disabled=False
                )
                self.ui_components.append(self.src_input)

                # Destination path input
                self.dest_input = widgets.Text(
                    value='',
                    placeholder='请输入目标路径，无需添加/home/tom/',
                    style={'description_width': 'initial'},
                    layout=Layout(width='1000px', height='auto'),
                    description='请输入复制好的目标路径(无需添加/home/tom/):',
                    disabled=False
                )
                self.ui_components.append(self.dest_input)

                # Move/Copy button
                execute_button = XLButton(
                    description='执行操作',
                    style={'description_width': 'initial'},
                    layout=Layout(width='300px', height='auto'),
                    button_style='success'
                )

                # Clear paths button
                clear_paths_button = widgets.Button(
                    description='清空路径',
                    style={'description_width': 'initial'},
                    layout=Layout(width='150px', height='auto'),
                    button_style='warning'
                )

                # Setup button actions
                execute_button.on_click_with_style(self.execute_button_click,"正在执行...")
                clear_paths_button.on_click(self.clear_paths_button_click)

                self.ui_components.append(HBox([execute_button, clear_paths_button]))

                self.last_src_path = ""
                self.last_dest_path = ""

            def execute_button_click(self, _):
                ui_constructor.clear_output()

                src_path = "/home/tom/" + self.src_input.value.strip()
                dest_path = "/home/tom/" + self.dest_input.value.strip()

                if src_path == "/home/tom/" or dest_path == "/home/tom/":
                    with rootOut:
                        print(red_text("错误：源路径和目标路径不能为空！"))
                    return

                operation = "复制" if self.move_or_copy.value == '复制' else "移动"
                confirmation_message = f"你要{operation}的路径是:\n源: {src_path}\n目标: {dest_path}\n请再次点击按钮以确认{operation}"

                if self.last_src_path != src_path or self.last_dest_path != dest_path:
                    with rootOut:
                        print(confirmation_message)
                    self.last_src_path, self.last_dest_path = src_path, dest_path
                    return

                command = "cp -r" if operation == "复制" else "mv"
                with rootOut:
                    cmd_run(f"echo 请稍等，正在{operation}! && {command} {src_path} {dest_path} && echo {operation}完成!")

                self.last_src_path, self.last_dest_path = "", ""

            def clear_paths_button_click(self, _):
                self.last_src_path, self.last_dest_path = "", ""
                self.src_input.value = ""
                self.dest_input.value = ""

            def get_ui_components(self):
                return VBox(self.ui_components)

        file_move_copy_tool_ui = UIConstructor()

        # 使用示例
        file_move_copy_tool = FileMoveCopyUI()
        file_move_copy_ui_components = file_move_copy_tool.get_ui_components()

        # 添加到UI构造器
        file_move_copy_tool_ui.add_component(file_move_copy_ui_components)


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
                cmd_run("rm -rf ~/.cache/pip")
                cmd_run("echo 清理完成!")
        #绑定加速函数
        clear_buttom.on_click(clear_buttom_click)
        other_ui.add_component(clear_buttom)

        ffmpeg_download = XLButton(
                description='点我安装ffmpeg',
                button_style='info',
                icon='download',
                layout=Layout(width='200px', height='auto')
        )
        if os.system(f'ffmpeg -version') == 0:
            ffmpeg_download.button_yes_end('已成功安装ffmpeg')
        ui_constructor.clear_output()
        def ffmpeg_download_f(self):
            with rootOut:
                if os.system(f'ffmpeg -version') != 0:
                    ffmpeg_download.button_start('正在安装...')
                    cmd_run("sudo apt-get update && sudo apt-get install ffmpeg -y")
                    cmd_run("sudo apt-get install ffmpeg -y && echo 安装完成")
                if os.system(f'ffmpeg -version') == 0:
                    ffmpeg_download.button_yes_end('已成功安装ffmpeg')
                    ui_constructor.clear_output()
                else:
                    ffmpeg_download.button_no_end('安装ffmpeg失败, 请保留错误信息并询问作者')
        ffmpeg_download.on_click(ffmpeg_download_f)
        other_ui.add_component(ffmpeg_download)


        #===========

    
        accordion = widgets.Accordion(children=[official_help,extensions_install_ui.get_ui_no_out(),del_ui.get_ui_no_out(),file_move_copy_tool_ui.get_ui_no_out(),other_ui.get_ui_no_out()])
        accordion.set_title(0, '官方帮助文档')
        accordion.set_title(1, '扩展/插件安装')
        accordion.set_title(2, '文件/目录 删除')
        accordion.set_title(3, '文件/目录 移动/复制')
        accordion.set_title(4, '其它工具')
        accordion.selected_index = None
        ui_constructor.add_component(accordion)

    return ui_constructor.get_ui()