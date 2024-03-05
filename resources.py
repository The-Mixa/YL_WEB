from flask_restful import reqparse, abort, Resource
from data import db_session
from data.jobs import Jobs
from flask import jsonify


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('job', 'team_leader', 'collaborators', 'work_size',
                                  'start_date', 'end_date', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})
    

class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        job = session.query().all()
        return jsonify({'job': [item.to_dict(
            only=('job', 'team_leader', 'collaborators', 'work_size',
                                  'start_date', 'end_date', 'is_finished')) for item in job]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job = args['job'],
            team_leader = args['team_leader'],
            collaborators = args['collaborators'],
            work_size = args['work_size'],
            start_date = args['start_date'],
            end_date = args['end_date'],
            is_finished = args['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'id': job.id})
    


parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('start_date', required=True)
parser.add_argument('end_date', required=True)
parser.add_argument('is_finished', required=True, type=bool)