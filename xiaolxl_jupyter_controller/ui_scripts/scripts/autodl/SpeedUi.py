import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import subprocess
import os

from ...tools.compoment.ui_tool import * 
from ...tools.utils.speed_tool import * 
from ...tools.utils.print_tool import * 

def show(data,cmd_run,controllers):
    network_version_json, is_from_network = controllers['jsonFetcher'].fetch_json(data['branch'],"ui_scripts/data/xiaolxl_jupyter_controller_version.json")
    versionController = controllers['versionController']
    is_allow_network = data['jsonFetcherNetwork']

    network_version = versionController.get_version_from_json(network_version_json)

    # 加速按钮
    speed = XLButton(description='点我自动学术加速', button_style='info', icon='close', layout=Layout(width='auto', height='auto'))
    
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

    # ============================================

    version_ui = widgets.HTML(value="")
    is_version_lower = versionController.is_version_lower(network_version)
    if is_version_lower and is_from_network:
        version_ui.value = html_red_text("启动器检测到新版本, 请及时更新", single_line=False)
    if not is_allow_network:
        version_ui.value = html_blue_text("你已关闭启动器更新检测，请记得手动检查更新", single_line=False)
    if is_allow_network and not is_from_network:
        version_ui.value = html_blue_text("自动检测启动器新版本失败，请记得手动检查更新", single_line=False)

    # ============================================

    display(HBox([speed,version_ui]))