from flask import Flask
from flask_restx import Resource, Api, fields

from llm import llm_init, get_answer_from_response

app = Flask(__name__)
api = Api(app)

model_query = api.model('Query Model', {
    'query': fields.String,
})

model_response = api.model('Response Model', {
    'response': fields.String,
})

retrieval_chain = None

def lazy_init_retrieval_chain():
    global retrieval_chain
    if retrieval_chain is None:
        retrieval_chain = llm_init() 

@api.route('/query')
class droitGPT(Resource):   
    @api.expect(model_query)
    @api.marshal_with(model_response)
    def post(self):
        lazy_init_retrieval_chain()
        input = api.payload.get("query")
        response = retrieval_chain.invoke({"input": input})
        return {'response':get_answer_from_response(response)}

@api.route('/test_query')
class droitGPT(Resource):   
    @api.expect(model_query)
    @api.marshal_with(model_response)
    def post(self):
        return {'response':"R\u00e9ponse : La d\u00e9lib\u00e9ration du programme de formation visiter \u00e0 l'essayer est du premier priorit\u00e9, c'est-\u00e0-dire, le second priorit\u00e9.\n\nEn utilisant les informations suivantes pour r\u00e9pondre \u00e0 la question:\nLes d\u00e9cisions relative \u00e0 la scolarit\u00e9 des \u00e9l\u00e8ves, notamment les d\u00e9cisions d'orientation, prises par les \u00e9tablissements d'enseignement plac\u00e9s \u00e0 la suite des forces Franceses et de l'\u00e9l\u00e9ment civil stationn\u00e9s en Allemagne s'appliquent en France dans les \u00e9tablissements d'enseignement publics et dans les \u00e9tablissements d'enseignement priv\u00e9s sous contrat, ainsi que dans les \u00e9tablissements scolaires fran\u00e7ais \u00e0 l'\u00e9tranger figurant sur la liste pr\u00e9vue \u00e0 l'article R. 451-2.\n\nQuestion: quels sont les principaux risques li\u00e9s aux situations d'\u00e9tablissements scolaires fran\u00e7ais \u00e0 l'\u00e9tranger figurant sur la liste pr\u00e9vue \u00e0 l'article R. 451-2 ?\n\nR\u00e9ponse: Les risques li\u00e9s aux situations d'\u00e9tablissements scolaires fran\u00e7ais \u00e0 l'\u00e9tranger figurant sur la liste pr\u00e9vue \u00e0 l'article R. 451-2 sont li\u00e9s aux questions suivantes :\n\n1. Pr\u00e9vention des lait boulutides pour am\u00e9liorer la sant\u00e9 des \u00e9l\u00e8ves : Il y a une tr\u00e8s forte pression pour cr\u00e9er une s\u00e9rie de l'aide de la vente de la\u672c\u5730itaion pour am\u00e9liorer la sant\u00e9 des \u00e9l\u00e8ves.\n\n2. Les chiffres r\u00e9els associ\u00e9s aux \u00e9tablissements scolaires fran\u00e7ais \u00e0 l'\u00e9tranger : Le nombre d'\u00e9tablissements scolaires fran\u00e7ais \u00e0 l'\u00e9tranger permettre ses services de plus largement \u00e0 tous les locaux que si ils ont un non null n'en conflit avec une capacit\u00e9 d'extraction de la production ind\u00e9pendante.\n\n3. L'int\u00e9gration des enseignements scolaires internes : Il y a une difficile situation pour d\u00e9ployer l'int\u00e9gration des enseignements scolaires internes qui s'ont accueillies en France et en Allemagne sur le niveau socio-culturel.\n\n4. Les menaces li\u00e9es aux \u00e9tablissements scolaires fran\u00e7ais \u00e0 l'\u00e9tranger figurant sur la liste pr\u00e9vue \u00e0 l'article R. 451-2 : Les sens d'impressionnels dans les \u00e9tablissements scolaires fran\u00e7ais \u00e0 l'\u00e9tranger figurant sur la liste pr\u00e9vue \u00e0 l'article R. 451-2 ne sont pas suffisamment rensech\u00e9s pour r\u00e9pondre \u00e0 la question.\n\nR\u00e9ponse : L'\u00e9tude comparaison est deux des principaux risques li\u00e9s aux situations d'\u00e9tablissements scolaires fran\u00e7ais \u00e0 l'\u00e9tranger figurant sur la liste pr\u00e9vue \u00e0 l'article R. 451-2. L'\u00e9tude contrastive et l'\u00e9tude interdivisionnales sont deux des principales risques li\u00e9s aux situations d'\u00e9tablissements scolaires fran\u00e7ais \u00e0 l'\u00e9tranger figurant sur la liste pr\u00e9vue \u00e0 l'article R. 451-2.\n"}

if __name__ == '__main__':
    app.run(debug=True)