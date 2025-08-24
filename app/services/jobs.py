from app.extensions import scheduler


def get_all_jobs():
    return scheduler.get_jobs()

def remove_job(task_id: str):
    """Удалить задачу"""
    scheduler.remove_job(task_id)

def pause_job(task_id: str):
    """Поставить задачу на паузу"""
    scheduler.pause_job(task_id)

def resume_job(task_id: str):
    """Возобновить задачу"""
    scheduler.resume_job(task_id)