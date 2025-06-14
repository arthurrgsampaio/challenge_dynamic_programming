"""
Módulo de controle de estoque para o desafio DASA/Challenge.

Turma: 2ESR-2025

Integrantes:
    - 558488 Anthony Motobe
    - 555342 Arthur Rodrigues
    - 554743 Guilherme Abe
    - 554779 Gustavo Paulino
    - 558017 Victor Dias
"""

import copy

stock = {
    "Almoxarifado A": {
        "luvas": {"current": 120, "ideal": 150},
        "máscaras": {"current": 60, "ideal": 100},
        "álcool": {"current": 80, "ideal": 80}
    },
    "Almoxarifado B": {
        "luvas": {"current": 30, "ideal": 100},
        "máscaras": {"current": 150, "ideal": 100},
        "álcool": {"current": 20, "ideal": 80}
    }
}

memory_diff = {}


def calculate_diff(current, ideal):
    """
    Calcula a diferença entre o valor ideal e o valor atual de um item, utilizando memoização para evitar cálculos repetidos.
    """
    key = (current, ideal)
    if key in memory_diff:
        return memory_diff[key]
    result = ideal - current
    memory_diff[key] = result
    return result


def get_products(stock):
    """
    Retorna uma lista de todos os produtos presentes em todos os estoques.
    """
    products = set()
    for location in stock:
        products.update(stock[location].keys())
    return list(products)


def redistribute_items(auto_confirm=True):
    """
    Sugere e executa redistribuição de itens entre estoques, mostrando uma tabela com os valores antes e depois.
    Se auto_confirm=True, aplica as alterações automaticamente; caso contrário, solicita confirmação do usuário.
    """
    temp_stock = copy.deepcopy(stock)
    redistributions = []
    products = get_products(temp_stock)
    changes = []
    for product in products:
        shortage_locations = []
        surplus_locations = []
        for location in temp_stock:
            if product in temp_stock[location]:
                current = temp_stock[location][product]['current']
                ideal = temp_stock[location][product]['ideal']
                diff = calculate_diff(current, ideal)
                if diff > 0:
                    shortage_locations.append([location, diff])
                elif diff < 0:
                    surplus_locations.append([location, abs(diff)])
        for shortage in shortage_locations:
            for surplus in surplus_locations:
                if surplus[1] == 0:
                    continue
                transferred_quantity = min(shortage[1], surplus[1])
                if transferred_quantity > 0:
                    redistributions.append(
                        (product, surplus[0], shortage[0], transferred_quantity)
                    )
                    temp_stock[surplus[0]][product]['current'] -= transferred_quantity
                    temp_stock[shortage[0]][product]['current'] += transferred_quantity
                    surplus[1] -= transferred_quantity
                    shortage[1] -= transferred_quantity
                    changes.append((product, surplus[0], shortage[0], transferred_quantity))
    if not redistributions:
        print("Nenhuma redistribuição sugerida.")
        return
    print(
        "+----------------------+----------------------+----------------------+-------+-----------------------+-------------------------+")
    print(
        f"| {'Produto':<20} | {'De (Estoque)':<20} | {'Para (Estoque)':<20} | {'Qtd.':<5} | {'Valor atualizado (De)':<20} | {'Valor atualizado (Para)':<24}|")
    print(
        "+----------------------+----------------------+----------------------+-------+-----------------------+-------------------------+")
    for product, from_, to, qty in redistributions:
        current_from_before = stock[from_][product]['current']
        current_to_before = stock[to][product]['current']
        current_from_after = current_from_before - qty
        current_to_after = current_to_before + qty
        print(
            f"| {product:<20} | {from_:<20} | {to:<20} | {qty:<5} | {current_from_before} -> {current_from_after:<14} | {current_to_before} -> {current_to_after:<18}|")
    print(
        "+----------------------+----------------------+----------------------+-------+-----------------------+-------------------------+")
    if auto_confirm:
        for product, from_, to, qty in redistributions:
            stock[from_][product]['current'] -= qty
            stock[to][product]['current'] += qty
        print("Redistribuição realizada com sucesso!")
    else:
        confirm = input("Deseja realizar as alterações sugeridas? (s/n): ").strip().lower()
        if confirm == 's':
            for product, from_, to, qty in redistributions:
                stock[from_][product]['current'] -= qty
                stock[to][product]['current'] += qty
            print("Redistribuição realizada com sucesso!")
        else:
            print("Nenhuma alteração foi feita.")


def view_inventories():
    """
    Exibe todos os estoques e seus itens em formato de tabela.
    """
    print("+----------------------+------------------------------------------------+")
    print(f"| {'Estoque':<20} | {'Itens':<47}|")
    print("+----------------------+------------------------------------------------+")
    for idx, (key, items) in enumerate(stock.items()):
        products = list(items.items())
        if products:
            product, data = products[0]
            item_str = f"{product}: atual={data['current']}, ideal={data['ideal']}"
            print(f"| {key:<20} | {item_str:<47}|")
            for product, data in products[1:]:
                item_str = f"{product}: atual={data['current']}, ideal={data['ideal']}"
                print(f"| {'':<20} | {item_str:<47}|")
        else:
            print(f"| {key:<20} | {'':<47}|")
        if idx < len(stock) - 1:
            print("+----------------------+------------------------------------------------+")
    print("+----------------------+------------------------------------------------+")


