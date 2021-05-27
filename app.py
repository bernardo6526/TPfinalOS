from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():
    return redirect("/home") #esse direct foi feito pois a route '/' nao consegue usar POST
if __name__ == '__main__':
   app.run(debug=True)

@app.route("/home", methods=["POST", "GET"])
def form_get():
    if request.method == "POST": #post feito no submit
	    user = request.form["dano"]
	    return redirect(url_for("user", usr=user))
    else: #é feito um get quando a página é carregada
	    return render_template("index.html")

@app.route("/dano<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"