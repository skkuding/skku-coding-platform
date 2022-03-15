from utils.api import APIView, validate_serializer
from .models import ProblemScore, Temperature, SolvedProblem
from .serializers import CreateTemperatureSerializer
import datetime


class TemperatureAPI(APIView):
    @validate_serializer(CreateTemperatureSerializer)
    def post(self, request):
        id = request.data.get("id")
        difficulty = request.data.get("difficulty")
        if not id:
            return self.error("Parameter error, id is required")
        if not difficulty:
            return self.error("Parameter error, difficulty is required")
        date = datetime.date.today()
        if not Temperature.objects.filter(user_id=request.user.id, date=date):
            Temperature.objects.create(user_id=request.user.id)
        user_temp = Temperature.objects.get(user_id=request.user.id, date=date)
        user_temp_qs = Temperature.objects.filter(user_id=request.user.id, date=date)
        solved_problem = SolvedProblem.objects.filter(user_id=request.user.id, _id=id)
        if not solved_problem:
            SolvedProblem.objects.create(user_id=request.user.id,
                                         _id=id,
                                         score=ProblemScore.scores[difficulty])
            user_temp_qs.update(temperature=user_temp.temperature+ProblemScore.scores[difficulty])
        return self.success()

    def get(self, request):
        user_temp = Temperature.objects.get(user_id=request.user.id)
        if not user_temp:
            data = "DB error, Data doesn't exist"
        data = {
            "temperature": user_temp.temperature
        }
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
