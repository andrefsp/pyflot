"""
pyflot demo app based on Flask
"""

import flot
from flask import Flask, render_template

class Fx(flot.Series):
    data = [(1, 3), (2, 2), (3, 5), (4, 4)]

class MyGraph(flot.Graph):
    fx = Fx()

app = Flask(__name__)

@app.route("/")
def root():
    my_graph = MyGraph()
    return render_template('index.html', my_graph=my_graph)

if __name__ == "__main__":
    app.run(debug=True)

