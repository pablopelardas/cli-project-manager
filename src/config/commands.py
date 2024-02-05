from pytermgui import tim, palette
from widgets import example
from multiprocessing import Process
import os

palette.regenerate(primary="mediumpurple")

def fn_exit(shell):
    shell.stop()
def fn_ls(config):
    project_paths = config.get_project_paths()
    for i in range(len(project_paths)):
        print(f"{i+1}. {project_paths[i]}")
def fn_config(config):
    print(config._config)
def fn_add_project_path(config, *args):
    if len(args) == 0:
        try:
            input_path = input("Enter the path to add (pwd to add current path): ")
            handle_input_path(input_path, config.add_project_path)
        except ValueError as e:
            print(e)
    else:
        handle_path_args(*args, fn=config.add_project_path)

def fn_remove_project_path(config, *args):
    if len(args) == 0:
        try:
            input_path = input("Enter the path to remove (pwd to remove current path): ")
            handle_input_path(input_path, config.remove_project_path)
        except ValueError as e:
            print(e)
    else:
        handle_path_args(*args, fn=config.remove_project_path)
# 150
def fn_welcome():
    tim.print("[primary+3]Welcome to [!gradient(150) italic]LocalProjectManager!")
    tim.print("[primary+3]Type [bold firebrick]'exit'[/][primary+3] to exit the program")
    tim.print("[primary+3]Type [bold rosybrown]'config'[/][primary+3] to read the config file")
    tim.print("[primary+3]Type [bold royalblue]'add'[/][primary+3] to add a project to the list")
    tim.print("[primary+3]Type [bold sienna]'rm'[/][primary+3] to remove a project from the list")
    tim.print("[primary+3]Type [bold primary]'ls'[/][primary+3] to list the projects")
    tim.print("[primary+3]Type [bold darkslateblue]'help'[/][primary+3] to read again this message")

def fn_clear():
    print("\033c")

def open_project(num, config):
    try:
        num = int(num)
        project_paths = config.get_project_paths()
        if num < 1 or num > len(project_paths):
            print(f"Project number must be between 1 and {len(project_paths)}")
            return
        p = Process(target=os.system, args=(f"code {project_paths[num-1]}",))
        p.start()
        config._processes.append(p)
    except ValueError:
        print("Project number must be an integer")

def open_gui(config):
    # run example in a new process to avoid blocking the shell
    try:
        p = Process(target=os.system, args=("python3 ./widgets/example.py",))
        p.start()
        config._processes.append(p)
    except Exception as e:
        print(f"An error occurred: {e}")
        
def handle_path_args(*args, fn):
    for path in args:
        try:
            if path == "pwd" or path == '.':
                path = os.getcwd()
            elif path[0] != "/":
                if path[0] == "~":
                    path = os.path.expanduser(path)
                elif path[0] == ".":
                    path = os.path.join(os.getcwd(), path[1:])
                else:
                    path = os.path.join(os.getcwd(), path)
            fn(path)
        except ValueError as e:
            print(e)

def handle_input_path(path, fn):
    try:
        if path == "pwd":
            path = os.getcwd()
        if path[0] != "/":
            path = os.path.join(os.getcwd(), path)
        fn(path)
    except ValueError as e:
        print(e)