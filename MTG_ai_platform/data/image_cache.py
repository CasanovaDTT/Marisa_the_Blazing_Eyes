import os
import requests
from PIL import Image
from io import BytesIO

class ImageCache:
    def __init__(self, cache_dir="cache/images"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_image(self, card_name: str, url: str) -> str:
        # 返回本地图片路径，若不存在则下载
        safe_name = card_name.replace(' ', '_').replace('/', '_')
        local_path = os.path.join(self.cache_dir, f"{safe_name}.jpg")
        if os.path.exists(local_path):
            return local_path
        # 下载
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(resp.content)
                return local_path
        except:
            pass
        return None