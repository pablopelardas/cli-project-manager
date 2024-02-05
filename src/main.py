

from config import Config, initialize_commands
from shell import Shell
import os
import pytermgui as ptg
import py_hot_reload

def main():
    config = Config()
    shell = Shell(prompt="LPM >> ")
    try:
        # clear terminal
        print("\033c")
        initialize_commands(shell, config)
        # run the shell
        shell.welcome()
        shell.run()
        # end of the program

    except KeyboardInterrupt:
        # check if there is any running subprocess and kill it        
        for process in config._processes:
            process.kill()

    except Exception as e:
        for process in config._processes:
            process.kill()
        print(f"An error occurred: {e}")


# initialize the app
# py_hot_reload.run_with_reloader(main)
main()