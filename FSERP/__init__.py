import os,sys
DIR = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__),'trytond')))#Replace with your path
print DIR, "outside"
if os.path.isdir(DIR):
    sys.path.insert(0, DIR)
    print DIR

print sys.path
import trytond
