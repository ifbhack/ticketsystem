from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return 'wagyu beef'

app.run(host='0.0.0.0')
