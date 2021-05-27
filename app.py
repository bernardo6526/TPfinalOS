from flask import Flask, redirect, url_for, render_template, request
from mip import Model, xsum, maximize, BINARY
import sys


contador = 0
itens = {}
mochila = {}
campeao = {}


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
	    global campeao
	    campeao = request.form
	    imprimir("----------------\n")
	    imprimir(campeao);
	    imprimir("----------------\n")
	    otimizacao()
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

def addItem(name, valor, peso, mitico, bota, ad, atksp, crit, ls, let, ARMP, ap, ah, mana, manaRegen, heal, sp, ov, fmp, mp, health, armor, mr, hr):
  global contador
  item = {
      contador:{
        #dados do problema
        "name": name,
        "valor": float(valor),
        "peso" : float(peso),
        "mitico": float(mitico),
        "bota": float(bota),
        #offensive stats
        "ad": float(ad),
        "atksp": float(atksp),
        "crit": float(crit),
        "ls": float(ls),
        "let": float(let),
        "ARMP": float(ARMP),
        #magical stats
        "ap": float(ap),
        "ah": float(ah),
        "mana": float(mana),
        "manaRegen": float(manaRegen),
        "heal": float(heal),
        "sp": float(sp),
        "ov": float(ov),
        "fmp": float(fmp),
        "mp": float(mp),
        #defensive stats
        "health": float(health),
        "armor": float(armor),
        "mr": float(mr),
        "hr": float(hr),
      }
  }
  itens.update(item)
  contador += 1

def calculoValor(id):
  id = int(id)
  valor = float(itens[id]['valor']/10)
  global campeao

  champ = campeao.copy()

  #dados equipe inimiga
  champ['dano'] = float(champ['dano'])
  champ['tanks'] = float(champ['tanks'])

  #dados gerais campeao
  champ['tank'] = float(champ['tank'])
  champ['suporte'] = float(champ['suporte'])

  #offensive stats
  champ['ad'] = float(champ['ad'])
  champ['atksp'] = float(champ['atksp'])
  champ['crit'] = float(champ['crit'])
  champ['ls'] = float(champ['ls'])
  champ['let'] = float(champ['let'])
  champ['ARMP'] = float(champ['ARMP'])

  #magical stats
  champ['ap'] = float(champ['ap'])
  champ['ah'] = float(champ['ah'])
  champ['mana'] = float(champ['mana'])
  champ['manaRegen'] = float(champ['manaRegen'])
  champ['heal'] = float(champ['heal'])
  champ['sp'] = float(champ['sp'])
  champ['ov'] = float(champ['ov'])
  champ['fmp'] = float(champ['fmp'])
  champ['mp'] = float(champ['mp'])

  #defensive stats
  champ['health'] = float(champ['health'])
  champ['armor'] = float(champ['armor'])
  champ['mr'] = float(champ['mr'])
  champ['hr'] = float(champ['hr'])

  #tank suporte,ad, atksp, crit, ls, let, ARMP, ap, ah, 
  #mana, manaRegen, heal, sp, ov, fmp, mp, health, armor, mr, hr

  imprimir("-----DEBUG-------\n")
  imprimir(campeao['ad'])
  imprimir("-----DEBUG-------\n")
  
  #offensive stats
  valor += champ['ad']*itens[id]['ad'] + champ['atksp']*itens[id]['atksp']
  valor += champ['crit']*itens[id]['crit'] + champ['ls']*(itens)[id]['ls']
  valor += champ['let']*itens[id]['let']*(5-champ['tanks']) + champ['ARMP']*itens[id]['ARMP']*champ['tanks']

  #magical stats
  valor += champ['ap']*itens[id]['ap'] + champ['ah']*itens[id]['ah'] + champ['mana']*itens[id]['mana']
  valor += champ['manaRegen']*itens[id]['manaRegen'] + champ['heal']*itens[id]['heal']*champ['suporte']
  valor += champ['sp']*itens[id]['sp']*champ['suporte'] + champ['ov']*itens[id]['ov']
  valor += champ['fmp']*itens[id]['fmp']*(5-champ['tanks']) + champ['mp']*itens[id]['mp']*champ['tanks']

  #defensive stats
  valor += (1+champ['tank'])*itens[id]['health'] + (1+champ['tank'])*champ['armor']*itens[id]['armor']*champ['dano']
  valor += (1+champ['tank'])*itens[id]['mr']*(5-champ['dano']) + (1+champ['tank'])*itens[id]['hr']

  itens[id]['valor'] = valor
  return valor

def carregaItens():
  addItem(
    #name,         valor, peso, mitico, bota
    "Eco de Luden",-200,    1,    0,      0,
    #ad,atksp, crit, ls, let, ARMP
    0,  0,      0,    0,  0,  0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     100,  0,   600,       0,       0,   0,  0,   0,  0,
    #health, armor, mr, hr
    0,          0,    0,0
  )

  addItem(
    #name,         valor, peso, mitico, bota
    "Gume do Infinito",-200,    1,    0,      0,
    #ad,atksp, crit, ls, let, ARMP
    70,  0,      30,    0,  0,  0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  0,   0,       0,       0,   0,  0,   0,  0,
    #health, armor, mr, hr
    0,          0,    0,0
  )

def otimizacao():
  carregaItens()

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
    idEscolhido = int(selected[j])
    itemLevado = {
      idEscolhido:{
        "name": itens[idEscolhido]['name'],      
      }
    }
    mochila.update(itemLevado)


  imprimir(mochila)






   




