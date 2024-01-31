

from config import Config, initialize_commands
from shell import Shell

def main():
    try:
        # clear terminal
        print("\033c")
        # create a Config object
        config = Config()
        # create a Shell object
        shell = Shell(prompt="LPM >> ")
        # add commands to the shell
        initialize_commands(shell, config)
        # run the shell
        shell.welcome()
        shell.run()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)



# initialize the app
main()
