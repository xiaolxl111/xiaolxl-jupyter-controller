import os
import gradio as gr

from xiaolxl_jupyter_controller.ui_scripts.tools.utils.download_tool import get_download_command
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.json_config_manager2 import JsonConfigManager
from xiaolxl_jupyter_controller.ui_scripts.tools.utils.config_tool import get_config_dirs, get_config_path


def run_command(command: str) -> str:
    """Execute a shell command and return its output."""
    stream = os.popen(command)
    output = stream.read()
    stream.close()
    return output


def download_file(url: str, filename: str, install_key: str, config_file: str) -> str:
    """Download a file using the existing download_tool logic."""
    default_config = os.path.join(os.path.dirname(__file__),
                                  'xiaolxl_jupyter_controller/ui_scripts/data/autodl',
                                  'default_config.json')
    ui_config = JsonConfigManager(config_file, default_config, debug=False)
    download_path = get_config_path(ui_config, install_key)
    command = get_download_command(url, download_path, filename, 'more')
    return run_command(command)


def build_demo(config_file: str):
    default_config = os.path.join(os.path.dirname(__file__),
                                  'xiaolxl_jupyter_controller/ui_scripts/data/autodl',
                                  'default_config.json')
    ui_config = JsonConfigManager(config_file, default_config, debug=False)
    install_dirs = get_config_dirs(ui_config)

    with gr.Blocks() as demo:
        gr.Markdown("# Xiaolxl Jupyter Controller (Gradio)")
        with gr.Tab("Download"):
            url = gr.Textbox(label="File URL")
            filename = gr.Textbox(label="Output filename")
            install = gr.Dropdown(choices=[d[1] for d in install_dirs], label="Install location")
            out = gr.Textbox(label="Command Output")
            download_btn = gr.Button("Download")

            download_btn.click(lambda u, f, i: download_file(u, f, i, config_file),
                               inputs=[url, filename, install],
                               outputs=out)
        with gr.Tab("Shell"):
            cmd = gr.Textbox(label="Shell command")
            cmd_out = gr.Textbox(label="Command Output")
            run_btn = gr.Button("Run")
            run_btn.click(run_command, inputs=cmd, outputs=cmd_out)
    return demo


def launch(config_file: str = '/root/autodl-tmp/default_ui.json'):
    demo = build_demo(config_file)
    demo.launch()


if __name__ == '__main__':
    launch()
