from flask import Flask
from flask_cors import CORS
from app.routes.main import router as main_router

app = Flask(__name__)
CORS(app)
app.register_blueprint(main_router)

@app.route('/')
def home():
    return {"message": "🎌 Translator ID ⇄ JP aktif dengan keigo refinement"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
