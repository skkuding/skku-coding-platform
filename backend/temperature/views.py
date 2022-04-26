from utils.api import APIView, validate_serializer
from .models import ProblemScore, Temperature, SolvedProblem
from problem.models import Problem
from .serializers import CreateTemperatureSerializer
import datetime

def createTemperature(user, date):
    if Temperature.objects.filter(user=user, date=date).exists(): return
    solved_problem = SolvedProblem.objects.filter(user=user)
    solved_problem = list(solved_problem)
    temp = 0
    for t in solved_problem:
        temp += ProblemScore.scores[t.problem.difficulty] / (2 ** ((date - t.solved_time) // 7))
    Temperature.objects.create(user=user, temperature=temp)

class TemperatureAPI(APIView):
    def post(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Parameter error, id is required")
        difficulty = Problem.objects.get(id=id).difficulty
        date = datetime.date.today()
        createTemperature(request.user, date)
        user_temp = Temperature.objects.get(user=request.user, date=date)
        user_temp_qs = Temperature.objects.filter(user=request.user, date=date)
        solved_problem = SolvedProblem.objects.filter(user=request.user, problem=Problem.objects.get(id=id))
        if not solved_problem:
            SolvedProblem.objects.create(user=request.user,
                                         problem=Problem.objects.get(id=id))
            user_temp_qs.update(temperature=user_temp.temperature+ProblemScore.scores[difficulty])
        return self.success()

    def get(self, request):
        date = datetime.date.today()
        createTemperature(request.user, date)
        user_temp = Temperature.objects.get(user=request.user, date=date)
        if not user_temp:
            return self.error("DB error, Data doesn't exist")
        else:
            data = { "temperature": user_temp.temperature }
            return self.success(data)

class RankAPI(APIView):
    def get(self, request):
        date = datetime.date.today()
        for idx, temp in enumerate(list(Temperature.objects.filter(date=date).order_by("-temperature"))):
            if temp.user_id == request.user.id:
                rank = idx + 1
                break
        data = {
            "rank": rank
        }
        return self.success(data)
class TemperatureListAPI(APIView):
    def get(self, request):
        user_temps = Temperature.objects.get(user=request.user)
        data = user_temps
        return self.success(data)

class SolvedProblemListAPI(APIView):
    def get(self, request):
        solved_problems = SolvedProblem.objects.filter(user_id=request.user.id)
        data = solved_problems
        return self.success(data)
class RankListAPI(APIView):
    def get(self, request):
        data = []
        solved_problem = SolvedProblem.objects.filter(user=request.user)
        solved_problem = list(solved_problem)
        return self.success(data)
