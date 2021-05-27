
let campeoes = [
    {"id":0,"nome":"Corki","mana":true,"ad":1, "ap":0, "tank":0 ,"armor":0, "mr":0,
     "letalidade":0,"magicPenFlat":1,"armorPen":0,"magicPen":1}
    
];


onload = () => {
    const dadosCarregados = JSON.parse(localStorage.getItem('dados'));
    if (dadosCarregados) dados = dadosCarregados;

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
      label.innerHTML = i.nome;
      label.setAttribute('data-id', i.id);
      label.setAttribute('class', 'blockLabel'); // aumenta a area para clicar no label
      lista.appendChild(label);
  
      label.onclick = () => {
        ativa('tela2');
        // muda o nome da tela de build
        let tituloCompra = document.querySelector('#lblnome');
        tituloCompra.innerHTML = i.nome + " build";
        tituloCompra.innerHTML = "Preencha os dados sobre a partida";
        // mostra a tela de build
        ativa('tela2');
        // chama o preenchimento de dados
        preencheFormCampeao(i.id);
      };
  
      champs.appendChild(lista);
  
    }); // fim do for
  }; // fim mostraCampeoes

  function preencheFormCampeao(id){
    var campeao = campeoes.filter((obj) => obj.id == id);
    campeao = campeao[0];
    document.getElementById("formNome").value = campeao.nome;
    document.getElementById("formMana").value = campeao.mana;
    document.getElementById("formAd").value = campeao.ad;
    document.getElementById("formAp").value = campeao.ap;
    document.getElementById("formTank").value = campeao.tank;
    document.getElementById("formArmor").value = campeao.armor;
    document.getElementById("formMr").value = campeao.mr;
    document.getElementById("formLetalidade").value = campeao.letalidade;
    document.getElementById("formMagicPenFlat").value = campeao.magicPenFlat;
    document.getElementById("formArmorPen").value = campeao.armorPen;
    document.getElementById("formMagicPen").value = campeao.magicPen;
  }
