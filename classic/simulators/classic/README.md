# Simulador de Batalhas Axie Infinity Classic

## Visão Geral

Este projeto é um simulador completo de batalhas para o Axie Infinity Classic que analisa todas as combinações possíveis de equipes, executa simulações de batalhas e apresenta as 10 melhores equipes através de um painel web interativo com métricas de desempenho detalhadas.

## Características Principais

### Motor de Simulação
- Análise Completa: Processamento de todas as classes de Axies, partes do corpo e cartas disponíveis
- Simulações Binárias: Execução rápida de batalhas sem interface visual durante o processamento
- Mecânicas Fiéis: Implementação das regras originais do jogo incluindo bônus de classe e atributos

### Sistema de Análise
- Geração de Equipes: Criação automática de todas as combinações viáveis de equipes
- Avaliação de Performance: Cálculo de taxa de vitórias, pontuação e estatísticas detalhadas
- Ranking Inteligente: Identificação das 10 melhores equipes baseada em múltiplos critérios

### Interface Web Interativa
- Dashboard Responsivo: Interface moderna e intuitiva para visualização dos resultados
- Gráficos Dinâmicos: Visualizações interativas de performance e distribuição de classes
- Detalhes Completos: Informações detalhadas de cada Axie, incluindo atributos e cartas
- Comparação de Equipes: Análise comparativa entre as melhores equipes

## Como Usar

### 1. Executar Simulações

Para executar uma nova simulação completa:

```bash
cd axie_simulator
python3 simulation_runner.py
```

### 2. Visualizar Resultados

Para acessar o painel web interativo:

```bash
cd axie-simulator-dashboard
pnpm install
pnpm run dev --host
```

Acesse http://localhost:5173 no seu navegador.

## Resultados Obtidos

### Top 10 Melhores Equipes

O simulador identificou as seguintes equipes como as mais eficazes:

1. Equipe 1 - 87.8% de vitórias (Beast + Bird + Bird)
2. Equipe 2 - 90.2% de vitórias (Beast + Bird + Bird)
3. Equipe 3 - 100.0% de vitórias (Bird + Bird + Reptile)
4. Equipe 4 - 94.3% de vitórias (Beast + Bird + Bird)
5. Equipe 5 - 93.9% de vitórias (Bird + Bird + Reptile)

### Insights Principais

- Dominância de Birds: A classe Bird aparece em 90% das melhores equipes
- Combinações Eficazes: Beast + Bird + Bird é a combinação mais comum
- Alta Performance: As melhores equipes mantêm taxas de vitória acima de 87%
- Diversidade Limitada: Apenas 5 classes diferentes aparecem no top 10

## Tecnologias Utilizadas

### Backend
- Python 3.11: Linguagem principal
- JSON: Armazenamento e troca de dados
- Regex: Processamento de dados textuais

### Frontend
- React 18: Framework de interface
- Vite: Build tool e servidor de desenvolvimento
- Tailwind CSS: Estilização
- Recharts: Gráficos e visualizações
- Lucide React: Ícones

## Arquivos de Saída

### Relatórios
- battle_report.txt: Relatório detalhado com histórico de todas as batalhas
- simulation_results.json: Resultados completos de todas as equipes simuladas
- top_10_teams.json: Dados das 10 melhores equipes com detalhes completos

### Interface Web
- Dashboard interativo com múltiplas visualizações
- Gráficos de performance e distribuição
- Detalhes completos de cada equipe e Axie
- Comparações entre equipes

---

Desenvolvido para análise estratégica do Axie Infinity Classic

