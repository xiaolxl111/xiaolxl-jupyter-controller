import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import subprocess
import os

from ui_tool import * 
from speed_tool import * 

def show(data,cmd_run,controllers):

    # 加速按钮
    speed = XLButton(description='点我自动学术加速', button_style='info', icon='close')
    
    # 判断是否已经加速
    if get_is_speed():
        speed.button_yes_end("你已处于加速状态,再次点击取消")

    # 自动加速
    def autospeed(self):
        if get_is_speed() != True:
            speed.button_start("正在自动学术加速")

            
            result = subprocess.run('bash -c "source /etc/network_turbo && env | grep proxy"', shell=True, capture_output=True, text=True)
            output = result.stdout
            for line in output.splitlines():
                if '=' in line:
                    var, value = line.split('=', 1)
                    os.environ[var] = value

            speed.button_yes_end("加速成功,再次点击取消 (新版加速不会显示区域)")
        else:
            del(os.environ["http_proxy"])
            del(os.environ["https_proxy"])
            speed.reset_button()
        
    speed.on_click(autospeed)

    display(speed)