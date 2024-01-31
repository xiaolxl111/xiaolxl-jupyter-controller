import ipywidgets as widgets
import json

from ...tools.ui_tool import * 
from ...tools.config_tool import * 

def getUi(data,cmd_run,controllers):
    def is_version_smaller(version1, version2):
        # 将版本号分割成数字列表
        nums1 = [int(part) for part in version1.split('.')]
        nums2 = [int(part) for part in version2.split('.')]

        # 比较对应的数字
        for n1, n2 in zip(nums1, nums2):
            if n1 < n2:
                return True
            elif n1 > n2:
                return False

        # 如果一个版本号比另一个短，并且到目前为止所有数字都相等，那么更短的版本号更小
        return len(nums1) < len(nums2)
    def read_project_config():
        try:
            with open("../ServerConfig.json", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None
        except Exception as e:
            return None

    project_config = read_project_config()
    network_project_config_json, is_from_network = controllers['jsonFetcher'].fetch_json("https://jihulab.com/xiaolxl_pub/xiaolxl-jupyter-controller/-/raw/main/xiaolxl_jupyter_controller/ui_scripts/localtools/serverconfigs/autodl_webui/ServerConfig.json", "../localtools/serverconfigs/autodl_webui/ServerConfig.json")

    if project_config:
        is_version_lower = is_version_smaller(project_config["project_version"], network_project_config_json["project_version"])
        # 创建包含本地和网络更新信息的HTML内容
        html_content = f"""
        <style>
            .update-block, .hot-update-block {{
                background-color: #fff;
                margin-bottom: 20px;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                max-height: 300px;
                overflow-y: auto;
            }}
            .update-header {{
                font-size: 20px;
                margin-bottom: 10px;
                color: #444;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
            }}
            .version-info {{
                background-color: #e7e7e7;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }}
            .current-version {{
                background-color: #add8e6;  /* 浅蓝色背景 */
            }}
            .version-info h3 {{
                margin-top: 0;
            }}
            .update-content {{
                margin-left: 20px;
            }}
        </style>
        <div class="container">
            <div class="update-block">
                <div class="update-header">当前版本：{project_config["project_version"]}{' (有新版本，请更新)' if is_version_lower else ''}</div>
                <div>更新日期：{project_config["project_update_time"]}</div>
            </div>

            <div class="update-block">
                <div class="update-header">更新信息树</div>
                <!-- 动态生成更新信息 -->
                {"".join([f'''
                <div class="version-info{' current-version' if info['version'] == project_config["project_version"] else ''}">
                    <h3>版本 {info["version"]} - 更新时间：{info["update_time"]}</h3>
                    <div class="update-content">
                        {"<p>" + "</p><p>".join(info["update_infor"]) + "</p>"}
                    </div>
                </div>
                ''' for info in project_config["project_update_infor"]])}
            </div>
        </div>
        """
    else:
        # 创建仅包含网络更新信息树的HTML内容
        html_content = f"""
        <div class="update-block">
            <div class="update-block">
                <div class="update-header">此镜像版本暂不支持显示本地镜像版本,请更新镜像后查看</div>
            </div>
            <div class="update-header">更新信息树</div>
            <!-- 动态生成更新信息树 -->
            {"".join([f'''
            <div class="version-info">
                <h3>版本 {info["version"]} - 更新时间：{info["update_time"]}</h3>
                <div class="update-content">
                    {"<p>" + "</p><p>".join(info["update_infor"]) + "</p>"}
                </div>
            </div>
            ''' for info in network_project_config_json["project_update_infor"]])}
        </div>
        """
    ui_constructor = UIConstructor()
    ui_constructor.add_component(
        widgets.HTML(value=html_content,)
    )
    
    return ui_constructor.get_ui_no_out()