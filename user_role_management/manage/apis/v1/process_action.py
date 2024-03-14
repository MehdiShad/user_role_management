from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from user_role_management.manage import models
from user_role_management.api.mixins import ApiAuthMixin
from user_role_management.manage.services import process_action as process_action_services
from user_role_management.manage.selectors import process_action as process_action_selector
from user_role_management.api.pagination import LimitOffsetPagination, get_paginated_response_context
from user_role_management.core.exceptions import handle_validation_error, error_response, success_response
from user_role_management.utils.serializer_handler import CustomSingleResponseSerializerBase, CustomMultiResponseSerializerBase


class OutPutProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Process
        fields = '__all__'


class CustomProcessSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutProcessSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomProcessMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutProcessSerializer())

    class Meta:
        fields = ('is_success', 'data')


class ProcessesApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputProcessSerializer(serializers.Serializer):
        company_id = serializers.IntegerField()
        name = serializers.CharField(max_length=155)

    class FilterProcessSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=155, required=False)

    @extend_schema(request=InputProcessSerializer, responses=CustomProcessSingleResponseSerializer, tags=['Process'])
    def post(self, request: HttpRequest):
        serializer = self.InputProcessSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            process = process_action_services.create_process(request, **serializer.validated_data)
            if not process['is_success']:
                raise Exception(process['message'])
            return Response(CustomProcessSingleResponseSerializer(process, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterProcessSerializer], responses=CustomProcessMultiResponseSerializer,
                   tags=['Process'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterProcessSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            processes = process_action_selector.get_filtered_processes(request, filters=filter_serializer.validated_data)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutProcessSerializer,
                queryset=processes,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProcessApi(ApiAuthMixin, APIView):
    class UpdateProcessSerializer(ProcessesApi.InputProcessSerializer):
        company_id = serializers.IntegerField(required=False)
        name = serializers.CharField(max_length=155, required=False)

    @extend_schema(responses=CustomProcessSingleResponseSerializer, tags=['Process'])
    def get(self, request: HttpRequest, process_id: int):
        try:
            process = process_action_selector.get_process(request=request, id=process_id)
            if not process['is_success']:
                raise Exception(process['message'])
            return Response(CustomProcessSingleResponseSerializer(process, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateProcessSerializer, responses=CustomProcessSingleResponseSerializer, tags=['Process'])
    def put(self, request: HttpRequest, process_id: int):
        serializer = self.UpdateProcessSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            process = process_action_services.update_process(request=request, id=process_id, **serializer.validated_data)
            if not process['is_success']:
                raise Exception(process['message'])
            return Response(CustomProcessSingleResponseSerializer(process, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# ====================================================================

class OutPutActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Action
        fields = '__all__'


class CustomActionSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutActionSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomActionMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutActionSerializer())

    class Meta:
        fields = ('is_success', 'data')


class ActionsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputActionSerializer(serializers.Serializer):
        process_id = serializers.IntegerField()
        title = serializers.CharField(max_length=155)

    class FilterActionSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(request=InputActionSerializer, responses=CustomActionSingleResponseSerializer, tags=['Action'])
    def post(self, request: HttpRequest):
        serializer = self.InputActionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            action = process_action_services.create_action(request=request, **serializer.validated_data)
            if not action['is_success']:
                raise Exception(action['message'])
            return Response(CustomActionSingleResponseSerializer(action, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterActionSerializer], responses=CustomActionMultiResponseSerializer,
                   tags=['Action'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterActionSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            actions = process_action_selector.get_filtered_actions(request, filters=filter_serializer.validated_data)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutActionSerializer,
                queryset=actions,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ActionApi(ApiAuthMixin, APIView):
    class UpdateActionSerializer(ActionsApi.InputActionSerializer):
        process_id = serializers.IntegerField(required=False)
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(responses=CustomActionSingleResponseSerializer, tags=['Action'])
    def get(self, request: HttpRequest, action_id: int):
        try:
            action = process_action_selector.get_action(request=request, id=action_id)
            if not action['is_success']:
                raise Exception(action['message'])
            return Response(CustomActionSingleResponseSerializer(action, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(request=UpdateActionSerializer, responses=CustomActionSingleResponseSerializer, tags=['Action'])
    def put(self, request: HttpRequest, action_id: int):
        serializer = self.UpdateActionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            action = process_action_services.update_action(request=request, id=action_id, **serializer.validated_data)
            if not action['is_success']:
                raise Exception(action['message'])
            return Response(CustomActionSingleResponseSerializer(action, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
