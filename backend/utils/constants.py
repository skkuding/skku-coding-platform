class Choices:
    @classmethod
    def choices(cls):
        d = cls.__dict__
        return [d[item] for item in d.keys() if not item.startswith("__")]


class ContestType:
    PUBLIC_CONTEST = "Public"
    PASSWORD_PROTECTED_CONTEST = "Password Protected"


class ContestStatus:
    CONTEST_NOT_START = "1"
    CONTEST_ENDED = "-1"
    CONTEST_UNDERWAY = "0"


class ContestRuleType(Choices):
    ACM = "ACM"
    OI = "OI"


class AssignmentStatus:
    ASSIGNMENT_NOT_START = "1"
    ASSIGNMENT_ENDED = "-1"
    ASSIGNMENT_UNDERWAY = "0"


class CacheKey:
    waiting_queue = "waiting_queue"
    contest_rank_cache = "contest_rank_cache"
    website_config = "website_config"
    auth_token_cache = "email_auth/token"
    auth_email_cache = "email_auth/email"


class Difficulty(Choices):
    Level1 = "Level1"
    Level2 = "Level2"
    Level3 = "Level3"
    Level4 = "Level4"
    Level5 = "Level5"
    Level6 = "Level6"
    Level7 = "Level7"


CONTEST_PASSWORD_SESSION_KEY = "contest_password"
