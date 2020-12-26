"""
GoBuster on Steriods (gbos for short) is an individual project to enhance gobuster's directory search capabilities by forking new gobuster processes running on multuple threads to search into newly discovered directories efficiently, using the given wordlist
By @Mohamed512a
"""
import sys
import argparse
import subprocess
from time import sleep
import random
import threading 


class GobusterScan:
    def __init__(self, args:str, parent_dir=""):
        self.args = args
        self.parent_dir = parent_dir

    def start(self):
        command: str = "gobuster dir " + self.args
        command_list: list = command.split(" ")
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for _dir in iter(p.stdout.readline, b''):
            _dir = _dir.decode("utf8")
            if _dir and _dir[0] == "/": # is it a new directory? then dig deeper
                _dir = _dir.split(" ")[0]
                acc_dirs = self.parent_dir+_dir
                print(acc_dirs)

                _args = self.get_appended_url_args(_dir)
                gobuster_scan = GobusterScan(_args, parent_dir=acc_dirs)

                _t = threading.Thread(target=gobuster_scan.start) 
                _t.start()


        while p.poll() is None:
            sleep(0.1) 
        err = p.stderr.read()
        if p.returncode != 0:
            print("Error: " + str(err))

    def get_appended_url_args(self, dir:str) -> str: # i.e. dir = "/home"
        index:int = self.args.index("-u")
        
        _args_1:str = self.args[:index]
        _args_2:str = self.args[index + 3:]
        
        url = _args_2.split(" ")[0]
        url = url + dir

        _args_2 = _args_2[_args_2.index(" "):]

        new_args = _args_1 + "-u " + url + _args_2
        return new_args



def main(args: str) -> None:
    scan:GobusterScan = GobusterScan(args)
    _t = threading.Thread(target=scan.start) 
    _t.start()

if __name__ == "__main__":
    args_as_is:list = sys.argv[1:]
    args_str:str = " ".join(args_as_is)
        
    main(args_str)
