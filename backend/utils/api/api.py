import functools
import io
import json
import logging

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

logger = logging.getLogger("")


class APIError(Exception):
    def __init__(self, msg, err=None):
        self.err = err
        self.msg = msg
        super().__init__(err, msg)


class ContentType(object):
    json_request = "application/json"
    json_response = "application/json;charset=UTF-8"
    url_encoded_request = "application/x-www-form-urlencoded"
    multipart_request = "multipart/form-data"
    binary_response = "application/octet-stream"


class JSONResponse(object):
    content_type = ContentType.json_response

    @classmethod
    def response(cls, data):
        resp = HttpResponse(json.dumps(data, indent=4), content_type=cls.content_type)
        resp.data = data
        return resp


class APIView(View):
    """
    The parent class of Django view, and the usage of django-rest-framework is basically the same
      - request.data to get parsed json or urlencoded data, dict type
      - self.success, self.error and self.invalid_serializer can be modified according to industry needs,
        Written in the parent class is to develop a unified writing for different people, and no longer use your own success/error format
      - self.response returns a django HttpResponse, which is implemented in self.response_class
      - The parse request class needs to be defined in request_parser, currently only supports json and urlencoded types, used to parse the requested data
    """
    response_class = JSONResponse
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def _get_request_data(self, request):
        if request.method not in ["GET", "DELETE"]:
            body = request.body
            content_type = request.META.get("CONTENT_TYPE")
            if not content_type:
                raise ValueError("content_type is required")
            for parser in self.parser_classes:
                if content_type.startswith(parser.media_type):
                    break
            # else means the for loop is not interrupted by break
            else:
                raise ValueError("unknown content_type '%s'" % content_type)
            if body:
                if parser == JSONParser:
                    return parser().parse(io.BytesIO(body))
                else:
                    return parser().parse(
                        io.BytesIO(body),
                        media_type=content_type,
                        parser_context={"request": request}
                    )
            return {}
        return request.GET

    def response(self, data):
        return self.response_class.response(data)

    def success(self, data=None):
        return self.response({"error": None, "data": data})

    def error(self, msg="error", err="error"):
        return self.response({"error": err, "data": msg})

    def extract_errors(self, errors, key="field"):
        if isinstance(errors, dict):
            if not errors:
                return key, "Invalid field"
            key = list(errors.keys())[0]
            return self.extract_errors(errors.pop(key), key)
        elif isinstance(errors, list):
            return self.extract_errors(errors[0], key)

        return key, errors

    def invalid_serializer(self, serializer):
        key, error = self.extract_errors(serializer.errors)
        if key == "non_field_errors":
            msg = error
        else:
            msg = f"{key}: {error}"
        return self.error(err=f"invalid-{key}", msg=msg)

    def server_error(self):
        return self.error(err="server-error", msg="server error")

    def paginate_data(self, request, query_set, object_serializer=None, context=None):
        """
        :param request: django's request
        :param query_set: django model query set or other list like objects
        :param object_serializer: Used to serialize the query set, if it is None, slice the query set directly
        :return:
        """
        try:
            limit = int(request.GET.get("limit", "10"))
        except ValueError:
            limit = 10
        if limit < 0 or limit > 250:
            limit = 10
        try:
            offset = int(request.GET.get("offset", "0"))
        except ValueError:
            offset = 0
        if offset < 0:
            offset = 0
        results = query_set[offset:offset + limit]
        if object_serializer:
            count = query_set.count()
            if not context:
                results = object_serializer(results, many=True).data
            else:
                results = object_serializer(results, context=context, many=True).data
        else:
            count = query_set.count()
        data = {"results": results,
                "total": count}
        return data

    def dispatch(self, request, *args, **kwargs):
        if self.parser_classes:
            try:
                request.data = self._get_request_data(self.request)
            except ValueError as e:
                return self.error(err="invalid-request", msg=str(e))
        try:
            return super(APIView, self).dispatch(request, *args, **kwargs)
        except APIError as e:
            ret = {"msg": e.msg}
            if e.err:
                ret["err"] = e.err
            return self.error(**ret)
        except Exception as e:
            logger.exception(e)
            return self.server_error()


class CSRFExemptAPIView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CSRFExemptAPIView, self).dispatch(request, *args, **kwargs)


def validate_serializer(serializer):
    """
    @validate_serializer(TestSerializer)
    def post(self, request):
        return self.success(request.data)
    """
    def validate(view_method):
        @functools.wraps(view_method)
        def handle(*args, **kwargs):
            self = args[0]
            request = args[1]
            s = serializer(data=request.data)
            if s.is_valid():
                request.data = s.data
                request.serializer = s
                return view_method(*args, **kwargs)
            else:
                return self.invalid_serializer(s)

        return handle

    return validate
