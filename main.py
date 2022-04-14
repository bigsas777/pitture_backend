from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_pitture.db'
db = SQLAlchemy(app)

class ModelPittura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    codice_hex = db.Column(db.String(7), nullable=False)
    disponibilita = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Pittura(id = {this.id}, nome = {nome}, HEX = {codice_hex}, Disponibilità = {disponibilita} litri)"


# Pittura
pitt_put_args = reqparse.RequestParser()
pitt_put_args.add_argument("nome", type=str, help="Nome della pittura richiesto", required=True)
pitt_put_args.add_argument("codice_hex", type=str, help="Codice esadecimale del colore richiesto", required=True)
pitt_put_args.add_argument("disponibilita", type=int, help="Disponibilità in magazzino in litri richiesta", required=True)

pitt_update_args = reqparse.RequestParser()
pitt_update_args.add_argument("nome", type=str, help="Nome della pittura")
pitt_update_args.add_argument("codice_hex", type=str, help="Codice esadecimale del colore")
pitt_update_args.add_argument("disponibilita", type=int, help="Disponibilità in magazzino in litri")

resource_field = {
    'id': fields.Integer,
    'nome': fields.String,
    'codice_hex': fields.String,
    'disponibilita': fields.Integer
}

class Pittura(Resource):
    @marshal_with(resource_field) # Decorator
    def get(self, id_pitt):

        if id_pitt == 'all':
            result = ModelPittura.query.all()
        elif id_pitt.isdigit():
            id_pitt = eval(id_pitt)
            result = ModelPittura.query.filter_by(id=id_pitt).first()
        else:
            abort(404, message='ID richiesto non valido...') # Codice 404, elemento non trovato

        if not result:
            abort(404, message='Impossibile trovare una pittura con questo ID...') # Codice 404, elemento non trovato
            
        return result

    @marshal_with(resource_field)
    def put(self, id_pitt):
        args = pitt_put_args.parse_args()
        result = ModelPittura.query.filter_by(id=id_pitt).first()
        if result:
            abort(409, message="ID della pittura già in uso...")
        pittura = ModelPittura(id=id_pitt, nome=args['nome'], codice_hex=args['codice_hex'], disponibilita=args['disponibilita'])
        db.session.add(pittura)
        db.session.commit()

        return pittura, 201 # Codice 201, oggetto creato con successo

    def patch(self, id_pitt):
        args = pitt_update_args.parse_args()
        result = ModelPittura.query.filter_by(id=id_pitt).first()
        if not result:
            abort(404, message="Pittura inesistente...")

api.add_resource(Pittura, "/pitture/<string:id_pitt>")


if __name__ == "__main__":
    app.run()
