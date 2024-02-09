import platformdirs
import json
import os
from shell import Command
from config.commands import *


class Config:
    def __init__(self):
        self._app_name = "LocalProjectManager"
        self._app_config_dir = platformdirs.user_config_dir(self._app_name)
        print(self._app_config_dir)
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
                    "projects": [
                    ],
                    "combos": []         
                }
                # dict to json
                default_config = json.dumps(default_config, indent=4)
                f.write(default_config)
    def _load_config(self):
        with open(self._app_config_file, "r") as f:
            self._config = json.load(f)
            if "projects" not in self._config:
                self._config["projects"] = []
            if "combos" not in self._config:
                self._config["combos"] = []
    def _save_config(self):
        with open(self._app_config_file, "w") as f:
            f.write(json.dumps(self._config, indent=4))
    def add_project_path(self, project):
        for saved_project in self._config["projects"]:
            if project["path"] == saved_project["path"]:
                raise ValueError(f"Project '{project['path']}' already in list")
            if project["alias"] == saved_project["alias"]:
                raise ValueError(f"Alias '{project['alias']}' already in list")
        # verify if path exists
        if not os.path.exists(project["path"]):
            raise ValueError(f"Path '{project['path']}' does not exist")
        # add path to config
        self._config["projects"].append(project)
        self._save_config()
    def remove_project_path(self, project):
        # verify if path exists
        for saved_project in self._config["projects"]:
            if project["path"] == saved_project["path"] or project["alias"] == saved_project["alias"]:
                # remove path from config
                self._config["projects"].remove(saved_project)
                self._save_config()
                return
        raise ValueError(f"Project '{project['path']}' - Alias '{project['alias']}' not in list")
    def modify_project(self, project, alias):
        for saved_project in self._config["projects"]:
            if project["path"] == saved_project["path"] or project["alias"] == saved_project["alias"]:
                saved_project["alias"] = alias
                self._save_config()
                return
        raise ValueError(f"Project '{project['path']}' not in list")
    def add_combo(self, combo):
        for saved_combo in self._config["combos"]:
            if combo["name"] == saved_combo["name"]:
                raise ValueError(f"Combo '{combo['name']}' already in list")
        self._config["combos"].append(combo)
        self._save_config()
    def remove_combo(self, combo_name):
        found = False
        for combo in self._config["combos"]:
            if combo_name == combo.get("name"):
                self._config["combos"].remove(combo)
                self._save_config()
                found = True
                return
        if not found:
            raise ValueError(f"Combo '{combo_name}' not in list")
    def get_projects(self):
        return self._config["projects"]
    def get_combos(self):
        return self._config["combos"]
    def get_combo_projects(self, combo_name):
        for combo in self._config["combos"]:
            if combo_name == combo.get("name"):
                return combo.get("projects")
        raise ValueError(f"Combo '{combo_name}' not in list")
    def get_project(self, alias):
        for project in self._config["projects"]:
            if alias == project.get("alias"):
                return project
        raise ValueError(f"Project '{alias}' not in list")
def initialize_commands(shell, config):
    
    commands = [
        Command("exit", lambda: fn_exit(shell)),
        Command(":q", lambda: fn_exit(shell)),
        Command("ls", lambda : fn_ls(config)),
        Command("add", lambda *args: fn_add_project(config)),
        Command("rm", lambda *args: fn_remove_project(config)),
        Command("open", lambda: open_project(config)),
        Command("lsc", lambda: fn_ls_combo(config)),
        Command("addc", lambda: fn_add_combo(config)),
        Command("rmc", lambda: fn_remove_combo(config)),
        Command("openc", lambda: fn_open_combo(config)),
        Command("config", lambda: fn_config(config)),
        Command("clear", lambda: fn_clear()),
        Command("help", lambda: fn_welcome()),
        Command("mod", lambda *args: fn_modify_project(config))
    ]
    config._commands = commands
    for command in commands:
        shell.add_command(command.name, command.func)
    return shell

