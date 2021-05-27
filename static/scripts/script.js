
contador = 0
/*let campeoes = [
    {"id":0,"nome":"Corki","mana":true,"ad":1, "ap":0, "tank":0 ,"armor":0, "mr":0,
     "letalidade":0,"magicPenFlat":1,"armorPen":0,"magicPen":1}
    
]; */

let campeoes = [];


onload = () => {
    //const dadosCarregados = JSON.parse(localStorage.getItem('dados'));
    // if (dadosCarregados) dados = dadosCarregados;

    addCampeao("Corki",0,0,1,1,1,1,0,0,0,0.5,1,1,0,0,1,1,1,1,1,1,1);
    console.log(campeoes);

    // cria um objeto com as abas
    let tabs = document.querySelectorAll('.navBar .tab');

    const mostra = (elem) => {
        if (elem) {
        for (let i = 0; i < tabs.length; i++) tabs[i].classList.remove('active');
        elem.classList.add('active');
        }

        for (let i = 0; i < tabs.length; i++) {
        let comp = tabs[i].getAttribute('for');
        if (tabs[i].classList.contains('active'))
            document.querySelector('#' + comp).classList.remove('hidden');
        else document.querySelector('#' + comp).classList.add('hidden');
        }
    };

    for (let i = 0; i < tabs.length; i++)
        tabs[i].onclick = (e) => {
        mostra(e.target);
    };

    const inicio = document.getElementById("tab1");
    inicio.onclick = () => {
        ativa('tela1');
    };

    mostra();
    mostraCampeoes();
};

const ativa = (comp) => {
    let listaDeTelas = document.querySelectorAll('body > .component');
    listaDeTelas.forEach((c) => c.classList.add('hidden'));
    document.querySelector('#' + comp).classList.remove('hidden');
};

function atualizaSlider(){
    const inimigoAD = document.querySelector('#inimigoAD');
    const inimigoAP = document.querySelector('#inimigoAP');
    var dano = document.getElementById("dano").value;
    inimigoAD.innerHTML = 'AD='+dano;
    inimigoAP.innerHTML = 'AP='+(5-dano);
}

const mostraCampeoes = () => {
    const champs = document.querySelector('#listaCampeoes');
    champs.innerHTML = '';
    campeoes.forEach((i) => {
      // cria o elemento da lista
      let lista = document.createElement('li');
      let label = document.createElement('label');
      label.innerHTML = i.name;
      label.setAttribute('data-id', i.id);
      label.setAttribute('class', 'blockLabel'); // aumenta a area para clicar no label
      lista.appendChild(label);
  
      label.onclick = () => {
        ativa('tela2');
        // muda o nome da tela de build
        let tituloPagina = document.querySelector('#lblnome');
        //tituloCompra.innerHTML = i.name + " build";
        tituloPagina.innerHTML = "Preencha os dados sobre a partida";
        // chama o preenchimento de dados
        preencheFormCampeao(i.id);
        // mostra a tela de build
        ativa('tela2');        
      };
  
      champs.appendChild(lista);
  
    }); // fim do for
  }; // fim mostraCampeoes

  function preencheFormCampeao(id){
    var campeao = campeoes.filter((obj) => obj.id == id);
    campeao = campeao[0];
    document.getElementById("formNome").value = campeao.name;
    document.getElementById("formTank").value = campeao.tank;
    document.getElementById("formSuporte").value = campeao.suporte;

    document.getElementById("formAd").value = campeao.ad;
    document.getElementById("formAtksp").value = campeao.atksp;
    document.getElementById("formCrit").value = campeao.crit;
    document.getElementById("formLs").value = campeao.ls;
    document.getElementById("formLet").value = campeao.let;
    document.getElementById("formARMP").value = campeao.ARMP;
    
    document.getElementById("formAp").value = campeao.ap;
    document.getElementById("formAh").value = campeao.ah;
    document.getElementById("formMana").value = campeao.mana;
    document.getElementById("formManaRegen").value = campeao.manaRegen;
    document.getElementById("formHeal").value = campeao.heal;
    document.getElementById("formSp").value = campeao.sp;
    document.getElementById("formOv").value = campeao.ov;
    document.getElementById("formFmp").value = campeao.fmp;
    document.getElementById("formMp").value = campeao.mp;

    document.getElementById("formHealth").value = campeao.health;
    document.getElementById("formArmor").value = campeao.armor;
    document.getElementById("formMr").value = campeao.mr;
    document.getElementById("formHr").value = campeao.hr;
  }

function addCampeao(name, tank, suporte, ad, atksp, crit, ls, 
    let, ARMP, ap,ah, mana, manaRegen, heal, sp, ov, fmp, mp, health, armor, mr, hr){
    campeao = {
          "id": contador,
          "name": name,
          "tank": tank,
          "suporte" : suporte,
          //offensive stats
          "ad": ad,
          "atksp": atksp,
          "crit": crit,
          "ls": ls,
          "let": let,
          "ARMP": ARMP,
          //magical stats
          "ap": ap,
          "ah": ah,
          "mana": mana,
          "manaRegen": manaRegen,
          "heal": heal,
          "sp": sp,
          "ov": ov,
          "fmp": fmp,
          "mp": mp,
          //defensive stats
          "health": health,
          "armor": armor,
          "mr": mr,
          "hr": hr,
        }
    
    campeoes.push(campeao)
    contador += 1
}
