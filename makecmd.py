import os


def generate_command():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(script_dir, '.venv', 'Scripts', 'python.exe')
    main_script_path = os.path.join(script_dir, 'main.py')

    command = f"{venv_path} {main_script_path}\nexit"
    return command


def main():
    command = generate_command()

    # Path to the cmd.bat file
    bat_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cmd.bat')

    # Write the command to cmd.bat
    with open(bat_file_path, 'w') as bat_file:
        bat_file.write(command)

    print(f"Command written to {bat_file_path}")


if __name__ == "__main__":
    main()