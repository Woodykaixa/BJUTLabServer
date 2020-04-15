import os
from signal import SIGKILL
from time import sleep
import re
import multiprocessing


def reboot():
    ps_line = os.popen('ps -aux|grep gunicorn|awk \'NR==1 {print $2}\'').read()
    pid = re.findall(r'\d+', ps_line)[0]
    print('Kill gunicorn. PID: {}'.format(pid))
    os.kill(int(pid), SIGKILL)
    sleep(15)
    os.system('gunicorn \'BJUTLabServer:create_app()\'')


print('Rebooting gunicorn.')
p = multiprocessing.Process(target=reboot)
p.start()
sleep(20)
p.terminate()
os.kill(os.getpid(), SIGKILL)
