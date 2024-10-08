import zipfile
import csv
import os
import sys
import io

class VirtualShell:
    def __init__(self, config_file):
        self.config = self.read_config(config_file)
        self.username = self.config['username']
        self.hostname = self.config['hostname']
        self.vfs_path = self.config['vfs_path']
        self.startup_script = self.config['startup_script']
        self.vfs = self.load_vfs()
        self.current_path = '/'

    def read_config(self, config_file):
        config = {}
        with open(config_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                config.update(row)
        return config

    def load_vfs(self):
        vfs = {}
        with zipfile.ZipFile(self.vfs_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                vfs['/'+file_info.filename] = zip_ref.read(file_info.filename)
        return vfs

    def run_startup_script(self):
        if self.startup_script in self.vfs:
            commands = self.vfs[self.startup_script].decode().splitlines()
            for command in commands:
                self.execute_command(command)

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]

        if cmd == 'ls':
            self.ls(args)
        elif cmd == 'cd':
            self.cd(args)
        elif cmd == 'exit':
            self.exit()
        elif cmd == 'uname':
            self.uname(args)
        elif cmd == 'tac':
            self.tac(args)
        elif cmd == 'rev':
            self.rev(args)
        else:
            print(f"Unknown command: {cmd}")

    def ls(self, args):
        path = args[0] if args else self.current_path
        for file in self.vfs:
            if file.startswith(path):
                print(file)

    def cd(self, args):
        if not args:
            print("Usage: cd <directory>")
            return
        new_path = args[0]
        if new_path == '..':
            self.current_path = os.path.dirname(self.current_path)
        elif new_path.startswith('/'):
            self.current_path = new_path
        else:
            self.current_path = os.path.join(self.current_path, new_path)

    def exit(self):
        sys.exit(0)

    def uname(self, args):
        print("VirtualOS")

    def tac(self, args):
        if not args:
            print("Usage: tac <file>")
            return
        file_path = args[0]
        if file_path in self.vfs:
            content = self.vfs[file_path].decode().splitlines()
            for line in reversed(content):
                print(line)

    def rev(self, args):
        if not args:
            print("Usage: rev <file>")
            return
        file_path = args[0]
        if file_path in self.vfs:
            content = self.vfs[file_path].decode()
            print(content[::-1])

    def start(self):
        self.run_startup_script()
        while True:
            prompt = f"{self.username}@{self.hostname}:{self.current_path}$ "
            command = input(prompt)
            self.execute_command(command)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python virtual_shell.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    shell = VirtualShell(config_file)
    shell.start()
