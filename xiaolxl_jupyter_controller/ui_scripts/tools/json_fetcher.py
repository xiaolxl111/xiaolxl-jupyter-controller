import requests
import os
import json

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

    def get_abs_path(self, relative_path):
        """
        获取相对于当前脚本的绝对路径。

        :param relative_path: 相对于当前脚本的相对路径。
        :return: 绝对路径。
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(script_dir, relative_path)
        self.log(f"相对路径 '{relative_path}' 的绝对路径为: {abs_path}")
        return abs_path

    def fetch_json(self, url, relative_path):
        """
        从远程 URL 或本地路径获取 JSON 数据，并返回一个元组，
        其中包含 JSON 数据和一个布尔值（指示数据是否来自网络）。

        :param url: 远程 URL 地址。
        :param relative_path: 本地文件的相对路径。
        :return: 一个元组，包含 JSON 数据和一个布尔值。
        """
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
            local_path = self.get_abs_path(relative_path)
            self.log(f"尝试从本地路径获取 JSON 数据: {local_path}")
            try:
                if os.path.exists(local_path):
                    with open(local_path, 'r') as file:
                        data = json.load(file)
                        self.log("成功从本地文件获取 JSON 数据。")
            except Exception as e:
                self.log(f"从本地文件获取数据失败，错误信息: {e}")

        return data, fetched_from_network

# 使用示例
# fetcher = JsonFetcher(timeout=5, debug=True, fetch_from_network=False)
# data, _  = fetcher.fetch_json("https://example.com/data.json", "../data/local_data.json")
