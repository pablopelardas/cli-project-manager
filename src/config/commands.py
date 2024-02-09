from pytermgui import tim, palette
from multiprocessing import Process
import os

palette.regenerate(primary="mediumpurple")

def fn_exit(shell):
    shell.stop()
def fn_ls(config):
    projects = config.get_projects()
    for project in projects:
        tim.print(f"[primary+3] [bold secondary]{project['alias']}[/] - [tertiary]{project['path']}")
def fn_config(config):
    print(config._config)
def fn_add_project(config):
        try:
            input_path = input("Enter the path of the project to add (pwd to add current path): ")
            alias = input("Enter the alias for the project: ")
            handle_input_path(input_path, config.add_project_path, alias)
        except ValueError as e:
            print(e)

def fn_remove_project(config):
        try:
            input_path = input("Enter the path or alias of the project to remove: ")
            handle_input_path(input_path, config.remove_project_path, input_path)
        except ValueError as e:
            print(e)
def fn_modify_project(config):
    try:
        input_path = input("Enter the path or alias of the project to modify: ")
        alias = input("Enter the new alias for the project: ")
        def func(project):
            config.modify_project(project, alias)
        handle_input_path(input_path, func, input_path)
    except ValueError as e:
        print(e)
def fn_add_combo(config):
    try:
        combo = input("Enter the name of the combo to add: ")
        fn_ls(config)
        alias = input("Enter the alias of the project to add to the combo (separated by space): ")
        combo_obj = {"name": combo, "projects": alias.split(" ")}
        config.add_combo(combo_obj)
    except ValueError as e:
        print(e)
def fn_remove_combo(config):
    try:
        combo = input("Enter the name of the combo to remove: ")
        config.remove_combo(combo)
    except ValueError as e:
        print(e)
def fn_open_combo(config):
    try:
        combo = input("Enter the name of the combo to open: ")
        config.get_combo_projects(combo)
        for project in config.get_combo_projects(combo):
            p = config.get_project(project)
            os.system(f"code {p["path"]}")
    except ValueError as e:
        print(e)
def fn_ls_combo(config):
    combos = config.get_combos()
    for combo in combos:
        tim.print(f"[primary+3] [bold secondary]{combo['name']}[/] - [tertiary]{' '.join(combo['projects'])}")
def fn_mod_combo(config):
    try:
        fn_ls_combo(config)
        combo = input("Enter the name of the combo to modify: ")
        alias = input("Enter the new alias for the combo: ")
        config.modify_combo(combo, alias)
    except ValueError as e:
        print(e)

def fn_welcome():
    tim.print("[primary+3]Welcome to [!gradient(150) italic]LocalProjectManager!")
    tim.print("[primary+3]This is a simple tool to manage your local projects and open them with a single command")
# divide general from projects and combo commands
    print("")
    tim.print("[secondary]===[primary+3]General[secondary]===[primary+3]")
    print("")
    tim.print("[primary+3]Type [bold firebrick]'exit'[/][primary+3] to exit the program")
    tim.print("[primary+3]Type [bold darkslateblue]'help'[/][primary+3] to read again this message")
    tim.print("[primary+3]Type [bold darkorange]'clear'[/][primary+3] to clear the terminal")

    print("")
    tim.print("[secondary]===[primary+3]Projects[secondary]===[primary+3]")
    print("")
    tim.print("[primary+3]Type [bold primary]'ls'[/][primary+3] to list the projects")
    tim.print("[primary+3]Type [bold royalblue]'add'[/][primary+3] to add a project to the list")
    tim.print("[primary+3]Type [bold sienna]'rm'[/][primary+3] to remove a project from the list")
    tim.print("[primary+3]Type [bold darkorange]'open'[/][primary+3] to open a project")

    print("")
    tim.print("[secondary]===[primary+3]Combos[secondary]===[primary+3]")
    print("")
    tim.print("[primary+3]Type [bold primary]'lsc'[/][primary+3] to list the combos")
    tim.print("[primary+3]Type [bold royalblue]'addc'[/][primary+3] to add a combo to the list")
    tim.print("[primary+3]Type [bold sienna]'rmc'[/][primary+3] to remove a combo from the list")
    tim.print("[primary+3]Type [bold darkorange]'openc'[/][primary+3] to open a combo")
    print("")
    print("")

def fn_clear():
    print("\033c")

def open_project(config):
    try:
        
        fn_ls(config)
        alias = input("Enter the alias of the project to open: ")
        project = config.get_project(alias)
        # find the project
        if not project:
            raise ValueError(f"Project '{alias}' not in list")
        os.system(f"code {project['path']}")
    except Exception as e:
        print(e)
   
def handle_path_args(*args, fn):
    for arg in args:
        try:
            if arg == "pwd" or arg == '.':
                path = os.getcwd()
            elif arg[0] != "/":
                if arg[0] == "~":
                    path = os.path.expanduser(arg)
                elif arg[0] == ".":
                    path = os.path.join(os.getcwd(), arg[1:])
                else:
                    path = os.path.join(os.getcwd(), arg)
            fn(path)
        except ValueError as e:
            print(e)

def handle_input_path(path, fn, alias= None):
    try:
        if path == "pwd" or path == '.':
            path = os.getcwd()
        if path[0] != "/":
            if path[0] == "~":
                path = os.path.expanduser(path)
            elif path[0] == ".":
                path = os.path.join(os.getcwd(), path[1:])
            else:
                path = os.path.join(os.getcwd(), path)
        project = {"path": path, "alias": alias if alias else path.split("/")[-1]}
        fn(project)
    except ValueError as e:
        print(e)