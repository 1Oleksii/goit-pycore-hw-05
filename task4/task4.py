def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command"
    return inner


@input_error
def add_contact(args, contacts):
    if len(args) < 2:
        raise IndexError
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) < 2:
        raise IndexError
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    if not args:
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError
    return contacts[name]


@input_error
def show_all(args, contacts):
    if not contacts:
        return "No contacts available."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    
    commands = {
        "hello": lambda args: "How can I help you?",
        "add": lambda args: add_contact(args, contacts),
        "change": lambda args: change_contact(args, contacts),
        "phone": lambda args: show_phone(args, contacts),
        "all": lambda args: show_all(args, contacts)
    }

    while True:
        user_input = input("Enter a command: ")
        command_parts = user_input.strip().split()
        
        if not command_parts:
            continue
            
        command = command_parts[0].lower()
        args = command_parts[1:] if len(command_parts) > 1 else []
        
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command in commands:
            result = commands[command](args)
            print(result)
        else:
            print("Unknown command. Try again.")


if __name__ == "__main__":
    main()