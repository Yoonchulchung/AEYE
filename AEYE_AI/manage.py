from flask import Flask
from AEYE import create_aeye_opticnet_framework
import click

framework = create_aeye_opticnet_framework()

if __name__ == "__main__":
    framework.run(host='0.0.0.0', port=2000, debug=True)