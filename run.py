import json
import time
import sys
import subprocess
import random

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_banners(filename):
    with open(filename, 'r') as file:
        content = file.read()
    banners = content.split('----\n')
    return banners

def loading_animation():
    print(Colors.OKGREEN + "Loading ", end="")
    for _ in range(3):
        for frame in ['.', '..', '...']:
            print(frame, end="\r")
            time.sleep(0.5)
    print("Done!   " + Colors.ENDC)

def typing_animation(text, speed=0.05):
    try:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
    except KeyboardInterrupt:
        print("\nOperation interrupted.")
        raise

def execute_command(command, inputs=[]):
    try:
        for input_detail in inputs:
            user_input = input(input_detail["prompt"])
            command = command.replace(input_detail["placeholder"], user_input)
        loading_animation()
        typing_animation(f"Executing: {command}\n")
        subprocess.run(command, shell=True, check=True)
        typing_animation("Command executed successfully.\n")
    except subprocess.CalledProcessError as e:
        typing_animation(f"An error occurred: {e}\n", speed=0.02)


def load_menu():
    with open('toolkits.json', 'r') as file:
        return json.load(file)

def print_menu(options):
    for option in options:
        print(Colors.OKBLUE + f"{option['key']}. {option['description']}" + Colors.ENDC)

def display_banner():
    # banner_text = """
    # """
    # print(Colors.OKBLUE + banner_text + Colors.ENDC)

    banners = load_banners('banners.txt')
    selected_banner = random.choice(banners).strip()
    print(Colors.OKBLUE + selected_banner + Colors.ENDC)

    typing_animation("-----------------------------------\n", speed=0.03)
    typing_animation(Colors.HEADER + "  Toolkits ♡ by 1n - retasin.com  \n" + Colors.ENDC)
    typing_animation("-----------------------------------\n" + Colors.ENDC)

def main_menu():
    try:
        subprocess.run("clear", shell=True, check=True)
        menu_data = load_menu()
        display_banner()

        current_menu = menu_data['options']
        menu_stack = []

        while True:
            print("\n")
            print_menu(current_menu)
            print(Colors.WARNING + "\n0. Return to Previous Menu" if menu_stack else "\n0. Exit" + Colors.ENDC)
            choice = input("\nEnter your choice: ")

            if choice == '0':
                if menu_stack:
                    current_menu = menu_stack.pop()
                else:
                    subprocess.run("clear", shell=True, check=True)
                    # print("Exiting the program.")
                    print(Colors.WARNING + "\nThanks for using RTS-KIT, dont forget give star on our github!\n" + Colors.ENDC)
                    break
            else:
                selected_option = next((item for item in current_menu if item['key'] == choice), None)
                if selected_option:
                    if 'sub_menu' in selected_option:
                        menu_stack.append(current_menu)
                        current_menu = selected_option['sub_menu']
                    elif 'function' in selected_option:
                        execute_command(
                            selected_option['function'],
                            inputs=selected_option.get("inputs", [])
                        )
                else:
                    typing_animation(Colors.FAIL + "Invalid choice, please try again.\n" + Colors.ENDC)


    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting program.")
        sys.exit(0)

if __name__ == "__main__":
    main_menu()
