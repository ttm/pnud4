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
bows=__builtin__.bows

### derivados:
eg=g.edges()
ed=d.edges(data=True)
ed_=d_.edges(data=True)

def NL(narray):
    return narray/narray.sum()

def recomendaParticipante(destinatario, idd, metodo="topologico",polaridade="ambas",ordenacao="compartimentada"):
    u"""Sistema de recomendação de usuários para outros usuários e comunidades

    Parâmetros
    ----------
    destinatario : {"participante","comunidade","linha_editorial"}, string
        O destinatário é o tipo de entidade a quem está sendo feita a recomendação: participante, comunidade ou linha_editorial. Campo auxiliar "idd" para id do destinatário (comunidade ou participante).
    idd : string
        O idd (id do destinatário) deve ser o identifier do profile: slug do usuario ou da comunidade. É identifier da tabela profiles.
    metodo : {"topologico","textual","hibrido"}, string
        Caso o método seja "topológico", usar somente a rede. Usar relações de força e outras. Caso o método seja "textual", usar somente o texto produzido. Por hora, a medida de similaridade é a distância euclidiana e usar o inverso + alpha arbitrário. Caso o métodos seja "híbrido", usar os dois.
    polaridade : {"similar","dissimilar","ambas"}, string
        A polaridade é de "similar"idade (amigos prováveis, recursos que possuem afinidade) ou de "dissimilar"idade (amigos improváveis ou até de mesmo antagônicos, recursos que destoam e podem incentivar reações dos usuários). Pode-se escolher também "ambas".
    ordenacao : {"compartimentada","embaralhada","intercalada"}, string
        A ordenação em que o cliente as recomendações. Se "compartimentada", o cliente recebe JSON com campos {recomendados, pontuacao, criterio} para cada criterio diferente, com uma pontuacao para cada recomendado. Se "embaralhada", o cliente recebe o JSON como uma sequência de tuplas (recomendado, pontuacao, criterios), para cada recomendacao diferente. Se "intercalada", recebe uma recomendacao de cada criterio, de forma intercalada.
    """
    recomendacoes=[]
    if destinatario=="linha_editorial":
        ###
        # topologico
        # puxa a rede em si, retorna geral
        if metodo in ("topologico","hibrido"):
            wd=d.degree(weight="weight")
            wd_=[(i,wd[i]) for i in wd.keys()]
            wd_.sort(key=lambda x: -x[1])
            recomendados=[i[0] for i in wd_]
            pontuacao=[i[1] for i in wd_]
            criterio="numero de interacoes (forca do participante no grafo de interacao)"
            recomendacoes.append({"recomendados":recomendados,
                                  "pontuacao":pontuacao,
                                  "criterio":criterio})
            ud=d.degree()
            ud_=[(i,ud[i]) for i in ud.keys()]
            ud_.sort(key=lambda x: -x[1])
            recomendados=[i[0] for i in ud_]
            pontuacao=[i[1] for i in ud_]
            criterio="quantidade de participantes com que interagiu (grau do participante no grafo de interacao)"
            recomendacoes.append({"recomendados":recomendados,
                                  "pontuacao":pontuacao,
                                  "criterio":criterio})
            gd=g.degree()
            gd_=[(i,gd[i]) for i in gd.keys()]
            gd_.sort(key=lambda x: -x[1])
            recomendados=[i[0] for i in gd_]
            pontuacao=[i[1] for i in gd_]
            criterio="quantidade de participantes amigos"
            recomendacoes.append({"recomendados":recomendados,
                                  "pontuacao":pontuacao,
                                  "criterio":criterio})


        ###
        # textual
        # usa BoW para comparar os usuarios com a media geral,
        # retorna dos mais típicos e os outliers
    
        ###
        # hibrido
    if destinatario=="participante":
        uri="http://participa.br/profiles/"+idd
        if metodo in ("topologico","hibrido"):
            ###
            # todos os participantes x_n com que interagiu,
            # na ordem decrescente de interação:
            # {d_i}_0^n, I[x_n]>=I[x_(n-1)],
            # com I a intensidade interacao, o número de mensagens trocadas
            if uri in d_.nodes():
                x_n=d_[uri]
                x_n_=[(i,x_n[i]["weight"]) for i in x_n.keys()]
                x_n_.sort(key=lambda x: -x[1])
        
                # é feita sugestão dos participantes que não são amigos:
                # x_n!=g_n, g_n um amigo
                if uri in g.nodes():
                    viz=g.neighbors(uri)
                    x_n_=[i for i in x_n_ if i[0] not in viz]
            recomendados=[i[0] for i in x_n_]
            pontuacao=[i[1] for i in x_n_]
            criterio="numero de interacoes"
            recomendacoes.append({"recomendados":recomendados,
                                  "pontuacao":pontuacao,
                                  "criterio":criterio})
            ###
            # avançado e talvez desnecessário: recomenda usuários
            # com quem os amigos mais interagiram 
            # e q jah n sao amigos do participante que recebe a recomendação
            # pode ficar pesado quando o usuário tiver muitos amigos

            ###
            # achar amigo de amigo, excluir amigos e recomendar
            if uri in g.nodes():
                vizs=g.neighbors(uri)
                vizs_=set(vizs)
                vv=[]
                for viz in vizs:
                    vv+=g.neighbors(viz)
                vv_=list(set(vv))
                candidatos=[(i,vv.count(i)) for i in vv_ if i not in vizs_]
                candidatos.sort(key=lambda x: -x[1])

            recomendados=[i[0] for i in candidatos]
            pontuacao=[i[1] for i in candidatos]
            criterio="mais amigos em comum"
            recomendacoes.append({"recomendados":recomendados,
                                  "pontuacao":pontuacao,
                                  "criterio":criterio})
            ###
            if polaridade in ("dissimilar","ambas"):
                recomendacoesD=[] # para recomendacoes com polaridade dissimilar
                ### maiores geodesicas partindo do destinatario. 
                if uri in g.nodes():
                    caminhos=x.shortest_paths.single_source_shortest_path(g,uri)
                    caminhos_=[caminhos[i] for i in caminhos.keys()]
                    caminhos_.sort(key=lambda x : -len(x))
                    #distantes=[(i[-1],len(i)) for i in caminhos_]
                    recomendados=[i[-1] for i in caminhos_ if len(i)>2]
                    pontuacao=  [len(i) for i in caminhos_ if len(i)>2]
                    criterio="participantes na mesma rede de amizades, mas mais distantes entre si em numero de amizades que os separam"
                    recomendacoesD.append({"recomendados": recomendados,
                                    "pontuacao":pontuacao,
                                    "criterio":criterio})
                # feito para amigos, agora com a rede de interacao
                if uri in d.nodes():
                    caminhos=x.shortest_paths.single_source_shortest_path(d,uri)
                    caminhos_=[caminhos[i] for i in caminhos.keys()]
                    caminhos_.sort(key=lambda x : -len(x))
                    recomendados=[i[-1] for i in caminhos_ if len(i)>2]
                    pontuacao=  [len(i) for i in caminhos_ if len(i)>2]
                    criterio="participantes na mesma rede de amizades, mas mais distantes entre si em numero de interacoes que os separam"
                    recomendacoesD.append({"recomendados":recomendados,
                                        "pontuacao":pontuacao,
                                        "criterio":criterio})
                # participantes de outras componentes conexas com relacao ao destinatario
                if uri in g.nodes():
                    comps=x.connected_components(g)
                    # caso haja duas componentes conexas
                    if len(comps)>1:
                        recomendados=[]
                        # caso sejam exatamente duas componentes:
                        if len(comps)==2:
                           for comp in comps:
                                if uri not in comp:
                                    # recomenda a componente toda
                                    recomendados+=[(i,1) for i in comp]
                                    criterio="participantes da unica componente de amizade disconexa com a do beneficiario que recebe a recomendacao, pontuacao dummy"
                        # caso sejam mais de duas componentes:
                        else:
                            for comp in comps:
                                if uri not in comp:
                                    # escolhe participante da componente
                                    recomendados.append((random.sample(comp,1),len(comp)))
                                    criterio="participante de componente de amizade disconexa com a do beneficiario que recebe a recomendacao, pontuacao eh o numero de participantes da componente"
                        recomendados_=[i[0] for i in recomendados]
                        pontuacao=[i[1] for i in recomendados]
                        recomendacoesD.append({"recomendados": recomendados_,
                                        "pontuacao":pontuacao,
                                        "criterio":criterio})
        if metodo in ("textual","hibrido"):
            # acha amigos
            if uri in g.nodes():
                amigos=g.neighbors(uri)
            else:
                amigos=[]
            # verifica se bow eh vazia
            # listar pelos que tem vocabulário mais semelhante
            # segundo critério de menor distancia euclidiana
            bow=bows[uri]
            if bow[0].N() == 0:
                # bow do destinatario vazia, usando media geral:
                ocorrencias=[h[i] for i in palavras_escolhidas]
                bow=ocorrencias)
                bow=n.array(ocorrencias,dtype=float)
            else:
                bow=n.array(bow[1],dtype=float)
            uris=bows.keys()
            rec=[]
            for uri_ in uris:
                if uri_ != uri and uri_ not in amigos:
                    bow_=n.array(bows[uri_][1],dtype=n.float)
                    distancia=n.sum((NL(bow)-NL(bow_))**2)
                    rec.append((uri_,distancia))
                    rec.sort(key = lambda x: x[1])
            if len(rec)>0:
                recomendados=[i[0] for i in rec]
                pontuacao=[1/(i[1]+1) for i in rec]
                criterio="semelhanca dentre vocabularios E (0,1]. Calculo: semelhanca = 1/(1+distancia^2 das bags of words dos participantes, do vocabulario selecionado)"
                recomendacoes.append({"recomendados":recomendados,
                          "pontuacao":pontuacao,
                          "criterio":criterio})
        if metodo=="hibrido":
            # fazer medida composta de vocabulario e proximidade na rede de interação
            # fazer medida composta de vocabulario e proximidade na rede de amizades
            # pega amigo de amigo, rankeia por media de amigos em comum e vocabulario em comum
        ## polaridade negativa:
            # pega amigo de amigo, rankeia por inverso da media de amigos em comum e vocabulario diferente
            pass
    #####
    # a ordenacao eh por padrao compartimentada e por semelhança
    # primeiro inverter se for dissemelhante ou ambas as polaridades
    if polaridade in ("dissimilar","ambas"):
        try:
            recomendacoesD
        except:
            recomendacoesD=[]
        # inversao das ordenacoes anteriores
        for i in xrange(len(recomendacoes)):
            recomendacoesD.append({})
            recomendacoesD[i]["recomendados"]=recomendacoes[i]["recomendados"][::-1]
            recomendacoesD[i]["pontuacao"]=recomendacoes[i]["pontuacao"][::-1]
            recomendacoesD[i]["criterio"]="INVERTIDO: "+recomendacoes[i]["criterio"]
        if polaridade == "ambas":
            recomendacoes=recomendacoes+recomendacoesD
        else:
            recomendacoes=recomendacoesD
    # o embaralhamento e intercalação são cortezias da api
    if ordenacao=="embaralhada":
        recs=[]
        for i in xrange(len(recomendacoes)):
            for j in xrange(len(recomendacoes[i]["recomendados"])):
                recomendado=recomendacoes[i]["recomendados"][j]
                pontuacao=recomendacoes[i]["pontuacao"][j]
                criterio=recomendacoes[i]["criterio"]
                recs.append((recomendado, pontuacao, criterio))
        random.shuffle(recs)
        recomendacoes=recs
    if ordenacao=="intercalada":
        recs=[]
        cond=1
        cont=0
        while cond:
            for i in xrange(len(recomendacoes)):
                if cont<len(recomendacoes[i]["recomendados"]):
                    recomendado=recomendacoes[i]["recomendados"][cont]
                    pontuacao=recomendacoes[i]["pontuacao"][cont]
                    criterio=recomendacoes[i]["criterio"]
                    recs.append((recomendado, pontuacao, criterio))
            cont+=1
            if cont>=7:
                cond=0
        recomendacoes=recs
    return recomendacoes
