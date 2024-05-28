from flask import Flask

app = Flask(__name__)

# 直接 routes.py をインポート
from . import routes