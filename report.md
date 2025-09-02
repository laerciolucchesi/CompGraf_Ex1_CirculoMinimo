# Relatório de Resultados: Comparação de Algoritmos de Círculo Mínimo

## Objetivo

Este experimento visa comparar a performance de dois algoritmos para encontrar o círculo mínimo que envolve um conjunto de pontos: um algoritmo heurístico simples e um algoritmo eficiente baseado no método de Welzl. O objetivo é verificar qual algoritmo oferece melhor equilíbrio entre velocidade de execução e qualidade da solução para diferentes tamanhos de conjuntos de pontos.

## Introdução (Contexto)

O problema do círculo mínimo é fundamental em geometria computacional, com aplicações em áreas como visão computacional, robótica e análise de dados espaciais. Enquanto algoritmos exatos garantem a solução ótima, algoritmos heurísticos podem oferecer soluções aproximadas com menor custo computacional. A motivação para este estudo surge da necessidade de entender quando cada abordagem é mais adequada, especialmente considerando o trade-off entre precisão e velocidade em aplicações práticas.

## Metodologia

### Configuração dos Experimentos
- **Distribuição de pontos**: Coordenadas X,Y ∈ [-1, 1] com distribuição Gaussiana (σ = 0.1)
- **Tamanhos dos conjuntos**: 1.024 a 1.048.576 pontos (11 níveis)
- **Repetições**: 1.000 execuções por teste para estabilidade estatística
- **Seeds controlados**: Para reprodutibilidade dos resultados

### Algoritmos Testados
1. **Algoritmo Heurístico**: Implementação simples com complexidade O(n) esperada
2. **Algoritmo Eficiente**: Implementação de Welzl com complexidade O(n) esperada

### Métricas Coletadas
- Tempos de execução (média ± desvio padrão)
- Razões de performance (Eficiente/Heurístico)
- Qualidade das soluções (diferenças percentuais dos raios)
- Complexidade algorítmica estimada via regressão log-log

## Resultados

### Tabela 1: Resumo dos Resultados por Tamanho de Conjunto

| Pontos | Tempo Heurístico (s) | Tempo Eficiente (s) | Razão | Dif. Raio (%) |
|--------|---------------------|---------------------|-------|---------------|
| 1.024  | 0.0005 ± 0.0001     | 0.0037 ± 0.0021     | 7.0   | +3.30         |
| 2.048  | 0.0011 ± 0.0002     | 0.0076 ± 0.0041     | 7.1   | +4.24         |
| 4.096  | 0.0022 ± 0.0004     | 0.0163 ± 0.0095     | 7.5   | +4.24         |
| 8.192  | 0.0044 ± 0.0007     | 0.0318 ± 0.0177     | 7.4   | +3.98         |
| 16.384 | 0.0088 ± 0.0013     | 0.0631 ± 0.0371     | 7.3   | +0.15         |
| 32.768 | 0.0192 ± 0.0043     | 0.1638 ± 0.0871     | 8.7   | +4.32         |
| 65.536 | 0.0396 ± 0.0076     | 0.3805 ± 0.2003     | 9.8   | +1.19         |
| 131.072| 0.0880 ± 0.0159     | 0.9478 ± 0.5046     | 10.9  | +2.71         |
| 262.144| 0.1688 ± 0.0286     | 2.0615 ± 1.1403     | 12.4  | +2.06         |
| 524.288| 0.3584 ± 0.0519     | 4.6795 ± 2.5603     | 13.2  | +1.80         |
| 1.048.576| 0.7190 ± 0.1056   | 10.6818 ± 5.6140    | 15.1  | +1.20         |

### Gráficos de Análise

O projeto gera cinco visualizações principais:

1. **Comparação de Performance (Log-Log)**: Mostra tempos de execução em escala logarítmica com envelopes de desvio padrão
2. **Comparação de Performance (Decimal)**: Versão em escala linear para visualizar transições
3. **Razão de Performance (Semi-Log)**: Razão Eficiente/Heurístico com envelopes ±1σ
4. **Razão de Performance (Decimal)**: Mesma razão em escala linear
5. **Diferença dos Raios**: Qualidade das soluções em escala semi-log

### Estatísticas Gerais
- **Razão média de performance**: 9.7x (Eficiente é 9.7x mais lento)
- **Diferença percentual média dos raios**: +2.65% (Heurístico produz círculos maiores)
- **Complexidade estimada Heurístico**: O(n^1.047)
- **Complexidade estimada Eficiente**: O(n^1.163)

## Análise / Discussão

### Padrões Observados

**Performance Computacional**: O algoritmo heurístico é consistentemente mais rápido, com razões que variam de 7x a 15x dependendo do tamanho do conjunto. Para conjuntos pequenos (< 16.384 pontos), a razão é relativamente estável (~7x), mas cresce linearmente para conjuntos maiores, atingindo 15x para 1 milhão de pontos.

**Qualidade das Soluções**: O algoritmo heurístico produz círculos ligeiramente maiores (2.65% em média), mas sempre maiores ou iguais aos do algoritmo eficiente, confirmando sua correção. A diferença percentual diminui com o aumento do tamanho do conjunto, sugerindo melhor estabilidade para problemas maiores.

**Complexidade Algorítmica**: Ambos os algoritmos apresentam complexidade próxima de O(n), com o heurístico ligeiramente mais eficiente (expoente 1.047 vs 1.163). Isso confirma que ambos escalam linearmente, mas com constantes diferentes.

### Variáveis de Impacto

**Tamanho do Conjunto**: É a variável mais influente, afetando tanto os tempos absolutos quanto as razões de performance. Para conjuntos pequenos, o overhead do algoritmo eficiente é mais significativo.

**Distribuição dos Pontos**: A distribuição Gaussiana com σ = 0.1 cria conjuntos bem distribuídos, representativos de cenários reais, mas pode não capturar casos extremos.

### Limitações do Experimento

- **Hardware específico**: Resultados podem variar em diferentes sistemas
- **Distribuição limitada**: Apenas distribuição Gaussiana foi testada
- **Tamanhos discretos**: Saltos entre potências de 2 podem mascarar transições graduais
- **Medições isoladas**: Não considera cache effects ou otimizações do sistema operacional

## Conclusão

Os resultados mostram que o algoritmo heurístico oferece melhor performance computacional (7-15x mais rápido) em troca de uma pequena perda de precisão (círculos 2.65% maiores em média). A principal lição é que para aplicações que podem tolerar aproximações e priorizam velocidade, o algoritmo heurístico é preferível, especialmente para conjuntos grandes. O algoritmo eficiente mantém sua utilidade em cenários onde a precisão é crítica, confirmando que ambos têm seu lugar em diferentes contextos de aplicação.
