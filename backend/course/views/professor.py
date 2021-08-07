from django.http import request
from utils.api import APIView, validate_serializer

from account.models import User
from account.decorators import ensure_created_by, admin_role_required

from ..models import Course, Registration
from ..serializers import (CourseProfessorSerializer, CreateCourseSerializer, EditCourseSerializer,
                            RegisterSerializer, EditRegisterSerializer, RegistrationSerializer, UserListSerializer)

class CourseAPI(APIView):
    @admin_role_required
    def get(self, request):
        cousre_id = request.GET.get("id")

        if not id:
            return self.error("Invalid parameter, id is required")

        if cousre_id:
            try:
                course = Course.objects.get(id=cousre_id)
                ensure_created_by(course, request.user)
                return self.success(CourseProfessorSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Course does not exist")

        courses = Course.objects.filter(created_by=request.user)
        return self.success(self.paginate_data(request, courses, CourseProfessorSerializer))

    @validate_serializer(CreateCourseSerializer)
    @admin_role_required
    def post(self, request):
        data = request.data
        course = Course.objects.create(title=data["title"],
                                        course_code=data["course_code"],
                                        class_number=data["class_number"],
                                        created_by=request.user,
                                        registered_year=data["registered_year"],
                                        semester=data["semester"])
        return self.success(CourseProfessorSerializer(course).data)

    @validate_serializer(EditCourseSerializer)
    @admin_role_required
    def put(self, request):
        data = request.data
        try:
            course = Course.objects.get(id=data.pop("id"))
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        for k, v in data.items():
            setattr(course, k, v)
        course.save()
        return self.success(CourseProfessorSerializer(course).data)

    @admin_role_required
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")
        try:
            course = Course.objects.get(id=id)
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exists")

        course.delete()
        return self.success()


class StudentManagementAPI(APIView):
    @validate_serializer(RegisterSerializer)
    @admin_role_required
    def post(self, request):
        data = request.data
        course_id = data["course_id"]
        user_id = data["user_id"]

        try:
            User.objects.get(id=user_id)
            course = Course.objects.get(id=course_id)
            ensure_created_by(course, request.user)
        except User.DoesNotExist:
            return self.error("User does not exist")
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        try:
            Registration.objects.get(user_id=user_id, course_id=course_id)
            return self.error("User has been already registered to the course")
        except Registration.DoesNotExist:
            registration = Registration.objects.create(user_id=user_id,
                                        course_id=course_id)
        return self.success(RegistrationSerializer(registration).data)

    @admin_role_required
    def get(self, request):
        course_id = request.GET.get("course_id")
        get_students_count = request.GET.get("count")

        if not course_id:
            return self.error("Invalid parameter, course_id is required")

        try: 
            course = Course.objects.get(id=course_id)
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        registration = Registration.objects.filter(course_id=course_id)

        # Return number of total registered students
        if get_students_count:
            return self.success({ 'total_students': registration.count() })

        return self.success(self.paginate_data(request, registration, UserListSerializer))

    @validate_serializer(EditRegisterSerializer)
    @admin_role_required
    def put(self, request):
        data = request.data
        course_id = data["course_id"]

        try:
            registration = Registration.objects.get(id=data.pop("registration_id"))
        except Registration.DoesNotExist:
            return self.error("Register information does not exist")

        try:
            course = Course.objects.get(id=course_id)
            ensure_created_by(course, request.user)
            course = Course.objects.get(id=registration.course_id)
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        try:
            Registration.objects.get(user_id=registration.user_id, course_id=course_id)
            return self.error("User has been already registered to the course")
        except Registration.DoesNotExist:
            for k, v in data.items():
                setattr(registration, k, v)
            registration.save()

        return self.success(RegistrationSerializer(registration).data)

    @admin_role_required
    def delete(self, request):
        id = request.GET.get("registration_id")
        if not id:
            return self.error("Invalid parameter, registration_id is required")

        try:
            registration = Registration.objects.get(id=id)
            course = Course.objects.get(id=registration.course_id)
            ensure_created_by(course, request.user)
        except Registration.DoesNotExist:
            return self.error("Register information does not exists")

        registration.delete()
        return self.success()