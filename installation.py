import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
print("INSTALLED PACKEGES: 1/4")
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
print("INSTALLED PACKEGES: 2/4")
subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome"])
print("INSTALLED PACKEGES: 3/4")
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
print("INSTALLED PACKEGES: 4/4")
