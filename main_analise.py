import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def carregar_dados(arquivo_json="dados.json"):
    """
    Carrega os dados do arquivo JSON.
    """
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {arquivo_json} não encontrado!")
        print("Execute primeiro o teste.py para gerar os dados.")
        return None

def calcular_complexidade_estimada(numeros_pontos, tempos):
    """
    Calcula a complexidade estimada usando regressão linear em escala log-log.
    Retorna a estimativa da potência (ex: 1.0 para O(n), 2.0 para O(n²))
    """
    if len(numeros_pontos) < 2:
        return None
    
    # Converte para logaritmos
    log_n = np.log(numeros_pontos)
    log_t = np.log(tempos)
    
    # Regressão linear
    coeffs = np.polyfit(log_n, log_t, 1)
    estimativa = coeffs[0]  # Coeficiente angular = potência estimada
    
    return estimativa

def calcular_estatisticas(dados):
    """
    Calcula estatísticas a partir dos dados brutos.
    """
    resultados = dados["resultados"]
    
    # Extrai dados brutos para análise
    numeros_pontos = [r["num_pontos"] for r in resultados]
    
    # Calcula médias e desvios padrão dos tempos
    medias_tempos_heuristico = []
    medias_tempos_eficiente = []
    desvios_tempos_heuristico = []
    desvios_tempos_eficiente = []
    
    for resultado in resultados:
        # Médias dos tempos
        media_heur = sum(resultado["tempos_heuristico"]) / len(resultado["tempos_heuristico"])
        media_ef = sum(resultado["tempos_eficiente"]) / len(resultado["tempos_eficiente"])
        medias_tempos_heuristico.append(media_heur)
        medias_tempos_eficiente.append(media_ef)
        
        # Desvios padrão dos tempos
        desvio_heur = (sum((x - media_heur)**2 for x in resultado["tempos_heuristico"]) / len(resultado["tempos_heuristico"]))**0.5
        desvio_ef = (sum((x - media_ef)**2 for x in resultado["tempos_eficiente"]) / len(resultado["tempos_eficiente"]))**0.5
        desvios_tempos_heuristico.append(desvio_heur)
        desvios_tempos_eficiente.append(desvio_ef)
    
    # Calcula razões de performance e seus desvios padrão
    razoes = []
    desvios_razoes = []
    
    for resultado in resultados:
        tempos_heur = resultado["tempos_heuristico"]
        tempos_ef = resultado["tempos_eficiente"]
        
        # Calcula razões para cada medição individual
        razoes_medicao = []
        for t_ef, t_heur in zip(tempos_ef, tempos_heur):
            if t_heur > 0:
                razao = t_ef / t_heur
                razoes_medicao.append(razao)
        
        # Média e desvio padrão das razões
        if razoes_medicao:
            razoes.append(np.mean(razoes_medicao))
            desvios_razoes.append(np.std(razoes_medicao))
        else:
            razoes.append(0)
            desvios_razoes.append(0)
    
    # Calcula complexidade estimada
    complexidade_heur = calcular_complexidade_estimada(numeros_pontos, medias_tempos_heuristico)
    complexidade_ef = calcular_complexidade_estimada(numeros_pontos, medias_tempos_eficiente)
    
    # Calcula diferenças percentuais dos raios
    diferencas_perc_raios = []
    for resultado in resultados:
        raio_heur = resultado["raio_heuristico"]
        raio_ef = resultado["raio_eficiente"]
        diff_perc = ((raio_heur - raio_ef) / raio_ef) * 100 if raio_ef > 0 else 0
        diferencas_perc_raios.append(diff_perc)
    
    # Calcula complexidade teórica
    # O(n) para ambos, mas com constantes diferentes
    complexidade_teorica = [n for n in numeros_pontos]
    
    return {
        "numeros_pontos": numeros_pontos,
        "medias_tempos_heuristico": medias_tempos_heuristico,
        "medias_tempos_eficiente": medias_tempos_eficiente,
        "desvios_tempos_heuristico": desvios_tempos_heuristico,
        "desvios_tempos_eficiente": desvios_tempos_eficiente,
        "razoes": razoes,
        "desvios_razoes": desvios_razoes,
        "diferencas_perc_raios": diferencas_perc_raios,
        "complexidade_teorica": complexidade_teorica,
        "complexidade_estimada_heur": complexidade_heur,
        "complexidade_estimada_ef": complexidade_ef
    }

