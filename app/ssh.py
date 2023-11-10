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
            
            # stdin, stdout, stderr = client.exec_command('uname -a')
            # output = stdout.read().decode('utf-8').strip()
            
            
            stdin, stdout, stderr = client.exec_command('cat /etc/os-release')  # Получить информацию о дистрибутиве
            output = stdout.read().decode('utf-8')
            
            
            stdin, stdout, stderr = client.exec_command('uname -r')
            build = stdout.read().decode('utf-8').strip()
            
            stdin, stdout, stderr = client.exec_command('uname -m')
            architecture = stdout.read().decode('utf-8').strip()
            
            
            client.close()
            
            os_info = parse_linux_info(output, build, architecture)
            return os_info
        except Exception as e:
            print(f"Ошибка SSH: {str(e)}")
            return None
            
def parse_linux_info(output, build, architecture):
    try:
        lines = output.split('\n')
        for line in lines:
            if line.startswith("VERSION="):
                version = line.split('=')[1].strip('"\n')
            if line.startswith("NAME="):
                os = line.split('=')[1].strip('"\n')
        
        # lines = output.split()
        # if len(lines) >= 4:
        #     os = lines[0]
        #     version = lines[2]
        #     build = lines[9]
            # architecture = lines[10]
        return {
            'os': os,
            'version': version,
            'build': build,
            'architecture': architecture
        }
    except:
        return {
            'os': None,
            'version': None,
            'build': None,
            'architecture': None
        }
            
    

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
