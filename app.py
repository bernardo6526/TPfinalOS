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
      
      #limpa as variaveis
	    global contador,itens,mochila,campeao
	    contador = 0
	    itens = {}
	    mochila = {}
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
  pesoAtributo = 5
  baseStat = 0.1

  #dados equipe inimiga
  champ['dano'] = float(champ['dano'])*pesoAtributo
  champ['tanks'] = float(champ['tanks'])*pesoAtributo

  #dados gerais campeao
  champ['tank'] = float(champ['tank'])*pesoAtributo
  champ['suporte'] = float(champ['suporte'])*pesoAtributo

  #offensive stats
  champ['ad'] = float(champ['ad'])*pesoAtributo
  champ['atksp'] = float(champ['atksp'])*pesoAtributo
  champ['crit'] = float(champ['crit'])*pesoAtributo
  champ['ls'] = float(champ['ls'])*pesoAtributo
  champ['let'] = float(champ['let'])*pesoAtributo
  champ['ARMP'] = float(champ['ARMP'])*pesoAtributo

  #magical stats
  champ['ap'] = float(champ['ap'])*pesoAtributo
  champ['ah'] = float(champ['ah'])*pesoAtributo
  champ['mana'] = float(champ['mana'])*pesoAtributo
  champ['manaRegen'] = float(champ['manaRegen'])*pesoAtributo
  champ['heal'] = float(champ['heal'])*pesoAtributo
  champ['sp'] = float(champ['sp'])*pesoAtributo
  champ['ov'] = float(champ['ov'])*pesoAtributo
  champ['fmp'] = float(champ['fmp'])*pesoAtributo
  champ['mp'] = float(champ['mp'])*pesoAtributo

  #defensive stats
  champ['health'] = float(champ['health'])*pesoAtributo
  champ['armor'] = float(champ['armor'])*pesoAtributo
  champ['mr'] = float(champ['mr'])*pesoAtributo
  champ['hr'] = float(champ['hr'])*pesoAtributo

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
  valor += (baseStat+champ['tank']*champ['health'])*itens[id]['health'] + (baseStat+champ['tank']*champ['armor'])*itens[id]['armor']*champ['dano']
  valor += (baseStat+champ['tank']*champ['mr'])*itens[id]['mr']*(5-champ['dano']) + (baseStat+champ['tank']*champ['hr'])*itens[id]['hr']

  itens[id]['valor'] = valor
  return valor

