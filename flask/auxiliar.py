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
    exclude = set(string.punctuation+u'\u201c'+u'\u2018'+u'\u201d'+u'\u2022'+u'\u2013')
    palavras=string.join([i["texto"]["value"].lower() for i in msgs])
    palavras = ''.join(ch for ch in palavras if ch not in exclude)
    palavras_=palavras.split()
    stopwords = set(k.corpus.stopwords.words('portuguese'))
    palavras__=[pp for pp in palavras_ if pp not in stopwords]
    fdist_=k.FreqDist(palavras__)
