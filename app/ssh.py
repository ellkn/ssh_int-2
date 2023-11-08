import paramiko

def execute_ssh_command(host, username, password, command):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read()
        ssh_client.close()
        return output.decode('utf-8')
    except Exception as e:
        return str(e)
