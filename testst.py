from subprocess import call
import os

base = os.getcwd()
call(['python main.py --p=30001'], cwd=base+'/image-model-test-assistant',shell=True)


