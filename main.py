
from display.dymatic_layout import *
from display.style_layout import *

def check_and_download_file():

    files = [
        {
            "file_name": "GeoLite2-ASN.mmdb",
            "url": "https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb"
        },
        {
            "file_name": "GeoLite2-Country.mmdb",
            "url": "https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb"
        }
    ]

    for file_info in files:
        file_name = file_info["file_name"]
        url = file_info["url"]
        file_path = os.path.join("src", file_name)

        if os.path.isfile(file_path):
            pass
        else:
            print(f"File {file_name} does not exist. Downloading from {url}...")
            try:
                urllib.request.urlretrieve(url, file_path)
                print(f"File {file_name} downloaded and saved to ")
            except Exception as e:
                print(f"Failed to download {file_name}. Error: {e}")



def change_file_asyncio():
    file_name = "proactor_events.py"
    src_path = Path("src") / file_name
    dest_folder = Path.home() / "AppData" / "Local" / "Programs" / "Python" / "Python312" / "Lib" / "asyncio"
    dest_path = dest_folder / file_name

    if not src_path.is_file():
        print(f"File {file_name} does not exist in src directory.")
        return

    try:
        shutil.copy2(str(src_path), str(dest_path))
    except Exception as e:
        print(f"Failed to move {file_name}. Error: {e}")


def config_settings():
    if "win" in sys.platform.lower():
        folder_path = Path.home() / r"AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState"
        file_path = [file_path.name for file_path in folder_path.glob("*.json")]
        if 'settings.json' in str(file_path):
            with open(f"{folder_path}\\settings.json", 'r', encoding='utf-8') as file:
                data = json.load(file)

                data['initialCols'] = 120
                data['initialRows'] = 40

                profiles = data["profiles"]
                list_profiles = profiles["list"]

                profiles_0 = list_profiles[0]
                font_list_0 = profiles_0['font']
                font_list_0['size'] = 11
                font_list_0['face'] = 'Cascadia Mono'
                font_list_0['weight'] = 990
                profiles_0['padding'] = '8'
                profiles_0['adjustIndistinguishableColors'] = 'always'

                profiles_1 = list_profiles[1]
                font_list_1 = profiles_1['font']
                font_list_1['size'] = 15
                font_list_1['face'] = 'Cascadia Mono'
                profiles_1['padding'] = '10'
                profiles_1['adjustIndistinguishableColors'] = 'always'

                with open(f"{folder_path}\\settings.json", 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)

def clear():
    try:
        if "linux" in sys.platform.lower():
            os.system("clear")
        elif "win" in sys.platform.lower():
            os.system("cls")
        else:
            os.system("clear")
    except (Exception,):
        os.system("cls")

def main():
    clear()
    config_settings()
    check_and_download_file()
    change_file_asyncio()
    layout = StyleLayout().update_style_layout()
    dymatic = DymaticLayout(layout=layout, live=None)
    dymatic.dymatic_select()

    with Live(layout, refresh_per_second=1000, screen=True) as live:
        dymatic.live = live
        try:
            keyboard.on_press(dymatic.handle_key_press)
            keyboard.wait("esc")
        except KeyboardInterrupt:
            pass
        finally:
            keyboard.unhook_all()


if __name__ == '__main__':
    main()


# from pynput import keyboard
# from display.dymatic_layout import *
# from display.style_layout import *
# import os
# import sys
# import termios
#
#
# def clear():
#     try:
#         if "linux" in sys.platform.lower():
#             os.system("clear")
#         elif "win" in sys.platform.lower():
#             os.system("cls")
#         else:
#             os.system("clear")
#     except Exception:
#         os.system("cls")
#
# def disable_echo():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     new_settings = termios.tcgetattr(fd)
#     new_settings[3] = new_settings[3] & ~termios.ECHO  # Disable echo
#     termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
#     return old_settings
#
# def restore_terminal(old_settings):
#     fd = sys.stdin.fileno()
#     termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#
# def main():
#     clear()
#     layout = StyleLayout().update_style_layout()
#     dymatic = DymaticLayout(layout=layout, live=None)
#     dymatic.dymatic_select()
#
#     def on_press(key):
#         try:
#             event = type('Event', (), {'name': key.char if hasattr(key, 'char') else key.name})()
#             dymatic.handle_key_press(event)
#         except AttributeError:
#             pass
#
#     old_settings = disable_echo()  # Disable terminal echo
#     try:
#         with Live(layout, refresh_per_second=1000, screen=True) as live:
#             dymatic.live = live
#             try:
#                 with keyboard.Listener(on_press=on_press) as listener:
#                     listener.join()
#             except KeyboardInterrupt:
#                 pass
#     finally:
#         restore_terminal(old_settings)  # Restore terminal settings
#
# if __name__ == "__main__":
#     main()