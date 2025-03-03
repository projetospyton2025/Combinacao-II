from flask import Flask, render_template, jsonify, request
import os
import math
from itertools import combinations

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tabela_combinacoes')
def tabela_combinacoes():
    return render_template('tabela_combinacoes.html')

@app.route('/api/combinacoes/<int:tamanho>')
def get_combinacoes(tamanho):
    # Verificar se o tamanho está dentro dos limites permitidos
    if tamanho < 1 or tamanho > 10:
        return jsonify({"error": "Tamanho inválido. Deve ser entre 1 e 10."}), 400
    
    # Gerar todas as combinações possíveis
    digitos = list(range(10))  # dígitos de 0 a 9
    todas_combinacoes = list(combinations(digitos, tamanho))
    
    # Converter combinações para formato de lista
    combinacoes_formatadas = [list(comb) for comb in todas_combinacoes]
    
    # Calcular total
    total = len(combinacoes_formatadas)
    
    # Agrupar por primeiro dígito
    por_primeiro_digito = {}
    for i in range(10):
        por_primeiro_digito[i] = [comb for comb in combinacoes_formatadas if comb[0] == i]
    
    return jsonify({
        "tamanho": tamanho,
        "total": total,
        "por_primeiro_digito": por_primeiro_digito
    })

# Função para calcular o número de combinações de n elementos tomados k a k
def calcular_combinacoes(n, k):
    return math.comb(n, k)

# Função para calcular o número de agrupamentos com duas dezenas
def calcular_agrupamentos_duas_dezenas(tamanho):
    # Para agrupamentos de dois dígitos (0-9), temos 10 escolher 2 = 45 possibilidades
    if tamanho <= 2:
        return tamanho  # Para tamanho 1, apenas 1 agrupamento, para 2, são 2 agrupamentos
    else:
        # Para tamanhos maiores, calculamos quantas combinações de 2 dígitos temos dos 10 dígitos
        return calcular_combinacoes(10, 2)

# Função para calcular combinações de agrupamento em 2
def calcular_combinacoes_agrupadas(tamanho):
    if tamanho <= 2:
        return tamanho
    # Para tamanhos maiores, calculamos com base no número de combinações possíveis dentro de cada agrupamento
    agrupamentos = calcular_agrupamentos_duas_dezenas(tamanho)
    combinacoes_por_agrupamento = calcular_combinacoes(tamanho, 2)
    return agrupamentos * combinacoes_por_agrupamento

@app.route('/api/estatisticas')
def get_estatisticas():
    # Calcular o número de combinações para cada tamanho de 1 a 10
    estatisticas = []
    n = 10  # número total de dígitos (0-9)
    
    for k in range(1, n + 1):
        total_combinacoes = calcular_combinacoes(n, k)
        
        # Calcular os agrupamentos com duas dezenas
        agrupamentos_duas_dezenas = calcular_agrupamentos_duas_dezenas(k)
        
        # Calcular combinações destes agrupamentos
        combinacoes_agrupadas = calcular_combinacoes_agrupadas(k)
        
        estatisticas.append({
            "tamanho": k,
            "total": total_combinacoes,
            "agrupamentos_duas_dezenas": agrupamentos_duas_dezenas,
            "combinacoes_agrupadas": combinacoes_agrupadas
        })
    
    return jsonify(estatisticas)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)