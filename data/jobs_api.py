from flask import Blueprint, jsonify, make_response, request

from . import db_session
from .jobs import Jobs

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'news':
                [item.to_dict(
                    only=('job', 'team_leader', 'collaborators', 'work_size',
                          'start_date', 'end_date', 'is_finished')
                ) for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {'job': job.to_dict(only=('job', 'team_leader', 'collaborators', 'work_size',
                                  'start_date', 'end_date', 'is_finished'))}
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'collaborators', 'work_size', 'start_date', 'finish_date', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    job = Jobs(
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        collaborators=request.json['collaborators'],
        work_size=request.json['work_size'],
        start_date=request.json['start_date'],
        finish_date=request.json['finish_date'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def change_job(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'collaborators', 'work_size', 'start_date', 'finish_date', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    job.job = request.json['job']
    job.team_leader = request.json['team_leader'],
    job.collaborators = request.json['collaborators'],
    job.work_size = request.json['work_size'],
    job.start_date = request.json['start_date'],
    job.finish_date = request.json['finish_date'],
    job.is_finished = request.json['is_finished']

    db_sess.commit()
    return jsonify({'id': job.id})
