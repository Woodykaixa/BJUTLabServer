import os
import re
from signal import SIGKILL
from time import sleep


out = os.popen('pstree -ap|grep gunicorn').read().split('\n')[0]
pid = re.findall(r'\d+', out)[0]
os.kill(int(pid), SIGKILL)
os.system('git clone https://github.com/Woodykaixa/BJUTLabServer.git')
sleep(2)
os.system('cd /usr/BJUTLabServer && source venv/bin/activate && gunicorn "BJUTLabServer:create_app()"')
