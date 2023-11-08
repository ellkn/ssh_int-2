from flask import Flask, request, render_template
import ssh
import logging

# ИНИЦИАЛИЗАЦИЯ ФРЕЙМВОРКА ФЛАСК
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOPSECRETKEY'

# # ЛОГИРОВАНИЕ В СИСТЕМЕ
# logging.basicConfig(filename="logs/info.log", filemode='a', level=logging.INFO, format='%(asctime)s | %(message)s')


# Главная страница с формой для SSH
@app.route('/', methods=['GET', 'POST'])
def ssh_index():
    if request.method == 'POST':
        host = request.form.get('host')
        username = request.form.get('username')
        password = request.form.get('password')
        command = request.form.get('command')
        result = ssh.execute_ssh_command(host, username, password, command)
        return render_template('ssh_result.html', result=result)
    return render_template('ssh_form.html')

@app.route('/result', methods=['GET', 'POST'])
def ssh_result():
    pass




if __name__ == '__main__':
    app.run(debug=True)