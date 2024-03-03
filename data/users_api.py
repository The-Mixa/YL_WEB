from flask import Blueprint, jsonify, make_response, request

from . import db_session
from .users import User

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(
                    only=('id', 'surname', 'name', 'age', 'position',
                          'speciality', 'address', 'email', 'city_from')
                ) for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {'user': user.to_dict(only=('surname', 'name', 'age', 'position',
                                    'speciality', 'address', 'email', 'city_from'))}
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email', 'city_from']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        address=request.json['address'],
        email=request.json['email'],
        speciality=request.json['speciality'],
        city_from=request.json['city_from']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def change_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'positoin',
                  'speciality', 'address', 'email']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    user.surname=request.json['surname']
    user.name=request.json['name']
    user.age=request.json['age']
    user.position=request.json['position']
    user.address=request.json['address']
    user.email=request.json['email']
    user.speciality=request.json['speciality'],
    city_from = request.json['city_from']

    db_sess.commit()
    return jsonify({'id': user.id})
