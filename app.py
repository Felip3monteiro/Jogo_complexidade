from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('index.html')

@app.route('/start-game')
def start_game():
    # Use o interpretador Python para executar o script do jogo
    os.system('main.py')
    return "Jogo iniciado"

if __name__ == '__main__':
    app.run(debug=True)