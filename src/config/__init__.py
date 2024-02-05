import platformdirs
import json
import os
from shell import Command
from config.commands import *


class Config:
    def __init__(self):
        self._app_name = "LocalProjectManager"
        self._app_config_dir = platformdirs.user_config_dir(self._app_name)
        self._app_config_file = os.path.join(self._app_config_dir, "config.json")
        self._config = {}
        self._commands = []
        self._processes = []
        self.__initialize_dir()
        self.__initialize_config_file()
        self._load_config()

    def __initialize_dir(self):
        # verify if app data directory exists
        if not os.path.exists(self._app_config_dir):
            os.makedirs(self._app_config_dir)

    def __initialize_config_file(self):
        # verify that the config file exists
        if not os.path.exists(self._app_config_file):
            with open(self._app_config_file, "w") as f:
                default_config = {
                    "project_paths": [
                        "~/working/ypf/projects"
                    ],                      
                }
                # dict to json
                default_config = json.dumps(default_config, indent=4)
                f.write(default_config)
    def _load_config(self):
        with open(self._app_config_file, "r") as f:
            self._config = json.load(f)
    def _save_config(self):
        with open(self._app_config_file, "w") as f:
            f.write(json.dumps(self._config, indent=4))
    def add_project_path(self, path):
        # verify if path exists
        if not os.path.exists(path):
            raise ValueError(f"Path '{path}' does not exist")
        if path in self._config["project_paths"]:
            raise ValueError(f"Path '{path}' already in list")
        # add path to config
        self._config["project_paths"].append(path)
        self._save_config()
    def remove_project_path(self, path):
        # verify if path exists
        if not os.path.exists(path):
            raise ValueError(f"Path '{path}' does not exist")
        if path not in self._config["project_paths"]:
            raise ValueError(f"Path '{path}' not in list")
        # remove path from config
        self._config["project_paths"].remove(path)
        self._save_config()
    def get_project_paths(self):
        return self._config["project_paths"]
def initialize_commands(shell, config):
    
    commands = [
        Command("exit", lambda: fn_exit(shell)),
        Command(":q", lambda: fn_exit(shell)),
        Command("ls", lambda : fn_ls(config)),
        Command("config", lambda: fn_config(config)),
        Command("add", lambda *args: fn_add_project_path(config, *args)),
        Command("rm", lambda *args: fn_remove_project_path(config, *args)),
        Command("clear", lambda: fn_clear()),
        Command("open", lambda num: open_project(num, config)),
        Command("gui", lambda: open_gui(config)),
        Command("help", lambda: fn_welcome())
    ]
    for command in commands:
        shell.add_command(command.name, command.func)
    return shell

