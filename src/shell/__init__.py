from config.commands import fn_welcome
class Shell():
    def __init__(self, prompt=""):
        self.prompt = prompt
        self.commands = {}
        self.running = True

    def add_command(self, name, func):
        self.commands[name] = Command(name, func)

    def welcome(self):
        fn_welcome()

    def run(self):
        while self.running:
            command = input(self.prompt)
            parts = command.split(" ")
            command = parts[0]
            args = parts[1:]
            if command in self.commands:
                self.commands[command].run(*args)
            else:
                print(f"Command '{command}' not found")
    

    def stop(self):
        self.running = False

class Command:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)