import random
import math
import time

#------------- FUNÇÕES GERAIS E MODELAGENS ------------------------

#função que cria tabuleiro aleatório
def criar_tabuleiro(n):
# Cria uma lista de N números aleatórios de 0 a n-1 diretamente
   return [random.randint(0, n-1) for _ in range(n)] 

#função que calcula o número de pares de rainhas se atacando
def calculo_custo(tabuleiro):
   ataques = 0
   n = len(tabuleiro)
   for i in range(n):
      for j in range(i+1, n): #compara cada rainha com as outras
         if tabuleiro[i] == tabuleiro[j]: #verifica ataque na mesma linha
            ataques += 1
         elif abs(tabuleiro[i] - tabuleiro[j]) == abs(i - j): #verifica ataque na diagonal
            ataques += 1
   return ataques

#função que calcula o fitness de um cromossomo
def calculo_fitness(tabuleiro):
      return (1/(1+calculo_custo(tabuleiro)))
   
#funcao que cria uma nova população a partir de pais selecionados
def selecao_torneio(populaçao,fitness):
   indice1 = random.randint(0, len(populaçao) - 1)
   indice2 = random.randint(0, len(populaçao) - 1)
   indice3 = random.randint(0, len(populaçao) - 1)
   
   #retorna o indivíduo com o maior fitness entre os 3
   if fitness[indice1] >= fitness[indice2] and fitness[indice1] >= fitness[indice3]:
      return populaçao[indice1]
   elif fitness[indice2] >= fitness[indice1] and fitness[indice2] >= fitness[indice3]:
      return populaçao[indice2]
   else:
      return populaçao[indice3] 
   
#função que realiza o crossover entre dois pais
def crossover(pai1, pai2, n):  
   
   if len(pai1) != len(pai2):
      return pai1 #retorna um dos pais em caso de erro
   
   ponto_corte = random.randint(1, n-1)
   filho = pai1[:ponto_corte] + pai2[ponto_corte:] #crossover de um ponto
   return filho
   
def mutação(individuo, n):
   # Sorteia um índice (coluna) e um novo valor (linha)
      indice_mutacao = random.randint(0, n - 1)
      nova_posicao = random.randint(0, n - 1)
      individuo[indice_mutacao] = nova_posicao
      return individuo
   
#------------- IMPLEMENTAÇÃO DOS ALGORITMOS ------------------------

#funcao que implementa o algoritmo de Hill Climbing
def hill_climbing(n, max_interacoes=1000): #max_interacoes é o número máximo de iterações platô
   tabuleiro_atual = criar_tabuleiro(n)
   custo_atual = calculo_custo(tabuleiro_atual)
   
   for _ in range(max_interacoes):
      if custo_atual == 0:
         return tabuleiro_atual, custo_atual,"Minimo Global"

      melhor_vizinho = None
      custo_melhor_vizinho = custo_atual
      
      for coluna in range(n):
         posicao_orignal = tabuleiro_atual[coluna]
         for linha in range(n):
            if tabuleiro_atual[coluna] == linha:
               continue
            
            tab_vizinho = list(tabuleiro_atual) #cria uma cópia do tabuleiro atual
            tab_vizinho[coluna] = linha
            custo_vizinho = calculo_custo(tab_vizinho)     
            
            if custo_vizinho < custo_melhor_vizinho:
               melhor_vizinho = tab_vizinho
               custo_melhor_vizinho = custo_vizinho
      
      #se não houver vizinho melhor, chegou a um mínimo (local ou global)
      if custo_melhor_vizinho >= custo_atual:
         return tabuleiro_atual, custo_atual, "Minimo Local"
      
      #move para o melhor vizinho
      tabuleiro_atual = melhor_vizinho
      custo_atual = custo_melhor_vizinho
   return tabuleiro_atual, custo_atual, "Minimo Local (maximo iterações atingido)"

#função que implementa o algoritmo de Simulated Annealing
def simulated_annealing(n, temperatura_inicial=1000, taxa_resfriamento=0.99, temperatura_final = 0.0001, iteracoes_por_temp = 100):
   #parametros
   temperatura = temperatura_inicial
   estado_atual = criar_tabuleiro(n)
   custo_atual = calculo_custo(estado_atual)
   

   while temperatura > temperatura_final:
      for i in range(iteracoes_por_temp):
         if custo_atual == 0:
          return estado_atual, custo_atual, "Minimo Global!"
      
       #pega um vizinho aleatório, nao o melhor
         coluna_aleatoria = random.randint(0, n-1)
         linha_aleatoria = random.randint(0, n-1)
         pos_original = estado_atual[coluna_aleatoria]
         
         #garante que a nova linha seja diferente
         while linha_aleatoria == pos_original:
            linha_aleatoria = random.randint(0, n - 1)
            
         
         vizinho = list(estado_atual)
         vizinho[coluna_aleatoria] = linha_aleatoria
         custo_vizinho = calculo_custo(vizinho)

         #decide se aceita o vizinho
         delta_custo = custo_vizinho - custo_atual

         #se o vizinho for melhor, aceita
         if delta_custo < 0:
            estado_atual = vizinho
            custo_atual = custo_vizinho
            
         #se for pior, aceita com uma certa probabilidade
         else:
            probabilidade = math.exp(-delta_custo / temperatura)
            if random.random() < probabilidade:
               estado_atual = vizinho
               custo_atual = custo_vizinho
        
      # Reduz a temperatura
      temperatura *= taxa_resfriamento
    
   status = "Mínimo Global" if custo_atual == 0 else "Mínimo Local"
   return estado_atual, custo_atual, status
   
