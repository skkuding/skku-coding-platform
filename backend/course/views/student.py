from utils.api import APIView

from ..models import Course, Takes
from ..serializers import CourseSerializer, CourseListSerializer, TakesSerializer

class CourseAPI(APIView):
    def get(self, request):
        cousre_id = request.GET.get("id")
        user_id = request.GET.get("user_id")
        if cousre_id:
            try:
                course = Course.objects.get(id=cousre_id)
                return self.success(CourseSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Contest does not exist")

        courses = Takes.objects.filter(user_id=user_id)

        return self.success(self.paginate_data(request, courses, CourseListSerializer))
