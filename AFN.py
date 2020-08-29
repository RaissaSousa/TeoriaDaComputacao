def verificar_e_closure(afn, estado_atual):
    """
    Verificar se ha estados alcancaveis através de transicoes e-closure
    a partir do estado atual.
    :param afn: automato finito nao deterministico
    :param estado_atual:
    :return: lista de estados alcancaveis concatenado com o estado atual
    """
    estados_para_testar = [estado_atual]
    estados_encontrados = [estado_atual]

    while len(estados_para_testar) > 0:
        for estado in estados_para_testar.copy():
            if 'e' in afn['states'][estado]:
                transacoes_e_closure = afn['states'][estado]['e']

                for estado_alcancavel in transacoes_e_closure:
                    if estado_alcancavel not in estados_encontrados:
                        estados_para_testar.append(estado_alcancavel)
                        estados_encontrados.append(estado_alcancavel)

            estados_para_testar.remove(estado)

    return estados_encontrados


def testar_string(afn, string):
    """
    Testa se um string e aceita pelo automato
    :param afn: automato finito nao deterministico
    :param string: string a ser testada
    :return: True ou False, ultimos estados acessados
    """
    estados_atuais = [afn['initial']]

    for simbolo in string:
        proximos_estados = []

        for estado_atual in estados_atuais:
            estados_atuais_alcancaveis = verificar_e_closure(afn, estado_atual)

            for estado in estados_atuais_alcancaveis:
                if simbolo in afn['states'][estado]:
                    proximos_estados += afn['states'][estado][simbolo]  # mescla as duas listas

        estados_atuais = proximos_estados

    for estado in estados_atuais:
        if estado in afn['final']:
            return True, estados_atuais

    return False, estados_atuais
