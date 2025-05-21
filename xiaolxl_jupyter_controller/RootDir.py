from pathlib import Path

def get_project_root_dir():
    # 定位到项目根目录
    root_dir = Path(__file__).parent.resolve()
    root_dir = root_dir.parent
    return root_dir

def get_import_root_dir():
    # 定位到项目根目录
    root_dir = Path(__file__).parent.resolve()
    return root_dir