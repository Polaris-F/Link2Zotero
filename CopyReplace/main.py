import platform
import subprocess
import pyperclip
import time
import configparser
import re
from pathlib import Path
from threading import Thread
import sys
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image

# 使用 RawConfigParser 读取配置文件，保留原始字符串格式
config = configparser.RawConfigParser()
config.read(r'config.ini')
replace_url = config.get('Settings', 'replace_url').strip('"')
icon_path = Path(config.get('Settings', 'icon_path').strip('"'))

# 检查系统类型并导入相应的通知库
if platform.system() == 'Windows':
    if platform.release() == '11':
        from win11toast import toast
    else:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
else:
    print('This script is only supported on Windows 10 or 11.')
    exit()

# 定义在 Windows 10 上显示消息的函数
def show_Msg_win10(Msg_title="Link2Zotero", Msg_content="未监测到待替换字段"):
    if icon_path.exists():
        toaster.show_toast(Msg_title, Msg_content, icon_path=str(icon_path), duration=3)
    else:
        print(f"Icon file not found: {icon_path}")
        toaster.show_toast(Msg_title, Msg_content, duration=3)

# 定义在 Windows 11 上显示消息的函数
def show_Msg_win11(Msg_title="Link2Zotero", Msg_content="未监测到待替换字段"):
    if icon_path.exists():
        toast(Msg_title, Msg_content, icon=str(icon_path))
    else:
        toast(Msg_title, Msg_content)

# 定义处理剪贴板文本的函数，使用正则表达式
def process(clip_text: str) -> (str, int): # type: ignore
    # 使用正则表达式匹配 "zotero://" 且前面没有 "#" 的部分
    pattern = r'(?<!#)(zotero://[^\s]+)'
    # 统计匹配到的链接数量
    link_count = len(re.findall(pattern, clip_text))
    # 替换匹配到的链接
    new_text = re.sub(pattern, replace_url, clip_text)
    return new_text, link_count

# 剪贴板监控主函数
def clipboard_monitor():
    last_clip_text = ""
    while True:
        clip_text = pyperclip.paste()
        if clip_text and clip_text != last_clip_text and "zotero://" in clip_text:
            processed_text, link_count = process(clip_text)
            if link_count > 0:  # 只有在有替换发生时才进行操作
                last_clip_text = processed_text
                pyperclip.copy(processed_text)
                print(f"Processed: {processed_text}")
                msg_content = f"Successfully replaced {link_count} links"
                if platform.release() == '11':
                    show_Msg_win11("Link2Zotero", msg_content)
                else:
                    show_Msg_win10("Link2Zotero", msg_content)
        time.sleep(0.5)  # 每500毫秒检测一次剪贴板内容

# 系统托盘相关函数
def on_quit(icon, item):
    icon.stop()

def on_restart(icon, item):
    python = sys.executable
    icon.stop()  # 停止托盘图标，释放资源
    
    # 添加延时，等待资源释放
    time.sleep(2)  # 等待2秒（你可以根据需要调整时间）

    subprocess.Popen([python] + sys.argv)
    sys.exit()  # 退出当前进程

# 设置系统托盘图标和菜单
def setup_tray_icon():
    # 使用本地图片作为托盘图标
    image = Image.open(icon_path)
    icon = Icon("Link2Zotero", image, "Link2Zotero", Menu(
        MenuItem('Restart', on_restart),
        MenuItem('Quit', on_quit)
    ))
    icon.run()
    image.close()  # 确保图像文件在使用后被关闭


if __name__ == "__main__":
    # 启动剪贴板监控线程
    clipboard_thread = Thread(target=clipboard_monitor, daemon=True)
    clipboard_thread.start()
    
    # 设置并启动系统托盘图标
    setup_tray_icon()
