from utils.api import APIView, validate_serializer
from .models import ProblemScore, Temperature, SolvedProblem
from .serializers import CreateTemperatureSerializer


class TemperatureAPI(APIView):
    @validate_serializer(CreateTemperatureSerializer)
    def post(self, request):
        id = request.data.get("id")
        difficulty = request.data.get("difficulty")
        if not id:
            return self.error("Parameter error, id is required")
        if not difficulty:
            return self.error("Parameter error, difficulty is required")
        user_temp = Temperature.objects.get(user_id=request.user.id)
        user_temp_qs = Temperature.objects.filter(user_id=request.user.id)
        if not user_temp:
            Temperature.objects.create(user_id=request.user.id, temperature=0)
        solved_problem = SolvedProblem.objects.filter(user_id=request.user.id, id=id)
        if not solved_problem:
            SolvedProblem.objects.create(user_id=request.user.id,
                                         id=id,
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
        data = "123"
        return self.success(data)