def add_inventory(auto=False):
    """
    Adiciona um novo estoque ao dicionário principal.
    Se auto=True, o nome é gerado automaticamente (para uso em demonstrações).
    Caso contrário, solicita o nome ao usuário via input.
    """
    if auto:
        name = "Novo Estoque"
        idx = 1
        while f"{name} {idx}" in stock:
            idx += 1
        name = f"{name} {idx}"
    else:
        print("+--------------------------+")
        print(f"| {'Cadastro de novo estoque':<25}|")
        print("+--------------------------+")
        name = input("Digite o nome do novo estoque ou 'cancelar', para sair: ").strip()
        if not name:
            print("Nome inválido. Operação cancelada.")
            return
        if name in stock:
            print("Já existe um estoque com esse nome.")
            return
        if name == "cancelar":
            return
    stock[name] = {}
    print("+--------------------------------------------------------+")
    print(f"| {'Estoque ' + name + ' cadastrado com sucesso!':<55}|")
    print("+--------------------------------------------------------+")


def add_items_to_inventory(auto=False):
    """
    Adiciona itens a um estoque existente.
    Se auto=True, adiciona automaticamente ao último estoque criado.
    Caso contrário, solicita ao usuário o estoque e o item via input.
    """
    stocks = list(stock.keys())
    if auto:
        stock_name = stocks[-1]
    else:
        print("+---+--------------------------------+")
        print(f"| {'#':<1} | {'Estoques disponíveis':<30} |")
        print("+---+--------------------------------+")
        for idx, name in enumerate(stocks, 1):
            print(f"| {idx:<1} | {name:<30} |")
        print("+---+--------------------------------+")
        while True:
            try:
                choice = int(input("Digite o número do estoque: "))
                if 1 <= choice <= len(stocks):
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Por favor, digite um número válido.")
        stock_name = stocks[choice - 1]
    products = list(stock[stock_name].keys())
    if auto:
        if products:
            prod_name = products[0]
            qty = 10
            stock[stock_name][prod_name]['current'] += qty
            print(f"Quantidade atualizada para {stock[stock_name][prod_name]['current']}.")
        else:
            new_name = "Novo Item"
            idx = 1
            while new_name in stock[stock_name]:
                idx += 1
            new_name = f"{new_name} {idx}"
            current = 10
            ideal = 20
            stock[stock_name][new_name] = {'current': current, 'ideal': ideal}
            print(f"Item '{new_name}' adicionado ao {stock_name}.")
    else:
        print(f"Você selecionou: {stock_name}")
        print("+---+------------------------------------------+")
        print(f"| {'#':<1} | {'Item':<20} | {'Atual':<7} | {'Ideal':<7} |")
        print("+---+------------------------------------------+")
        for idx, prod in enumerate(products, 1):
            data = stock[stock_name][prod]
            print(f"| {idx:<1} | {prod:<20} | {data['current']:<7} | {data['ideal']:<7} |")
        if not products:
            print(f"| - | {'Nenhum item cadastrado.':<41}|")
        print("+---+------------------------------------------+")
        print("Deseja:")
        print("1. Adicionar quantidade a um item já existente")
        print("2. Criar um novo item")
        print("3. Cancelar cadastro")
        while True:
            option = input("Digite 1, 2 ou 3: ")
            match option:
                case '1':
                    if not products:
                        print("Não há itens existentes neste estoque. Selecione a opção 2 para criar um novo item.")
                        continue
                    while True:
                        try:
                            prod_idx = int(input("Escolha o item pelo número: "))
                            if 1 <= prod_idx <= len(products):
                                break
                            else:
                                print("Opção inválida. Tente novamente.")
                        except ValueError:
                            print("Por favor, digite um número válido.")
                    prod_name = products[prod_idx - 1]
                    qty = int(input(f"Digite a quantidade a adicionar em '{prod_name}': "))
                    stock[stock_name][prod_name]['current'] += qty
                    print(f"Quantidade atualizada para {stock[stock_name][prod_name]['current']}.")
                    break
                case '2':
                    new_name = input("Digite o nome do novo item: ")
                    current = int(input("Digite a quantidade atual: "))
                    ideal = int(input("Digite a quantidade ideal: "))
                    stock[stock_name][new_name] = {'current': current, 'ideal': ideal}
                    print(f"Item '{new_name}' adicionado ao {stock_name}.")
                    break
                case '3':
                    break
                case _:
                    print("Opção inválida. Tente novamente.")


