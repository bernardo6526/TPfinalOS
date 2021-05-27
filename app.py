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
	    dadosForm = request.form
	    return render_template("build.html",dados=dadosForm,build=itens)
    else: #é feito um get quando a página é carregada
	    return render_template("index.html")

# creating list       
itens = {
  0:{"nome": "Eco de Luden",
   "ap": 100,
   "mana": 100},
  1:{"nome": "Cajado do Vazio",
   "ap": 100,
   "mana": 0}
}
