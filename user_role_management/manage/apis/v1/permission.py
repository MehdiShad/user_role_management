from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from django.contrib.auth.models import Permission
from user_role_management.api.mixins import ApiAuthMixin
from user_role_management.manage.models import Process, Action
from user_role_management.manage.services import permission as permission_services
from user_role_management.manage.selectors import permission as permission_selector
from user_role_management.api.pagination import LimitOffsetPagination, get_paginated_response_context
from user_role_management.core.exceptions import handle_validation_error, error_response, success_response
from user_role_management.utils.serializer_handler import CustomSingleResponseSerializerBase, \
    CustomMultiResponseSerializerBase, FilterWithSearchSerializerBase


class OutPutPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class CustomPermissionSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutPermissionSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomPermissionMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutPermissionSerializer())

    class Meta:
        fields = ('is_success', 'data')


class PermissionsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputPermissionSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=155)
        codename = serializers.CharField(max_length=155)
        content_type_id = serializers.IntegerField()

    class FilterPermissionSerializer(FilterWithSearchSerializerBase):
        name = serializers.CharField(max_length=155, required=False)
        codename = serializers.CharField(max_length=155, required=False)
        content_type_id = serializers.IntegerField(required=False)

    @extend_schema(request=InputPermissionSerializer, responses=CustomPermissionSingleResponseSerializer,
                   tags=['Permission'])
    def post(self, request: HttpRequest):
        serializer = self.InputPermissionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            permission = permission_services.create_permission(request=request, **serializer.validated_data)
            if not permission['is_success']:
                raise Exception(permission['message'])
            return Response(CustomPermissionSingleResponseSerializer(permission, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterPermissionSerializer], responses=CustomPermissionMultiResponseSerializer,
                   tags=['Permission'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterPermissionSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            permissions = permission_selector.get_filtered_permissions(request, filters=filter_serializer.validated_data)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutPermissionSerializer,
                queryset=permissions,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PermissionApi(ApiAuthMixin, APIView):
    class UpdatePermissionSerializer(PermissionsApi.InputPermissionSerializer):
        pass

    @extend_schema(responses=CustomPermissionSingleResponseSerializer, tags=['Permission'])
    def get(self, request: HttpRequest, permission_id: int):
        try:
            permission = permission_selector.get_permission(request=request, id=permission_id)
            if not permission['is_success']:
                raise Exception(permission['message'])
            return Response(CustomPermissionSingleResponseSerializer(permission, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdatePermissionSerializer, responses=CustomPermissionSingleResponseSerializer,
                   tags=['Permission'])
    def put(self, request: HttpRequest, permission_id: int):
        serializer = self.UpdatePermissionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            permission = permission_services.update_permission(request=request, id=permission_id,
                                                               **serializer.validated_data)
            if not permission['is_success']:
                raise Exception(permission['message'])
            return Response(CustomPermissionSingleResponseSerializer(permission, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# =================================================================

class CustomAccessProcessesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'


class CustomeAccessActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class CustomUserPermissionMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    access_processes = serializers.ListSerializer(child=CustomAccessProcessesSerializer())
    access_actions = serializers.ListSerializer(child=CustomeAccessActionsSerializer())

    class Meta:
        fields = ('access_processes', 'access_actions')


class UserPermissionsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputPermissionSerializer(serializers.Serializer):
        # title = serializers.CharField(max_length=155)
        pass

    class FilterPermissionSerializer(FilterWithSearchSerializerBase):
        # title = serializers.CharField(max_length=155, required=False)
        pass

    @extend_schema(parameters=[FilterPermissionSerializer], responses=CustomPermissionMultiResponseSerializer,
                   tags=['Permission'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterPermissionSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            permissions = permission_selector.get_user_permissions(request)
            return Response(CustomUserPermissionMultiResponseSerializer(permissions).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
