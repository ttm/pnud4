#-*- coding: utf8 -*-
import __builtin__, networkx as x
# incluir a montagem das redes e o bag of words jah na triplificação
# TTM por enquanto está na inicialização que faz o __builtin__:
# 1) fazer cpickle e tb 2) versão que triplifica e acrescenta no jena.
# Por fim, 3) implementar no plugin de triplificação se do interesse do Noosfero ou do participa.br
# puxa rede de amizades
g=__builtin__.g
# tb com rede direcionada, de interação
d=__builtin__.d
d_=x.Graph()
efoo=d.edges(data=True)
for e in efoo:
    if d_.has_edge(e[0],e[1]):
        d_[e[0]][e[1]]["weight"]+=e[2]["weight"]
    else:
        d_.add_edge(e[0],e[1],weight=e[2]["weight"])
# histograma de palavras e as palavras mais usadas:
h=__builtin__.fdist_
palavras_escolhidas=__builtin__.palavras_escolhidas
# histograma de cada participante:
hs=__builtin__.bows

### derivados:
eg=g.edges()
ed=d.edges(data=True)
ed_=d_.edges(data=True)

def recomendaParticipante(destinatario, idd, metodo="hib",polaridade="mis"):
    u"""Sistema de recomendação de usuários para outros usuários e comunidades

    O destinatário é o tipo de entidade a quem está sendo feita a recomendação: participante, comunidade ou linha_editorial. Campo auxiliar "idd" para id do destinatário (comunidade ou participante).
    O idd (id do destinatário) deve ser o identifier do profile: slug do usuario ou da comunidade. É identifier da tabela profiles.

    Caso o método seja top(ológico), usar somente a rede. Usar relações de força e outras.
    Caso o método seja tex, usar somente o texto produzido. Calcular a distância euclidiana e usar o inverso + alpha arbitrário como medida de similaridade.
    Caso o métodos seja hib, usar os dois.

    A polaridade é de similaridade (amigos prováveis, recursos que possuem afinidade) ou de dissimilaridade (amigos improváveis ou até de meios antagônicos, recursos que destoam e podem incentivar reações dos usuários)"""

    if metodo=="top":
        ###
        # todos os participantes x_n com que interagiu,
        # na ordem decrescente de interação:
        # {d_i}_0^n, I[x_n]>=I[x_(n-1)],
        # com I a intensidade interacao, o número de mensagens trocadas
        #x_ni=d.in_edges("http://participa.br/profiles/"+idd,data=True)
        #x_no=d.out_edges("http://participa.br/profiles/"+idd,data=True)
        uri="http://participa.br/profiles/"+idd
        if uri in d_.nodes():
            x_n=d_[uri]
            x_n_=[(i,x_n[i]["weight"]) for i in in x_n.keys()]
            x_n_.sort(key=lambda x: -x[1])
    
            # é feita sugestão dos participantes que não são amigos:
            # x_n!=g_n, g_n um amigo
            if uri in g.nodes():
                viz=g.neighbors(uri)
                x_n_=[i for i in x_n_ if i[0] not in viz]


        ###
        # avançado e talvez desnecessário: recomenda usuários
        # com quem os amigos mais interagiram 
        # e q jah n sao amigos do participante que recebe a recomendação
        # pode ficar pesado quando o usuário tiver muitos amigos

        ###
        # achar amigo de amigo, excluir amigos e recomendar
        if uri in g.nodes():
            vizs=g.neighbors[uri]
            vizs_=set(vizs)
            vv=[]
            for viz in vizs:
                vv+=g.neighbors(viz)
            vv_=list(set(vv))
            candidatos=[(i,vv.count(i)) for i in vv_ if i not in vizs_]
            candidatos.sort(key=lambda x: -x[1])


        ###
        # polaridade negativa: maiores geodesicas partido do destinatario
	# tanto para amigos quanto de interacao
        # inversao das ordenacoes anteriores
        # amigos sem amigos algum ou de componentes disconexas com a do destinatario

    if metodo=="tex":
        # listar pelos que tem vocabulário mais semelhante
        # segundo critério de menor distancia euclidiana
        # negativo: listar pelo criterio de maior distância euclidiana
        pass
    if metodo=="hib":
        # fazer medida composta de vocabulario e proximidade na rede de interação
        # fazer medida composta de vocabulario e proximidade na rede de interação e de amizades
        # pega amigo de amigo, rankeia por media de amigos em comum e vocabulario em comum
	## polaridade negativa:
        # pega amigo de amigo, rankeia por inverso da media de amigos em comum e vocabulario diferente
        pass
    return "ba"
def recomendaComunidade(destinatario, idd, metodo="hib",polaridade="mis"):
    # recomenda por vocabulario em comum do usado na comunidade com o participante
    # por possuir membros amigos ou que interagiram muito
    # por possuir mais amigos de amigos
    # mais amigos de pessoas com quem interagiu
    # mais pessoas que iteragiram com seus amigos
    # por media de amigos e vocabulario utilizado
    pass
def recomendaTrilha(destinatario, idd, metodo="hib",polaridade="mis"):
    # que prazo final nao tenha passado
    # e prazo inicial esteja proximo
    # que possui amigos que colaboraram
    # que possui amigos e pessoas que interagiram com o destinatario
    # cujos textos sao proximos aos do participante
    pass
def recomendaArtigo(destinatario, idd, metodo="hib",polaridade="mis"):
    # que seja de amigo ou de pessoa com quem interagiu
    # que tenha vocabulario parecido ou proximo
    # que tenha maior media de ambas
    pass
def recomendaComentario(destinatario, idd, metodo="hib",polaridade="mis"):
    # que seja de amigo ou de pessoa com quem interagiu
    # que tenha vocabulario parecido ou proximo
    # que tenha maior media de ambas
    pass
