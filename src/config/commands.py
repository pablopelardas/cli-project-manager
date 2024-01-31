import os

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

def fn_welcome():
    print("Welcome to LocalProjectManager")
    print("Type 'exit' to exit the program.")
    print("Type 'config' to see the current configuration.")
    print("Type 'add' to add a new project path to the configuration.")
    print("Type 'rm' to remove a project path from the configuration.")
    print("Type 'ls' to list all the project paths.")
    print("Type 'help' to see this message again.")

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