import os, sys
import ipywidgets as widgets
from ipywidgets import Layout,Label,HBox,VBox,GridBox
from traitlets import link
import subprocess

from ...tools.component.ui_tool import * 
from ...tools.utils.print_tool import * 
from ...tools.utils.config_tool import * 
from ...tools.utils.speed_tool import * 
from ...tools.utils import thread_out
from ...tools.utils.download_tool import * 
from ...tools.component.directory_link import * 

def getUi(data,cmd_run,controllers):
    ui_constructor = UIConstructor()
    rootOut = ui_constructor.get_output_component()

    logOut = controllers['logOut']
    uiConfig = controllers['uiConfig']

    with rootOut:
        class ComponentsControl:
            def __init__(self):
                self.components = []

            def add_component(self, component):
                self.components.append(component)

            def updata_from_config(self, config_name):
                for component in self.components:
                    component.updata_from_config(config_name)

            def set_to_config(self, config_name):
                for component in self.components:
                    component.set_to_config(config_name)

            def set_command(self, command):
                for component in self.components:
                    component.set_command(command)

        class CommandBuilder:
            def __init__(self):
                self.directory = ""
                self.environment_variables = []
                self.python_path = ""
                self.use_unbuffered = False
                self.script = "launch.py"
                self.arguments = []

            def set_directory(self, directory):
                self.directory = f"cd {directory}"
            
            def add_environment_variable(self, variable, value):
                self.environment_variables.append(f"{variable}={value}")
            
            def set_python_path(self, path):
                self.python_path = path

            def set_unbuffered(self, unbuffered=True):
                self.use_unbuffered = unbuffered
            
            def add_argument(self, argument):
                self.arguments.append(argument)

            def add_custom_launch_arguments(self, custom_args):
                args = custom_args.split()
                self.arguments.extend(args)

            def add_custom_environment_variables(self, custom_env_vars):
                vars = custom_env_vars.split()
                for var in vars:
                    key, value = var.split('=')
                    self.environment_variables.append(f"{key}={value}")

            def build(self):
                command_parts = []
                if self.directory:
                    command_parts.append(self.directory)
                
                unbuffered_flag = "-u" if self.use_unbuffered else ""
                python_command = f"{self.python_path} {unbuffered_flag} {self.script}".strip()
                if self.arguments:
                    python_command += " " + " ".join(self.arguments)

                if self.environment_variables:
                    env_vars_command = " ".join(self.environment_variables)
                    python_command = env_vars_command + " " + python_command

                command_parts.append(python_command)

                return " && ".join(command_parts)
            
            def clear(self):
                self.directory = ""
                self.environment_variables = []
                self.python_path = ""
                self.use_unbuffered = False
                self.script = "launch.py"
                self.arguments = []

        class SelectUIBaseComponent: 
            def __init__(self, checkbox_desc, html_content, configKey):
                self.configKey = configKey

                self.checkBox = widgets.Checkbox(
                    value=get_run_config_value(uiConfig,self.configKey),
                    description=checkbox_desc,
                    layout=Layout(width='auto', height='auto'),
                    disabled=False,
                    indent=False
                )
                
                self.HtmlTip = widgets.HTML(
                    value=html_content,
                )
                
                self.uiBox = HBox([self.checkBox, self.HtmlTip])

            def set_to_config(self,config_name):
                set_run_config_value(uiConfig,self.configKey,self.checkBox.value,config_name)

            def updata_from_config(self,config_name):
                value = get_run_config_value(uiConfig,self.configKey,config_name)
                self.checkBox.value = value

            def get_ui(self):
                return self.uiBox
            
            def get_checkBox_ui(self):
                return self.checkBox
            
            def get_value(self):
                return self.checkBox.value

            def set_command(self,command):
                raise NotImplementedError("这个方法必须被继承使用")

        class RadioUIBaseComponent: 
            def __init__(self, radio_desc, html_content, radio_options, configKey):
                self.configKey = configKey

                self.tip = widgets.HTML(
                    value = html_content,
                )
                
                self.radioButton = widgets.RadioButtons(
                        options = radio_options,
                        value = get_run_config_value(uiConfig,self.configKey),
                        style = {'description_width': 'initial'},
                        layout = Layout(width='auto', height='auto'),
                        description = radio_desc,
                        disabled = False
                    )
                
                self.uiBox = VBox([self.tip, self.radioButton])

            def set_to_config(self,config_name):
                set_run_config_value(uiConfig,self.configKey,self.radioButton.value,config_name)

            def updata_from_config(self,config_name):
                self.radioButton.value = get_run_config_value(uiConfig,self.configKey,config_name)

            def get_ui(self):
                return self.uiBox
            
            def get_radioButton_ui(self):
                return self.radioButton
            
            def get_value(self):
                return self.radioButton.value

            def set_command(self,command):
                raise NotImplementedError("这个方法必须被继承使用")

        class InputUIBaseComponent: 
            def __init__(self, input_desc, html_content, configKey):
                self.configKey = configKey

                self.input = widgets.Text(description=input_desc,value=get_run_config_value(uiConfig,self.configKey),style={'description_width': 'initial'},layout={'width': '550px'})
                self.html = widgets.HTML(value=html_content)
                
                self.uiBox = HBox([self.input, self.html])

            def set_to_config(self,config_name):
                set_run_config_value(uiConfig,self.configKey,self.input.value,config_name)

            def updata_from_config(self,config_name):
                value = get_run_config_value(uiConfig,self.configKey,config_name)
                self.input.value = value

            def get_ui(self):
                return self.uiBox
            
            def get_input_ui(self):
                return self.input
            
            def get_value(self):
                return self.input.value

            def set_command(self,command):
                raise NotImplementedError("这个方法必须被继承使用")


        #===========


        componentsControl = ComponentsControl() # UI配置链
        commandBuilder = CommandBuilder() # 命令配置链

        printQueueManager = PrintQueueManager() # 创建输出管理
        warnPrintQueue = PrintQueue() # 创建警告输出队列
        printQueueManager.add_queue(warnPrintQueue) # 输出管理添加警告输出队列



        #===========


        configSet_constructor = UIConstructor()
        configSet_out = configSet_constructor.get_output_component()

        # 获取配置集
        configSets = get_run_configs_formatted(uiConfig)
        configSets_dropdown = widgets.Dropdown(
            options=configSets,
            value=configSets[0][1],
            description='选择配置:',
            style={'description_width': 'initial'},
            disabled=False,
        )
        configSet_constructor.add_component(configSets_dropdown)

        # 第零行 UI 组件
        set_html_tip = widgets.HTML(value = html_blue_text("后面的任何设置如果没有保存,都会被视为临时的设置,只对启动命令生效(点击启动按钮不会自动载入或保存配置)"))
        configSet_constructor.add_component(set_html_tip)

        # 第一行 UI 组件
        set_default_button = XLButton(description="设置当前选择配置为默认配置", layout=Layout(width='250px', height='auto'), style={'button_color': '#90EE90'})
        default_html_tip = widgets.HTML(value = html_blue_text("提示: 启动器全局其他地方将会使用默认配置"))
        configSet_constructor.add_hbox_component([set_default_button,default_html_tip])

        # 第二行 UI 组件
        save_button = XLButton(description="保存到当前选择配置", style={'button_color': '#ADD8E6'})
        load_button = XLButton(description="载入当前选择配置", style={'button_color': '#FFDAB9'})
        delete_button = XLButton(description="删除当前选择配置", style={'button_color': '#FFC0CB'})
        configSet_constructor.add_hbox_component([save_button,load_button,delete_button])

        # 第三行 UI 组件
        new_config_name_input = widgets.Text(description="新配置名称:")
        save_new_config_button = XLButton(description="保存到新配置", style={'button_color': '#D8BFD8'})
        configSet_constructor.add_hbox_component([new_config_name_input,save_new_config_button])

        def updata_list(b,select_index=""):
            # 更新配置选择列表的逻辑
            configSets_dropdown.options = get_run_configs_formatted(uiConfig)
            if select_index != "":
                configSets_dropdown.value = select_index

        def set_default_config(b):
            configSet_constructor.clear_output()
            with configSet_out:
                # 设置默认配置的逻辑
                update_run_config_index(uiConfig,configSets_dropdown.value)
                uiConfig.save_config()
                select_index = configSets_dropdown.value
                print(green_text("已成功设置默认配置为:") + cyan_text(get_Dropdown_name_by_key(configSets_dropdown,configSets_dropdown.value)))
                updata_list(b,select_index)
                uiConfig.print_config()

        def save_config(b):
            configSet_constructor.clear_output()
            with configSet_out:
                # 保存配置的逻辑
                componentsControl.set_to_config(configSets_dropdown.value)
                uiConfig.save_config()
                select_index = configSets_dropdown.value
                print(green_text("已成功保存当前配置到:") + cyan_text(get_Dropdown_name_by_key(configSets_dropdown,configSets_dropdown.value)))
                updata_list(b,select_index)
                uiConfig.print_config()

        def load_config(b):
            configSet_constructor.clear_output()
            with configSet_out:
                uiConfig.print_config()
                # 载入配置的逻辑
                componentsControl.updata_from_config(configSets_dropdown.value)
                print(green_text("已成功加载配置:") + cyan_text(get_Dropdown_name_by_key(configSets_dropdown,configSets_dropdown.value)))

        def delete_config(b):
            configSet_constructor.clear_output()
            with configSet_out:
                # 删除配置的逻辑
                if configSets_dropdown.value == "xiaolxlDefault":
                    print(red_text("无法删除初始配置！"))
                else:
                    delName = get_Dropdown_name_by_key(configSets_dropdown,configSets_dropdown.value)
                    remove_run_config(uiConfig,configSets_dropdown.value)
                    uiConfig.save_config()
                    updata_list(b)
                    uiConfig.print_config()
                    print(green_text("已成功删除配置:") + cyan_text(delName))

        def save_new_config(b):
            configSet_constructor.clear_output()
            with configSet_out:
                # 保存新配置的逻辑
                newKey = generate_random_letters()
                componentsControl.set_to_config(newKey)
                uiConfig.save_config()
                updata_list(b,newKey)
                uiConfig.print_config()
                print(green_text("已成功保存新配置:") + cyan_text(nameInputUI.get_input_ui().value))

        # 绑定事件处理函数
        set_default_button.on_click(set_default_config)
        save_button.on_click(save_config)
        load_button.on_click(load_config)
        delete_button.on_click(delete_config)
        save_new_config_button.on_click(save_new_config)

        ui_constructor.add_accordion_component(configSet_constructor.get_ui(),'配置选择',isOpen=True)


        #===========


        configHighSet_constructor = UIConstructor()

        class NameInputUI(InputUIBaseComponent):
            def set_command(self, command):
                pass
        nameInputUI = NameInputUI("配置名字", html_blue_text("设置当前选择的配置名字"), "name")
        link((new_config_name_input, 'value'), (nameInputUI.get_input_ui(), 'value')) # 双向绑定名字值
        nameInputUI.get_input_ui().value = get_run_config_value(uiConfig,"name") # 临时设置一下不然是空
        configHighSet_constructor.add_component(nameInputUI.get_ui())
        componentsControl.add_component(nameInputUI)

        class CkptDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--ckpt-dir " + self.get_value())
        ckptDirInputUI = CkptDirInputUI("配置大模型目录", html_blue_text("设置大模型目录"), "ckpt_dir")
        configHighSet_constructor.add_component(ckptDirInputUI.get_ui())
        componentsControl.add_component(ckptDirInputUI)
        
        class EmbeddingsDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--embeddings-dir " + self.get_value())
        embeddingsDirInputUI = EmbeddingsDirInputUI("配置Embedding模型目录", html_blue_text("设置Embedding模型目录"), "embeddings_dir")
        configHighSet_constructor.add_component(embeddingsDirInputUI.get_ui())
        componentsControl.add_component(embeddingsDirInputUI)

        class HypernetworkDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--hypernetwork-dir " + self.get_value())
        hypernetworkDirInputUI = HypernetworkDirInputUI("配置超网络Hypernetwork目录", html_blue_text("设置超网络Hypernetwork目录"), "hypernetwork_dir")
        configHighSet_constructor.add_component(hypernetworkDirInputUI.get_ui())
        componentsControl.add_component(hypernetworkDirInputUI)

        class LoRaDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--lora-dir " + self.get_value())
        loraDirInputUI = LoRaDirInputUI("配置LoRA模型目录", html_blue_text("设置LoRA模型目录"), "lora_dir")
        configHighSet_constructor.add_component(loraDirInputUI.get_ui())
        componentsControl.add_component(loraDirInputUI)

        class VaeDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--vae-dir " + self.get_value())
        vaeDirInputUI = VaeDirInputUI("配置VAE模型目录", html_blue_text("设置VAE模型目录"), "vae_dir")
        configHighSet_constructor.add_component(vaeDirInputUI.get_ui())
        componentsControl.add_component(vaeDirInputUI)

        class ControlNetDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--controlnet-dir " + self.get_value())
        controlNetDirInputUI = ControlNetDirInputUI("配置ControlNet模型目录", html_blue_text("设置ControlNet模型目录"), "controlnet_dir")
        configHighSet_constructor.add_component(controlNetDirInputUI.get_ui())
        componentsControl.add_component(controlNetDirInputUI)

        class ControlNetAnnotatorModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--controlnet-annotator-models-path " + self.get_value())
        controlNetAnnotatorModelsPathInputUI = ControlNetAnnotatorModelsPathInputUI("配置ControlNet预处理模型路径", html_blue_text("设置ControlNet预处理模型路径"), "controlnet_annotator_models_path")
        configHighSet_constructor.add_component(controlNetAnnotatorModelsPathInputUI.get_ui())
        componentsControl.add_component(controlNetAnnotatorModelsPathInputUI)

        class TempDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                pass
        tempDirInputUI = TempDirInputUI("配置数据盘文件目录", html_blue_text("设置数据盘文件目录(不代表设置后它就变成数据盘, 这里只是一个目录定位)"), "temp_dir")
        configHighSet_constructor.add_component(tempDirInputUI.get_ui())
        componentsControl.add_component(tempDirInputUI)

        class SdWebUiDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.set_directory(self.get_value())
        sdWebUiDirInputUI = SdWebUiDirInputUI("配置SDWebUI主目录", html_blue_text("设置Stable Diffusion Web UI程序主目录(不代表设置后会自动移动, 这里只是一个目录定位)"), "sdWebUi_dir")
        configHighSet_constructor.add_component(sdWebUiDirInputUI.get_ui())
        componentsControl.add_component(sdWebUiDirInputUI)

        class SdWebUiExtensionsDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                pass
        sdWebUiExtensionsDirInputUI = SdWebUiExtensionsDirInputUI("配置SDWebUI扩展插件目录", html_blue_text("设置Stable Diffusion Web UI扩展插件目录(不代表设置后会自动移动, 这里只是一个目录定位)"), "sdWebUiExtensions_dir")
        configHighSet_constructor.add_component(sdWebUiExtensionsDirInputUI.get_ui())
        componentsControl.add_component(sdWebUiExtensionsDirInputUI)

        class AnimateDiffDirInputUI(InputUIBaseComponent):
            def set_command(self, command):
                pass
        animateDiffDirInputUI = AnimateDiffDirInputUI("配置AnimateDiff模型目录", html_blue_text("设置AnimateDiff模型目录(不代表设置后会自动移动, 这里只是一个目录定位)"), "animatediff_dir")
        configHighSet_constructor.add_component(animateDiffDirInputUI.get_ui())
        componentsControl.add_component(animateDiffDirInputUI)

        class DreamboothModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--dreambooth-models-path=" + self.get_value())
        dreamboothModelsPathInputUI = DreamboothModelsPathInputUI("配置dreambooth工作模型目录", html_blue_text("设置dreambooth工作模型目录"), "dreambooth_models_path")
        configHighSet_constructor.add_component(dreamboothModelsPathInputUI.get_ui())
        componentsControl.add_component(dreamboothModelsPathInputUI)

        class ModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                pass
        modelsPathInputUI = ModelsPathInputUI("配置models目录", html_blue_text("设置各种模型依赖的主要models位置(不代表设置后会自动移动, 这里只是一个目录定位)"), "models_dir")
        configHighSet_constructor.add_component(modelsPathInputUI.get_ui())
        componentsControl.add_component(modelsPathInputUI)

        class CodeformerModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--codeformer-models-path " + self.get_value())
        codeformerModelsPathInputUI = CodeformerModelsPathInputUI("配置Codeformer模型目录", html_blue_text("设置Codeformer模型目录"), "codeformer_models_path")
        configHighSet_constructor.add_component(codeformerModelsPathInputUI.get_ui())
        componentsControl.add_component(codeformerModelsPathInputUI)

        class GFPGANModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--gfpgan-models-path " + self.get_value())
        gfpganModelsPathInputUI = GFPGANModelsPathInputUI("配置GFPGAN模型目录", html_blue_text("设置GFPGAN模型目录"), "gfpgan_models_path")
        configHighSet_constructor.add_component(gfpganModelsPathInputUI.get_ui())
        componentsControl.add_component(gfpganModelsPathInputUI)

        class ESRGANModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--esrgan-models-path " + self.get_value())
        esrganModelsPathInputUI = ESRGANModelsPathInputUI("配置ESRGAN模型目录", html_blue_text("设置ESRGAN模型目录"), "esrgan_models_path")
        configHighSet_constructor.add_component(esrganModelsPathInputUI.get_ui())
        componentsControl.add_component(esrganModelsPathInputUI)

        class BSRGANModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--bsrgan-models-path " + self.get_value())
        bsrganModelsPathInputUI = BSRGANModelsPathInputUI("配置BSRGAN模型目录", html_blue_text("设置BSRGAN模型目录"), "bsrgan_models_path")
        configHighSet_constructor.add_component(bsrganModelsPathInputUI.get_ui())
        componentsControl.add_component(bsrganModelsPathInputUI)

        class RealESRGANModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--realesrgan-models-path " + self.get_value())
        realesrganModelsPathInputUI = RealESRGANModelsPathInputUI("配置RealESRGAN模型目录", html_blue_text("设置RealESRGAN模型目录"), "realesrgan_models_path")
        configHighSet_constructor.add_component(realesrganModelsPathInputUI.get_ui())
        componentsControl.add_component(realesrganModelsPathInputUI)

        class ScuNETModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--scunet-models-path " + self.get_value())
        scunetModelsPathInputUI = ScuNETModelsPathInputUI("配置ScuNET模型目录", html_blue_text("设置ScuNET模型目录"), "scunet_models_path")
        configHighSet_constructor.add_component(scunetModelsPathInputUI.get_ui())
        componentsControl.add_component(scunetModelsPathInputUI)

        class SwinIRModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--swinir-models-path " + self.get_value())
        swinirModelsPathInputUI = SwinIRModelsPathInputUI("配置SwinIR模型目录", html_blue_text("设置SwinIR模型目录"), "swinir_models_path")
        configHighSet_constructor.add_component(swinirModelsPathInputUI.get_ui())
        componentsControl.add_component(swinirModelsPathInputUI)

        class LDSRModelsPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--ldsr-models-path " + self.get_value())
        ldsrModelsPathInputUI = LDSRModelsPathInputUI("配置LDSR模型目录", html_blue_text("设置LDSR模型目录"), "ldsr_models_path")
        configHighSet_constructor.add_component(ldsrModelsPathInputUI.get_ui())
        componentsControl.add_component(ldsrModelsPathInputUI)

        class SDWebUICacheFileInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_environment_variable("SD_WEBUI_CACHE_FILE", self.get_value())
        sdWebUICacheFileInputUI = SDWebUICacheFileInputUI("配置SD WebUI缓存文件", html_blue_text("设置SD WebUI缓存文件路径"), "sd_webui_cache_file")
        configHighSet_constructor.add_component(sdWebUICacheFileInputUI.get_ui())
        componentsControl.add_component(sdWebUICacheFileInputUI)

        class SdWebUiPortInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--port=" + self.get_value())
        sdWebUiPortInputUI = SdWebUiPortInputUI("配置SDWebUI开启的监听端口", html_blue_text("设置Stable Diffusion Web UI端口(默认6006)"), "SdWebUi_port")
        configHighSet_constructor.add_component(sdWebUiPortInputUI.get_ui())
        componentsControl.add_component(sdWebUiPortInputUI)

        ui_constructor.add_accordion_component(configHighSet_constructor.get_ui_no_out(),'配置高级设置(一般不改)',isOpen=False)


        #===========


        directoryLinkSet_constructor = UIConstructor()
        directoryLinkSet_out = directoryLinkSet_constructor.get_output_component()

        directory_mapper_ui = DirectoryMapperUI(uiConfig.get_directory_mapper_items(), uiConfig, directoryLinkSet_out)
        directoryLinkSet_constructor.add_component(directory_mapper_ui.get_ui())

        ui_constructor.add_accordion_component(directoryLinkSet_constructor.get_ui(),'目录映射设置(一般不改)',isOpen=False)


        #===========


        class LoginUIComponent: 
            def __init__(self):
                self.nameInputConfigKey = "login_name"
                self.passInputConfigKey = "login_pass"
                self.isOpenConfigKey = "open_login"

                self.tip = widgets.HTML(
                    value="<font size='2' color='red'>设置webui是否需要登录,密码和用户名请勿出现特殊符合和空格!建议英文字母+数字</font>",
                )
                
                self.name_input = widgets.Text(
                    value=get_run_config_value(uiConfig,self.nameInputConfigKey),
                    placeholder='留空则随机',
                    description='用户名:',
                    disabled=False
                )
                self.pass_input = widgets.Text(
                    value=get_run_config_value(uiConfig,self.passInputConfigKey),
                    placeholder='留空则随机',
                    description='密码:',
                    disabled=False
                )

                self.is_open = widgets.RadioButtons(
                    options = [('开启','open'), ('关闭','close'), ('自动(开启学术加速的时候自动打开)','auto')],
                    value = get_run_config_value(uiConfig,self.isOpenConfigKey), # Defaults to 'pineapple'
                    style = {'description_width': 'initial'},
                    layout = Layout(width='400px', height='auto'),
                    description = '请选择是否开启登录：',
                    disabled = False
                )

                self.uiBox = VBox([self.tip, self.name_input, self.pass_input, self.is_open])

            def set_to_config(self,config_name):
                set_run_config_value(uiConfig,self.nameInputConfigKey,self.name_input.value,config_name)
                set_run_config_value(uiConfig,self.passInputConfigKey,self.pass_input.value,config_name)
                set_run_config_value(uiConfig,self.isOpenConfigKey,self.is_open.value,config_name)

            def updata_from_config(self,config_name):
                self.name_input.value = get_run_config_value(uiConfig,self.nameInputConfigKey,config_name)
                self.pass_input.value = get_run_config_value(uiConfig,self.passInputConfigKey,config_name)
                self.is_open.value = get_run_config_value(uiConfig,self.isOpenConfigKey,config_name)

            def get_ui(self):
                return self.uiBox
            
            def get_name_input_value(self):
                return self.name_input.value
            
            def get_pass_input_value(self):
                return self.pass_input.value
            
            def get_is_open_value(self):
                return self.is_open.value

            def set_command(self,command):
                _name = self.get_name_input_value()
                _pass = self.get_pass_input_value()

                if _name == "":
                    _name = generate_random_letters(length=8)
                    self.name_input.value = _name

                if _pass == "":
                    _pass = generate_random_letters(length=8)
                    self.pass_input.value = _pass

                _is_open = self.get_is_open_value()
                if _is_open == "open":
                    command.add_argument("--gradio-auth " + f"{_name}:{_pass}")
                    with rootOut:
                        print(yellow_text("你已开启登录功能，请在启动设置-登录隐私处查看密码和用户名"))

                if _is_open == "auto":
                    if get_is_speed():
                        command.add_argument("--gradio-auth " + f"{_name}:{_pass}")
                        with rootOut:
                            print(yellow_text("你已开启登录功能，请在启动设置-登录隐私处查看密码和用户名"))

        loginSet_constructor = UIConstructor()

        loginUIComponent = LoginUIComponent()
        componentsControl.add_component(loginUIComponent)
        loginSet_constructor.add_component(loginUIComponent.get_ui())

        ui_constructor.add_accordion_component(loginSet_constructor.get_ui_no_out(),'登录隐私设置',isOpen=False)


        #===========


        customSet_constructor = UIConstructor()

        class CustomLaunchArgumentsInputUI(InputUIBaseComponent):
            def set_command(self, command):
                if self.get_value() != "":
                    command.add_custom_launch_arguments(self.get_value())
        customLaunchArgumentsInputUI = CustomLaunchArgumentsInputUI(
            "自定义WebUi启动参数",
            html_blue_text("自定义WebUi启动参数(空格分隔)[例子:--xxx-xx --xxxx=xxxx]"),
            "custom_launch_arguments")
        componentsControl.add_component(customLaunchArgumentsInputUI)
        customSet_constructor.add_component(customLaunchArgumentsInputUI.get_ui())

        class CustomEnvironmentVariablesInputUI(InputUIBaseComponent):
            def set_command(self, command):
                if self.get_value() != "":
                    command.add_custom_environment_variables(self.get_value())
        customEnvironmentVariablesInputUI = CustomEnvironmentVariablesInputUI(
            "自定义WebUi启动环境变量",
            html_blue_text("自定义WebUi启动环境变量(空格分隔)[例子:XXXXX=xxxx XXXXXX=xxx] ",single_line=False) + html_red_text("【此设置只会在自定义启动方式中生效！】",single_line=False),
            "custom_environment_variables")
        componentsControl.add_component(customEnvironmentVariablesInputUI)
        customSet_constructor.add_component(customEnvironmentVariablesInputUI.get_ui())

        ui_constructor.add_accordion_component(customSet_constructor.get_ui_no_out(),'自定义启动参数',isOpen=False)


        #===========


        startSet_constructor = UIConstructor()

        class SdWebUiStartMethodRadioUI(RadioUIBaseComponent):
            def set_command(self, command):
                if self.get_value() == 'background':
                    command.set_unbuffered(True)
        sdWebUiStartMethodRadioUI = SdWebUiStartMethodRadioUI(
            '请选择stable-diffusion-webui的运行方式:',
            "<font size='2' color='red'><p>TIP: </p><p>后台版(多线程)：无法查看各类进度输出,导致你会怀疑程序卡住,同时运行时间长后会导致卡顿</p><p>正常版(单线程)：运行后无法执行下载模型等操作(点击后不会有反应),需要取消运行后才能进行操作</p><p>自定义版(最佳)：运需要手动在控制台运行(包括学术加速)，但可以同时操作启动器的功能且关闭网页后再打开也能在控制台看到输出</p></font>",
            [('后台版','background'), ('正常版','normal'), ('自定义版','custom')],
            "sd_webui_start_method")
        componentsControl.add_component(sdWebUiStartMethodRadioUI)
        startSet_constructor.add_component(sdWebUiStartMethodRadioUI.get_ui())

        class SdWebUiThemeRadioUI(RadioUIBaseComponent):
            def set_command(self, command):
                if self.get_value() == 'dark':
                    command.add_argument("--theme dark")
                if self.get_value() == 'light':
                    command.add_argument("--theme light")
                pass
        sdWebUiThemeRadioUI = SdWebUiThemeRadioUI(
            '请选择stable-diffusion-webui的样式:',
            "<font size='2' color='red'><p>TIP: </p><p>夜间模式(暗黑色): 一般夜晚使用</p><p>白天默认(亮白色): 一般白天使用</p><p>使用默认浏览器主题：根据浏览器主题自动设置</p></font>",
            [('夜间模式(暗黑色)','dark'), ('白天默认(亮白色)','light'), ('使用默认浏览器主题','auto')],
            "sd_webui_theme")
        componentsControl.add_component(sdWebUiThemeRadioUI)
        startSet_constructor.add_component(sdWebUiThemeRadioUI.get_ui())

        startSet_constructor.add_component(widgets.HTML(value="<h4>重要参数<h4/><hr>",)) # =====================

        class CheckAndDownloadTheCoreSelectUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    modList, _ = controllers['jsonFetcher'].fetch_json(data['branch'],"ui_scripts/data/autodl_webui/automodList.json")
                    def download_files(modList, uiConfig, specified_type):
                        # 获取指定类型的文件信息列表
                        mod_children = modList.get(specified_type, {}).get("modChildren", [])
                        total_files = len(mod_children)  # 总文件数
                        downloaded_files = 0  # 已下载文件数
                        for mod_child in mod_children:
                            downloaded_files += 1  # 更新下载文件计数
                            # 获取下载路径
                            download_path = get_config_path(uiConfig, mod_child['parentPath']) + mod_child['sonPath']
                            # 检查文件是否已下载
                            if not check_downloaded(mod_child['downloadType'], mod_child['fileName'], download_path, mod_child):
                                # 打印当前下载进度
                                with rootOut:
                                    print(f"正在下载第{downloaded_files}个文件, 总共有{total_files}个文件")
                                # 获取下载命令
                                download_command = get_download_command(
                                    mod_child['url'], 
                                    download_path, 
                                    mod_child['fileName'], 
                                    "more", 
                                    mod_child['downloadType']
                                )
                                # 执行下载命令
                                with rootOut:
                                    cmd_run(download_command)
                    with rootOut:
                        haveckpt = has_mods_files(get_config_path(uiConfig,"ckpt_dir"))
                        if not haveckpt:
                            print("正在自动下载模型:")
                            download_files(modList, uiConfig, "mod")
                            print("模型下载完成")
                        havevae = has_vae_files(get_config_path(uiConfig,"vae_dir"))
                        if not havevae:
                            print("正在自动下载vae:")
                            download_files(modList, uiConfig, "vae")
                            print("vae下载完成")
                        print("正在自动下载核心依赖:")
                        download_files(modList, uiConfig, "core")
                        print("核心依赖下载完成")
                else:
                    with rootOut:
                        haveckpt = has_files(get_config_path(uiConfig,"ckpt_dir"))
                        havevae = has_files(get_config_path(uiConfig,"vae_dir"))
                        if not haveckpt or not havevae:
                            command.add_argument("--no-download-sd-model")  # 取消模型自动下载
                            print(red_text("警告! 大模型目录没有模型或VAE目录没有VAE, 请在下载器里下载, 或使用自己的文件, 如果没有特殊需求你的本次启动将会报错!"))
        checkAndDownloadTheCoreSelectUI = CheckAndDownloadTheCoreSelectUI("检查并下载核心文件", 
            html_blue_text("包含[超分模型,脸部修复模型,常用VAE,常用大模型(一个)] | 如果你有特殊需求不想这样可以关闭"),
            "check_and_download_the_core")
        componentsControl.add_component(checkAndDownloadTheCoreSelectUI)
        startSet_constructor.add_component(checkAndDownloadTheCoreSelectUI.get_ui())

        class CheckGPUSelectUI(SelectUIBaseComponent):
            def set_command(self, command):
                pass
        checkGPUSelectUI = CheckGPUSelectUI("强制检查GPU",
            html_blue_text("防止在无卡模式运行 | 如果你有特殊需求想在CPU上运行可以关闭(注意关闭不等于可以在CPU上运行,你需要自己进行参数设置) | 如果你确认不会失误那么关闭可以略微提高运行速度"),
            "check_GPU")
        componentsControl.add_component(checkGPUSelectUI)
        startSet_constructor.add_component(checkGPUSelectUI.get_ui())

        class IgnoreCmdArgsErrorsSelectUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_environment_variable("IGNORE_CMD_ARGS_ERRORS", "true")
        ignoreCmdArgsErrorsSelectUI = IgnoreCmdArgsErrorsSelectUI("忽略命令行参数错误",
            html_blue_text("如果启用，系统将忽略无效或错误的命令行参数 | 这可能有助于避免某些启动错误，但可能会隐藏配置问题"),
            "ignore_cmd_args_errors")
        componentsControl.add_component(ignoreCmdArgsErrorsSelectUI)
        startSet_constructor.add_component(ignoreCmdArgsErrorsSelectUI.get_ui())

        class SkipInstallSelectUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--skip-install")
        skipInstallSelectUI = SkipInstallSelectUI("开启急速启动", html_blue_text("跳过插件依赖的安装和网络更新步骤，加速过程 [--skip-install]") + html_red_text("(注意！)如果你有更新/安装过插件/WebUi请勿开启! | 开启后会出现很多报错,理论上忽略即可"), "skip_install")
        componentsControl.add_component(skipInstallSelectUI)
        startSet_constructor.add_component(skipInstallSelectUI.get_ui())


        class EnvPathInputUI(InputUIBaseComponent):
            def set_command(self, command):
                if self.get_value() != "":
                    command.add_environment_variable("PATH", get_run_config_value(uiConfig,"env_path") + "$PATH")
        envPathInputUI = EnvPathInputUI("虚拟环境路径",
            html_blue_text("一般不改 | 特殊需求可以自行修改,设置为空则为默认,设置后需要保存并重启内核和启动器"),
            "env_path")
        componentsControl.add_component(envPathInputUI)
        startSet_constructor.add_component(envPathInputUI.get_ui())

        startSet_constructor.add_component(widgets.HTML(value="<h4>常用参数<h4/><hr>",)) # =====================

        class TcmallocSelectUI(SelectUIBaseComponent):
            def check_package_installed(self, package_name):
                status = os.system(f"dpkg -l {package_name} > /dev/null 2>&1")
                return status == 0
    
            def set_command(self, command):
                if self.get_value():
                    if self.check_package_installed("libgoogle-perftools-dev"):
                        os.environ['LD_PRELOAD']="libtcmalloc.so.4"
                        command.add_environment_variable("LD_PRELOAD", "libtcmalloc.so.4")
                    else:
                        with rootOut:
                            print("正在安装tcmalloc, 请稍等...")
                        cmd_run("apt-get update && apt-get install -y libgoogle-perftools-dev")
                        cmd_run("apt-get install -y libgoogle-perftools-dev")
                        if self.check_package_installed("libgoogle-perftools-dev"):
                            os.environ['LD_PRELOAD']="libtcmalloc.so.4"
                            command.add_environment_variable("LD_PRELOAD", "libtcmalloc.so.4")
                            with rootOut:
                                print("安装tcmalloc完成")
                        else:
                            with rootOut:
                                print("安装tcmalloc失败,请询问作者")
                else:
                    os.environ.pop('LD_PRELOAD', None)
        tcmallocSelectUI = TcmallocSelectUI("使用 tcmalloc 进行内存管理", html_blue_text("可略微提升速度并大大降低 CPU 内存泄漏(第一次开启会自动进行安装)"), "use_tcmalloc")
        componentsControl.add_component(tcmallocSelectUI)
        startSet_constructor.add_component(tcmallocSelectUI.get_ui())

        class GradioShareSelectUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--share")
        gradioShareSelectUI = GradioShareSelectUI("开启gradio分享链接", html_blue_text("您将获得xxx.app.gradio链接,如果未开启登录任何人都可以访问这个链接 [--share]"), "gradio_share")
        componentsControl.add_component(gradioShareSelectUI)
        startSet_constructor.add_component(gradioShareSelectUI.get_ui())

        class XformersSelectUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--xformers")
        xformersSelectUI = XformersSelectUI("启用xformers", html_blue_text("xformers极大改善内存消耗和速度 [--xformers]"), "xformers")
        componentsControl.add_component(xformersSelectUI)
        startSet_constructor.add_component(xformersSelectUI.get_ui())

        class DisableSafeUnpickleUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--disable-safe-unpickle")
        disableSafeUnpickleUI = DisableSafeUnpickleUI("不启动安全检查", html_blue_text("勾选后可以解决某些模型加载时报错 [--disable-safe-unpickle]"), "disable_safe_unpickle")
        componentsControl.add_component(disableSafeUnpickleUI)
        startSet_constructor.add_component(disableSafeUnpickleUI.get_ui())

        class EnableInsecureExtensionAccessUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--enable-insecure-extension-access")
        enableInsecureExtensionAccessUI = EnableInsecureExtensionAccessUI("允许WebUi内置的扩展安装", html_blue_text("允许使用WebUi内置的扩展安装功能 [--enable-insecure-extension-access]"), "enable_insecure_extension_access")
        componentsControl.add_component(enableInsecureExtensionAccessUI)
        startSet_constructor.add_component(enableInsecureExtensionAccessUI.get_ui())

        class DisableGradioQueueUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--no-gradio-queue")
        disableGradioQueueUI = DisableGradioQueueUI(
            "关闭gradio队列(解决新版webui网络问题)",
            html_blue_text("如果开启了学术加速后使用有红色的网络报错弹框请开启这个 [--no-gradio-queue]"),
            "disable_gradio_queue"
        )
        componentsControl.add_component(disableGradioQueueUI)
        startSet_constructor.add_component(disableGradioQueueUI.get_ui())

        class DisableHalfVaeUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--no-half-vae")
        disableHalfVaeUI = DisableHalfVaeUI(
            "不启用半精VAE",
            html_blue_text("勾选后解决生成图片时,可能的VAE精度不足所导致的报错 [--no-half-vae]"),
            "disable_half_vae"
        )
        componentsControl.add_component(disableHalfVaeUI)
        startSet_constructor.add_component(disableHalfVaeUI.get_ui())

        class DisableNaNCheckUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--disable-nan-check")
        disableNaNCheckUI = DisableNaNCheckUI(
            "忽略NaNs检查",
            html_blue_text("勾选后解决生成图片时,出现NaNs导致的报错(错误图片以黑图出现而不会直接中断) [--disable-nan-check]"),
            "disable_nan_check"
        )
        componentsControl.add_component(disableNaNCheckUI)
        startSet_constructor.add_component(disableNaNCheckUI.get_ui())

        class StartUIWithoutLoadingModelsUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--ui-debug-mode")
        startUIWithoutLoadingModelsUI = StartUIWithoutLoadingModelsUI(
            "启动UI但不加载模型",
            html_blue_text("不加载模型以快速启动UI [--ui-debug-mode]"),
            "start_ui_without_loading_models"
        )
        componentsControl.add_component(startUIWithoutLoadingModelsUI)
        startSet_constructor.add_component(startUIWithoutLoadingModelsUI.get_ui())

        class MaxBatchCountInputUI(InputUIBaseComponent):
            def set_command(self, command):
                command.add_argument("--max-batch-count=" + self.get_value())
        maxBatchCountInputUI = MaxBatchCountInputUI(
            "最大批次数量",
            html_blue_text("UI的最大批计数值(默认16) [--max-batch-count]"),
            "max_batch_count")
        componentsControl.add_component(maxBatchCountInputUI)
        startSet_constructor.add_component(maxBatchCountInputUI.get_ui())


        startSet_constructor.add_component(widgets.HTML(value="<h4>检查与警告<h4/><hr>",)) # =====================


        class SkipVersionCheckUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--skip-version-check")
        skipVersionCheckUI = SkipVersionCheckUI(
            "不检查torch，xformer版本",
            html_blue_text("不要检查torch和xformer的版本 [--skip-version-check]"),
            "skip_version_check"
        )
        componentsControl.add_component(skipVersionCheckUI)
        startSet_constructor.add_component(skipVersionCheckUI.get_ui())

        class SkipPythonVersionCheckUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--skip-python-version-check")
        skipPythonVersionCheckUI = SkipPythonVersionCheckUI(
            "不检查Python版本",
            html_blue_text("不要检查Python的版本 [--skip-python-version-check]"),
            "skip_python_version_check"
        )
        componentsControl.add_component(skipPythonVersionCheckUI)
        startSet_constructor.add_component(skipPythonVersionCheckUI.get_ui())

        class CloseTensorflowWarnUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
                    command.add_environment_variable("TF_CPP_MIN_LOG_LEVEL", "2")
                else:
                    os.environ['TF_CPP_MIN_LOG_LEVEL']='0'
                    command.add_environment_variable("TF_CPP_MIN_LOG_LEVEL", "0")
        closeTensorflowWarnUI = CloseTensorflowWarnUI(
            "关闭tensorflow警告",
            html_blue_text("勾选后不会在启动出现tensorflow警告信息"),
            "close_tensorflow_warn"
        )
        componentsControl.add_component(closeTensorflowWarnUI)
        startSet_constructor.add_component(closeTensorflowWarnUI.get_ui())


        startSet_constructor.add_component(widgets.HTML(value="<h4>API相关参数<h4/><hr>",)) # =====================


        class EnableWebUIApiUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--api")
        enableWebUIApiUI = EnableWebUIApiUI(
            "开启Web UI的API功能",
            html_blue_text("开启Web UI的API功能 [--api]"),
            "enable_web_ui_api"
        )
        componentsControl.add_component(enableWebUIApiUI)
        startSet_constructor.add_component(enableWebUIApiUI.get_ui())

        class EnableApiLogUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--api-log")
        enableApiLogUI = EnableApiLogUI(
            "启用API所有日志记录",
            html_blue_text("启用所有API请求的日志记录 [--api-log]"),
            "enable_api_log"
        )
        componentsControl.add_component(enableApiLogUI)
        startSet_constructor.add_component(enableApiLogUI.get_ui())

        class OnlyStartApiUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    command.add_argument("--nowebui")
        onlyStartApiUI = OnlyStartApiUI(
            "只启动API, 不启动UI",
            html_blue_text("只启动API, 不启动UI [--nowebui]"),
            "only_start_api"
        )
        componentsControl.add_component(onlyStartApiUI)
        startSet_constructor.add_component(onlyStartApiUI.get_ui())

        class CorsAllowOriginsInputUI(InputUIBaseComponent):
            def set_command(self, command):
                if self.get_value() != "":
                    command.add_argument("--cors-allow-origins=" + self.get_value())
        corsAllowOriginsInputUI = CorsAllowOriginsInputUI(
            "允许的CORS来源(跨源访问)",
            html_blue_text("允许的CORS来源以逗号分隔列表的形式(无空格)[例子:https://www.painthua.com,https://www.baidu.com]"),
            "cors_allow_origins")
        componentsControl.add_component(corsAllowOriginsInputUI)
        startSet_constructor.add_component(corsAllowOriginsInputUI.get_ui())


        startSet_constructor.add_component(widgets.HTML(value="<h4>网络相关<h4/><hr>",)) # =====================


        class EnableHuggingFaceMirrorUI(SelectUIBaseComponent):
            def set_command(self, command):
                if self.get_value():
                    os.environ['HF_ENDPOINT']="https://hf-mirror.com"
                    command.add_environment_variable("HF_ENDPOINT", "https://hf-mirror.com")
                else:
                    os.environ.pop('HF_ENDPOINT', None)
        enableHuggingFaceMirrorUI = EnableHuggingFaceMirrorUI(
            "开启抱脸镜像",
            html_blue_text("开启抱脸huggingface镜像,可以解决大部分国内访问huggingface的网络问题"),
            "enable_hf_network"
        )
        componentsControl.add_component(enableHuggingFaceMirrorUI)
        startSet_constructor.add_component(enableHuggingFaceMirrorUI.get_ui())


        ui_constructor.add_accordion_component(startSet_constructor.get_ui_no_out(),'启动设置',isOpen=False)


        #===========

        start_tip = widgets.HTML(
            value="<p>启动完毕后通过自定义服务打开网站</p><p><font color='#0fa3ff'><a href='https://www.autodl.com/console/instance/list' target='_blank'>点击此处打开服务器列表</a><font/></p><p></p>",
        )
        ui_constructor.add_component(start_tip)

        file = open(get_xiaolxl_jupyter_controller_path() + "/xiaolxl_jupyter_controller/ui_scripts/img/自定义服务.png", "rb")
        image = file.read()
        start_tip_img = widgets.Image(
            value=image,
            format='png'
        )
        ui_constructor.add_component(start_tip_img)

        sd_start_button = XLButton(description="SD, 启动！", button_style='info', layout=Layout(width='150px', height='auto'))
        def sd_start_fun(self):
            ui_constructor.clear_output()
            commandBuilder.clear()

            if checkGPUSelectUI.get_value():
                import torch
                if not torch.cuda.is_available():
                    with rootOut:
                        print("没有GPU,已终止运行")
                    return

            with rootOut:
                def is_xl_env():
                    # 获取当前 Python 解释器的路径
                    executable_path_result = subprocess.run(["python", "-c", "import sys; print(sys.executable)"], capture_output=True, text=True)
                    executable_path = executable_path_result.stdout.strip()
                    # 检查路径中是否包含 'xl_env'
                    return 'xl_env' in executable_path
                if not is_xl_env():
                    print(yellow_text("警告! 你选择的运行环境不是xl_env, 如果没有特殊需求你的本次启动将会报错!"))

                havetemp = has_files("/root/temp")
                if havetemp:
                    print("发现你是第一次运行, 正在初始化镜像依赖")
                    cmd_run("mkdir /root/.cache")
                    cmd_run("mv -b -f /root/temp/* /root/.cache/")
                    cmd_run("echo '移动完成'")

                commandBuilder.set_python_path("python") # 新版启动器环境已用环境变量切换，无需手动指定
                componentsControl.set_command(commandBuilder)
                finallyCommand = commandBuilder.build()

                _sdWebUiStartMethod = sdWebUiStartMethodRadioUI.get_value()
                if _sdWebUiStartMethod == 'background':
                    thread_out.run_thread_out(finallyCommand,rootOut)
                if _sdWebUiStartMethod == 'normal':
                    cmd_run(finallyCommand)
                if _sdWebUiStartMethod == 'custom':
                    print("请复制下方命令到控制台中手动运行")
                    print("")
                    print(finallyCommand)
                    print("")

                    if get_is_speed():
                        print("如果需要学术加速, 请打开右侧网址, 找到对应加速命令提前运行即可: https://www.autodl.com/docs/network_turbo/")
                    else:
                        print("如果之前开启过学术加速需要解除, 请打开右侧网址, 找到对应接触命令提前运行即可: https://www.autodl.com/docs/network_turbo/")
        sd_start_button.on_click_with_style(sd_start_fun,"正在运行...")
        ui_constructor.add_component(sd_start_button)

        # CommandBuilder使用示例
        # builder = CommandBuilder()
        # builder.set_directory("/root/stable-diffusion-webui")
        # builder.add_environment_variable("TF_CPP_MIN_LOG_LEVEL", "2")
        # builder.set_python_path("/root/miniconda3/envs/xl_env/bin/python")
        # builder.set_unbuffered(False)  # 启用无缓冲输出
        # builder.add_argument("--disable-safe-unpickle")
        # builder.add_argument("--port=6006")
        # builder.add_argument("--xformers")
        # builder.add_argument("--no-half-vae")
        # builder.add_argument("--disable-nan-check")
        # command = builder.build()
        # print(command)

    return ui_constructor.get_ui()