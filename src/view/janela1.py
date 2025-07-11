#para pegar a data de hoje
from datetime import date
import time

#Necessário para realizar import em python
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

#importando os módulos de model
from model.pedido import Pedido

#importando os módulos de controle
from controler.pedidoControler import PedidoControler
from controler.itemControler import ItemControler

#criação da classe janela
class Janela1:
    
    @staticmethod
    def mostrar_janela1(database_name: str) -> None:
        """
        View para o usuário utilizar o software
        return None
        """
        
        menu = ItemControler.mostrar_itens_menu(database_name)
        
        print('----------Menu----------\n')
        print(f'{menu} \n')
        
        a = 'y'  # controla o loop principal

        while a == 'y':
            lista_itens = []
            valor_total = 0
            
            # Loop para validar entrada do usuário (sim ou não)
            while True:
                a = input('Cadastrar pedido (y-Sim, n-Nao): ').strip().lower()
                
                if a in ['y', 's', 'sim']:
                    a = 'y'  # garante que a == 'y' para continuar
                    break
                
                elif a in ['n', 'nao']:
                    a = 'n'  # para sair do loop principal depois
                    print("Voltando ao Menu Inicial...\n")
                    time.sleep(2)
                    break
                
                else:
                    print("Entrada inválida. Por favor, digite 'y' (sim) ou 'n' (não).")
            
            # Se usuário quiser cadastrar pedido, com validação para continuar ou não
            if a == 'y':
                print("----------Cadastrar pedido----------\n")
                adicionar = 'y'  # controla se o usuário quer adicionar mais itens ao pedido
                
                # busca todos os pedidos para calcular o próximo número do pedido
                pedidos = PedidoControler.search_in_pedidos_all(database_name)
                numero_pedido = len(pedidos) + 1
                
                # Loop para adicionar itens ao pedido
                while adicionar == 'y':
                    item = int(input('Numero do item: '))
                    quantidade = int(input('Quantidade: '))
                    
                    # calculando em tempo de execução o valor do pedido
                    valor_item = ItemControler.valor_item(database_name, item)
                    if not valor_item or not valor_item[0]:
                        print("Item não encontrado. Tente novamente.")
                        continue
                        
                    total_item = valor_item[0][0] * quantidade
                    print(f'Valor deste item: R${total_item}')
                    valor_total += total_item
                    
                    for _ in range(quantidade):  # acrescenta o mesmo item várias vezes, conforme quantidade
                        lista_itens.append((numero_pedido, item))
                    
                    while True:
                        adicionar = input('Adicionar novo item? (y-Sim, n-Nao):').strip().lower()
                        if adicionar in ['y', 's', 'sim']:
                            adicionar = 'y'
                            break
                        elif adicionar in ['n', 'nao']:
                            adicionar = 'n'
                            break
                        else:
                            print("Entrada inválida. Por favor, digite 'y' (sim) ou 'n' (não)")

                # Finalizar pedido
                print('\n----------Finalizar pedido----------\n')
                print(f'Numero do pedido: {numero_pedido}')
                
                delivery = input('Delivery (S/N): ').strip().lower()
                if delivery == 's':
                    delivery = True
                elif delivery == 'n':
                    delivery = False
                else:
                    print('Valor incorreto, recomeçando cadastro...')
                    continue  # reinicia o loop principal
                
                endereco = input('Endereco: ').strip()
                status_aux = int(input('Status: 1-preparo, 2-pronto, 3-entregue: '))
                
                if status_aux == 1:
                    status = 'preparo'
                elif status_aux == 2:
                    status = 'pronto'
                else:
                    status = 'entregue'
                
                print(f'Valor Final: R${valor_total}')
                data_hoje = date.today()
                data_formatada = data_hoje.strftime('%d/%m/%Y')
                print(f'Data do pedido: {data_formatada}')
                print(f'Endereço: {endereco}')
                
                pedido = Pedido(status, str(delivery), endereco, data_formatada, float(valor_total))
                PedidoControler.insert_into_pedidos(database_name, pedido)
                
                for elem in lista_itens:
                    ItemControler.insert_into_itens_pedidos(database_name, elem)