import AbstractExtract
import os
from base64 import *
import subprocess
import multiprocessing
import subprocess
import yaml

class BinProcessor(AbstractExtract.ExtractFrameWork):

    __dump = None
    __conf_file = "scalpel.conf"
    __mountPoint = "my_mountPoint"
    __processor = None
    __passwd = None
    __name = None
    __commands = [
        "mkdir Playground",#0
        "cp scalpel.conf Playground/",#1
    ]
    __scalpel_runner=[
        f"sudo -S scalpel -c {__conf_file} -o Output ",
    ]
    [
        "sudo -S umount mountpoint",
        "sudo -S rmdir mountpoint",

    ]
    __foremost_runner=[
        f"sudo -S foremost -o Output -c {__conf_file} -i "
    ]

    def get_pass(self):
        with open('data.yaml', 'r') as file:
            yaml_data = yaml.safe_load(file)
        line=yaml_data['wsl']['wsl_pass']
        return line

    def setupDump(self):

        for cmd in range(2):
            command = self.__commands[cmd]
            full_command = ["wsl", "bash", "-ic", command]
            subprocess.run(full_command, shell=True, text=True, check=True)
        os.chdir("Playground")
        for i in self.__dump:
            name = i["name"]
            data = i["content"]
            print(f"Name: {name}, Type: {type(name)}")  # Debugging print statement
            try:
                with open(name, "wb") as f:
                    f.write(b64decode(data))
            except TypeError as e:
                print(f"Error: {e}, Name: {name}, Type: {type(name)}")  # Additional debug info
            finally:
                self.__name = name
        


    def startAnalysis(self):
        arr = None
        if self.__processor == "Scalpel":
            arr = f"echo {self.__passwd} | " + self.__scalpel_runner[0]+ self.__name
        else:
            arr = f"echo {self.__passwd} | "+ self.__foremost_runner[0] + self.__name

        full_command = ["wsl", "bash", "-ic", arr]
        subprocess.run(full_command, shell=True, text=True, check=True)

    def cleanUp():
        pass
