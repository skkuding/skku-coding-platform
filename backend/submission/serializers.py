from .models import Submission
from account.models import User
from utils.api import serializers
from utils.serializers import LanguageNameChoiceField
from utils.api._serializers import UsernameSerializer


class CreateSubmissionSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    language = LanguageNameChoiceField()
    code = serializers.CharField(max_length=1024 * 1024)
    contest_id = serializers.IntegerField(required=False)
    assignment_id = serializers.IntegerField(required=False)
    captcha = serializers.CharField(required=False)


class ShareSubmissionSerializer(serializers.Serializer):
    id = serializers.CharField()
    shared = serializers.BooleanField()


class EditSubmissionScoreSerializer(serializers.Serializer):
    id = serializers.CharField()
    score = serializers.IntegerField(min_value=0, max_value=100)


class SubmissionModelSerializer(serializers.ModelSerializer):
    problem_name = serializers.CharField(source="problem.title")

    class Meta:
        model = Submission
        fields = "__all__"


# Serializer that does not display submission info, used for ACM rule_type
class SubmissionSafeModelSerializer(serializers.ModelSerializer):
    problem = serializers.SlugRelatedField(read_only=True, slug_field="_id")

    class Meta:
        model = Submission
        exclude = ("info", "contest", "assignment", "ip")


class SubmissionListSerializer(serializers.ModelSerializer):
    problem = serializers.SlugRelatedField(read_only=True, slug_field="_id")
    show_link = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Submission
        exclude = ("info", "contest", "assignment", "code", "ip")

    def get_show_link(self, obj):
        # No user or anonymous user
        if self.user is None or not self.user.is_authenticated:
            return False
        return obj.check_user_permission(self.user)


class SubmissionListProfessorSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        try:
            user = User.objects.get(id=obj.user_id)
        except User.DoesNotExist:
            return None
        return UsernameSerializer(user).data

    class Meta:
        model = Submission
        exclude = ("contest", "assignment", "shared", "ip")
