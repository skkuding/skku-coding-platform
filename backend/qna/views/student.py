from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.api import APIView, validate_serializer
from utils.decorators import login_required, ensure_created_by

from ..models import Question, Answer
from course.models import Course
from ..serializers import (CreateQuestionSerializer, QuestionSerializer, EditQuestionSerializer,
                           AnswerSerializer, CreateAnswerSerializer, EditAnswerSerializer)


class QuestionAPI(APIView):
    @validate_serializer(CreateQuestionSerializer)
    @swagger_auto_schema(
        request_body=CreateQuestionSerializer,
        operation_description="Uploading Question.",
        responses={200: QuestionSerializer},
    )
    @login_required
    def post(self, request):
        data = request.data
        course_id = request.data["course_id"]

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exists")

        data["created_by"] = request.user
        data["course"] = course
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
        except Question.DoesNotExist:
            return self.error("Question does not exist")

        if not request.user.is_question_admin(question):
            return self.error("No permission for this action")

        for k, v in data.items():
            setattr(question, k, v)
        question.save()
        return self.success(QuestionSerializer(question).data)

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
        question_id = request.GET.get("question_id")

        if not question_id:
            return self.error("Invalid parameter, question_id is required")

        try:
            question = Question.objects.get(id=question_id, course_id=course_id)
            ensure_created_by(question, request.user)
        except Question.DoesNotExist:
            return self.error("Question does not exist")

        question.delete()
        return self.success()

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
            if not question.is_open:
                return self.error("You cannot answer resolved question")
            data["question"] = question
            data["created_by"] = request.user
        except Question.DoesNotExist:
            return self.error("Question does not exist")

        if data.pop("closure", False):
            if not request.user.is_question_admin(question):
                return self.error("No permission for closure")
            question.is_open = False
            question.save()

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
        except Answer.DoesNotExist:
            return self.error("Answer does not exist")
        if answer.created_by != request.user and not request.user.is_super_admin():
            return self.error("No permission for this action")

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
        data = Answer.objects.select_related("created_by").filter(question_id=question_id)
        return self.success(AnswerSerializer(data, many=True).data)

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
    @login_required
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")
        try:
            answer = Answer.objects.get(id=id)
        except Answer.DoesNotExist:
            return self.error("Answer does not exist")
        if answer.created_by != request.user and not request.user.is_super_admin():
            return self.error("No permission for this action")
        answer.delete()
        return self.success()
