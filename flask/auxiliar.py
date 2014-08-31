PREFIX="""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ops: <http://purl.org/socialparticipation/ops#>
PREFIX opa: <http://purl.org/socialparticipation/opa#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX tsioc: <http://rdfs.org/sioc/types#>
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX schema: <http://schema.org/>"""

def fazRedeAmizades():
    q="""SELECT DISTINCT ?aname ?bname
       WHERE {
          ?a foaf:knows ?b .
          ?a foaf:name ?aname .
          ?b foaf:name ?bname .
       }"""
    sparql=SPARQLWrapper(URL_ENDPOINT_)
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    g=x.Graph()
    for amizade in results["results"]["bindings"]:
        nome1=amizade["aname"]["value"]
        nome2=amizade["bname"]["value"]
        g.add_edge(nome1,nome2)
    __builtin__.g=g


def fazRedeInteracao():
    q="""SELECT DISTINCT ?aname ?bname
       WHERE {
           ?comentario dc:type tsioc:Comment.
           ?participante1 ops:performsParticipation ?comentario.
           ?participante1 foaf:name ?aname.
           ?artigo sioc:has_reply ?comentario.
           ?participante2 ops:performsParticipation ?artigo.
           ?participante2 foaf:name ?bname.
       }"""
    sparql=SPARQLWrapper(URL_ENDPOINT_)
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    d=x.DiGraph()
    for interacao in results["results"]["bindings"]:
        nome_chegada=interacao["aname"]["value"]
        nome_partida=interacao["bname"]["value"]
        if (nome_partida,nome_chegada) in d.edges():
            d[nome_partida][nome_chegada]["weight"]+=1
        else:
            d.add_edge(nome_partida,nome_chegada,weight=1.)
    __builtin__.d=d

def fazBoW():
    """Faz Bag of Words de todos os comentários do site"""
    q="SELECT ?comentario ?titulo ?texto WHERE \
               {?comentario dc:type tsioc:Comment.\
              OPTIONAL {?comentario dc:title ?titulo . }\
               OPTIONAL {?comentario schema:text ?texto .}}"
    sparql=SPARQLWrapper(URL_ENDPOINT_)
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    msgs_=results["results"]["bindings"]
    msgs=[mm for mm in msgs_ if ("titulo" not in mm.keys()) or
          (("teste de stress" not in mm["titulo"]["value"].lower())
          and ("comunidade de desenvolvedores e nesse caso, quanto mais"
               not in mm["texto"]["value"].lower()))]
    palavras=string.join([i["texto"]["value"].lower() for i in msgs])
    palavras = ''.join(ch for ch in palavras if ch not in EXCLUDE)
    palavras_=palavras.split()
    palavras__=[pp for pp in palavras_ if pp not in STOPWORDS]
    fdist_=k.FreqDist(palavras__)
    # escolhendo as 400 palavras mais incidentes para referência
    palavras_escolhidas=fdist_.keys()[:400]
    __builtin__.palavras_escolhidas=palavras_escolhidas
    __builtin__.fdist_=fdist_

def fazBoWs():
    """Faz Bag of Words de cada usuário"""
    # puxa todos os usuarios
    q="""SELECT DISTINCT ?participante
           WHERE {
              ?foo dc:contributor ?participante .
           }"""
    sparql=SPARQLWrapper(URL_ENDPOINT_)
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    participantes_=results["results"]["bindings"]
    participantes=[i["participante"]["value"] for i in participantes_]
    # inicia loop
    if "palavras_escolhidas" not in __builtin__.keys():
        print(u"rode BoW antes, para saber do vocabulário geral do portal")
    else:
        palavras_escolhidas=__builtin__.palavras_escolhidas
    bows={}
    for participante in participantes:
        # puxa todos os comentarios de cada usuario
        # e os article bodys
        q="""SELECT DISTINCT ?abody ?cbody
             WHERE {
                 <%s> ops:performsParticipation ?participacao.
                 OPTIONAL { ?participacao schema:articleBody ?abody. }
                 OPTIONAL { ?participacao schema:text ?cbody. }
             }"""%(uri,)
        sparql = SPARQLWrapper("http://localhost:82/participabr/query")
        sparql.setQuery(PREFIX+q)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        results_=results["results"]["bindings"]
        textos1=[i["cbody"]["value"] for i in results_ if "cbody" in i.keys()]
        textos2=[i["abody"]["value"] for i in results_ if "abody" in i.keys()]
        textos=textos1+textos2
        texto=string.join(textos).lower()
        texto_= ''.join(ch for ch in texto if ch not in EXCLUDE)
        texto__=texto_.split()
        texto___=[pp for pp in texto__ if pp not in STOPWORDS]
        fdist=k.FreqDist(texto___)
        ocorrencias=[fdist[i] for i in palavras_escolhidas]
        bows[participante]=(fdist,ocorrencias)

        # faz BoW e guarda num dict