#função que implementa o algoritmo de Algoritmo Genético   
def algoritmo_genético(n, populacao_tamanho=300, geracoes=2500, taxa_crossover= 0.8, taxa_mutacao=0.2):
   populacao = [criar_tabuleiro(n) for _ in range(populacao_tamanho)]
   
   for geracao in range(geracoes):
      #calcula o fitness de cada indivíduo
      fitness = [calculo_fitness(individuo) for individuo in populacao]
      
      if max(fitness) == 1.0:
         melhor_individuo = populacao[fitness.index(1.)]
         custo = calculo_custo(melhor_individuo)
         return melhor_individuo, custo, "Mínimo Global"
      
      #cria uma nova população
      nova_populacao = []
      
      #eletismo: adiciona o melhor indivíduo da geração passada
      indice_elite = fitness.index(max(fitness))
      nova_populacao.append(populacao[indice_elite])
      
      #preenche o resto da população com filhos.
      while len(nova_populacao) < populacao_tamanho:
         pai1 = selecao_torneio(populacao, fitness)
         pai2 = selecao_torneio(populacao, fitness)
         
         if random.random() < taxa_crossover:
            filho = crossover(pai1, pai2, n)
         else:
            filho = list(pai1)
      
      
         #aplica mutação
         if random.random() < taxa_mutacao:
            filho = mutação(filho, n)
      
            
         nova_populacao.append(filho)
      
      populacao = nova_populacao
      
   #se o loop acabar, retorna o melhor resultado encontrado.
   fitnesses_finais = [calculo_fitness(ind) for ind in populacao]
   indice_melhor = fitnesses_finais.index(max(fitnesses_finais))
   melhor_individuo = populacao[indice_melhor]
   custo = calculo_custo(melhor_individuo)
    
   return melhor_individuo, custo, "Mínimo Local (limite de gerações atingido)"  
   
def main():
   while True:
      print(f"\nEscolha o algoritmo para resolver o problema das N-Rainhas:")
      print("1. Hill Climbing")
      print("2. Simulated Annealing")
      print("3. Algoritmo Genético")
      escolha = input(f"\nDigite o número do algoritmo (1, 2 ou 3): ")
      
      if escolha not in ['1', '2', '3']:
         print("Escolha inválida. Encerrando o programa.")
         continue
      
      try: 
         n = int(input("Digite o tamanho do tabuleiro (n): "))
         execucoes = 5
      except ValueError:
            print("Tamanho do tabuleiro inválido.")
            continue
      
      if escolha == '1':
         print(f"\n===== Testando Hill Climbing com n = {n} =====")
         nome_algoritmo = "Hill Climbing"
         algoritmo = hill_climbing
      elif escolha == '2':
         print(f"\n===== Testando Simulated Annealing com n = {n} =====")
         nome_algoritmo = "Simulated Annealing"
         algoritmo = simulated_annealing
      else:
         print(f"\n===== Testando Algoritmo Genético com n = {n} =====")
         nome_algoritmo = "Algoritmo Genético"
         algoritmo = algoritmo_genético  

      resultados = []
      tempos = []
      
      for tentativa in range(1, execucoes + 1):
         inicio = time.time()
         solucao, custo, status = algoritmo(n)
         fim = time.time()
         duracao = fim - inicio

         resultados.append((custo, status))
         tempos.append(duracao)

         print(f"\nTentativa {tentativa}:")
         print(f"Tabuleiro solução: {solucao}")
         print(f"Custo (pares de rainhas se atacando): {custo}")
         print(f"Status: {status}")
         print(f"Tempo de execução: {duracao:.4f} segundos")
       
        
      media_custo = sum(c for c, _ in resultados) / execucoes
      media_tempo = sum(tempos) / execucoes
      print(f"\nResumo para {nome_algoritmo} com n = {n}:")
      print(f"Média de custo: {media_custo:.2f}")
      print(f"Média de tempo: {media_tempo:.4f} segundos") 
      
      print("\nDeseja testar outro algoritmo? (s/n)")
      continuar = input().strip().lower()
      if continuar != 's':
         print("Encerrando o programa.")
         break
      
if __name__ == "__main__":
    main()