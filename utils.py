import json
import AFN


def _union_dict(a, b):
    new_dict = {**a, **b}       # mescla os dict
    for key in a:
        if key in b:
            new_dict[key] = a[key] + ',' + b[key]
    return new_dict


def _get_new_states(afn, estado):
    afn['initial'] = estado
    funcao_de_transicao = {}
    for simbolo in afn['states'][estado]:
        _, estados_alcancaveis = AFN.testar_string(afn, simbolo)
        novo_estado = ','.join(estados_alcancaveis)
        funcao_de_transicao.update({simbolo: novo_estado})
    return funcao_de_transicao


def convert_afn_to_afd(afn):
    afd = {'initial': afn['initial'], 'final': [], 'states': {}}
    estados_atuais = [afn['initial']]

    while len(estados_atuais) > 0:
        for estado in estados_atuais.copy():
            afd['states'][estado] = {}

            if ',' in estado:                   # se o estado for um conjunto de estados ex: {'q0,q1'}
                funcao_de_transicao = {}
                for estado_item in estado.split(','):  # pega cada estado-item do estado-conjunto, ex: 'q1' e 'q2' separadamente
                    nova_funcao_de_transicao = _get_new_states(afn, estado_item)
                    funcao_de_transicao = _union_dict(funcao_de_transicao, nova_funcao_de_transicao)       # união
            else:
                funcao_de_transicao = _get_new_states(afn, estado)

            for novo_estado in funcao_de_transicao.values():
                if novo_estado not in afd['states']:
                    estados_atuais.append(novo_estado)
            afd['states'][estado] = funcao_de_transicao
            estados_atuais.remove(estado)

    return afd


def open_automaton(path):
    with open(path) as json_file:
        automaton = json.load(json_file)

    return automaton


afn_1 = open_automaton('afn_2.json')
afd = convert_afn_to_afd(afn_1)
print(afd)
