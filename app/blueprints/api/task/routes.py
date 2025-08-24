from flask import jsonify

from app import services
from app.blueprints.api.task import task


@task.route("/<job_name>/logs")
def get_logs(job_name):
    logs = services.get_job_logs_by_id(job_name)

    return jsonify({
        "job_name": job_name,
        "logs": [
            {
                "message": log.message,
                "is_success": True if log.is_success else False,
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ]
    })