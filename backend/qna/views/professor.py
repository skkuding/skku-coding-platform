from utils.decorators import admin_role_required
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.api import APIView
from ..serializers import QuestionSerializer
from ..models import Question


class QuestionAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="course_id",
                in_=openapi.IN_QUERY,
                description="Id of course",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="question_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        operation_description="Get Question"
      )
    @admin_role_required
    def get(self, request):
        course_id = request.GET.get("course_id")
        question_id = request.GET.get("question_id")
        if question_id:
            try:
                question = Question.objects.get(id=question_id, course_id=course_id)
                return self.success(QuestionSerializer(question).data)
            except Question.DoesNotExist:
                return self.error("Question does not exist")
        question = Question.objects.all().order_by("-create_time")

        return self.success(self.paginate_data(request, question, QuestionSerializer))
