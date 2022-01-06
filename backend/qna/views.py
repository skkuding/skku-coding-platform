from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.api import APIView, validate_serializer
from utils.decorators import login_required, ensure_created_by, super_admin_required

from .models import Question, Answer
from .serializers import (  CreateQuestionSerializer,QuestionSerializer,EditQuestionSerializer,
                            AnswerSerializer, CreateAnswerSerializer, EditAnswerSerializer)

class QuestionAPI(APIView):
    @validate_serializer(CreateQuestionSerializer)
    @swagger_auto_schema(
        request_body=CreateQuestionSerializer,
        operation_description="Uploading Question."
    )
    @login_required
    def post(self, request):
      data = request.data
      question = Question.objects.create(**data)
      return self.success(QuestionSerializer(question).data)
 
    @validate_serializer(EditQuestionSerializer)
    @swagger_auto_schema(
        request_body=EditQuestionSerializer,
        operation_description="Edit Question."
    )
    @login_required
    def put(self, request):
      data = request.data
      try:
          question = Question.objects.get(id=data.pop("id"))
          ensure_created_by(question, request.user)
      except Question.DoesNotExist:
          return self.error("Question does not exist")

      for k, v in data.items():
          setattr(question, k, v)
      question.save()
      return self.success(QuestionSerializer(question).data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="unique announcement id"
            ),
        ],
        operation_description="Delete Announcement"
    )
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
                name="assignment_id",
                in_=openapi.IN_QUERY,
                description="Id of assignment to delete",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="question_id",
                in_=openapi.IN_QUERY,
                description="Id of question to delete",
                required=True,
                type=openapi.TYPE_INTEGER,
            )
        ],
        operation_description="Delete question",
    )
    @login_required
    def delete(self, request):
        course_id = request.GET.get("course_id")
        assignment_id = request.GET.get("assignment_id")
        question_id = request.GET.get("question_id")

        if not course_id:
            return self.error("Invalid parameter, course_id is required")
        if not assignment_id:
            return self.error("Invalid parameter, assignment_id is required")

        try:
            question = Question.objects.get(id=question_id)
            ensure_created_by(question, request.user)
        except Question.DoesNotExist:
            return self.error("Question does not exist")

        question.delete()
        return self.success()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        operation_description="Get Question"
    )
    def get(self, request):
        question_id = request.GET.get("id")
        if question_id:
            try:
                question = Question.objects.get(id=question_id)
                return self.success(QuestionSerializer(question).data)
            except Question.DoesNotExist:
                return self.error("Question does not exist")
        question = Question.objects.all().order_by("-create_time")
        
        return self.success(self.paginate_data(request, question, QuestionSerializer))

class AnswerAPI(APIView):
    @swagger_auto_schema(
        request_body=CreateAnswerSerializer,
        operation_description="Create new answer",
        responses={200: AnswerSerializer},
    )
    @validate_serializer(CreateAnswerSerializer)
    @login_required
    def post(self, request):
        data = request.data
        try:
            question = Question.objects.get(id=data.pop("question_id"))
            data["question"] = question
            data["created_by"] = request.user
        except Question.DoesNotExist:
            return self.error("Question does not exist")
        answer = Answer.objects.create(**data)
        answer.update_admin_type(request.user)
        return self.success(AnswerSerializer(answer).data)

    @swagger_auto_schema(
        request_body=EditAnswerSerializer,
        operation_description="Edit answer",
        responses={200: AnswerSerializer},
    )
    @validate_serializer(EditAnswerSerializer)
    @login_required
    def put(self, request):
        data = request.data
        try:
            answer = Answer.objects.get(id=data.pop("id"))
        except:
            return self.error("Answer does not exist")
        if answer.created_by != request.user and not request.user.is_super_admin():
            return self.error("No permission for edit")
        
        answer.content = data["content"]
        answer.save()
        return self.success(AnswerSerializer(answer).data)
        
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="question_id",
                in_=openapi.IN_QUERY,
                description="Unique ID of an question",
                type=openapi.TYPE_INTEGER,
            )
        ],
        operation_description="Get answer list for requesting question",
        responses={200: AnswerSerializer},
    )
    def get(self, request):
        question_id = request.GET.get("question_id")
        if not question_id:
            return self.error("Invalid parameter, id is required")
        try:
            data = Answer.objects.select_related("created_by").filter(question_id=question_id)
            return self.success(AnswerSerializer(data, many=True).data)
        except:
            return self.error("Question does not exist")
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Unique ID of an answer",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")
        try:
            answer = Answer.objects.get(id=id)
        except Answer.DoesNotExist:
            return self.error("Answer does not exists")
        if answer.created_by != request.user and not request.user.is_super_admin():
            return self.error("No permission for deletion")
        answer.delete()
        return self.success()