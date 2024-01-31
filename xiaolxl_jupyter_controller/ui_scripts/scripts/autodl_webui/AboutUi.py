import ipywidgets as widgets

from ...tools.ui_tool import * 
from ...tools.config_tool import * 

def getUi(data,cmd_run,controllers):
    versionController = controllers['versionController']

    ui_constructor = UIConstructor()

    versionConfig = versionController.get_data()
    network_version_json, is_from_network = controllers['jsonFetcher'].fetch_json("https://jihulab.com/xiaolxl_pub/xiaolxl-jupyter-controller/-/raw/main/xiaolxl_jupyter_controller/ui_scripts/data/xiaolxl_jupyter_controller_version.json", "../data/xiaolxl_jupyter_controller_version.json")
    network_version = versionController.get_version_from_json(network_version_json)
    is_version_lower = versionController.is_version_lower(network_version)
    # 创建HTML内容
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
            <div class="update-header">启动器当前版本：{versionController.get_version()}{' (启动器有新版本，请更新)' if is_version_lower else ''}</div>
            <div>更新日期：{versionController.get_update_time()}</div>
        </div>

        <div class="update-block">
            <div class="update-header">启动器更新信息</div>
            <!-- 动态生成更新信息 -->
            {"".join([f'''
            <div class="version-info{' current-version' if info['version'] == versionController.get_version() else ''}">
                <h3>版本 {info["version"]} - 更新时间：{info["update_time"]}</h3>
                <div class="update-content">
                    {"<p>" + "</p><p>".join(f"{i + 1}. {line}" for i, line in enumerate(info["update_infor"])) + "</p>"}
                </div>
            </div>
            ''' for info in versionConfig["update_info"]])}
        </div>

        <div class="hot-update-block">
            <div class="update-header">启动器热更新信息(远程列表更新)</div>
            <!-- 动态生成热更新信息 -->
            {"".join([f'''
            <div class="version-info">
                <h3>更新时间：{info["update_time"]}</h3>
                <div class="update-content">
                    {"<p>" + "</p><p>".join(f"{i + 1}. {line}" for i, line in enumerate(info["update_infor"])) + "</p>"}
                </div>
            </div>
            ''' for info in versionConfig["hot_update_info"]])}
        </div>
    </div>
    """
    ui_constructor.add_component(
        widgets.HTML(value=html_content,)
    )
    
    ui_constructor.add_component(
        widgets.HTML(value="<hr>",)
    )
    
    ui_constructor.add_component(
        widgets.HTML(value="<h3>启动器作者: 小李xiaolxl</h3><h3><font color='#0fa3ff'><a target='_blank' href='https://space.bilibili.com/34590220/'>访问作者B站空间</a></font></h3><h3><font color='#0fa3ff'><a target='_blank' href='https://pd.qq.com/s/274pgt03r'>加入AIGC世界QQ频道</a></font></h3>",)
    )

    ui_constructor.add_component(
        widgets.HTML(value="AIGC交流QQ群: 741821455")
    )

    file = open(get_xiaolxl_jupyter_controller_path() + "/xiaolxl_jupyter_controller/ui_scripts/img/qq.jpg", "rb")
    image = file.read()
    qq_img = widgets.Image(
        value=image,
        format='jpg',
        width="25%",
        height="auto"
    )
    ui_constructor.add_component(qq_img)

    ui_constructor.add_component(
        widgets.HTML(value="<hr>",)
    )

    ui_constructor.add_component(
        widgets.HTML(value="整合版1.0镜像介绍页：<font color='#0fa3ff'><a target='_blank' href='https://www.codewithgpu.com/i/AUTOMATIC1111/stable-diffusion-webui/NovelAI-Consolidation-Package'>点我访问</a></font>",)
    )
    
    ui_constructor.add_component(
        widgets.HTML(value="整合版2.0镜像介绍页：<font color='#0fa3ff'><a target='_blank' href='https://www.codewithgpu.com/i/AUTOMATIC1111/stable-diffusion-webui/NovelAI-Consolidation-Package-2'>点我访问</a></font>",)
    )
    
    ui_constructor.add_component(
        widgets.HTML(value="整合版3.0镜像介绍页：<font color='#0fa3ff'><a target='_blank' href='https://www.codewithgpu.com/i/AUTOMATIC1111/stable-diffusion-webui/NovelAI-Consolidation-Package-3.1'>点我访问</a></font>",)
    )

    ui_constructor.add_component(
        widgets.HTML(value="【推荐】整合版4.0镜像(3.1-V15)介绍视频：<font color='#0fa3ff'><a target='_blank' href='https://www.bilibili.com/video/BV115411z7wb/'>点我观看</a></font>",)
    )

    ui_constructor.add_component(
        widgets.HTML(value="<hr>",)
    )
    
    ui_constructor.add_component(
        widgets.HTML(value="启动器开源地址：<font color='#0fa3ff'><a target='_blank' href='https://jihulab.com/xiaolxl_pub/xiaolxl-jupyter-controller'>点我访问</a></font>",)
    )
    
    return ui_constructor.get_ui_no_out()