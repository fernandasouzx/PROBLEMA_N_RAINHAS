# Análise Comparativa de Algoritmos de Busca Heurística para o Problema das N-Rainhas

**Autora:** Fernanda Lima de Souza  
**Instituição:** Universidade Federal de Mato Grosso (UFMT)

---

## Descrição Geral
O problema das N-Rainhas consiste em posicionar **N rainhas em um tabuleiro N×N** de modo que nenhuma ataque outra.  
Foram implementados e avaliados três algoritmos heurísticos — **Hill-Climbing**, **Simulated Annealing** e **Algoritmo Genético** — em **Python**, para **N = {32, 64, 128}**.

Os testes consideraram:
- Qualidade da solução  
- Tempo de execução  
- Taxa de sucesso  

---

## Resultados Obtidos

| Algoritmo           | Desempenho              | Tempo Médio | Sucesso                                  |
|---------------------|------------------------|--------------|-------------------------------------------|
| Hill-Climbing       | Rápido, mas ineficaz   | Baixo        | 0%                                        |
| Simulated Annealing | Melhor equilíbrio       | Médio        | 100% (N=32,64), 40% (N=128)              |
| Algoritmo Genético  | Robusto, porém lento   | Alto         | ≤ 40%                                    |

---

## Conclusão
O **Simulated Annealing** apresentou o melhor custo-benefício, conciliando confiabilidade e eficiência.  
O **Hill-Climbing** mostrou limitação em mínimos locais, e o **Algoritmo Genético** foi o mais custoso computacionalmente.

---

## Execução (Python)

```bash
# Clonar o repositório
git clone https://github.com/fernandasouzx/PROBLEMAS_N_RAINHAS.git
cd PROBLEMAS_N_RAINHAS
python3 algoritmos_ia.py

# Executar
python3 main.py
