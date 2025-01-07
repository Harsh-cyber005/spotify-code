import requests
import os
import platform

url = ""
output = ""

def get_ffmpeg():
    print("Checking for ffmpeg...")
    platform_name = platform.system()
    if platform_name == "Windows":
        if os.path.exists("./binaries/ffmpeg-win64-v4.2.2.exe"):
            print("ffmpeg-win64-v4.2.2.exe already exists")
            return "./binaries/ffmpeg-win64-v4.2.2.exe"
    elif platform_name == "Linux":
        if os.path.exists("./binaries/ffmpeg-linux64-v4.2.2"):
            print("ffmpeg-linux64-v4.2.2 already exists")
            return "./binaries/ffmpeg-linux64-v4.2.2"

    if platform_name == "Windows":
        url = "https://raw.githubusercontent.com/Harsh-cyber005/ffmpeg-win64-v.4.2.2/refs/heads/master/ffmpeg-win64-v4.2.2.exe"
        output = "./binaries/ffmpeg-win64-v4.2.2.exe"
    elif platform_name == "Linux":
        url = "https://raw.githubusercontent.com/Harsh-cyber005/ffmpeg-win64-v.4.2.2/refs/heads/master/ffmpeg-linux64-v4.2.2"
        output = "./binaries/ffmpeg-linux64-v4.2.2"
    if not os.path.exists("./binaries"):
        os.makedirs("./binaries")

    r = requests.get(url, allow_redirects=True)
    open(output, 'wb').write(r.content)

    return output