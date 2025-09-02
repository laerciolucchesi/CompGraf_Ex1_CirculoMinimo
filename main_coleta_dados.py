import random
import json
import time
from geometria import Ponto, Circulo
from algoritmos.heuristico import calcular_circulo_heuristico
from algoritmos.eficiente import calcular_circulo_eficiente

def gerar_pontos_gaussiana(n=100, x_min=-1, x_max=1, y_min=-1, y_max=1, sigma=0.1):
    """
    Gera pontos usando distribuição gaussiana (normal) - maior densidade no centro.
    """
    pontos = []
    
    while len(pontos) < n:
        # Gera coordenadas usando distribuição normal
        x = random.gauss(0, sigma)
        y = random.gauss(0, sigma)
        
        # Verifica se está dentro dos limites
        if x_min <= x <= x_max and y_min <= y <= y_max:
            pontos.append(Ponto(x, y))
    
    return pontos

def executar_testes():
    """
    Executa os testes e salva os dados em arquivo JSON.
    """
    # Configuração
    X_MIN, X_MAX = -1, 1
    Y_MIN, Y_MAX = -1, 1
    SIGMA = 0.1
    NUM_MEDICOES = 1000
    
    # Lista de pontos para teste
    numeros_pontos = []
    n = 2**10
    while n <= 2**20:
        numeros_pontos.append(n)
        n *= 2
    
    # Dados para salvar
    dados_teste = {
        "configuracao": {
            "x_min": X_MIN,
            "x_max": X_MAX,
            "y_min": Y_MIN,
            "y_max": Y_MAX,
            "sigma": SIGMA,
            "num_medicoes": NUM_MEDICOES
        },
        "resultados": []
    }
    
    print("Iniciando coleta de dados de performance...")
    print(f"Total de testes: {len(numeros_pontos)}")
    print(f"Medições por teste: {NUM_MEDICOES}")
    print("=" * 50)
    
    for i, num_pontos in enumerate(numeros_pontos):
        print(f"Teste {i+1}/{len(numeros_pontos)}: {num_pontos} pontos")
        
        # Gera pontos uma vez (mesmos pontos para todas as medições)
        random.seed(42)
        pontos = gerar_pontos_gaussiana(num_pontos, X_MIN, X_MAX, Y_MIN, Y_MAX, SIGMA)
        
        # Warm-up: executa cada algoritmo uma vez antes das medições
        _ = calcular_circulo_heuristico(pontos)
        _ = calcular_circulo_eficiente(pontos, seed=42)
        
        # Listas para armazenar os tempos de execução
        tempos_heuristico = []
        tempos_eficiente = []
        
        # Calcula os raios uma única vez (são determinísticos)
        random.seed(42)
        circulo_heuristico = calcular_circulo_heuristico(pontos)
        circulo_eficiente = calcular_circulo_eficiente(pontos, seed=42)
        raio_heuristico = circulo_heuristico.raio
        raio_eficiente = circulo_eficiente.raio
        
        for medicao in range(NUM_MEDICOES):
            # Testa algoritmo heurístico
            random.seed(42 + medicao)
            inicio_heuristico = time.perf_counter()
            _ = calcular_circulo_heuristico(pontos)
            fim_heuristico = time.perf_counter()
            tempo_heuristico = fim_heuristico - inicio_heuristico
            tempos_heuristico.append(tempo_heuristico)
            
            # Testa algoritmo eficiente
            inicio_eficiente = time.perf_counter()
            _ = calcular_circulo_eficiente(pontos, seed=42 + medicao)
            fim_eficiente = time.perf_counter()
            tempo_eficiente = fim_eficiente - inicio_eficiente
            tempos_eficiente.append(tempo_eficiente)
        
        # Salva os dados brutos deste teste
        resultado_teste = {
            "num_pontos": num_pontos,
            "tempos_heuristico": tempos_heuristico,
            "tempos_eficiente": tempos_eficiente,
            "raio_heuristico": raio_heuristico,
            "raio_eficiente": raio_eficiente
        }
        
        dados_teste["resultados"].append(resultado_teste)
    
    # Salva os dados em arquivo JSON
    nome_arquivo = "dados.json"
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_teste, f, indent=2, ensure_ascii=False)
    
    print("=" * 50)
    print(f"Dados salvos em: {nome_arquivo}")
    print("Coleta de dados concluída!")

if __name__ == "__main__":
    executar_testes()
