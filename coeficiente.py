def coeficiente_rendimento(notas):
    ''' Recebe um array com as notas do aluno e retorna o coeficiente de
        rendimento do mesmo.
    '''
    soma_notas = 0

    for nota in notas:
        soma_notas += nota
    
    coeficiente = soma_notas / len(notas)

    return coeficiente