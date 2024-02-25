from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from user_role_management.users.models import Process
from user_role_management.api.mixins import ApiAuthMixin
from user_role_management.users.services import create_process
from user_role_management.users.selectors import get_all_processes
from user_role_management.api.pagination import LimitOffsetPagination, get_paginated_response_context
from user_role_management.core.exceptions import handle_validation_error, error_response, success_response


class OutPutProcessesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'


class CustomProcessesSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutProcessesSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomProcessesMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutProcessesSerializer())

    class Meta:
        fields = ('is_success', 'data')


class ProcessesApi(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 25

    class InputProcessesSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)

    class FilterProcessesSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)




    @extend_schema(request=InputProcessesSerializer, responses=CustomProcessesSingleResponseSerializer, tags=['Processes'])
    def post(self, request: HttpRequest):
        serializer = self.InputProcessesSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            process = create_process(request, **serializer.validated_data)
            if not process['is_success']:
                return Response(process, status=status.HTTP_400_BAD_REQUEST)
            return Response(CustomProcessesSingleResponseSerializer(process, context={"request": request}).data)
        except PermissionError as per:
            return error_response(message=str("You can't Start a process"))
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



    @extend_schema(parameters=[FilterProcessesSerializer], responses=CustomProcessesMultiResponseSerializer,
                   tags=['Processes'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterProcessesSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            attendance = get_all_processes(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutProcessesSerializer,
                queryset=attendance,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

