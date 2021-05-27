from flask import Flask, redirect, url_for, render_template, request

contador = 0
itens = {}
campeao = []


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
	    campeao = request.form
	    return render_template("build.html",campeao=campeao,build=itens)
    else: #é feito um get quando a página é carregada
	    return render_template("index.html")


#Offensive stats include attack damage(AD), attack speed(AS), critical strike chance(Crit), life steal(LS), 
#lethality(Let) and armorPen(ARMP).

#Magical stats include ability power(AP), 
#ability haste(AH), mana, mana regeneration(manaRegen), heal , shield power(SP), omnivamp(OV), 
# and flatMagicPen(FMP) and magicPen(MP).

#Defensive stats include health, armor, magic resistance(MR), and health regeneration(HR).

def addItem(name, valor, peso, mitico, bota, ad, atksp, crit, ls, let, ARMP, ah, mana, manaRegen, heal, sp, ov, fmp, mp, health, armor, mr, hr):
  global contador
  item = {
      contador:{
        #dados do problema
        "name": name,
        "valor": valor,
        "peso" : peso,
        "mitico": mitico,
        "bota": bota,
        #offensive stats
        "ad": ad,
        "as": atksp,
        "crit": crit,
        "ls": ls,
        "let": let,
        "ARMP": ARMP,
        #magical stats
        "ah": ah,
        "mana": mana,
        "manaRegen": manaRegen,
        "heal": heal,
        "sp": sp,
        "ov": ov,
        "fmp": fmp,
        "mp": mp,
        #defensive stats
        "health": health,
        "armor": armor,
        "mr": mr,
        "hr": hr,
      }
  }
  itens.update(item)
  contador += 1

addItem(
  #name,         valor, peso, mitico, bota
  "Eco de Luden",-200,    1,    0,      0,
  #ad,atksp, crit, ls, let, ARMP
  0,  0,      0,    0,  0,  0,
  #ah, mana, manaRegen, heal, sp, ov, fmp, mp
  0,   0,       0,       0,   0,  0,   0,  0,
  #health, armor, mr, hr
  0,          0,    0,0
)

addItem(
  #name,         valor, peso, mitico, bota
  "Gume do Infinito",-200,    1,    0,      0,
  #ad,atksp, crit, ls, let, ARMP
  0,  0,      0,    0,  0,  0,
  #ah, mana, manaRegen, heal, sp, ov, fmp, mp
  0,   0,       0,       0,   0,  0,   0,  0,
  #health, armor, mr, hr
  0,          0,    0,0
)

#calcular valor para cada item
#valor = 0
#for item in itens:
  #valor = item['ad']*

#rodar codigo de otimizacao e preencher vetor build com os melhores itens escolhidos

import amplpy
from amplpy import AMPL, Environment
import os

os.chdir(os.path.dirname(__file__) or os.curdir)
try:
    # Create an AMPL instance
    ampl = AMPL(
            Environment('.\env\Lib\site-packages\amplpy'))

    """
        # If the AMPL installation directory is not in the system search path:
        from amplpy import Environment
        ampl = AMPL(
            Environment('full path to the AMPL installation directory'))
        """

    if argc > 1:
        ampl.setOption("solver", argv[1])

    # Read the model and data files.
    ampl.read('models/mochilalol.mod')
    ampl.readData('models/mochilalol.dat')

    # Solve
    ampl.solve()

    # Get objective entity by AMPL name
    totalcost = ampl.getObjective("Total_Cost")
    objective = totalcost.value()

    # Resolve and display objective
    ampl.solve()
    print("New objective value:", totalcost.value())

    # Get the values of the variable Buy in a dataframe object
    x = ampl.getVariable("X")
    df = x.getValues()
except Exception as e:
    print(e)
    raise



   




