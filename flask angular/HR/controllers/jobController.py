from dao.database import init_db
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from sqlalchemy.orm import Session
from ..services.jobService import JobService
from dao.database import get_db, init_db

# Namespace for Job API
job_controller = Namespace('jobs', description='Job Management API')

# Job Model for Swagger
job_model = job_controller.model('Job', {
    'ID': fields.String(required=True, description='The unique identifier of the job'),
    'job_description': fields.String(required=False, description='The description of the job'),
})

# Function to initialize database
def set_database():
    init_db('hr2')

# API Routes
@job_controller.route('/')
class JobList(Resource):
    @job_controller.doc('get_all_jobs')
    @job_controller.response(200, 'Success', [job_model])
    def get(self):
        """Fetch all jobs."""
        set_database()
        with next(get_db()) as db:  # Open database session
            jobs = JobService.get_all_jobs(db)
            return jsonify(jobs)

    @job_controller.doc('create_job')
    @job_controller.expect(job_model, validate=True)
    @job_controller.response(201, 'Job created successfully', job_model)
    def post(self):
        """Create a new job."""
        job_data = request.json
        set_database()
        with next(get_db()) as db:  # Open database session
            new_job = JobService.create_job(db, job_data)
            return jsonify(new_job), 201


@job_controller.route('/<string:Id_job>')
@job_controller.param('Id_job', 'The unique identifier of the job')
class JobDetail(Resource):
    @job_controller.doc('get_job_by_id')
    @job_controller.response(200, 'Success', job_model)
    @job_controller.response(404, 'Job not found')
    def get(self, Id_job):
        """Fetch a job by its ID."""
        set_database()
        with next(get_db()) as db:  # Open database session
            job = JobService.get_job_by_id(db, Id_job)
            if job:
                return jsonify(job)
            return {'message': 'Job not found'}, 404

    @job_controller.doc('update_job')
    @job_controller.expect(job_model, validate=False)
    @job_controller.response(200, 'Job updated successfully', job_model)
    @job_controller.response(404, 'Job not found')
    def put(self, Id_job):
        """Update an existing job."""
        set_database()
        updated_data = request.json
        with next(get_db()) as db:  # Open database session
            updated_job = JobService.update_job(db, Id_job, updated_data)
            if updated_job:
                return jsonify(updated_job)
            return {'message': 'Job not found'}, 404

    @job_controller.doc('delete_job')
    @job_controller.response(204, 'Job deleted successfully')
    @job_controller.response(404, 'Job not found')
    def delete(self, Id_job):
        """Delete a job."""
        set_database()
        with next(get_db()) as db:  # Open database session
            deleted_job = JobService.delete_job(db, Id_job)
            if deleted_job:
                return '', 204
            return {'message': 'Job not found'}, 404
