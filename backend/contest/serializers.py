from utils.api import UsernameSerializer, serializers
from utils.constants import Difficulty

from .models import Contest, ContestAnnouncement, ContestPrize, ContestRuleType
from .models import ACMContestRank, OIContestRank
from group.serializers import GroupSummarySerializer


class CreateOrEditContestPrizeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    color = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=20)
    reward = serializers.CharField(max_length=20)


class ContestPrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestPrize
        fields = "__all__"


class BankFilterSerializer(serializers.Serializer):
    level = serializers.ChoiceField(choices=Difficulty.choices())
    tag = serializers.CharField(allow_blank=True)
    count = serializers.IntegerField()


class CreateContestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    description = serializers.CharField()
    requirements = serializers.ListField(child=serializers.CharField(max_length=128))
    constraints = serializers.ListField(child=serializers.CharField(max_length=128), allow_empty=True)
    allowed_groups = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
    scoring = serializers.CharField()
    prizes = serializers.ListField(child=CreateOrEditContestPrizeSerializer())
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    rule_type = serializers.ChoiceField(choices=[ContestRuleType.ACM, ContestRuleType.OI])
    password = serializers.CharField(allow_blank=True, max_length=32)
    visible = serializers.BooleanField()
    real_time_rank = serializers.BooleanField()
    allowed_ip_ranges = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=True)
    bank_filter = serializers.ListField(child=BankFilterSerializer(), allow_empty=True)
    rank_penalty_visible = serializers.BooleanField()


class EditContestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    description = serializers.CharField()
    requirements = serializers.ListField(child=serializers.CharField(max_length=128))
    constraints = serializers.ListField(child=serializers.CharField(max_length=128), allow_empty=True)
    allowed_groups = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
    scoring = serializers.CharField()
    prizes = serializers.ListField(child=CreateOrEditContestPrizeSerializer())
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    password = serializers.CharField(allow_blank=True, allow_null=True, max_length=32)
    visible = serializers.BooleanField()
    real_time_rank = serializers.BooleanField()
    allowed_ip_ranges = serializers.ListField(child=serializers.CharField(max_length=32))
    bank_filter = serializers.ListField(child=BankFilterSerializer(), allow_empty=True)
    rank_penalty_visible = serializers.BooleanField()


class ContestAdminSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    status = serializers.CharField()
    contest_type = serializers.CharField()
    allowed_groups = GroupSummarySerializer(many=True)
    prizes = ContestPrizeSerializer(many=True)
    is_bank = serializers.BooleanField()

    class Meta:
        model = Contest
        fields = "__all__"


class ContestSerializer(ContestAdminSerializer):
    participants_count = serializers.IntegerField(required=False)
    prizes = ContestPrizeSerializer(many=True)

    class Meta:
        model = Contest
        exclude = ("password", "visible", "allowed_ip_ranges")


class ContestAnnouncementSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = ContestAnnouncement
        fields = "__all__"


class CreateContestAnnouncementSerializer(serializers.Serializer):
    contest_id = serializers.IntegerField()
    problem_id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    content = serializers.CharField()
    visible = serializers.BooleanField()


class EditContestAnnouncementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    problem_id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=128, required=False)
    content = serializers.CharField(required=False, allow_blank=True)
    visible = serializers.BooleanField(required=False)


class ContestPasswordVerifySerializer(serializers.Serializer):
    contest_id = serializers.IntegerField()
    password = serializers.CharField(max_length=30, required=True)


class ACMContestRankSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    prize = ContestPrizeSerializer()

    class Meta:
        model = ACMContestRank
        fields = ["id", "accepted_number", "total_time", "total_penalty", "submission_info", "username", "prize"]

    def __init__(self, *args, **kwargs):
        self.is_contest_admin = kwargs.pop("is_contest_admin", False)
        super().__init__(*args, **kwargs)

    def get_username(self, obj):
        data = UsernameSerializer(obj.user, need_real_name=self.is_contest_admin).data
        username = data["username"]
        if len(username) >= 10:
            username = username[:4]+"****"+username[8:]
        return username


class ACMContestRankNoPenaltySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    prize = ContestPrizeSerializer()

    class Meta:
        model = ACMContestRank
        fields = ["id", "accepted_number", "total_time", "submission_info", "username", "prize"]

    def __init__(self, *args, **kwargs):
        self.is_contest_admin = kwargs.pop("is_contest_admin", False)
        super().__init__(*args, **kwargs)

    def get_username(self, obj):
        data = UsernameSerializer(obj.user, need_real_name=self.is_contest_admin).data
        username = data["username"]
        if len(username) >= 10:
            username = username[:4]+"****"+username[8:]
        return username


class OIContestRankSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = OIContestRank
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.is_contest_admin = kwargs.pop("is_contest_admin", False)
        super().__init__(*args, **kwargs)

    def get_user(self, obj):
        return UsernameSerializer(obj.user, need_real_name=self.is_contest_admin).data


class ACMContesHelperSerializer(serializers.Serializer):
    contest_id = serializers.IntegerField()
    problem_id = serializers.CharField()
    rank_id = serializers.IntegerField()
    checked = serializers.BooleanField()
