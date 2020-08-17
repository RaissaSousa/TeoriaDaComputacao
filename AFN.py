from modelo_automato import automaton


def verificar_e_closure(afn, estado_atual):
    """
    Verificar se ha estados alcancaveis através de transicoes e-closure
    a partir do estado atual.
    :param afn: automato finito nao deterministico
    :param estado_atual:
    :return: lista de estados alcancaveis concatenado com o estado atual
    """
    estados_atuais = [estado_atual]
    estados_e_closure = [estado_atual]

    while len(estados_atuais) > 0:
        for estado in estados_atuais.copy():
            if 'e' in afn['states'][estado]:
                transacoes_e_closure = afn['states'][estado]['e']

                for estado_alcancavel in transacoes_e_closure:
                    if estado_alcancavel not in estados_e_closure:
                        estados_atuais.append(estado_alcancavel)
                        estados_e_closure.append(estado_alcancavel)

            estados_atuais.remove(estado)

    return estados_e_closure


def testar_string(afn, string):
    """
    Testa se um string e aceita pelo automato
    :param afn: automato finito nao deterministico
    :param string: string a ser testada
    :return: True ou False
    """
    estados_atuais = [afn['initial']]

    for simbolo in string:
        proximos_estados = []

        for estado_atual in estados_atuais:
            estados_atuais_alcancaveis = verificar_e_closure(afn, estado_atual)

            for estado in estados_atuais_alcancaveis:
                if simbolo in afn['states'][estado]:
                    proximos_estados += afn['states'][estado][simbolo]

        estados_atuais = proximos_estados

    for estado in estados_atuais:
        if estado in afn['final']:
            return True

    return False


check = testar_string(automaton, '0110')
print(check)