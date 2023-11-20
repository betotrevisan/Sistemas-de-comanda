"""
Projeto de controle de consumo dos clientes do recanto SHWAB
"""

from datetime import datetime
import shutil
import os
import pandas as pd

# Criando a comanda


comanda_atual = None


def cria_comanda():
    numero_comanda = input('Digite o número da comanda do cliente: ')
    caminho_comanda = os.path.join("Comandas em uso", f"{numero_comanda}.csv")

    if os.path.exists(caminho_comanda):
        print(f'A comanda {numero_comanda} já existe.')
        return

    nova_comanda = pd.DataFrame(columns=['Código', 'Descrição', 'Valor Unitário', 'Quantidade', 'Subtotal'])

    # Salvando a comanda
    nova_comanda.to_csv(caminho_comanda, index=False)

    print(f'Comanda {numero_comanda} criada com sucesso.')
    print(nova_comanda)
    return


# Cliente realiza pedido

def realiza_compra():
    numero_comanda = input('Digite o número da comanda do cliente: ')
    caminho_comanda = os.path.join("Comandas em uso", f"{numero_comanda}.csv")

    precos = pd.read_csv('precos_shwab.csv', thousands='.', decimal=',')

    if not os.path.exists(caminho_comanda):
        print(f'A comanda {numero_comanda} não existe.')
        return cria_comanda()

    nova_comanda = pd.read_csv(caminho_comanda)

    while True:
        codigo_produto = input('Digite o código do produto (ou "sair" para finalizar a compra): ')

        if codigo_produto.lower() == 'sair':
            break

        produto = precos[precos['Código'] == int(codigo_produto)]
        print(produto)

        if produto.empty:
            print("Produto não encontrado para o código informado.")
            continue

        try:
            quantidade = int(input("Digite a quantidade do produto: "))
        except ValueError:
            print('Por gentileza, digite um valor numérico válido')
            continue

        # Adicionando dados na comanda
        valor_unitario = float(produto['Preço Unitário'].str.replace('R$', '').str.replace(',', '.').values[0])
        subtotal = valor_unitario * quantidade

        novo_item = {
            'Código': int(codigo_produto),
            'Descrição': produto['Descrição'].values[0],
            'Valor Unitário': valor_unitario,
            'QTD': quantidade,
            'Subtotal': subtotal
        }

        nova_comanda = nova_comanda._append(novo_item, ignore_index=True)

    # Calculando o 'Total'
    nova_comanda['Total'] = nova_comanda['Subtotal'].sum()

    # Formatando os valores com duas casas decimais
    colunas_float = ['Valor Unitário', 'Subtotal', 'Total']
    nova_comanda[colunas_float] = nova_comanda[colunas_float].map(lambda x: f'{x: .2f}')

    # Atualizando a comanda
    nova_comanda.to_csv(caminho_comanda, index=False)

    print(f'Compra realizada com sucesso na comanda {numero_comanda}.')
    print(nova_comanda)


# Efeutando o pagamento e finalizando a comanda:
def paga_comanda():
    def lista_comandas_em_uso():
        pasta_comandas_em_uso = "Comandas em uso"
        comandas_em_uso = os.listdir(pasta_comandas_em_uso)
        return comandas_em_uso

    comandas_em_uso = lista_comandas_em_uso()

    if not comandas_em_uso:
        print("Não há comandas em uso.")
        return

    print("Comandas em uso:")
    for i, comanda in enumerate(comandas_em_uso, start=1):
        print(f"{i}. {comanda}")

    escolha = input("Escolha o número da comanda a ser paga: ")

    try:
        indice_comanda = int(escolha) - 1
        comanda_a_pagar = comandas_em_uso[indice_comanda]
        caminho_comanda = os.path.join("Comandas em uso", comanda_a_pagar)
    except (ValueError, IndexError):
        print("Escolha inválida. Certifique-se de escolher um número válido.")
        return

    comanda_atual = pd.read_csv(caminho_comanda)

    # Exibir a comanda com duas casas decimais
    pd.set_option('display.float_format', '{:.2f}'.format)
    print(f'Comanda Atual: \n{comanda_atual}')

    pagamento_confirmado = input("O pagamento foi confirmado? (Digite 'sim' para confirmar): ").lower() == 'sim'

    if pagamento_confirmado:

        data_atual = datetime.now().strftime('%Y-%m-%d')
        pasta_pagos = os.path.join("Pagos", data_atual)
        os.makedirs(pasta_pagos, exist_ok=True)
        nome_arquivo_original = os.path.basename(comanda_a_pagar)
        hora_atual = datetime.now().strftime('%H-%M-%S')
        novo_nome_arquivo = f"{data_atual}_{nome_arquivo_original}_{hora_atual}"
        caminho_novo_arquivo = os.path.join(pasta_pagos, novo_nome_arquivo)
        shutil.move(caminho_comanda, caminho_novo_arquivo)
        print(f'A comanda {comanda_a_pagar} foi paga e movida para {pasta_pagos}.')
    else:
        print(f'Favor confirmar o pagamento.')


def main():
    while True:
        print("Escolha uma opção:")
        print("1. Criar comanda")
        print("2. Realizar compra")
        print("3. Pagar comanda")
        print("4. Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            cria_comanda()
        elif opcao == '2':
            realiza_compra()
        elif opcao == '3':
            paga_comanda()
        elif opcao == '4':
            print('Saindo da aplicação')
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":
    main()