def gerar_grafico_comparacao_log(estatisticas, nome_arquivo="plot_comparacao_log.png"):
    """
    Gera o gráfico de comparação de performance dos algoritmos em escala log-log.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Adiciona envelopes de desvio padrão transparentes
    numeros_pontos = estatisticas["numeros_pontos"]
    medias_heur = estatisticas["medias_tempos_heuristico"]
    desvios_heur = estatisticas["desvios_tempos_heuristico"]
    medias_ef = estatisticas["medias_tempos_eficiente"]
    desvios_ef = estatisticas["desvios_tempos_eficiente"]
    
    # Envelope superior e inferior para heurístico
    ax.fill_between(numeros_pontos, 
                     [m - d for m, d in zip(medias_heur, desvios_heur)],
                     [m + d for m, d in zip(medias_heur, desvios_heur)],
                     alpha=0.2, color='blue', label='±1σ Heurístico')
    
    # Envelope superior e inferior para eficiente
    ax.fill_between(numeros_pontos, 
                     [m - d for m, d in zip(medias_ef, desvios_ef)],
                     [m + d for m, d in zip(medias_ef, desvios_ef)],
                     alpha=0.2, color='orange', label='±1σ Eficiente')
    
    # Linhas principais dos algoritmos
    ax.loglog(numeros_pontos, medias_heur, 
               'o-', label='Algoritmo Heurístico', linewidth=2, markersize=8, color='blue')
    ax.loglog(numeros_pontos, medias_ef, 
               's-', label='Algoritmo Eficiente', linewidth=2, markersize=8, color='orange')
    
    # Linhas de complexidade estimada
    if estatisticas["complexidade_estimada_heur"] is not None:
        # Calcula linha de complexidade estimada para heurístico
        log_n = np.log(estatisticas["numeros_pontos"])
        log_t = np.log(estatisticas["medias_tempos_heuristico"])
        coeffs_heur = np.polyfit(log_n, log_t, 1)
        y_heur_est = np.exp(coeffs_heur[1]) * (estatisticas["numeros_pontos"] ** coeffs_heur[0])
        ax.loglog(estatisticas["numeros_pontos"], y_heur_est, ':', 
                   label=f'O(n^{estatisticas["complexidade_estimada_heur"]:.2f}) Heurístico', 
                   alpha=0.8, color='blue')
    
    if estatisticas["complexidade_estimada_ef"] is not None:
        # Calcula linha de complexidade estimada para eficiente
        log_n = np.log(estatisticas["numeros_pontos"])
        log_t = np.log(estatisticas["medias_tempos_eficiente"])
        coeffs_ef = np.polyfit(log_n, log_t, 1)
        y_ef_est = np.exp(coeffs_ef[1]) * (estatisticas["numeros_pontos"] ** coeffs_ef[0])
        ax.loglog(estatisticas["numeros_pontos"], y_ef_est, ':', 
                   label=f'O(n^{estatisticas["complexidade_estimada_ef"]:.2f}) Eficiente', 
                   alpha=0.8, color='orange')
    
    ax.set_xlabel('Número de Pontos')
    ax.set_ylabel('Tempo de Execução (segundos)')
    ax.set_title('Comparação de Performance dos Algoritmos\n(escalas log-log)')
    ax.legend(loc='upper left', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return nome_arquivo

def gerar_grafico_razao_performance(estatisticas, nome_arquivo="plot_razao_semilogx.png"):
    """
    Gera o gráfico de razão de performance entre os algoritmos com envelopes de desvio padrão.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Dados das razões e seus desvios padrão
    numeros_pontos = estatisticas["numeros_pontos"]
    razoes = estatisticas["razoes"]
    desvios_razoes = estatisticas["desvios_razoes"]
    
    # Envelope superior e inferior para as razões (±1σ)
    ax.fill_between(numeros_pontos, 
                     [r - d for r, d in zip(razoes, desvios_razoes)],
                     [r + d for r, d in zip(razoes, desvios_razoes)],
                     alpha=0.2, color='red', label='±1σ Razão')
    
    # Linha principal das razões
    ax.semilogx(numeros_pontos, razoes, 
                 'o-', color='red', linewidth=2, markersize=8, label='Razão Eficiente/Heurístico')

    ax.set_xlabel('Número de Pontos')
    ax.set_ylabel('Razão (Eficiente / Heurístico)')
    ax.set_title('Razão de Performance: Eficiente vs Heurístico')
    ax.legend(loc='upper left', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return nome_arquivo

def gerar_grafico_diferenca_raios(estatisticas, nome_arquivo="plot_diferenca_raios.png"):
    """
    Gera o gráfico de diferença percentual dos raios entre os algoritmos.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    ax.semilogx(estatisticas["numeros_pontos"], estatisticas["diferencas_perc_raios"], 
                 'o-', color='green', linewidth=2, markersize=8, label='Diferença % dos Raios')
    ax.set_xlabel('Número de Pontos')
    ax.set_ylabel('Diferença Percentual (%)')
    ax.set_title('Diferença Percentual dos Raios: Heurístico vs Eficiente')
    ax.legend(fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Adiciona linha horizontal em y=0 para referência
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return nome_arquivo

def gerar_grafico_razao_decimal(estatisticas, nome_arquivo="plot_razao_decimal.png"):
    """
    Gera o gráfico de razão de performance entre os algoritmos com eixo x em escala decimal.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Dados das razões e seus desvios padrão
    numeros_pontos = estatisticas["numeros_pontos"]
    razoes = estatisticas["razoes"]
    desvios_razoes = estatisticas["desvios_razoes"]
    
    # Envelope superior e inferior para as razões (±1σ)
    ax.fill_between(numeros_pontos, 
                     [r - d for r, d in zip(razoes, desvios_razoes)],
                     [r + d for r, d in zip(razoes, desvios_razoes)],
                     alpha=0.2, color='red', label='±1σ Razão')
    
    # Linha principal das razões (escala decimal)
    ax.plot(numeros_pontos, razoes, 
            'o-', color='red', linewidth=2, markersize=8, label='Razão Eficiente/Heurístico')
    
    ax.set_xlabel('Número de Pontos')
    ax.set_ylabel('Razão (Eficiente / Heurístico)')
    ax.set_title('Razão de Performance: Eficiente vs Heurístico\n(escala decimal)')
    ax.legend(loc='upper left', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return nome_arquivo

def gerar_grafico_comparacao_decimal(estatisticas, nome_arquivo="plot_comparacao_decimal.png"):
    """
    Gera o gráfico de comparação de performance dos algoritmos em escalas decimais.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Adiciona envelopes de desvio padrão transparentes
    numeros_pontos = estatisticas["numeros_pontos"]
    medias_heur = estatisticas["medias_tempos_heuristico"]
    desvios_heur = estatisticas["desvios_tempos_heuristico"]
    medias_ef = estatisticas["medias_tempos_eficiente"]
    desvios_ef = estatisticas["desvios_tempos_eficiente"]
    
    # Envelope superior e inferior para heurístico
    ax.fill_between(numeros_pontos, 
                     [m - d for m, d in zip(medias_heur, desvios_heur)],
                     [m + d for m, d in zip(medias_heur, desvios_heur)],
                     alpha=0.2, color='blue', label='±1σ Heurístico')
    
    # Envelope superior e inferior para eficiente
    ax.fill_between(numeros_pontos, 
                     [m - d for m, d in zip(medias_ef, desvios_ef)],
                     [m + d for m, d in zip(medias_ef, desvios_ef)],
                     alpha=0.2, color='orange', label='±1σ Eficiente')
    
    # Linhas principais dos algoritmos
    ax.plot(numeros_pontos, medias_heur, 
            'o-', label='Algoritmo Heurístico', linewidth=2, markersize=8, color='blue')
    ax.plot(numeros_pontos, medias_ef, 
            's-', label='Algoritmo Eficiente', linewidth=2, markersize=8, color='orange')
    
    # Linhas de complexidade estimada
    if estatisticas["complexidade_estimada_heur"] is not None:
        # Calcula linha de complexidade estimada para heurístico
        log_n = np.log(estatisticas["numeros_pontos"])
        log_t = np.log(estatisticas["medias_tempos_heuristico"])
        coeffs_heur = np.polyfit(log_n, log_t, 1)
        y_heur_est = np.exp(coeffs_heur[1]) * (estatisticas["numeros_pontos"] ** coeffs_heur[0])
        ax.plot(estatisticas["numeros_pontos"], y_heur_est, ':', 
                label=f'O(n^{estatisticas["complexidade_estimada_heur"]:.2f}) Heurístico', 
                alpha=0.8, color='blue')
    
    if estatisticas["complexidade_estimada_ef"] is not None:
        # Calcula linha de complexidade estimada para eficiente
        log_n = np.log(estatisticas["numeros_pontos"])
        log_t = np.log(estatisticas["medias_tempos_eficiente"])
        coeffs_ef = np.polyfit(log_n, log_t, 1)
        y_ef_est = np.exp(coeffs_ef[1]) * (estatisticas["numeros_pontos"] ** coeffs_ef[0])
        ax.plot(estatisticas["numeros_pontos"], y_ef_est, ':', 
                label=f'O(n^{estatisticas["complexidade_estimada_ef"]:.2f}) Eficiente', 
                alpha=0.8, color='orange')
    
    ax.set_xlabel('Número de Pontos')
    ax.set_ylabel('Tempo de Execução (segundos)')
    ax.set_title('Comparação de Performance dos Algoritmos\n(escalas decimais)')
    ax.legend(loc='upper left', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return nome_arquivo

def gerar_graficos(estatisticas):
    """
    Gera os cinco gráficos separadamente e salva cada um em um arquivo.
    """
    print("\nGerando gráficos...")
    
    # Gráfico 1: Comparação de performance em escala log
    arquivo1 = gerar_grafico_comparacao_log(estatisticas, "plot_comparacao_log.png")
    print(f"  Gráfico de comparação (log-log) salvo em: {arquivo1}")
    
    # Gráfico 2: Comparação de performance em escala decimal
    arquivo2 = gerar_grafico_comparacao_decimal(estatisticas, "plot_comparacao_decimal.png")
    print(f"  Gráfico de comparação (decimal) salvo em: {arquivo2}")
    
    # Gráfico 3: Razão de performance (semi-log)
    arquivo3 = gerar_grafico_razao_performance(estatisticas, "plot_razao_semilogx.png")
    print(f"  Gráfico de razão (semi-log) salvo em: {arquivo3}")
    
    # Gráfico 4: Razão de performance (decimal)
    arquivo4 = gerar_grafico_razao_decimal(estatisticas, "plot_razao_decimal.png")
    print(f"  Gráfico de razão (decimal) salvo em: {arquivo4}")
    
    # Gráfico 5: Diferença dos raios
    arquivo5 = gerar_grafico_diferenca_raios(estatisticas, "plot_diferenca_raios.png")
    print(f"  Gráfico de diferença dos raios salvo em: {arquivo5}")
    
    return [arquivo1, arquivo2, arquivo3, arquivo4, arquivo5]

def gerar_relatorio(dados, estatisticas, nome_arquivo="relatorio.txt"):
    """
    Gera relatório textual da análise.
    """
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("RELATÓRIO DE ANÁLISE DE PERFORMANCE\n")
        f.write("=" * 50 + "\n\n")
        
        # Informações da configuração
        f.write("CONFIGURAÇÃO DOS TESTES:\n")
        f.write("-" * 30 + "\n")
        config = dados["configuracao"]
        f.write(f"Limites X: [{config['x_min']}, {config['x_max']}]\n")
        f.write(f"Limites Y: [{config['y_min']}, {config['y_max']}]\n")
        f.write(f"Sigma (distribuição Gaussiana): {config['sigma']}\n")
        f.write(f"Número de medições por teste: {config['num_medicoes']}\n")
        
        # Resultados detalhados
        f.write("\nRESULTADOS DETALHADOS:\n")
        f.write("-" * 30 + "\n")
        
        for i, resultado in enumerate(dados["resultados"]):
            f.write(f"\nTeste {i+1}: {resultado['num_pontos']} pontos\n")
            f.write(f"  Heurístico: {estatisticas['medias_tempos_heuristico'][i]:.6f}s ± {estatisticas['desvios_tempos_heuristico'][i]:.6f}s")
            f.write(f" (raio: {resultado['raio_heuristico']:.6f})\n")
            f.write(f"  Eficiente:  {estatisticas['medias_tempos_eficiente'][i]:.6f}s ± {estatisticas['desvios_tempos_eficiente'][i]:.6f}s")
            f.write(f" (raio: {resultado['raio_eficiente']:.6f})\n")
            f.write(f"  Razão:      {estatisticas['razoes'][i]:.3f} ± {estatisticas['desvios_razoes'][i]:.3f}\n")
            
            # Calcula diferenças dos raios para este teste
            raio_heur = resultado['raio_heuristico']
            raio_ef = resultado['raio_eficiente']
            diff_abs = raio_heur - raio_ef
            diff_perc = (diff_abs / raio_ef) * 100 if raio_ef > 0 else 0
            
            f.write(f"  Dif. raio:  {diff_abs:+.6f} ({diff_perc:+.2f}%)\n")
            
            # Verifica se há erro (raio heurístico menor que eficiente)
            if raio_heur < raio_ef:
                f.write(f"  ERRO: Raio heurístico menor que eficiente!\n")
        
        # Análise geral
        f.write("\nANÁLISE DOS TEMPOS DE EXECUÇÃO:\n")
        f.write("-" * 30 + "\n")
        
        media_razao = np.mean(estatisticas["razoes"])
        
        f.write(f"Razão média (Eficiente/Heurístico): {media_razao:.3f}\n")
        
        # Análise dos raios
        f.write("\nANÁLISE DOS RAIOS:\n")
        f.write("-" * 30 + "\n")
        
        # Calcula estatísticas dos raios
        raios_heuristico = [r["raio_heuristico"] for r in dados["resultados"]]
        raios_eficiente = [r["raio_eficiente"] for r in dados["resultados"]]
        
        # Usa as diferenças percentuais já calculadas
        diferencas_abs = []
        diferencas_perc = estatisticas["diferencas_perc_raios"]
        erros_encontrados = []
        
        for i in range(len(raios_heuristico)):
            raio_heur = raios_heuristico[i]
            raio_ef = raios_eficiente[i]
            diff_abs = raio_heur - raio_ef
            
            diferencas_abs.append(diff_abs)
            
            # Verifica se há erro
            if raio_heur < raio_ef:
                erros_encontrados.append(i+1)
        
        # Estatísticas das diferenças
        if diferencas_abs:
            media_diff_abs = np.mean(diferencas_abs)
            media_diff_perc = np.mean(diferencas_perc)
            min_diff_abs = min(diferencas_abs)
            max_diff_abs = max(diferencas_abs)
            min_diff_perc = min(diferencas_perc)
            max_diff_perc = max(diferencas_perc)
            
            f.write(f"Diferença absoluta média: {media_diff_abs:+.6f}\n")
            f.write(f"Diferença percentual média: {media_diff_perc:+.2f}%\n")
            f.write(f"Variação absoluta: [{min_diff_abs:+.6f}, {max_diff_abs:+.6f}]\n")
            f.write(f"Variação percentual: [{min_diff_perc:+.2f}%, {max_diff_perc:+.2f}%]\n")
            
            # Interpretação
            if media_diff_perc > 0:
                f.write(f"O algoritmo heurístico produziu círculos, em média, {media_diff_perc:.2f}% maiores.\n")
            else:
                f.write(f"O algoritmo heurístico produziu círculos, em média, {abs(media_diff_perc):.2f}% menores.\n")
        
        # Verificação de erros
        if erros_encontrados:
            f.write(f"  ERROS ENCONTRADOS:\n")
            f.write(f"  - Testes com raio heurístico menor que eficiente: {erros_encontrados}\n")
            f.write(f"  - Total de erros: {len(erros_encontrados)}/{len(raios_heuristico)}\n")
            f.write(f"  - Isso indica um problema no algoritmo heurístico!\n")
        else:
            f.write(f"Nenhum erro encontrado: todos os raios heurísticos são >= eficientes.\n")
        
        # Complexidade
        f.write("\nCOMPLEXIDADE ESTIMADA:\n")
        f.write("-" * 30 + "\n")
        if estatisticas["complexidade_estimada_heur"] is not None:
            f.write(f"  - Algoritmo Heurístico: O(n^{estatisticas['complexidade_estimada_heur']:.3f})\n")
        else:
            f.write("  - Algoritmo Heurístico: Não foi possível calcular\n")
            
        if estatisticas["complexidade_estimada_ef"] is not None:
            f.write(f"  - Algoritmo Eficiente: O(n^{estatisticas['complexidade_estimada_ef']:.3f})\n")
        else:
            f.write("  - Algoritmo Eficiente: Não foi possível calcular\n")
    
    return nome_arquivo

def executar_analise(arquivo_json="dados.json"):
    """
    Executa a análise completa dos dados.
    """
    print("Iniciando análise dos dados...")
    
    # Carrega dados
    dados = carregar_dados(arquivo_json)
    if dados is None:
        return
    
    # Calcula estatísticas
    estatisticas = calcular_estatisticas(dados)
    
    # Gera gráficos separados
    arquivos_graficos = gerar_graficos(estatisticas)
    print(f"\nGráficos salvos:")
    for arquivo in arquivos_graficos:
        print(f"  - {arquivo}")
    
    # Gera relatório
    arquivo_relatorio = gerar_relatorio(dados, estatisticas)
    print(f"\nRelatório salvo em: {arquivo_relatorio}")
    
    print("\nAnálise concluída!")

if __name__ == "__main__":
    executar_analise()
