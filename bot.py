# constants
EXAMPLE_COMMAND = "do"

class Bot(str):

    def handle_command(self, command):
        """
            Executes bot command if the command is known
        """
        # Default response is help text for the user
        default_response = "Я пока знаю только одну команду. Попробуйте *{}*.".format(EXAMPLE_COMMAND)

        # Finds and executes the given command, filling in response
        response = None
        # This is where you start to implement more commands!
        if command.startswith(EXAMPLE_COMMAND):
            response = "Привет мир" + chr(0x1f596)

        return response or default_response