def carregaItens():

  #ms = 0
  addItem(
    #name,         valor, peso, mitico, bota
    "Eco de Luden",-3400,    1,      1,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     100,  0,   600,       0,   0,   0,  0,  0+20,  0,
    #health, armor, mr, hr
    0,          0,    0,0
  )

  #ms = 0
  addItem(
    #name,            valor, peso, mitico, bota
    "Cajado do Vazio",-2700,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     70,  0,   0,      0,       0,   0,  0,   0, 40,
    #health, armor, mr, hr
    0,          0,   0, 0
  )

  #ms = 0
  addItem(
    #name,                 valor, peso, mitico, bota
    "Ampulheta de Zhonyas",-2600,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
    65,  10,    0,         0,    0,  0,  0,   0,  0,
    #health, armor, mr, hr
    0,          45,   0, 0
  )

  #ms = 0
  addItem(
    #name,             valor, peso, mitico, bota
    "Gume do Infinito",-3400,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    70,     0,   30,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  0,   0,       0,       0,   0,  0,   0,  0,
    #health, armor, mr, hr
    0,          0,    0,0
  )

  #ms = 0
  addItem(
    #name,          valor, peso, mitico, bota
    "Mata-Cráquens",-3400,    1,      1,     0,
    #ad,atksp, crit, ls, let, ARMP
    65,  25+40,  20,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  0,   0,       0,       0,   0,  0,   0,  0,
    #health, armor, mr, hr
    0,          0,    0,0
  )

  #ms = 45
  addItem(
    #name,               valor, peso, mitico, bota
    "Passos de Mercúrio",-1100,    1,      0,     1,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  0,   0,       0,       0,   0,  0,   0,  0,
    #health, armor, mr, hr
    0,           0, 25, 0
  )

  #ms = 0
  addItem(
    #name,                valor, peso, mitico, bota
    "Grevas do Berserker",-1100,    1,      0,     1,
    #ad,atksp, crit, ls, let, ARMP
    0,     35,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  0,   0,       0,       0,   0,  0,   0,  0,
    #health, armor, mr, hr
    0,          0,    0, 0
  )

  #ms = 45
  addItem(
    #name,                      valor, peso, mitico, bota
    "Botas Ionianas da Lucidez",-1100,    1,      0,     1,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  20,    0,         0,    0,  0,  0,   0,  0,
    #health, armor, mr, hr
    0,           0,  0, 0
  )  

  #ms = 0
  addItem(
    #name,     valor, peso, mitico, bota
    "Redenção",-2300,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  15,   0,      100,     20, 20,  0,   0,  0,
    #health, armor, mr, hr
    200,        0,   0, 0
  )

  #ms = 0
  addItem(
    #name,                    valor, peso, mitico, bota
    "Manopla do Raio de Gelo",-2800,    1,      1,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,   0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  20,   0,          0,    0,  0,  0,   0,  0,
    #health, armor, mr, hr
    350+400,    25, 25, 0
  )

  #ms = 0
  addItem(
    #name,                 valor, peso, mitico, bota
    "Semblante Espiritual",-2900,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  10,    0,         0,    0,   0,  0,   0,  0,
    #health, armor, mr, hr
    450,         0, 40, 100
  )

  #ms = 0
  addItem(
    #name,                    valor, peso, mitico, bota
    "Hino Bélico de Shurelya",-2500,    1,      1,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     40, 20+20, 0,       100,    0,   0,  0,  0,  0,
    #health, armor, mr, hr
    200,         0,  0,  0
  )

  #ms = 0
  addItem(
    #name,               valor, peso, mitico, bota
    "Armadura de Warmog",-3000,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,  10,    0,         0,    0,   0,  0,  0,  0,
    #health, armor, mr, hr
    800,         0,  0, 200+5
  )

  #ms = 0
  addItem(
    #name,               valor, peso, mitico, bota
    "Sedenta por Sangue",-3400,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    55,     0,   20, 20,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,   0,    0,         0,    0,   0,  0,  0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                    valor, peso, mitico, bota
    "Crepúsculo de Draktharr",-3200,    1,      1,     0,
    #ad,atksp, crit, ls, let, ARMP
    60,     0,    0,  0,  18,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0, 20+20,  0,         0,    0,   0,  0,  0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                    valor, peso, mitico, bota
    "Espada do Rei Destruído",-3200,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    40,    25,    0, 10,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
     0,   0,    0,         0,    0,   0,  0,  0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,              valor, peso, mitico, bota
    "Cajado do Arcanjo",-3000,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
    65+15, 0, 500,         0,    0,   0,  0,  0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )
  
  #ms = 7%
  addItem(
    #name,             valor, peso, mitico, bota
    "Canhão Fumegante",-2500,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,     35,   20,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
    0,    0,    0,         0,    0,   0,  0,  0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  ) 

  #ms = 0
  addItem(
    #name,             valor, peso, mitico, bota
    "Turíbulo Ardente",-2300,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
    60,    0,    0,      100,   10, 10,  0,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 45
  addItem(
    #name,                  valor, peso, mitico, bota
    "Sapatos do Feiticeiro",-1100,    1,      0,     1,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
    0,    0,    0,         0,    0,  0,  0,  18,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                       valor, peso, mitico, bota
    "Regenerador de Pedra Lunar",-2500,    1,      1,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
    40,  20,    0,       100,    0,  0,  0,   0,  0,
    #health, armor, mr, hr
    200,         0,  0,  0
  )

  #ms = 7%
  addItem(
    #name,               valor, peso, mitico, bota
    "Dançarina Fantasma",-2600,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    20,    25,   20,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp, ov, fmp, mp
    0,    0,    0,         0,    0,  0,  0,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,       valor, peso, mitico, bota
    "Criafendas",-3200,    1,      1,     0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap   #ah, mana, manaRegen, heal, sp,   ov, fmp, mp
    80+32, 15,    0,         0,    0,  0,  8+8,   0,  0,
    #health, armor, mr, hr
    300,         0,  0,  0
  )

  #ms = 0
  addItem(
    #name,            valor, peso, mitico, bota
    "Sinal de Sterak",-3100,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    50,     0,    0,  0,   0,    0,
    #ap  #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,     0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    400,         0,  0,  0
  )

  #ms = 0
  addItem(
    #name,          valor, peso, mitico, bota
    "Hidra Raivosa",-3300,    1,      0,     0,
    #ad,atksp, crit, ls, let, ARMP
    65,     0,    0,  0,   0,    0,
    #ap  #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,    20,    0,         0,    0,  0,  10,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                        valor, peso, mitico, bota
    "Lembranças do Lorde Dominik",-3000,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    30,     0,   20,  0,   0,   35,
    #ap  #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,     0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                      valor, peso, mitico, bota
    "Cetro de Cristal de Rylai",-3000,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap  #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    90,     0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    350,         0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                      valor, peso, mitico, bota
    "Lâmina Fantasma de Youmuu",-3000,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    60,     0,    0,  0,  18,    0,
    #ap  #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,     0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                      valor, peso, mitico, bota
    "Capuz da Morte de Rabadon",-3600,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap    #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    120+42,  0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,    valor, peso, mitico, bota
    "Eclipse",-3200,    1,      1,    0,
    #ad,atksp, crit, ls, let, ARMP
    55,     0,    0,  0,  18,  0+16,
    #ap #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,    0,    0,         0,    0,  0,   8,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                 valor, peso, mitico, bota
    "Colhedor de Essência",-2800,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    45,     0,   20,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,   20,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 7%
  addItem(
    #name,              valor, peso, mitico, bota
    "Furacão de Runaan",-2600,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    0,     45,   20,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,    0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                 valor, peso, mitico, bota
    "Armadura de Espinhos",-2700,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,    0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    350,        60,  0,  0
  )
  
  #ms = 0
  addItem(
    #name,                 valor, peso, mitico, bota
    "Presságio de Randuin",-2700,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    0,      0,    0,  0,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,   10,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    250,        80,  0,  0
  )
  
  #ms = 0
  addItem(
    #name,       valor, peso, mitico, bota
    "A Coletora",-3000,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    55,     0,   20,  0,  12,    0,
    #ap #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,    0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 20
  addItem(
    #name,            valor, peso, mitico, bota
    "Limite da Razão",-3100,    1,      0,    0,
    #ad,atksp, crit, ls, let, ARMP
    40,    40,    0, 12,   0,    0,
    #ap #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,    0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    0,           0, 50,  0
  )

  #ms = 0
  addItem(
    #name,               valor, peso, mitico, bota
    "Lâmina Sanguinária",-3000,    1,      0,    0,
    #ad,atksp, crit,  ls,   let, ARMP
    50,    50,    0,   0,  10+8,    0,
    #ap #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,    0,    0,         0,    0,  0,  12,   0,  0,
    #health, armor, mr, hr
    0,           0,  0,  0
  )

  #ms = 0
  addItem(
    #name,                valor, peso, mitico, bota
    "Arco-escudo Imortal",-3400,    1,      1,    0,
    #ad,atksp, crit,  ls,   let, ARMP
    55+20, 20,   20,  10,     0,    0,
    #ap #ah, mana, manaRegen, heal, sp,  ov, fmp, mp
    0,    0,    0,         0,    0,  0,   0,   0,  0,
    #health, armor, mr, hr
    0+200,       0,  0,  0
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

  imprimir("DEBUG FOR----------")
  for i in qtdItens:
    string = str(itens[i]['valor'])+"/"+str(x[i].x)
    imprimir("________")
    imprimir(string)
    imprimir("________")
  imprimir("DEBUG FOR----------")  

  selected = [i for i in qtdItens if x[i].x == 1.0]
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






   




