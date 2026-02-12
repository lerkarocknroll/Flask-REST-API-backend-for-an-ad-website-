import pydantic
from flask import jsonify, request
from flask.views import MethodView
from models import Session, AdModel, HTTPError, CreateAdModel, UpdateAdModel

class AdView(MethodView):
    def get(self, id_ad: int):
        with Session() as session:
            ad = session.query(AdModel).filter(AdModel.id == id_ad).first()
            if ad is None:
                raise HTTPError(404, 'Ad not found')
            return jsonify({
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'created_at': ad.created_at.isoformat(),
                'owner': ad.owner,
            })

    def post(self):
        json_data = request.json
        if not json_data:
            raise HTTPError(400, 'No data provided')
        try:
            validated = CreateAdModel(**json_data).model_dump()
        except pydantic.ValidationError as er:
            raise HTTPError(400, er.errors())

        with Session() as session:
            ad = AdModel(**validated)
            session.add(ad)
            session.commit()
            return jsonify({
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'owner': ad.owner,
            }), 201

    def patch(self, id_ad: int):
        json_data = request.json
        if not json_data:
            raise HTTPError(400, 'No data provided')
        try:
            validated = UpdateAdModel(**json_data).model_dump(exclude_unset=True)
        except pydantic.ValidationError as er:
            raise HTTPError(400, er.errors())

        with Session() as session:
            ad = session.query(AdModel).filter(AdModel.id == id_ad).first()
            if ad is None:
                raise HTTPError(404, 'Ad not found')
            for key, value in validated.items():
                setattr(ad, key, value)
            session.commit()
            return jsonify({
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'owner': ad.owner,
            })

    def delete(self, id_ad: int):
        with Session() as session:
            ad = session.query(AdModel).filter(AdModel.id == id_ad).first()
            if ad is None:
                raise HTTPError(404, 'Ad not found')
            session.delete(ad)
            session.commit()
            return jsonify({'status': 'success'})
