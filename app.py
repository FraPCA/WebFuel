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
    return render_template('status.html')

@sock.on('updateRequest')
def updateSock(data):
    status = Status.update()
    sock.emit('update', status)
    print("Emesso update")
@sock.on('connect')
def hello():
    print("Ricevuta connessione da status")