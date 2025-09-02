# Comparação de Algoritmos de Círculo Mínimo

## Descrição

Este projeto implementa e compara dois algoritmos para encontrar o círculo mínimo que envolve um conjunto de pontos:

1. **Algoritmo Heurístico**: Implementação simples e rápida que aproxima ao raio mínimo
2. **Algoritmo Eficiente**: Implementação que forence o raio mínimo

## Funcionalidades

### Coleta de Dados
- Geração de pontos aleatórios com distribuição Gaussiana
- Execução de testes com diferentes tamanhos de conjuntos (16 a 1.048.576 pontos)
- 1000 medições por teste para análise estatística robusta
- Geração de dados em formato JSON para análise posterior

### Análise de Performance
- Cálculo de médias e desvios padrão dos tempos de execução
- Análise de complexidade algorítmica usando regressão log-log
- Comparação de razões de performance entre algoritmos
- Análise da qualidade das soluções (raios dos círculos)

### Visualização
- **5 gráficos** com diferentes perspectivas dos dados:
  1. `plot_comparacao_log.png` - Comparação de performance em escala log-log
  2. `plot_comparacao_decimal.png` - Comparação de performance em escala decimal
  3. `plot_razao_semilogx.png` - Razão de performance em escala semi-log
  4. `plot_razao_decimal.png` - Razão de performance em escala decimal
  5. `plot_diferenca_raios.png` - Diferença percentual dos raios

### Relatórios
- Relatório textual detalhado com estatísticas de cada teste
- Inclusão de desvios padrão para todas as métricas
- Análise de complexidade estimada
- Verificação de erros nos algoritmos

## Estrutura do Projeto

```
CompGraf_Ex1_CirculoMinimo/
├── algoritmos/
│   ├── eficiente.py      # Algoritmo eficiente
│   └── heuristico.py     # Algoritmo heurístico
├── main_coleta_dados.py  # Coleta de dados de performance
├── main_analise.py       # Análise e geração de gráficos
├── geometria.py          # Funções auxiliares de geometria (ponto e círculo)
├── dados.json            # Dados coletados (gerado automaticamente)
├── relatorio.txt         # Relatório de análise (gerado automaticamente)
├── requirements.txt      # Dependências Python
└── README.md             # Este arquivo
```

## Gráficos Gerados

### 1. Comparação de Performance (Log-Log)
- **Arquivo**: `plot_comparacao_log.png`
- **Escala**: Ambos os eixos logarítmicos
- **Conteúdo**: Tempos de execução vs número de pontos + envelopes ±1σ + linhas de complexidade estimada

### 2. Comparação de Performance (Decimal)
- **Arquivo**: `plot_comparacao_decimal.png`
- **Escala**: Ambos os eixos lineares
- **Conteúdo**: Mesmo que o anterior, mas em escala decimal para visualizar transições

### 3. Razão de Performance (Semi-Log)
- **Arquivo**: `plot_razao_semilogx.png`
- **Escala**: Eixo X logarítmico, Eixo Y linear
- **Conteúdo**: Razão Eficiente/Heurístico com envelopes ±1σ

### 4. Razão de Performance (Decimal)
- **Arquivo**: `plot_razao_decimal.png`
- **Escala**: Ambos os eixos lineares
- **Conteúdo**: Razão Eficiente/Heurístico em escala decimal

### 5. Diferença dos Raios
- **Arquivo**: `plot_diferenca_raios.png`
- **Escala**: Eixo X logarítmico, Eixo Y linear
- **Conteúdo**: Diferença percentual dos raios entre algoritmos

## Como Usar

### 1. Instalação das Dependências
```bash
pip install -r requirements.txt
```

### 2. Coleta de Dados
```bash
python main_coleta_dados.py
```
- Gera pontos aleatórios
- Executa algoritmos 1000 vezes para cada tamanho de conjunto
- Salva resultados em `dados.json`

### 3. Análise e Geração de Gráficos
```bash
python main_analise.py
```
- Carrega dados do `dados.json`
- Calcula estatísticas (médias, desvios padrão, razões)
- Gera os 5 gráficos separados
- Cria relatório textual em `relatorio.txt`

## Configuração dos Testes

- **Limites dos pontos**: X ∈ [-1, 1], Y ∈ [-1, 1]
- **Distribuição**: Gaussiana com σ = 0.1
- **Tamanhos dos conjuntos**: 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576 pontos
- **Medições por teste**: 1000 execuções
- **Seed**: Controlado para reprodutibilidade (42 + número da medição)

## Análise Estatística

### Métricas Calculadas
- **Tempos de execução**: Média ± desvio padrão para cada algoritmo
- **Razões de performance**: Média ± desvio padrão das razões individuais
- **Qualidade das soluções**: Diferenças percentuais dos raios
- **Complexidade estimada**: Expoente da regressão log-log

### Envelopes de Desvio Padrão
- **Transparência**: α = 0.2 (20%)
- **Cobertura**: ±1 desvio padrão (68% das medições)
- **Cores**: Azul (heurístico), laranja (eficiente), vermelho (razões)

## Algoritmos Implementados

### Algoritmo Heurístico
- **Complexidade**: O(n) esperado
- **Características**: Simples e rápido
- **Garantia**: Raio ≥ raio mínimo (não necessariamente ótimo)

### Algoritmo Eficiente
- **Complexidade**: O(n) esperado
- **Características**: Recursivo, baseado em geometria computacional
- **Garantia**: Raio mínimo exato
- **Randomização**: Usa `random.Random(seed).shuffle()` para atingir O(n)

## Relatório Gerado

O arquivo `relatorio.txt` contém:
- Configuração dos testes
- Resultados detalhados de cada teste
- Análise dos tempos de execução
- Análise da qualidade das soluções
- Verificação de erros nos algoritmos
- Complexidade estimada

## Dependências

- **matplotlib**: Geração de gráficos
- **numpy**: Cálculos numéricos e estatísticos
- **json**: Manipulação de dados
- **random**: Geração de pontos e seeds
- **time**: Medição de performance

## Características Técnicas

- **Reprodutibilidade**: Seeds controlados para todos os testes
- **Estatística robusta**: 1000 medições por teste
- **Visualização avançada**: Múltiplas escalas e envelopes de erro
- **Modularidade**: Funções separadas para cada tipo de gráfico
- **Formato de saída**: PNG de alta resolução (300 DPI)

