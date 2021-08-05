from .models import Submission
from utils.api import serializers
from utils.serializers import LanguageNameChoiceField


class CreateCodeSerializer(serializers.Serializer):
    # [{"code_id": 1, "locked": False, "code": ""}]
    code_id = serializers.IntegerField(min_value=1)
    locked = serializers.BooleanField()
    code = serializers.CharField(max_length=1024*1024, allow_blank=True, allow_null=True)


class CreateSubmissionSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    language = LanguageNameChoiceField()
    code = serializers.ListField(child=CreateCodeSerializer(), required=False, allow_empty=True)
    contest_id = serializers.IntegerField(required=False)
    captcha = serializers.CharField(required=False)


class ShareSubmissionSerializer(serializers.Serializer):
    id = serializers.CharField()
    shared = serializers.BooleanField()


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
        exclude = ("info", "contest", "ip")


class SubmissionListSerializer(serializers.ModelSerializer):
    problem = serializers.SlugRelatedField(read_only=True, slug_field="_id")
    show_link = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Submission
        exclude = ("info", "contest", "code", "ip")

    def get_show_link(self, obj):
        # No user or anonymous user
        if self.user is None or not self.user.is_authenticated:
            return False
        return obj.check_user_permission(self.user)
