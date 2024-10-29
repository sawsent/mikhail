from config.config import *
import os

def setup(is_mac_os=False):
    if is_mac_os:
        setup_mac_os()
    else:
        setup_windows()

    print(f"\nSuccessfully setup mikhail in {BASE_DIR}. Mikhail is ready for use!")

def setup_mac_os():
    os.system(f"chmod +x {BASE_DIR}/src/setup/mikhail-setup.sh") 
    os.system(f"{BASE_DIR}/src/setup/mikhail-setup.sh")


def setup_windows():
    os.system(f"call {BASE_DIR}\\src\\setup\\mikhail-setup.bat {BASE_DIR}")
