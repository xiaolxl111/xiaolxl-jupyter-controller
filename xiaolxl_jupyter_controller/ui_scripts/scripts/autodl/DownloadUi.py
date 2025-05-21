import os
import ipywidgets as widgets
from ipywidgets import Layout,Label,HBox,VBox,GridBox

from ...tools.component.ui_tool import * 
from ...tools.utils.print_tool import * 
from ...tools.utils.config_tool import * 
from ...tools.utils.download_tool import * 

def getUi(data,cmd_run,controllers):
    ui_constructor = UIConstructor()
    rootOut = ui_constructor.get_output_component()

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


        accordion = widgets.Accordion(children=[custom_download_constructor.get_ui_no_out()])
        accordion.set_title(0, '自定义下载')
        accordion.selected_index = 0
        ui_constructor.add_component(accordion)

        # logOut.print(red_text("这是一条消息。\n") + str(modList))
    
    return ui_constructor.get_ui()