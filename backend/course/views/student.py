from utils.api import APIView
from account.decorators import login_required

from ..models import Course, Registration
from ..serializers import CourseSerializer, CourseStudentSerializer

class CourseAPI(APIView):
    @login_required
    def get(self, request):
        course_id = request.GET.get("id")
        user_id = request.user.id

        if not id:
            return self.error("Invalid parameter, id is required")

        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                Registration.objects.get(user_id=user_id, course_id=course_id)
                return self.success(CourseSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Course does not exist")
            except Registration.DoesNotExist:
                return self.error("Invalid access, not registered user")

        courses = Registration.objects.filter(user_id=user_id)

        return self.success(self.paginate_data(request, courses, CourseStudentSerializer))
