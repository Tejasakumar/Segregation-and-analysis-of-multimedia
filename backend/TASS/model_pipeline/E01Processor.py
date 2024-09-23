import AbstractExtract
import os
from base64 import *
import subprocess
import multiprocessing
import subprocess
import yaml



class E01Processor(AbstractExtract.ExtractFrameWork):
    # _protected 
    # __private
    __dump = None
    __conf_file = "scalpel.conf"
    __mountPoint = "my_mountPoint"
    __processor = None
    __passwd = None
    __commands = [
        "mkdir Playground",#0
        "cp scalpel.conf Playground/",#1
        "sudo -S ewfmount",#2
        "sudo -S find mountpoint",#3
    ]
    __scalpel_runner=[
        f"sudo -S scalpel -c {__conf_file} -o Output {__mountPoint}/ewf1",
    ]
    [
        "sudo -S umount mountpoint",
        "sudo -S rmdir mountpoint",

    ]
    __foremost_runner=[
        f"sudo -S foremost -i {__mountPoint}/ewf1 -o Output -c {__conf_file}"
    ]

    def __init__(self , dump,processor):
        self.__dump = dump
        self.__processor = processor
        self.__passwd = self.get_pass()
        # self.__process_config()

    def get_pass(self):
        with open('data.yaml', 'r') as file:
            yaml_data = yaml.safe_load(file)
        line=yaml_data['wsl']['wsl_pass']
        # with open(file_path) as f:
        #     lines = f.readlines()
        #     line = lines[0]
        # delims = ["{", "}", "/n"]
        # for i in delims:
        #     line = line.replace(i, "")
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

        os.mkdir(self.__mountPoint)
        self.__dump.sort(key=lambda x: x["name"])
        
        text = f"echo {self.__passwd} | " + self.__commands[2]+f" {self.__dump[0]['name']} {self.__mountPoint}"
        full_command = ["wsl", "bash", "-ic", text]
        subprocess.run(full_command, check=True, shell=True, text=True)


    def startAnalysis(self):
        arr = None
        if self.__processor == "Scalpel":
            arr = f"echo {self.__passwd} | " + self.__scalpel_runner[0]
        else:
            arr = f"echo {self.__passwd} | "+ self.__foremost_runner[0]

        
        full_command = ["wsl", "bash", "-ic", arr]
        subprocess.run(full_command, shell=True, text=True, check=True)



    def cleanUp(self):
        print("Unmounting and cleaning ....")
        os.system(f"umount {self.__mountPoint}")
        print(f"Unmounted {self.__mountPoint}")
        os.chdir(f"..")
        os.system(f"rm -r Playground")
        print(f"cleaned up ")



    def __process_config(self):
        # Create a dictionary to store config content by format
        config_sections = {}
        current_section = None

        # Read the input config file
        with open(self.__conf_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    # New section header
                    current_section = line[2:].strip().replace("/", "_")
                    config_sections[current_section] = []
                elif current_section:
                    # Add line to the current section
                    config_sections[current_section].append(line)

        # Write each section to a separate config file
        for section, lines in config_sections.items():
            output_file = f'scalpel_{section}.conf'
            with open(output_file, 'w') as f:
                for line in lines:
                    f.write(line + '/n')
            self.__file_pointers.append(output_file)

    def __extract_files(self,image_path, output_dir):
    # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    # Define Scalpel command
        scalpel_command = [
            'scalpel', 
            '-c', 'scalpel.conf',  # Specify the path to scalpel.conf
            '-o', output_dir,      # Output directory for recovered files
            image_path             # Path to the forensic image
        ]

    # Run Scalpel command
        try:
            subprocess.run(scalpel_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running Scalpel: {e}")
        return
        
    def run_in_separate_process(self, target_function, *args):
        p = multiprocessing.Process(target=target_function, args=args)
        p.start()
        p.join()
