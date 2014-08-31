#-*- coding: utf8 -*-
# as duas redes estão no builtin
# incluir a montagem das redes e o bag of words jah na triplificação
def recomendaParticipante(destinatario, idd, metodo="hib",polaridade="mis"):
    u"""Sistema de recomendação de usuários para outros usuários e comunidades

    O destinatário é o tipo de entidade a quem está sendo feita a recomendação: participante, comunidade ou linha_editorial. Campo auxiliar "idd" para id do destinatário (comunidade ou participante).
    O idd (id do destinatário) deve ser o identifier do profile: slug do usuario ou da comunidade. É identifier da tabela profiles.

    Caso o método seja top(ológico), usar somente a rede. Usar relações de força e outras.
    Caso o método seja tex, usar somente o texto produzido. Calcular a distância euclidiana e usar o inverso + alpha arbitrário como medida de similaridade.
    Caso o métodos seja hib, usar os dois.

    A polaridade é de similaridade (amigos prováveis, recursos que possuem afinidade) ou de dissimilaridade (amigos improváveis ou até de meios antagônicos, recursos que destoam e podem incentivar reações dos usuários)"""
    # puxa rede de amizades
    # TTM por enquanto está na inicialização que faz o __builtin__:
    # 1) fazer cpickle e tb 2) versão que triplifica e acrescenta no jena.
    # por fim, 3) implementar no plugin de triplificação se do interesse do Noosfero ou do participa.br
    g=__builtin__.g
    # tb com rede direcionada, de interação
    d=__builtin__.d
    # ve todos que interagiu, na ordem crescente de interação:
    # {x_n}_0^n, I(x_n)>=I(x_(n-1_))
    # sugere os participantes que não são amigos, na ordem

    ###
    # avançado e talvez desnecessário: recomenda usuários
    # com quem os amigos mais interagiram 
    # e q jah n sao amigos do participante que recebe a recomendação
    # pode ficar pesado quando o usuário tiver muitos amigos

    ###
    # achar amigo de amigo, excluir amigos e recomendar

    ############
    h=__builtin__.fdist_
    hs=__builtin__.bows
    palavras_escolhidas=__builtin__.palavras_escolhidas
    # achar 
    
    return "ba"
def recomendaComunidade(destinatario, idd, metodo="hib",polaridade="mis"):
    pass
def recomendaTrilha(destinatario, idd, metodo="hib",polaridade="mis"):
    pass
def recomendaArtigo(destinatario, idd, metodo="hib",polaridade="mis"):
    pass
def recomendaComentario(destinatario, idd, metodo="hib",polaridade="mis"):
    pass
