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

if __name__ == '__main__':
    app.run(debug=True)