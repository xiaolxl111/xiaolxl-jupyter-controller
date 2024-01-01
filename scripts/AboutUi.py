import ipywidgets as widgets

from ui_tool import * 
from config_tool import * 

def getUi(data,cmd_run,controllers):
    ui_constructor = UIConstructor()

    ui_constructor.add_component(
        widgets.HTML(value="<h3><font color='#A52A2A'>启动器版本：" + "3.0.0 - 2023/12/31" + "</font></h3>",)
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

    file = open(get_xiaolxl_jupyter_controller_path() + "/img/qq.jpg", "rb")
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
        widgets.HTML(value="【推荐】整合版4.0镜像(3.1-V15)介绍视频：<font color='#0fa3ff'><a target='_blank' href=''>暂未发布</a></font>",)
    )

    ui_constructor.add_component(
        widgets.HTML(value="<hr>",)
    )
    
    ui_constructor.add_component(
        widgets.HTML(value="启动器开源地址：<font color='#0fa3ff'><a target='_blank' href='https://jihulab.com/xiaolxl_pub/xiaolxl-jupyter-controller'>点我访问</a></font>",)
    )
    
    return ui_constructor.get_ui_no_out()