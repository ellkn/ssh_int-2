from flask import Flask, request, render_template, redirect, flash, url_for
from ssh import SSHClient
from db import Database
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOPSECRETKEY'


# logging.basicConfig(filename="logs/info.log", filemode='a', level=logging.INFO, format='%(asctime)s | %(message)s')

@app.route('/', methods=['GET', 'POST'])
def ssh_index():
    if request.method == 'POST':
        ip = request.form.get('ip')
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not ip_pattern.match(ip):
            flash('Некорректный формат IP', category='error')
            return redirect(url_for('ssh_index'))
        username = request.form.get('username')
        password = request.form.get('password')
        ssh = SSHClient(ip, username, password)
        os_info = ssh.get_os_info()
        print(os_info)
        if os_info:
            db = Database()
            if db.add_history(ip, os_info.get('os', 'Не удалось определить'), os_info.get('version','Не удалось определить'), os_info.get('build','Не удалось определить'), os_info.get('architecture','Не удалось определить')):
                flash('Успешно добавлена запись', category='success')
                return redirect(url_for('ssh_result'))
        flash('Не удалось подключиться по ssh', category='error')
        return render_template('ssh_form.html')
    return render_template('ssh_form.html')


@app.route('/result')
def ssh_result():
    db = Database()
    return render_template('ssh_result.html', results = db.get_history())


if __name__ == '__main__':
    app.run(debug=True)