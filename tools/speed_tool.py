import os

# 判断是否已加速
def get_is_speed():
    return os.getenv("http_proxy") != None