def items_in_shortage(auto=False):
    """
    Exibe uma tabela com os itens em falta em cada estoque.
    Se auto=True, ajusta automaticamente os itens para o valor ideal.
    """
    result = []
    for stock_name in stock:
        for product in stock[stock_name]:
            current = stock[stock_name][product]['current']
            ideal = stock[stock_name][product]['ideal']
            difference = calculate_diff(current, ideal)
            if difference > 0:
                result.append((stock_name, product, difference))
    if not result:
        print("Nenhum item em falta em nenhum estoque.")
        return
    stocks_in_shortage = {}
    for stock_name, product, shortage in result:
        if stock_name not in stocks_in_shortage:
            stocks_in_shortage[stock_name] = []
        stocks_in_shortage[stock_name].append((product, shortage))
    for idx, (stock_name, items) in enumerate(stocks_in_shortage.items()):
        print(f"+---------------------------------------------+")
        print(f"| Estoque: {stock_name:<35}|")
        print(f"+---+----------------------+------------------+")
        print(f"| {'#':<1} | {'Item em falta':<20} | {'Qtd. para ideal':<17}|")
        print(f"+---+----------------------+------------------+")
        for i, (product, shortage) in enumerate(items, 1):
            print(f"| {i:<1} | {product:<20} | {shortage:<17}|")
        print(f"+---+----------------------+------------------+")
        if idx < len(stocks_in_shortage) - 1:
            print()
    if auto:
        for stock_name, items in stocks_in_shortage.items():
            for product, shortage in items:
                ideal = stock[stock_name][product]['ideal']
                stock[stock_name][product]['current'] = ideal
                print(f"Estoque de {stock_name} atualizado: {product} agora tem {ideal} unidades.")
        print("Todos os itens em falta foram atualizados para a quantidade ideal.")


def items_in_surplus(auto=False):
    """
    Exibe uma tabela com os itens em excesso em cada estoque.
    Se auto=True, ajusta automaticamente os itens para o valor ideal.
    """
    result = []
    for stock_name in stock:
        for product in stock[stock_name]:
            current = stock[stock_name][product]['current']
            ideal = stock[stock_name][product]['ideal']
            difference = calculate_diff(current, ideal)
            if difference < 0:
                result.append((stock_name, product, abs(difference)))
    if not result:
        print("Nenhum item em excesso em nenhum estoque.")
        return
    stocks_in_surplus = {}
    for stock_name, product, surplus in result:
        if stock_name not in stocks_in_surplus:
            stocks_in_surplus[stock_name] = []
        stocks_in_surplus[stock_name].append((product, surplus))
    for idx, (stock_name, items) in enumerate(stocks_in_surplus.items()):
        print(f"+---------------------------------------------+")
        print(f"| Estoque: {stock_name:<35}|")
        print(f"+---+----------------------+------------------+")
        print(f"| {'#':<1} | {'Item em excesso':<20} | {'Qtd. em excesso':<17}|")
        print(f"+---+----------------------+------------------+")
        for i, (product, surplus) in enumerate(items, 1):
            print(f"| {i:<1} | {product:<20} | {surplus:<17}|")
        print(f"+---+----------------------+------------------+")
        if idx < len(stocks_in_surplus) - 1:
            print()
    if auto:
        for stock_name, items in stocks_in_surplus.items():
            for product, surplus in items:
                stock[stock_name][product]['current'] = stock[stock_name][product]['ideal']
                print(
                    f"Estoque de {stock_name} atualizado: {product} agora tem {stock[stock_name][product]['ideal']} unidades.")
        print("Todos os itens em excesso foram atualizados para a quantidade ideal.")


def demonstration():
    """
    Executa automaticamente todas as funções principais para demonstração.
    """
    print("\n--- Demonstração Automática do Sistema ---\n")
    print("1. Visualizando estoques:")
    view_inventories()
    print("\n2. Cadastrando um novo estoque:")
    add_inventory(auto=True)
    print("\n3. Cadastrando produtos no novo estoque:")
    add_items_to_inventory(auto=True)
    print("\n4. Visualizando estoques novamente:")
    view_inventories()
    print("\n5. Verificando produtos em falta:")
    items_in_shortage(auto=True)
    print("\n6. Verificando produtos em excesso:")
    items_in_surplus(auto=True)
    print("\n7. Redistribuindo estoques:")
    redistribute_items(auto_confirm=True)
    print("\n--- Fim da Demonstração ---\n")


def start():
    """
    Função principal que inicia o menu de opções do sistema.
    """
    print("Bem vindo ao ...")
    while True:
        option = input("Menu de opções\n"
                       "1. Verificar estoques\n"
                       "2. Cadastrar estoque\n"
                       "3. Cadastrar produtos\n"
                       "4. Ver produtos em falta\n"
                       "5. Ver produtos em excesso\n"
                       "6. Redistribuir estoques\n"
                       "7. Rodar demonstração automática\n"
                       "8. Sair\n"
                       "Digite a opção desejada: ")

        match option:
            case "1":
                view_inventories()
            case "2":
                add_inventory(auto=False)
            case "3":
                add_items_to_inventory(auto=False)
            case "4":
                items_in_shortage(auto=False)
            case "5":
                items_in_surplus(auto=False)
            case "6":
                redistribute_items(auto_confirm=False)
            case "7":
                demonstration()
            case "8":
                print("Obrigado por usar nosso sistema.")
                break
            case _:
                print("Digite um valor válido.")


start()
