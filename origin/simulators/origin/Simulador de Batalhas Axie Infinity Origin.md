# Simulador de Batalhas Axie Infinity Origin

## Visão Geral

Este projeto é um simulador completo de batalhas para o Axie Infinity Origin que analisa todas as combinações possíveis de equipes, executa simulações binárias de batalhas e apresenta os resultados das 10 melhores equipes através de uma interface web amigável com gráficos e análises de desempenho.

## Características Principais

### 🎯 Funcionalidades Core
- **Simulação de Batalhas Binárias**: Motor de simulação que executa batalhas automatizadas entre equipes
- **Geração Inteligente de Equipes**: Sistema que cria equipes baseadas em funções (Tank, Damage, Support) e sinergias
- **Análise de Desempenho**: Ranking das melhores equipes com base em taxa de vitória
- **Interface Web Interativa**: Dashboard moderno com gráficos e visualizações

### 🔧 Tecnologias Utilizadas
- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: React, Vite, Tailwind CSS, shadcn/ui, Recharts
- **Análise de Dados**: Pandas, JSON
- **Visualização**: Gráficos de barras, pizza e estatísticas em tempo real

## Estrutura do Projeto

```
axie-battle-simulator/
├── backend/
│   ├── game_model.py          # Modelos de dados do jogo
│   ├── team_generator.py      # Gerador de equipes
│   ├── battle_simulator.py    # Motor de simulação de batalhas
│   ├── simulation_runner.py   # Orquestrador de simulações
│   ├── flask_backend.py       # API REST Flask
│   └── parsed_origin_info.json # Dados do jogo parseados
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Componente principal
│   │   ├── api.js            # Cliente da API
│   │   └── components/       # Componentes UI
│   ├── index.html
│   └── package.json
└── docs/
    ├── README.md
    └── simulation_report.txt
```

## Como Executar

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- pnpm

### Backend (Flask)
```bash
# Instalar dependências
pip install flask flask-cors

# Executar servidor
python3 flask_backend.py
```
O servidor estará disponível em `http://localhost:8000`

### Frontend (React)
```bash
# Navegar para o diretório
cd axie-battle-simulator

# Instalar dependências (já instaladas)
pnpm install

# Executar aplicação
pnpm run dev --host
```
A aplicação estará disponível em `http://localhost:5173`

## Funcionalidades Detalhadas

### 1. Geração de Equipes
O sistema gera equipes baseadas em diferentes composições:
- **Equipes Mistas**: 1 Tank + 1 Damage + 1 Support
- **Equipes Especializadas**: 3 Tanks, 3 Damage ou 3 Support
- **Equipes Híbridas**: 2 de um tipo + 1 de outro

### 2. Sistema de Batalha
- Simulação binária sem interface visual
- Cálculo de dano baseado em atributos dos Axies
- Aplicação de buffs/debuffs das cartas
- Determinação de vencedor por HP restante

### 3. Análise de Resultados
- **Taxa de Vitória**: Percentual de vitórias por equipe
- **Distribuição de Classes**: Análise das classes mais efetivas
- **Composição de Papéis**: Distribuição de Tank/Damage/Support
- **Estatísticas Gerais**: Métricas agregadas do desempenho

### 4. Interface Web
- **Dashboard Interativo**: Visualização em tempo real dos resultados
- **Gráficos Dinâmicos**: Barras, pizza e estatísticas
- **Responsivo**: Compatível com desktop e mobile
- **Tema Moderno**: Design profissional com Tailwind CSS

## Dados do Jogo

O simulador utiliza dados reais do Axie Infinity Origin, incluindo:
- **Cartas**: 200+ cartas com efeitos únicos
- **Classes**: 9 classes diferentes (Plant, Aquatic, Beast, etc.)
- **Mecânicas**: Buffs, debuffs, cura, energia, stuns
- **Atributos**: HP, Speed, Skill, Morale

## Resultados de Exemplo

### Top 3 Equipes (Simulação de Teste)
1. **Team_1** - Taxa de Vitória: 50%
   - Bird (Tank) + Mech (Damage) + Bug (Support)
   
2. **Team_2** - Taxa de Vitória: 50%
   - Dawn (Tank) + Dawn (Damage) + Mech (Support)
   
3. **Team_3** - Taxa de Vitória: 50%
   - Mech (Mixed) + Reptile (Tank) + Bird (Tank)

## Otimizações e Melhorias Futuras

### Implementadas
- ✅ Simulação binária eficiente
- ✅ Interface web responsiva
- ✅ API REST completa
- ✅ Análise estatística avançada

### Possíveis Melhorias
- 🔄 Implementação de mecânicas mais complexas (energia, cartas especiais)
- 🔄 Sistema de machine learning para predição de resultados
- 🔄 Simulação de torneios completos
- 🔄 Integração com dados reais do jogo

## Considerações Técnicas

### Performance
- Simulações executadas em memória para velocidade
- Resultados cacheados para consultas rápidas
- Interface otimizada com React e Vite

### Escalabilidade
- Arquitetura modular permite expansão fácil
- API REST permite integração com outros sistemas
- Dados estruturados em JSON para flexibilidade

### Confiabilidade
- Validação de dados de entrada
- Tratamento de erros robusto
- Logs detalhados para debugging

## Conclusão

O Simulador de Batalhas Axie Infinity Origin oferece uma solução completa para análise estratégica do jogo, combinando simulação precisa, análise estatística avançada e interface moderna. O sistema é projetado para ser confiável, eficiente e fácil de usar, fornecendo insights valiosos para otimização de estratégias de batalha.

---

**Desenvolvido com foco em:** Otimização, Confiabilidade e Experiência do Usuário

