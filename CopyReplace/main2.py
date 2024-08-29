import re
import time
import pyperclip
import pystray
from pystray import Icon, Menu, MenuItem
from PIL import Image
import pystray._win32
import threading
from notifypy import Notify


def repl(match: re.Match):
    return "https://hichennyang.github.io/zotero-link/#{}".format(match.group())

def main():
    notification = Notify(
        default_notification_application_name = "zotero-link",
        default_notification_icon = "logo.png"
    )
    # pattern = r"zotero://\S*\)\)"
    pattern = r'(?<!#)(zotero://[^\s]+)'
    pre_past = ""
    
    while True:
        string = pyperclip.paste()
        if pre_past != string:
            if re.match(".*"+pattern, string):
                string = re.sub(pattern, repl, string)
                pyperclip.copy(string)
                notification.title = ""
                notification.message = "替换完毕"
                notification.send()

            pre_past = string
        time.sleep(0.5)

def quit(icon: pystray._win32.Icon) -> None:
    icon.stop()

def setup(icon: pystray._win32.Icon) -> None:
    icon.visible = True
    threading.Thread(target=main, daemon=True).start()

if __name__ == "__main__":
    Icon(
        "zotero-link",
        icon = Image.open("logo.png"),
        title = "zotero-link",
        menu = Menu(
            MenuItem("退出", quit)
        )
    ).run(setup)