def recomendaComunidade(destinatario, idd, metodo="hibrido",polaridade="ambas"):
    # recomenda por vocabulario em comum do usado na comunidade com o participante
    #### puxar dados:
    # texto produzido pela comunidade
    # participantes na comunidade

    # por possuir membros amigos ou que interagiram muito
    # por possuir mais amigos de amigos
    # mais amigos de pessoas com quem interagiu
    # mais pessoas que iteragiram com seus amigos
    # por media de amigos e vocabulario utilizado
    pass
def recomendaTrilha(destinatario, idd, metodo="hibrido",polaridade="mista"):
    # que prazo final nao tenha passado
    # e prazo inicial esteja proximo
    # que possui amigos que colaboraram
    # que possui amigos e pessoas que interagiram com o destinatario
    # cujos textos sao proximos aos do participante
    pass
def recomendaArtigo(destinatario, idd, metodo="hibrido",polaridade="mista"):
    # que seja de amigo ou de pessoa com quem interagiu
    # que tenha vocabulario parecido ou proximo
    # que tenha maior media de ambas
    pass
def recomendaComentario(destinatario, idd, metodo="hibrido",polaridade="mista"):
    # que seja de amigo ou de pessoa com quem interagiu
    # que tenha vocabulario parecido ou proximo
    # que tenha maior media de ambas
    pass
def recomendaPalavra(destinatario, odd, metodo="hibrido", polaridade="mista")
