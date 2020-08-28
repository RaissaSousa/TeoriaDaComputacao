def testar_string(afd, string):
    """
    Testa se um string e aceita pelo automato
    :param afd: automato finito deterministico
    :param string: string a ser testada
    :return: True ou False
    """
    estado_atual = afd['initial']

    for simbolo in string:
        if simbolo in afd['states'][estado_atual]:
            estado_atual = afd['states'][estado_atual][simbolo]
        else:
            return False

    if estado_atual in afd['final']:
        return True

    return False
