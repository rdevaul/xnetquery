from core.state_machine import XNETStateMachine

def run_terminal_interface(state_machine: XNETStateMachine):
    print("Welcome to XNET Converse. Type '/help' for commands or ask about XNET.")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = state_machine.process(user_input)
        print(response)
