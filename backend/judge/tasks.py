import dramatiq

from account.models import User
from submission.models import Submission
from judge.dispatcher import JudgeDispatcher
from utils.shortcuts import DRAMATIQ_WORKER_ARGS


@dramatiq.actor(**DRAMATIQ_WORKER_ARGS())
def judge_task(data):
    uid = Submission.objects.get(id=data["submission_id"]).user_id
    if User.objects.get(id=uid).is_disabled:
        return
    JudgeDispatcher(data).judge()


@dramatiq.actor(**DRAMATIQ_WORKER_ARGS())
def coderun_task(data):
    JudgeDispatcher(data).judge()
