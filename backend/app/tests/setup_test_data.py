import requests
import os

def download_test_image():
    # 创建测试数据目录
    test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(test_data_dir, exist_ok=True)
    
    # 下载测试图片
    image_url = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
    image_path = os.path.join(test_data_dir, 'test_image.png')
    
    if not os.path.exists(image_path):
        response = requests.get(image_url)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded test image to: {image_path}")
    
    return image_path

if __name__ == "__main__":
    download_test_image() 