from config.config import *
import os

def setup(is_mac_os=False):
    if is_mac_os:
        setup_mac_os()
    else:
        setup_windows()

def setup_mac_os():
    os.system(f"chmod +x {BASE_DIR}/src/setup/mikhail-setup.sh") 
    os.system(f"{BASE_DIR}/src/setup/mikhail-setup.sh")


def setup_windows():
    print(BASE_DIR)
    os.system(f"call {BASE_DIR}\\src\\setup\\mikhail-setup.bat {BASE_DIR}")
