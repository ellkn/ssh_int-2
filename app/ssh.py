import paramiko

class SSHClient:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password


    def get_os_info(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(self.ip, username=self.username, password=self.password)
            
            stdin, stdout, stderr = client.exec_command('uname -a')
            output = stdout.read().decode('utf-8').strip()
            
            client.close()
            
            os_info = parse_linux_info(output)
            return os_info
        except Exception as e:
            print(f"Ошибка SSH: {str(e)}")
            return None
            
def parse_linux_info(output):
    
    lines = output.split()
    if len(lines) >= 4:
        os = lines[0]
        version = lines[2]
        build = lines[3]
        architecture = lines[10]
        return {
            'os': os,
            'version': version,
            'build': build,
            'architecture': architecture
        }
    else:
        return None
            
    

# def execute_ssh_command(host, username, password, command):
#     try:
#         ssh_client = paramiko.SSHClient()
#         ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh_client.connect(host, username=username, password=password)
#         stdin, stdout, stderr = ssh_client.exec_command(command)
#         output = stdout.read()
#         ssh_client.close()
#         return output.decode('utf-8')
#     except Exception as e:
#         return str(e)
