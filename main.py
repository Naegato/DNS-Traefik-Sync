import os
import paramiko
import ctypes
import sys
from dotenv import load_dotenv
import socket

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        raise False


def find_python_sync_tags(hosts_file, hosts_delimiter):
    start_index = -1
    end_index = -1

    with open(hosts_file, 'r') as hostsFile:
        lines = hostsFile.readlines()

        for i, line in enumerate(lines):
            if line.strip() == hosts_delimiter and start_index == -1:
                start_index = i
            elif line.strip() == hosts_delimiter:
                end_index = i

    return start_index, end_index, lines


def programs(ip_address, username, port, working_directory, url_regex, hosts_file, hosts_delimiter):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address, username=username, port=port)
    print("Successfully connected to", ip_address)

    # find [working_directory] -name "docker-compose.yaml"
    # grep -Po '^(?!#).*\.server\.home' [working_directory] | awk -F'`' '{print $2}'

    print("Searching for docker-compose.yaml files in", working_directory)
    stdin, stdout, stderr = ssh_client.exec_command(f'find {working_directory} -name "docker-compose.yaml"')

    urlArr = []

    print("Extracting URLs from docker-compose.yaml files")
    for line in stdout:
        if not isinstance(line, str):
            line = line.decode('utf-8')
        command = f"grep -Po '{url_regex}' " + line.strip() + " | awk -F'`' '{print $2}'"
        stdin2, stdout2, stderr2 = ssh_client.exec_command(command)
        for url in stdout2:
            urlArr.append(url.strip())

    if len(urlArr) > 0:
        start_index, end_index, lines = find_python_sync_tags(hosts_file, hosts_delimiter)

        if start_index == -1:
            print("Python Sync tags not found in hosts file.")
            with open(hosts_file, 'a') as hostsFile:
                hostsFile.write(f"\n\n{hosts_delimiter}\n{hosts_delimiter}")
                print("Added Python Sync tags to hosts file.")
            start_index, end_index, lines = find_python_sync_tags(hosts_file, hosts_delimiter)

        print(f"Found Python Sync tags between lines {start_index} and {end_index} in hosts file.")
        if start_index != -1 and end_index != -1:
            lines = lines[:start_index + 1] + lines[end_index:]

        if start_index != -1 and end_index != -1:
            with open(hosts_file, 'w') as hostsFile:
                hostsFile.writelines(
                    lines[:start_index + 1] + [ip_address + '\t\t' + url + '\n' for url in urlArr] + lines[
                                                                                                     start_index + 1:])
                print(f"Added {len(urlArr)} URLs between Python Sync tags in hosts file.")

    ssh_client.close()


def main():
    dir_name = os.path.dirname(os.path.realpath(__file__))

    load_dotenv(dotenv_path=f"{dir_name}/.env.local")
    load_dotenv(dotenv_path=f"{dir_name}/.env")

    username = os.getenv("USERNAME")
    ssh_port = os.getenv("SSH_PORT")
    working_directory = os.getenv("WORK_DIR")
    url_regex = os.getenv("URL_REGEX")
    hosts_file = os.getenv("HOSTS_FILE")
    hosts_delimiter = os.getenv("HOSTS_DELIMITER")
    domain = os.getenv("DOMAIN")

    ip_address = os.getenv("IP_ADDRESS")

    if domain:
        ip_address = socket.gethostbyname(domain);

    if (not ip_address or not username or not ssh_port or not working_directory
            or not url_regex or not hosts_file or not hosts_delimiter):
        print("Please provide all the required environment variables in .env.local or .env file.")
        os.system('pause')
        sys.exit(-1)

    if not is_admin():
        # Re-run the program with admin rights, don't use __file__ since py2exe won't know about it
        # Use sys.argv[0] as script path and sys.argv[1:] as arguments,
        # join them as lpstr, quoting each parameter or spaces will divide parameters
        lp_parameters = ""
        # Literally quote all parameters which get unquoted when passed to python
        for i, item in enumerate(sys.argv[0:]):
            lp_parameters += '"' + item + '" '
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, lp_parameters, None, 1)
    else:
        programs(ip_address, username, int(ssh_port), working_directory, url_regex, hosts_file, hosts_delimiter)
        os.system('pause')
        sys.exit()


if __name__ == "__main__":
    main()
