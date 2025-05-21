import requests
import os
import json
from xiaolxl_jupyter_controller import RootDir

class JsonFetcher:
    def __init__(self, timeout=10, debug=False, fetch_from_network=True):
        """
        初始化 JsonFetcher 类。
        :param timeout: 请求的超时时间，默认为 10 秒。
        :param debug: 是否开启调试模式，默认为 False。
        :param fetch_from_network: 是否从网络获取 JSON 数据，默认为 True。
        """
        self.timeout = timeout
        self.debug = debug
        self.fetch_from_network = fetch_from_network

    def log(self, message):
        """
        输出调试信息。
        :param message: 需要输出的消息。
        """
        if self.debug:
            print(f"[JsonFetcher]: {message}")

    def fetch_json(self, branch, relative_path):
        """
        从远程 URL 或本地路径获取 JSON 数据，并返回一个元组，
        其中包含 JSON 数据和一个布尔值（指示数据是否来自网络）。
        :param branch: GitHub 分支名。
        :param relative_path: 本地文件的相对路径。
        :return: 一个元组，包含 JSON 数据和一个布尔值。
        """
        base_url = "https://jihulab.com/xiaolxl_pub/xiaolxl-jupyter-controller/-/raw"
        url = f"{base_url}/{branch}/xiaolxl_jupyter_controller/{relative_path}"
        local_path = os.path.join(RootDir.get_import_root_dir(), relative_path)
        
        fetched_from_network = False
        data = {}

        if self.fetch_from_network:
            self.log(f"尝试从 URL 获取 JSON 数据: {url}")
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                fetched_from_network = True
                self.log("成功从远程 URL 获取 JSON 数据。")
            except requests.RequestException as e:
                self.log(f"从 URL 获取数据失败，错误信息: {e}")

        if not fetched_from_network:
            self.log(f"尝试从本地路径获取 JSON 数据: {local_path}")
            try:
                if os.path.exists(local_path):
                    with open(local_path, 'r') as file:
                        data = json.load(file)
                        self.log("成功从本地文件获取 JSON 数据。")
            except Exception as e:
                self.log(f"从本地文件获取数据失败，错误信息: {e}")

        return data, fetched_from_network