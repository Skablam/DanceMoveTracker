from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('/welcome.html')

@app.route("/movelist")
def movelist():
    return render_template('/move_list.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")