from assistant.droitGPT import droitGPT_init
from config import Config
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields

app = Flask(__name__)
app.config.from_object(Config())

cors = CORS(app)
api = Api(app)

model_message = api.model(
    "Message",
    {
        "speaker": fields.String,
        "text": fields.String,
    },
)
model_query = api.model(
    "Query Model",
    {
        "input": fields.String,
        "conversation": fields.List(fields.Nested(model_message)),
    },
)

model_response = api.model(
    "Response Model",
    {"response": fields.List(fields.String), "additional_info": fields.String},
)

assistant = None


def lazy_init_retrieval_chain():
    global assistant
    if assistant is None:
        assistant = droitGPT_init()


@api.route("/single_response")
class SingleResponse(Resource):
    @api.expect(model_query)
    @api.marshal_with(model_response)
    def post(self):
        lazy_init_retrieval_chain()
        input = api.payload.get("input")
        conversation = api.payload.get("conversation")
        response, additional_info = assistant.answer(input=input, conversation=conversation)
        return {
            "response": response,
            "additional_info": additional_info,
        }


if __name__ == "__main__":
    if Config.ENV == "development":
        app.run(debug=Config.DEBUG, port=Config.PORT, host=Config.HOST)
    elif Config.ENV == "production":
        # Run the app using Gunicorn
        from gunicorn.app.base import BaseApplication

        class FlaskApp(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    if key in self.cfg.settings and value is not None:
                        self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            "bind": f"{Config.HOST}:{Config.PORT}",
            "workers": Config.WORKERS_NUMBER,
        }

        FlaskApp(app, options).run()
    else:
        raise ValueError("Environment not recoginzed!")
