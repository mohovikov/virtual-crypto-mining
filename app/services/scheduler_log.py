from app.extensions import db
from app.models import SchedulerLog


def get_all_jobs_logs():
    return SchedulerLog.query.all()

def get_job_logs_by_id(job_name: str, limit: int = 20):
   return (SchedulerLog.query
        .filter_by(job_name=job_name)
        .order_by(SchedulerLog.created_at.desc())
        .limit(limit)
        .all())

def add_scheduler_log(job_name: str, message: str, is_success: bool = True):
    data = SchedulerLog(
        job_name=job_name,
        message=message,
        is_success=is_success
    )
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print(ex)