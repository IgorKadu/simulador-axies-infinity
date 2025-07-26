
import re
import json

def parse_classic_info(filepath):
    """Parseia informações do jogo Axie Infinity Classic de um arquivo Markdown.

    Args:
        filepath (str): O caminho para o arquivo Markdown contendo as informações.

    Returns:
        dict: Um dicionário contendo os dados parseados, incluindo atributos base,
              bônus de partes do corpo, atributos de raças puras e informações de cartas.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[ERROR] Arquivo não encontrado: {filepath}")
        return None
    except IOError as e:
        print(f"[ERROR] Erro ao ler o arquivo {filepath}: {e}")
        return None

    data = {}

    # Mapeamento de nomes de classes do português para o inglês para consistência interna
    class_name_mapping = {
        'Aquático': 'Aquatic',
        'Besta': 'Beast',
        'Pássaro': 'Bird',
        'Inseto': 'Bug',
        'Planta': 'Plant',
        'Réptil': 'Reptile',
        'Amanhecer': 'Dawn',
        'Crepúsculo': 'Dusk',
        'Mech': 'Mech'
    }

    def parse_generic_attribute_table(text, section_title, table_header_regex, num_columns, section_name):
        """Função auxiliar para parsear tabelas de atributos genéricas a partir do texto.

        Identifica uma seção pelo título e, dentro dela, encontra e parseia uma tabela Markdown.

        Args:
            text (str): O texto completo onde procurar a seção e a tabela.
            section_title (str): Expressão regular para encontrar o título da seção.
            table_header_regex (str): Expressão regular para encontrar o cabeçalho da tabela (para delimitar o conteúdo da tabela).
            num_columns (int): O número esperado de colunas na tabela de dados.
            section_name (str): Um nome descritivo para a seção (usado em mensagens de log).

        Returns:
            dict: Um dicionário onde as chaves são nomes (mapeados para inglês) e os valores são dicionários de atributos.
        """
        print(f"[DEBUG] Parsing section: {section_name}")
        attributes = {}
        
        # Encontra o início da seção usando a regex do título
        section_start_match = re.search(section_title, text, re.DOTALL)
        if not section_start_match:
            print(f"[WARN] Section '{section_name}' not found with title regex: {section_title}")
            return attributes

        # Extrai o conteúdo da seção após o título
        section_content = text[section_start_match.end():]
        
        # Regex para encontrar o bloco da tabela Markdown após o cabeçalho
        # Captura linhas que começam com '|' até encontrar outro título '##' ou o fim do texto.
        table_regex = table_header_regex + r's*
((?:|[^
]*
)+?)(?=
## |Z|


)'
        table_match = re.search(table_regex, section_content, re.DOTALL)

        if table_match:
            table_content = table_match.group(1).strip()
            print(f"[DEBUG] Table content found for {section_name}:
{table_content}
")
            
            # Processa cada linha da tabela
            for line in table_content.split('
'):
                # Ignora linhas vazias, linhas de separador de cabeçalho ou linhas que não parecem linhas de dados
                if not line.strip() or not line.strip().startswith('|') or not line.strip().endswith('|') or line.strip().startswith('|---') or line.strip().startswith('| Classe/Atributo'):
                    continue
                
                # Divide a linha pelos separadores '|' e remove espaços em branco
                parts = [p.strip() for p in line.split('|') if p.strip()]
                
                # Verifica se o número de partes corresponde ao número esperado de colunas
                if len(parts) == num_columns: 
                    name_pt = parts[0]
                    # Mapeia o nome (em português) para inglês, se existir no mapeamento
                    name_en = class_name_mapping.get(name_pt, name_pt) 
                    try:
                        # Lógica específica para parsear os valores dos atributos como inteiros
                        if section_name == 'Class Base Attributes' or section_name == 'Pure Breed Total Attributes':
                            attributes[name_en] = {
                                'HP': int(parts[1]),
                                'Velocidade': int(parts[2]),
                                'Habilidade': int(parts[3]),
                                'Moral': int(parts[4])
                            }
                        elif section_name == 'Body Part Bonus Attributes':
                            # Remove '+' antes de converter para int para bônus de partes
                            attributes[name_en] = {
                                'HP': int(parts[1].replace('+', '')),
                                'Velocidade': int(parts[2].replace('+', '')),
                                'Habilidade': int(parts[3].replace('+', '')),
                                'Moral': int(parts[4].replace('+', ''))
                            }
                    except ValueError as e:
                        print(f"[ERROR] Erro ao converter para int em {section_name}: '{line.strip()}' - {e}")
                        continue # Pula a linha malformada
                else:
                    print(f"[WARN] Skipping malformed line in {section_name} (expected {num_columns} columns, got {len(parts)}): '{line}'")
        else:
            print(f"[WARN] No table block found for {section_name} with regex: {table_header_regex}")
            
        print(f"[DEBUG] Finished parsing {section_name}. Found {len(attributes)} entries.")
        return attributes

    def parse_cards_table(text, class_name_mapping):
        """Parseia as tabelas de cartas para todas as classes a partir do texto.

        Args:
            text (str): O texto completo onde procurar as seções de cartas.
            class_name_mapping (dict): Mapeamento de nomes de classes do português para o inglês.

        Returns:
            dict: Um dicionário onde as chaves são nomes de classes (em inglês) e os valores são listas de dicionários de cartas.
        """
        print("[DEBUG] Parsing card sections...")
        cards_data = {}
        
        # Regex para encontrar as seções de cartas para cada classe.
        # Captura o nome da classe e o conteúdo da tabela de cartas.
        card_sections_regex = r'## Cartas da Classe (.*?) (Classic)s*
(?:|.*?|.*?|.*?|.*?|.*?|.*?|
|---+|(?:---+|){5}
((?:|[^
]*
)+?))(?=
## Cartas da Classe|Z|


)'
        card_sections = re.findall(card_sections_regex, text, re.DOTALL)

        if not card_sections:
            print("[WARN] No card sections found with the current regex.")
            
        # Processa cada seção de carta encontrada
        for class_name_pt, cards_table_content in card_sections:
            class_name_pt = class_name_pt.strip()
            # Mapeia o nome da classe para inglês
            class_name_en = class_name_mapping.get(class_name_pt, class_name_pt) 
            print(f"[DEBUG] Processing cards for class: {class_name_en}")
            cards_data[class_name_en] = [] # Inicializa a lista de cartas para a classe (usa o nome em inglês)

            # Processa cada linha do conteúdo da tabela de cartas
            for line in cards_table_content.strip().split('
'):
                # Ignora linhas vazias, linhas de separador de cabeçalho ou linhas de cabeçalho
                if not line.strip() or line.strip().startswith('|---') or line.strip().startswith('| Nome da Carta'):
                    continue
                    
                # Divide a linha pelos separadores '|' e remove espaços em branco
                parts = [p.strip() for p in line.split('|') if p.strip()]
                
                # Verifica se é uma linha de dados de carta (6 colunas)
                if len(parts) == 6: 
                    try:
                        # Cria um dicionário para a carta e converte valores numéricos para int
                        card = {
                            'Nome': parts[0],
                            'Tipo': parts[1],
                            'Energia': int(parts[2]),
                            'Ataque': int(parts[3]),
                            'Escudo': int(parts[4]),
                            'Descricao': parts[5]
                        }
                        cards_data[class_name_en].append(card)
                    except ValueError as e:
                        print(f"[ERROR] Erro ao converter para int ao parsear carta: '{line.strip()}' - {e}")
                        continue # Pula a linha malformada
                else:
                     print(f"[WARN] Skipping malformed card line in {class_name_en} (expected 6 columns, got {len(parts)}): '{line}'")
                        
        print("[DEBUG] Finished parsing card sections.")
        return cards_data

    # Parse Class Base Attributes
    data['class_base_attributes'] = parse_generic_attribute_table(
        content,
        r'## Atributos Base de Cada Classe de Axie',
        r'| Classe/Atributo | HP | Velocidade | Habilidade | Moral |
|---+|---+|---+|---+|---+|',
        5,
        'Class Base Attributes'
    )

    # Parse Body Part Bonus Attributes
    data['body_part_bonus_attributes'] = parse_generic_attribute_table(
        content,
        r'## Bônus de Atributos de Partes do Corpo do Axie',
        r'| Parte do Corpo/Atributo | HP | Velocidade | Habilidade | Moral |
|---+|---+|---+|---+|---+|',
        5,
        'Body Part Bonus Attributes'
    )

    # Parse Pure Breed Total Attributes
    data['pure_breed_total_attributes'] = parse_generic_attribute_table(
        content,
        r'## Atributos Totais para Raças Puras',
        r'| Classe/Atributo | HP | Velocidade | Habilidade | Moral |
|---+|---+|---+|---+|---+|',
        5,
        'Pure Breed Total Attributes'
    )

    # Parse Cards
    data['cards'] = parse_cards_table(content, class_name_mapping)

    return data

if __name__ == '__main__':
    # Bloco para testar a função de parsing diretamente
    # Define o caminho do arquivo de entrada e saída
    input_filepath = 'classic/data/raw/Classic_Info.md' # Ajuste o caminho conforme necessário
    output_filepath = 'classic/data/parsed/parsed_game_data.json' # Ajuste o caminho conforme necessário
    
    print(f"Attempting to parse data from: {input_filepath}")
    parsed_data = parse_classic_info(input_filepath)
    
    if parsed_data:
        try:
            # Salva os dados parseados em um arquivo JSON
            with open(output_filepath, 'w', encoding='utf-8') as f:
                json.dump(parsed_data, f, indent=4, ensure_ascii=False)
            print(f"Dados do jogo parseados e salvos em {output_filepath}")
        except IOError as e:
            print(f"[ERROR] Erro ao escrever no arquivo {output_filepath}: {e}")
    else:
        print("Parsing falhou. Nenhum dado foi salvo.")


