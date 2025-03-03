// Elementos do DOM
const tamanhoSelect = document.getElementById('tamanho');
const gerarBtn = document.getElementById('gerar');
const resultadoTitulo = document.getElementById('resultado-titulo');
const totalInfo = document.getElementById('total-info');
const combinacoesContainer = document.getElementById('combinacoes');
const anteriorBtn = document.getElementById('anterior');
const proximoBtn = document.getElementById('proximo');
const paginaInfo = document.getElementById('pagina-info');

// Variáveis para controle da paginação
let todasCombinacoes = [];
let paginaAtual = 1;
const itensPorPagina = 30;

// Função para gerar combinações
function gerarCombinacoes(conjunto, tamanho) {
    const combinacoes = [];
    
    function combinar(inicio, atual) {
        if (atual.length === tamanho) {
            combinacoes.push([...atual]);
            return;
        }
        
        for (let i = inicio; i < conjunto.length; i++) {
            atual.push(conjunto[i]);
            combinar(i + 1, atual);
            atual.pop();
        }
    }
    
    combinar(0, []);
    return combinacoes;
}

// Função para mostrar combinações na página atual
function mostrarCombinacoes() {
    combinacoesContainer.innerHTML = '';
    
    const inicio = (paginaAtual - 1) * itensPorPagina;
    const fim = Math.min(inicio + itensPorPagina, todasCombinacoes.length);
    
    for (let i = inicio; i < fim; i++) {
        const combDiv = document.createElement('div');
        combDiv.classList.add('comb-item');
        combDiv.textContent = todasCombinacoes[i].join(',');
        combinacoesContainer.appendChild(combDiv);
    }
    
    // Atualizar informações de paginação
    paginaInfo.textContent = `Página ${paginaAtual} de ${Math.ceil(todasCombinacoes.length / itensPorPagina)}`;
    anteriorBtn.disabled = paginaAtual === 1;
    proximoBtn.disabled = paginaAtual === Math.ceil(todasCombinacoes.length / itensPorPagina);
}

// Event listeners
gerarBtn.addEventListener('click', () => {
    const tamanho = parseInt(tamanhoSelect.value);
    const digitos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    
    // Gerar todas as combinações
    todasCombinacoes = gerarCombinacoes(digitos, tamanho);
    
    // Resetar paginação
    paginaAtual = 1;
    
    // Atualizar interface
    resultadoTitulo.textContent = `Combinações com ${tamanho} dígito(s)`;
    totalInfo.textContent = `Total de combinações: ${todasCombinacoes.length}`;
    
    // Mostrar combinações
    mostrarCombinacoes();
});

anteriorBtn.addEventListener('click', () => {
    if (paginaAtual > 1) {
        paginaAtual--;
        mostrarCombinacoes();
    }
});

proximoBtn.addEventListener('click', () => {
    if (paginaAtual < Math.ceil(todasCombinacoes.length / itensPorPagina)) {
        paginaAtual++;
        mostrarCombinacoes();
    }
});