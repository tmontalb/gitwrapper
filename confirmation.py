def ask_confirmation(message):

    answer = input(f"{message} [y/N]: ")

    return answer.lower() == "y"