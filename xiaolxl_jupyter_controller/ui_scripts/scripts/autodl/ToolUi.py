import os
import ipywidgets as widgets
from ipywidgets import Layout,Label,HBox,VBox,GridBox

from ...tools.compoment.ui_tool import * 
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
                <h3>1.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/arc/'>压缩与解压</a></font></h3>\
                <h3>2.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/netdisk/'>公网网盘上传下载</a></font></h3>\
                <h3>3.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/migrate_instance_2/'>迁移实例(同地区)</a></font></h3>\
                <h3>3.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/migrate_instance/'>迁移实例(不同地区)</a></font></h3>\
                <h3>4.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/ssh_proxy/'>SSH远程连接(无法使用自定义服务的时候使用)</a></font></h3>\
                <h3>5.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/network_turbo/'>学术加速</a></font></h3>\
                <h3>5.<font color='#0fa3ff'><a target='_blank' href='https://www.autodl.com/docs/price/'>充值与计费</a></font></h3>",
        )

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
                    placeholder='请输入源文件路径，无需添加/root/',
                    style={'description_width': 'initial'},
                    layout=Layout(width='1000px', height='auto'),
                    description='请输入复制好的源文件路径(无需添加/root/):',
                    disabled=False
                )
                self.ui_components.append(self.src_input)

                # Destination path input
                self.dest_input = widgets.Text(
                    value='',
                    placeholder='请输入目标路径，无需添加/root/',
                    style={'description_width': 'initial'},
                    layout=Layout(width='1000px', height='auto'),
                    description='请输入复制好的目标路径(无需添加/root/):',
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

                src_path = "/root/" + self.src_input.value.strip()
                dest_path = "/root/" + self.dest_input.value.strip()

                if src_path == "/root/" or dest_path == "/root/":
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


        autodl_cg_upload_ui = UIConstructor()

        autodl_cg_upload_ui.add_component(
            widgets.HTML(value="<font size='2' color='red'>如果你不清楚AutoDL-CG(cg upload)是什么，请勿使用</font>")
        )

        cg_upload_folder_path_input = widgets.Text(
            value='',
            placeholder='(例如: autodl-tmp/models)',
            style={'description_width': 'initial'},
            layout=Layout(width='800px', height='auto'),
            description='请输入要上传的文件目录(会自动扫描目录下全部文件，路径不用加/root/):',
            disabled=False
        )
        autodl_cg_upload_ui.add_component(cg_upload_folder_path_input)

        temp_token_input = widgets.Text(
            value='',
            placeholder='',
            style={'description_width': 'initial'},
            layout=Layout(width='800px', height='auto'),
            description='请输入临时Token',
            disabled=False
        )
        autodl_cg_upload_ui.add_component(temp_token_input)

        cg_upload_button = XLButton(description="开始上传", button_style='info', layout=Layout(width='150px', height='auto'))
        autodl_cg_upload_ui.add_component(cg_upload_button)

        def cg_upload_run(self):
            ui_constructor.clear_output()
            with rootOut:
                folder_path = "/root/" + cg_upload_folder_path_input.value
                temp_token = temp_token_input.value
                
                total_files = sum(len(files) for _, _, files in os.walk(folder_path))  
                file_count = 0  # 用于跟踪当前文件的索引  
                
                for root, _, files in os.walk(folder_path):
                    for file in files:  
                        file_count += 1  # 增加文件计数器  
                        
                        # 构造完整的本地文件路径  
                        local_file_path = os.path.join(root, file)  
                        
                        # 打印当前上传的文件信息  
                        print(f"正在上传 {file_count} 个文件中的第 {total_files} 个文件: {local_file_path}")  
                        
                        # 构造要执行的命令  
                        command = f'cg upload {local_file_path} --token {temp_token}'  
                        
                        # 执行命令  
                        cmd_run(command)
        
        cg_upload_button.on_click_with_style(cg_upload_run,"正在上传..")


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
                    cmd_run("cd /root/autodl-tmp/ && apt-get update && apt-get install ffmpeg -y")
                    cmd_run("cd /root/autodl-tmp/ && apt-get install ffmpeg -y && echo 安装完成")
                if os.system(f'ffmpeg -version') == 0:
                    ffmpeg_download.button_yes_end('已成功安装ffmpeg')
                    ui_constructor.clear_output()
                else:
                    ffmpeg_download.button_no_end('安装ffmpeg失败，请保留错误信息并询问作者')
        ffmpeg_download.on_click(ffmpeg_download_f)
        other_ui.add_component(ffmpeg_download)


        #===========

    
        accordion = widgets.Accordion(children=[official_help,del_ui.get_ui_no_out(),file_move_copy_tool_ui.get_ui_no_out(),autodl_cg_upload_ui.get_ui_no_out(),other_ui.get_ui_no_out()])
        accordion.set_title(0, '官方帮助文档')
        accordion.set_title(1, '文件/目录 删除')
        accordion.set_title(2, '文件/目录 移动/复制')
        accordion.set_title(3, 'AutoDL模型文件上传器')
        accordion.set_title(4, '其它工具')
        accordion.selected_index = None
        ui_constructor.add_component(accordion)

    return ui_constructor.get_ui()