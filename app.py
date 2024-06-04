from flask import Flask, render_template, request
from flask.json import jsonify
from flask_socketio import SocketIO

from pyCode import Status

app = Flask(__name__)
sock = SocketIO(app)

if __name__ == '__main__':
    sock.run(app)
    

@app.route("/fuel")
def fuel():
    return "<p>Fuel!</p>"


@app.route("/status")
def status():
    status = Status.update()
    return render_template('status.html', status = status)

@app.route("/updateStatus", methods = ['GET'])
def updateStatus():
    if(request.method == 'GET'):
        status = Status.update()
        return str(status)

@sock.on('updateRequest')
def updateSock(data):
    status = Status.update()
    resp = {'test': 'Prova'}
    sock.emit('update', str(status))
    print("Emesso update")
@sock.on('connect')
def hello():
    print("Ricevuta connessione da status")