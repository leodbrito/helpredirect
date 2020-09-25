// Função pra copiar o texto do elemento P de uma DIV para o clipboard
function copyDivText(x) {
    // Seleciona o elemento DIV cujo id é url_status
    var element = document.getElementById(x);
    // Torna o elemento editavel
    element.querySelector("p").contentEditable = "true"
    // Executa o foco no elemento
    element.querySelector("p").focus();
    // Seleciona tudo que está em focu 
    element.onfocus = document.execCommand('selectAll',false,null);
    // Copia o que estiver selecionado para a área de transferência
    document.execCommand("copy");
};

// Função pra copiar o texto da Textarea input para o clipboard
function copyText(x) {
    // captura o elemento input
    const inputText = document.querySelector(x);
    // seleciona todo o texto do elemento
    inputText.select();
    // Copia o que estiver selecionado para a área de transferência
    document.execCommand('copy');
};

// Função pra alterar o destino do metodo Post na pagina build_rules
function changePostTarget() {
    document.getElementById('source_url').setAttribute("id", "check_url");
    document.getElementById('dest_url').removeAttribute("required");
    document.getElementById('build_rules').action = "url_status";
}