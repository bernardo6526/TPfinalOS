from flask import Flask, redirect, url_for, render_template, request
from mip import Model, xsum, maximize, BINARY
import sys


contador = 0
itens = {}
mochila = {}
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
	    return render_template("build.html",campeao=campeao,build=mochila)
    else: #é feito um get quando a página é carregada
	    return render_template("index.html")


#Offensive stats include attack damage(AD), attack speed(AS), critical strike chance(Crit), life steal(LS), 
#lethality(Let) and armorPen(ARMP).

#Magical stats include ability power(AP), 
#ability haste(AH), mana, mana regeneration(manaRegen), heal , shield power(SP), omnivamp(OV), 
# and flatMagicPen(FMP) and magicPen(MP).

#Defensive stats include health, armor, magic resistance(MR), and health regeneration(HR).

def imprimir(msg):
  print(msg,file=sys.stderr)

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

def calculoValor(id):
  valor = itens[i]['valor']
  valor+= 300
  itens[i]['valor'] = valor
  return valor

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

#rodar codigo de otimizacao e preencher vetor build com os melhores itens escolhidos

# exemplo
#valor = [10, 9, 8, 7, 6, 5,4]
#peso = [1, 1, 1, 1, 1, 1,1]
#mitico = [1, 1, 0, 0, 0, 0,0]
#bota = [0, 0, 1, 1, 0, 0,0]

valor = []
peso = []
mitico = []
bota = []

#preenche os vetores
for i in range(len(itens)):
  valorCalculado = calculoValor(i)
  valor.append(valorCalculado)
  peso.append(itens[i]['peso'])
  mitico.append(itens[i]['mitico'])
  bota.append(itens[i]['bota'])

capacidade = 6
qtdItens = range(len(peso))

m = Model()

# variáveis de decisao (vetor X)
# binary garante que nao pode levar itens repetidos 
x = [m.add_var(var_type=BINARY) for i in qtdItens]

# maximiza o ganho
m.objective = maximize(xsum(valor[i] * x[i] for i in qtdItens))

#nao pode ultrapassar 6 itens
m += xsum(peso[i] * x[i] for i in qtdItens) <= capacidade

#nao pode levar mais de 1 item do tipo mitico
m += xsum(mitico[i] * x[i] for i in qtdItens) <= 1

#nao pode levar mais de 1 item do tipo bota
m += xsum(bota[i] * x[i] for i in qtdItens) <= 1


m.optimize()

selected = [i for i in qtdItens if x[i].x >= 0.99]
imprimir("selected items: {}".format(selected))

for j in range(len(selected)):
  idEscolhido = selected[j]
  itemLevado = {
    idEscolhido:{
      "name": itens[idEscolhido]['name'],      
    }
  }
  mochila.update(itemLevado)


imprimir(mochila)





   




