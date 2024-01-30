import os
import ipywidgets as widgets
from ipywidgets import Layout,Label,HBox,VBox,GridBox

from ...tools.ui_tool import * 
from ...tools.print_tool import * 
from ...tools.config_tool import * 
from ...tools.download_tool import * 

def getUi(data,cmd_run,controllers):
    ui_constructor = UIConstructor()
    rootOut = ui_constructor.get_output_component()

    modList, _ = controllers['jsonFetcher'].fetch_json("https://jihulab.com/xiaolxl_pub/xiaolxl-jupyter-controller/-/raw/main/xiaolxl_jupyter_controller/ui_scripts/data/autodl_webui/modList.json", "../data/autodl_webui/modList.json")
    logOut = controllers['logOut']
    uiConfig = controllers['uiConfig']

    with rootOut:

        ui_constructor.add_component(
            widgets.HTML(value="<font size='2' color='red'>1.下载前记得安装下载器,有问题的情况下可以尝试开启学术加速</font>\
                         <br><font size='2' color='red'>2.下载前记得检查空间是否足够</font>\
                         <br><font size='2' color='red'>3.模型请根据自己需要下载，不是全部需要下载</font>\
                         <br><font size='2' color='red'>4.下载内置模型如果有报错,可以等待一会儿再次下载</font>\
                         <br><font size='2' color='red'>5.如果出现已下载文件没有显示，可能是文件有更新或者原文件被移动或改名</font>")
        )

        install_download = XLButton(
                description='点我安装下载器',
                button_style='info',
                icon='download',
                layout=Layout(width='200px', height='auto')
        )

        if os.system(f'aria2c -v') == 0 and os.system(f'cg') == 0:
            install_download.button_yes_end('已成功安装下载器')
        ui_constructor.clear_output()

        # 安装下载器
        def install_download_f(self):
            with rootOut:
                if os.system(f'aria2c -v') != 0:
                    install_download.button_start('正在安装...')
                    cmd_run("cd /root/autodl-tmp/ && apt-get update && apt-get install aria2 -y")
                    cmd_run("cd /root/autodl-tmp/ && apt-get install aria2 -y && echo 安装完成")
                if os.system(f'cg') != 0:
                    install_download.button_start('正在安装...')
                    cmd_run("cd /root/autodl-tmp/ && pip install codewithgpu")
                    cmd_run("cd /root/autodl-tmp/ && pip install codewithgpu && echo 安装完成")
                if os.system(f'aria2c -v') == 0 and os.system(f'cg') == 0:
                    install_download.button_yes_end('已成功安装下载器')
                    ui_constructor.clear_output()
                else:
                    install_download.button_no_end('安装下载器失败，请保留错误信息并询问作者')
            
        install_download.on_click(install_download_f)
        ui_constructor.add_component(install_download)


        # ============================


        custom_download_constructor = UIConstructor()

        download_link_input = widgets.Textarea(
            value='',
            placeholder='请输入下载直链或种子地址',
            description='',
            disabled=False,
            layout=Layout(width='700px', height='80px')
        )
        custom_download_constructor.add_component(download_link_input)

        output_filename_input = widgets.Text(
            value='',
            placeholder='请输入下载后的文件名(必填,记得加后缀名!)[填写例子:mod.ckpt]',
            description='',
            disabled=False,
            layout=Layout(width='700px', height='auto')
        )
        custom_download_constructor.add_component(output_filename_input)

        # 创建/初始化目录地
        config_dirs = get_config_dirs(uiConfig)
        create_directories_from_config(uiConfig)
        installation_location_dropdown = widgets.Dropdown(
            options=config_dirs,
            value=config_dirs[0][1],
            description='选择安装位置:',
            style={'description_width': 'initial'},
            disabled=False,
        )
        download_method_dropdown = widgets.Dropdown(
            options=[("多线程下载(默认)","more"),("单一下载","one")],
            value="more",
            description='选择下载方式:',
            style={'description_width': 'initial'},
            disabled=False,
        )
        custom_download_constructor.add_component(HBox([installation_location_dropdown, download_method_dropdown]))

        is_hf_speed = widgets.Checkbox(
            value=True,
            description="是否开启抱脸链接加速(加速状态下可能第一次会报错,再次下载即可)",
            style={'description_width': 'initial'},
            layout=Layout(width='650px', height='auto')
        )
        custom_download_constructor.add_component(is_hf_speed)

        custom_download_path_input = widgets.Text(
            value='',
            placeholder='请输入自定义下载路径(可选,填后上方安装位置选择无效,请勿添加/root/)[填写例子:stable-diffusion-webui/scripts]',
            description='',
            disabled=False,
            layout=Layout(width='700px', height='auto')
        )
        custom_download_constructor.add_component(custom_download_path_input)

        download_button = XLButton(
            description='下载文件',
            button_style='success', 
            layout=Layout(width='150px', height='auto')
        )
        def replace_url_prefix(url):  
            if url.startswith("https://huggingface.co"):  
                return url.replace("https://huggingface.co", "https://hf-mirror.com", 1)  
            return url
        def download_click(self):
            with rootOut:
                ui_constructor.clear_output()
                download_url = download_link_input.value
                if output_filename_input.value=='':
                    logOut.exp("请输入文件名!")
                if download_link_input.value=='':
                    logOut.exp("请输入文件地址!")
                if is_hf_speed.value == True:
                    download_url = replace_url_prefix(download_link_input.value)
                if custom_download_path_input.value=="":
                    download_path = get_config_path(uiConfig, installation_location_dropdown.value)
                    cmd_run(get_download_command(download_url,download_path,output_filename_input.value,download_method_dropdown.value))
                else:
                    cmd_run(get_download_command(download_url,"/root/" + custom_download_path_input.value,output_filename_input.value,download_method_dropdown.value))
        download_button.on_click_with_style(download_click,"正在下载")
        custom_download_constructor.add_component(download_button)


        # ============================


        built_in_download_constructor = UIConstructor()

        # 自定义的按钮类
        class ModButton(XLButton):
            def __init__(self, mod_name, mod_children, **kwargs):
                super().__init__(description=mod_name,layout=Layout(width='150px', height='auto'), **kwargs)
                self.mod_children = mod_children
                self.on_click(self._on_click)
                if self.check_all_downloaded():
                    self.button_yes_end('已下载')

            def check_all_downloaded(self):
                try:
                    for mod_child in self.mod_children:
                        download_path = get_config_path(uiConfig, mod_child['parentPath']) + mod_child['sonPath']
                        filename = mod_child['fileName']
                        downloadType = mod_child['downloadType']
                        if not check_downloaded(downloadType, filename, download_path, mod_child):
                            return False
                except TypeError:
                    with rootOut:
                        print(red_text("检测到未知配置项,将会影响模型/依赖下载！请立即更新启动器！"))
                    return False
                return True

            def download_file(self,mod_child, index, total):
                with rootOut:
                    download_link = mod_child['url']
                    download_path = get_config_path(uiConfig, mod_child['parentPath']) + mod_child['sonPath']
                    filename = mod_child['fileName']
                    downloadType = mod_child['downloadType']

                    # 检查文件是否已下载
                    if check_downloaded(downloadType, filename, download_path, mod_child):
                        print(f"正在下载第{index + 1}个文件，共{total}个")
                        print(f"文件 {filename} 已下载，跳过...")
                    else:
                        download_command = get_download_command(download_link, download_path, filename, "more", mod_child['downloadType'])
                        print(f"正在下载第{index + 1}个文件，共{total}个")
                        cmd_run(download_command)

            def _on_click(self, b):
                with rootOut:
                    self.button_start('正在下载...')
                    ui_constructor.clear_output()
                    total_files = len(self.mod_children)
                    for index, child in enumerate(self.mod_children):
                        self.download_file(child, index, total_files)
                    if self.check_all_downloaded():
                        self.button_yes_end('已下载')
                    else:
                        self.button_no_end('下载失败，点击重新下载')

        for item in modList['ts']:
            title = item['title']
            built_in_download_constructor.add_component(widgets.HTML(value=f"<h4 style='color:blue'>{title}</h4>"))

            # 存储所有标签和按钮的列表
            components = []

            for mod in item['mods']:
                # 创建并添加标签
                file_temp = widgets.HTML(value=f"{mod['modName']}")

                # 创建并添加按钮
                button = ModButton("点我下载", mod['modChildren'])

                components.append(HBox([file_temp,button]))

            # 使用 GridBox 显示标签和按钮
            grid = widgets.GridBox(children=components, layout=widgets.Layout(
                width='100%',
                grid_template_columns='auto auto',
                grid_template_rows='auto auto',
                grid_gap='5px 10px')
            )
            built_in_download_constructor.add_component(grid)


        # ============================


        webSite_constructor = UIConstructor()

        cdg_ = widgets.HTML(
            value="<font size='4px' color='#0fa3ff'><a target='_blank' href='https://www.bilibili.com/read/cv21386117'>1.藏丹阁</a></font><br>",
        )
        webSite_constructor.add_component(cdg_)
        
        web_123114514 = widgets.HTML(
            value="<font size='4px' color='#0fa3ff'><a target='_blank' href='http://www.123114514.xyz/models'>2.123114514模型站</a></font>",
        )
        webSite_constructor.add_component(web_123114514)


        # ============================


        accordion = widgets.Accordion(children=[custom_download_constructor.get_ui_no_out(),built_in_download_constructor.get_ui_no_out(),webSite_constructor.get_ui_no_out()])
        accordion.set_title(0, '自定义下载')
        accordion.set_title(1, '内置模型下载')
        accordion.set_title(2, '模型网站')
        accordion.selected_index = None
        ui_constructor.add_component(accordion)

        # logOut.print(red_text("这是一条消息。\n") + str(modList))
    
    return ui_constructor.get_ui()