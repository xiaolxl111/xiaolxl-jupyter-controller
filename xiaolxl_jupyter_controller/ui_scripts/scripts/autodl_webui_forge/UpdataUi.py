import os
import shutil
import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox,Button,Dropdown,Text,HTML

from ...tools.compoment.ui_tool import * 
from ...tools.utils.print_tool import * 
from ...tools.utils.config_tool import * 
from ...tools.utils.git_tool import * 

def getUi(data,cmd_run,controllers):
    ui_constructor = UIConstructor()
    rootOut = ui_constructor.get_output_component()

    logOut = controllers['logOut']
    uiConfig = controllers['uiConfig']

    class GitManager:
        def __init__(self, path, name, force_update=False, can_delete=True):
            self.path = path
            self.name = name
            self.force_update = force_update
            self.can_delete = can_delete

            self.is_refreshed = False  # 新增属性来跟踪刷新状态

            # UI 组件
            self.refresh_button = self._create_button(f'{name} (点我刷新)', 'info', self._on_refresh)

            self.current_branch_label = self._create_label('当前版本分支: 请先刷新')
            self.current_sha_label = self._create_label('当前版本SHA: 请先刷新')
            self.current_date_label = self._create_label('当前版本日期: 请先刷新')

            self.branch_dropdown = self._create_dropdown([('请先刷新', '请先刷新')])
            self.sha_text = self._create_text_input('自定义版本SHA值: ')
            self.latest_date_label = self._create_label('最新版本日期: 请先刷新')

            self.set_version_button = self._create_button('设置插件版本', 'success', self._on_set_version)
            self.delete_plugin_button = self._create_button('删除插件', 'danger', self._on_delete_plugin)
            self.github_link_button = self._create_html_button('请先刷新')

            # 构建children_components列表
            children_components = [
                self.refresh_button, 
                VBox([self.current_branch_label, self.current_sha_label, self.current_date_label], layout=Layout(overflow='auto', width='310px', white_space='nowrap')), 
                VBox([self.branch_dropdown, self.sha_text, self.latest_date_label], layout=Layout(overflow='auto', width='320px', white_space='nowrap')), 
                self.set_version_button, 
                self.github_link_button
            ]

            # 如果can_delete为True，则在倒数第二的位置插入删除按钮
            if can_delete:
                children_components.append(self.delete_plugin_button)

            self.main_box = HBox(
                children_components,
                layout=Layout(border='solid 1px', width='auto', overflow='auto', display='flex')
            )

        def _create_button(self, description, button_style, on_click_function):
            button = Button(description=description, layout=Layout(overflow='visible', white_space='nowrap', width='auto', height='auto'), button_style=button_style)
            button.on_click(on_click_function)
            return button

        def _create_label(self, value):
            return Label(value=value,layout=Layout(overflow='visible',width='auto',white_space='nowrap'))

        def _create_dropdown(self, options):
            return Dropdown(options=options, value=options[0][1], description='分支选择: ', layout=Layout(overflow='visible', white_space='nowrap'))

        def _create_text_input(self, description):
            return Text(value='', placeholder='不填默认更新为最新', description=description, 
                        style={'description_width': 'initial'}, layout=Layout(overflow='visible', white_space='nowrap'))

        def _create_html_button(self, value):
            return HTML(value=f"<a target='_blank' style='vertical-align: middle;padding:0 3px;background-color:#d7d7d7;word-wrap:break-word;display: table-cell; text-align:center; width:100px; height:95px; border:2px solid black' href=''>{value}</a>")

        def _on_refresh(self, b):
            ui_constructor.clear_output()
            with rootOut:
                self._update_button(self.refresh_button, "正在检查...", "warning")

                # 获取主分支名称、当前分支、当前SHA和最新SHA
                main_branch_name = get_git_main_b_name(self.path)
                current_branch_name = get_git_nov_b_name(self.path)
                current_sha = get_git_now_v_sha(self.path)
                newest_sha = get_git_newest_v_sha(self.path)

                _now_time = get_git_now_v_time(self.path)
                _newest_time = get_git_newest_v_time(self.path)
                # 更新当前状态标签
                self.current_branch_label.value = '当前版本分支: ' + current_branch_name
                self.current_sha_label.value = '当前版本SHA: ' + current_sha
                self.current_date_label.value = '当前版本日期: ' + _now_time
                self.latest_date_label.value = '最新版本日期: ' + _newest_time

                # 更新分支下拉菜单
                all_branches = get_git_all_b_name(self.path)
                self.branch_dropdown.options = [(branch['branch_name'], branch['branch_name']) for branch in all_branches]
                self.branch_dropdown.value = current_branch_name

                # 更新GitHub链接
                repo_url = get_git_main_url(self.path)
                self.github_link_button.value = f"<a target='_blank' style='vertical-align: middle;padding:0 3px;background-color:#d7d7d7;word-wrap:break-word;display: table-cell; text-align:center; width:100px; height:95px; border:2px solid black' href='{repo_url}'>点我访问对应git项目链接</a>"

                if _now_time != _newest_time:
                    self._update_button(self.set_version_button, "设置插件版本(可更新)", "warning")
                else:
                    self._update_button(self.set_version_button, f'设置插件版本', "success")
                self._update_button(self.refresh_button, f'{self.name} (点我刷新)', "info")

                self.is_refreshed = True  # 标记刷新已完成

        def _on_set_version(self, b):
            if not self.is_refreshed:
                ui_constructor.clear_output()
                with rootOut:
                    print("请先刷新!")
                return
            
            self._update_button(self.set_version_button, "正在更新...", "warning")

            # 获取所选分支和SHA
            selected_branch = self.branch_dropdown.value
            selected_sha = self.sha_text.value.strip()

            # 如果启用了强制更新，先执行强制更新
            if self.force_update:
                force_update_git_repo(self.path)

            change_git_b_and_v(self.path, selected_branch, selected_sha)

            # 刷新UI以反映更改
            self._on_refresh(b)

        def _update_button(self, button, description, button_style):
            button.description = description
            button.button_style = button_style

        def _on_delete_plugin(self, b):
            with rootOut:
                try:
                    shutil.rmtree(self.path)  # 删除目录及其所有内容
                    # 更新UI或显示成功消息
                    logOut.print(f'插件目录 {self.path} 已成功删除')
                    scan_and_update(self)
                except Exception as e:
                    # 处理异常，例如目录不存在或删除失败
                    logOut.print(f'删除失败: {e}')

        def getUi(self):
            return self.main_box

    with rootOut:
        ui_constructor.add_component(
            widgets.HTML(value="<font size='2' color='red'>【重要】1.更新或进行任何操作前请刷新对应项目</font><br><font size='2' color='red'>【重要|仅限v15.3以下的镜像|v15.3以上的镜像只需要更新完启动器重启内核再运行启动器即可】2.更新启动器后关闭笔记本(MainUi.ipynb)点丢弃，再次打开笔记本(MainUi.ipynb)一定记得右上角选择xl_env环境</font><br><font size='2' color='red'>3.如果有网络问题可以开启学术加速</font><br><font size='2' color='red'>4.启动器如果检测到更新可能只是更新了网络数据, 可以选择不更新, 需要更新的时候可以看加速按钮旁边的提示</font>")
        )
        ui_constructor.add_component(GitManager(get_xiaolxl_jupyter_controller_path(),"启动器", force_update=True, can_delete=False).getUi())
        ui_constructor.add_component(GitManager(get_config_path(uiConfig,"sdWebUi_dir"),"webui主程序", force_update=False, can_delete=False).getUi())

        # =============================================================================

        git_extensions = []
        extensions_box = VBox([])

        def _refresh_ui():
            """更新UI界面"""
            extensions_box.children = tuple(git_manager.getUi() for git_manager in git_extensions)

            updata_scan.description = '扫描可更新程序与插件[设置版本前一定要先刷新！]'
            updata_scan.button_style = 'info'

        def _scan_extension_dir():
            dir_ = get_config_path(uiConfig,"sdWebUiExtensions_dir")

            files = [f for f in os.listdir(dir_) if f != '.ipynb_checkpoints']
            extension_list = [
                {
                    "name": d_path[d_path.rfind('/') + 1:],
                    "path": d_path,
                }
                for file_name in files
                for d_path in [os.path.join(dir_, file_name)]
                if os.path.isdir(d_path)
            ]
            return extension_list

        def scan_and_update(self):
            updata_scan.description = '正在扫描...'
            updata_scan.button_style = 'warning'

            scanned_extensions = _scan_extension_dir()
            scanned_paths = [extension["path"] for extension in scanned_extensions]

            # 添加新的插件
            for extension in scanned_extensions:
                if not any(git_manager.path == extension["path"] for git_manager in git_extensions):
                    new_git_manager = GitManager(extension["path"], extension["name"])
                    git_extensions.append(new_git_manager)

            # 移除已删除的插件
            for git_manager in git_extensions[:]:  # 使用列表副本进行迭代，以便安全删除
                if git_manager.path not in scanned_paths:
                    git_extensions.remove(git_manager)

            _refresh_ui()

        updata_scan = widgets.Button(
            description='扫描可更新程序与插件[设置版本前一定要先刷新！]',
            style={'description_width': 'initial'},
            layout=Layout(width='600px', height='auto'),
            button_style='info'
        )
        updata_scan.on_click(scan_and_update)
        

        scan_all_button = widgets.Button(
            description='扫描并刷新所有插件',
            style={'description_width': 'initial'},
            layout=Layout(width='auto', height='auto'),
            button_style='info'
        )
        def _on_scan_all_clicked(b):
            """处理全部扫描按钮的点击事件"""
            scan_and_update(None)  # 先扫描所有插件
            for git_manager in git_extensions:
                git_manager._on_refresh(None)  # 依次刷新每个插件
        # 为全部扫描按钮绑定事件处理函数
        scan_all_button.on_click(_on_scan_all_clicked)
        # 将新按钮添加到 UI 构造器中
        scan_buttons_box = HBox([updata_scan, scan_all_button])  # 用 HBox 放置两个按钮

        ui_constructor.add_component(scan_buttons_box)
        ui_constructor.add_component(extensions_box)


    return ui_constructor.get_ui()