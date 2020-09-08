from copy import deepcopy as copy
from utils import convert_afn_to_afd
import AFD
import AFN
import time


def _ordenar_potencia(potencia):
    potencia_ordenada = {}
    for estado in potencia:
        for aresta in potencia[estado]:
            potencia_ordenada[(estado, aresta)] = potencia[estado][aresta]
    potencia_ordenada = {k: v for k, v in sorted(potencia_ordenada.items(), key=lambda item: item[1], reverse=True)}
    return potencia_ordenada


def _calcular_potencia(dawg):
    potencia = {}
    estados_calculados = []

    for estado in dawg['states']:
        if estado != '{e}':
            for aresta in dawg['states'][estado]:
                if '{e}' in dawg['states'][estado][aresta]:
                    potencia[estado] = {'{e}': 1}
                    estados_calculados.append(estado)

    while len(estados_calculados) > 0:
        for estado_calculado in estados_calculados.copy():
            for estado in dawg['states']:
                if estado != '{e}':
                    for aresta in dawg['states'][estado]:
                        if estado_calculado in dawg['states'][estado][aresta]:

                            if estado in potencia:
                                potencia[estado].update({estado_calculado: sum(potencia[estado_calculado].values())})
                            else:
                                potencia[estado] = {estado_calculado: sum(potencia[estado_calculado].values())}

                            estados_calculados.append(estado)

            estados_calculados.remove(estado_calculado)

    return _ordenar_potencia(potencia)


def _extend(dawg, S_minus):
    potencias = _calcular_potencia(dawg)
    dawg_copy = copy(dawg)  # para testar sem modificar diretamente

    for aresta in potencias:
        for simbolo in dawg['alphabet']:
            if simbolo in dawg['states'][aresta[0]]:
                if aresta[1] not in dawg['states'][aresta[0]][simbolo]:
                    dawg_copy['states'][aresta[0]][simbolo].append(aresta[1])
            else:
                dawg_copy['states'][aresta[0]][simbolo] = [aresta[1]]

            if dawg_copy != dawg:
                for string_invalida in S_minus:
                    if AFN.testar_string(dawg_copy, string_invalida)[0]:
                        break
                else:
                    dawg = copy(dawg_copy)  # so executa se nao encontrar string invalida

                dawg_copy = copy(dawg)  # para testar sem modificar diretamente

    return dawg


def _build(dawg, estados):
    rotulo_do_estado = ';'.join(estados)
    dawg['states'][rotulo_do_estado] = {}
    novos_estados = []

    alfabeto_local = {}
    for estado in estados:
        simbolo = estado[0]
        if simbolo not in alfabeto_local:
            alfabeto_local[simbolo] = []
        alfabeto_local[simbolo].append(estado)

    for simbolo in alfabeto_local:
        dawg['states'][rotulo_do_estado][simbolo] = []
        proximos_estados = []

        for estado in alfabeto_local[simbolo]:
            proximo_estado = estado[1:]
            if len(proximo_estado) > 0:     # como o estado vazio não é utilizado para descobrir novos estados, ele nao vai para o rotulo
                proximos_estados.append(proximo_estado)
            else:
                dawg['states'][rotulo_do_estado][simbolo].append('{e}') # com o vazio e adicionado a transicao para o estado final

        if len(proximos_estados) > 0:
            dawg['states'][rotulo_do_estado][simbolo].append(';'.join(proximos_estados))
            novos_estados.append(proximos_estados)

    return novos_estados


def contruir_dawg(S_plus, S_minus, alphabet):
    # a utilização de ';' ao inves de ',' se da para nao ter conflito na hora da conversao para AFD
    dawg = {'initial': ';'.join(S_plus), 'final': ['{e}'], 'alphabet': alphabet, 'states': {'{e}': {}}}
    novos_estados = [dawg['initial'].split(';')]

    while len(novos_estados) > 0:
        for novo_estado in novos_estados.copy():
            novos_estados += _build(dawg, novo_estado)

            novos_estados.remove(novo_estado)

    dawg_e = _extend(dawg, S_minus)

    return dawg_e


def _open_dawg_arquivo(path):
    f = open(path, "r")
    lines = f.readlines()
    S_plus = []
    S_minus = []
    alphabet = []

    for x in lines:
        if x == '&':
            break
        string, classe = x.split('\t')
        if '+' in classe:
            S_plus.append(string)
        else:
            S_minus.append(string)

        alphabet += list(string)
    f.close()

    alphabet = list(set(alphabet))

    return [S_plus, S_minus, alphabet]


def _open_teste_dawg_arquivo(path):
    f = open(path, "r")
    lines = f.readlines()
    S_plus = []
    S_minus = []

    for x in lines:
        if 'Classification' in x:
            continue
        classe, string = x.split(',')
        string = string.replace('\n', '')
        if 'non-amyloid' in classe:
            S_minus.append(string)
        else:
            S_plus.append(string)
    f.close()

    return [S_plus, S_minus]


def contruir_dawg_arquivo(path):
    S_plus, S_minus, alphabet = _open_dawg_arquivo(path)

    dawg = contruir_dawg(S_plus, S_minus, alphabet)

    return dawg


def testar_dawg_arquivo(dawg, path):
    [S_plus, S_minus] = _open_teste_dawg_arquivo(path)
    acertos = 0
    total = len(S_plus) + len(S_minus)

    start = time.time()
    for string in S_minus:
        reposta, _ = AFN.testar_string(dawg, string)
        if not reposta:
            acertos += 1

    for string in S_plus:
        reposta, _ = AFN.testar_string(dawg, string)
        if reposta:
            acertos += 1

    end = time.time()
    tempo = end - start

    porcentagem = acertos/total * 100
    print('Porcentagem de acertos: {:.2f}%'.format(porcentagem))
    print('media de tempo: {}s'.format(tempo/total))


def testar_dawg_arquivo_convertendo_AFD(dawg, path):
    [S_plus, S_minus] = _open_teste_dawg_arquivo(path)
    acertos = 0
    total = len(S_plus) + len(S_minus)

    dawg = convert_afn_to_afd(dawg)

    start = time.time()

    for string in S_minus:
        reposta = AFD.testar_string(dawg, string)
        if not reposta:
            acertos += 1

    for string in S_plus:
        reposta = AFN.testar_string(dawg, string)
        if reposta:
            acertos += 1

    end = time.time()
    tempo = end - start

    porcentagem = acertos/total * 100
    print('Porcentagem de acertos convertendo: {:.2f}%'.format(porcentagem))
    print('media de tempo com AFD: {}s'.format(tempo/total))
