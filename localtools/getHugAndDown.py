import requests
from bs4 import BeautifulSoup
import subprocess

def cmd_run(com):
    !{com}

def get_model_names_and_urls(base_url="https://huggingface.co/lllyasviel/sd_control_collection/tree/main"):
    try:
        response = requests.get(base_url)
        if response.status_code != 200:
            return "Failed to retrieve data. Status code: " + str(response.status_code)

        soup = BeautifulSoup(response.content, 'html.parser')

        # 根据新的 HTML 结构更新选择器
        links = soup.find_all('a', {'class': 'group'})

        models = []
        for link in links:
            href = link.get('href')
            if href and '/resolve/main/' in href:
                model_name = href.split('/')[-1].split('?')[0]  # 提取文件名
                download_url = "https://huggingface.co" + href  # 构造完整的下载链接
                models.append((model_name, download_url))

        return models
    except Exception as e:
        return str(e)
    
def download_files_with_aria2c(models, download_directory="/root/autodl-tmp/upmod"):
    """
    Download files using aria2c.

    Args:
    models (list of tuples): List of model name and download URL tuples.
    download_directory (str): Path to the directory where files will be downloaded.
    """
    for model_name, url in models:
        # 构建完整的下载命令
        command = f'aria2c -s 16 -x 8 --seed-time=0 "{url}" -d "{download_directory}" -o "{model_name}"'
        cmd_run(command)

# Example usage
models = get_model_names_and_urls()
# for model_name, url in models:
#     print(f"Model: {model_name}, URL: {url}")

download_files_with_aria2c(models, '/root/autodl-tmp/upmod')