# hoffman_test_runner.py
import paramiko
import getpass

def run_hoffman_command():
    hostname = "hoffman2.idre.ucla.edu"
    username = input("Enter your Hoffman2 username: ")
    password = getpass.getpass("Enter your Hoffman2 password (leave blank if using SSH key): ")

    command = input("Enter the command to run on Hoffman2: ")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if password:
            client.connect(hostname, username=username, password=password)
        else:
            client.connect(hostname, username=username)

        stdin, stdout, stderr = client.exec_command(command)
        print("Output:")
        print(stdout.read().decode())
        print("Errors:")
        print(stderr.read().decode())

    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        client.close()
if __name__ == "__main__":
    run_hoffman_command()
