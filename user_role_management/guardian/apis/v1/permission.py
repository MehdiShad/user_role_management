from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from user_role_management.api.mixins import ApiAuthMixin
from user_role_management.guardian.services import permission as permission_services
from user_role_management.guardian.selectors import permission as permission_selector
from user_role_management.guardian.models.models import UserObjectPermission, GroupObjectPermission
from user_role_management.api.pagination import LimitOffsetPagination, get_paginated_response_context
from user_role_management.core.exceptions import handle_validation_error, error_response, success_response


class OutPutUserObjectPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObjectPermission
        fields = '__all__'


class CustomUserObjectPermissionSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutUserObjectPermissionSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomUserObjectPermissionMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutUserObjectPermissionSerializer())

    class Meta:
        fields = ('is_success', 'data')


class UserObjectPermissionsApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputUserObjectPermissionSerializer(serializers.Serializer):
        user = serializers.IntegerField()

    class FilterUserObjectPermissionSerializer(serializers.Serializer):
        user = serializers.IntegerField(required=False)

    @extend_schema(request=InputUserObjectPermissionSerializer, responses=CustomUserObjectPermissionSingleResponseSerializer, tags=['Permission'])
    def post(self, request: HttpRequest):
        serializer = self.InputUserObjectPermissionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_object_permission = permission_services.create_user_object_permission(request, **serializer.validated_data)
            return Response(CustomUserObjectPermissionSingleResponseSerializer(user_object_permission, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterUserObjectPermissionSerializer], responses=CustomUserObjectPermissionMultiResponseSerializer,
                   tags=['UserObjectPermission'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterUserObjectPermissionSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            companies = permission_selector.get_user_object_permissions(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutUserObjectPermissionSerializer,
                queryset=companies,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserObjectPermissionApi(APIView):
    class UpdateUserObjectPermissionSerializer(UserObjectPermissionsApi.InputUserObjectPermissionSerializer):
        pass

    @extend_schema(responses=CustomUserObjectPermissionSingleResponseSerializer, tags=['UserObjectPermission'])
    def get(self, request: HttpRequest, user_object_permission_id: int):
        try:
            user_object_permission = permission_selector.get_user_object_permission(request=request, id=user_object_permission_id)
            return Response(CustomUserObjectPermissionSingleResponseSerializer(user_object_permission, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateUserObjectPermissionSerializer, responses=CustomUserObjectPermissionSingleResponseSerializer, tags=['Permission'])
    def put(self, request: HttpRequest, user_object_permission_id: int):
        serializer = self.UpdateUserObjectPermissionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_object_permission = permission_services.update_user_object_permission(request=request, id=user_object_permission_id)
            return Response(CustomUserObjectPermissionSingleResponseSerializer(user_object_permission, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)





#==========================================================



class OutPutGroupObjectPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupObjectPermission
        fields = '__all__'


class CustomGroupObjectPermissionSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutGroupObjectPermissionSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomGroupObjectPermissionMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutGroupObjectPermissionSerializer())

    class Meta:
        fields = ('is_success', 'data')


class GroupObjectPermissionsApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputGroupObjectPermissionSerializer(serializers.Serializer):
        group = serializers.IntegerField()

    class FilterGroupObjectPermissionSerializer(serializers.Serializer):
        group = serializers.IntegerField(required=False)

    @extend_schema(request=InputGroupObjectPermissionSerializer, responses=CustomGroupObjectPermissionSingleResponseSerializer, tags=['Permission'])
    def post(self, request: HttpRequest):
        serializer = self.InputGroupObjectPermissionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            group_object_permission = permission_services.create_group_object_permission(request, **serializer.validated_data)
            return Response(CustomGroupObjectPermissionSingleResponseSerializer(group_object_permission, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterGroupObjectPermissionSerializer], responses=CustomGroupObjectPermissionMultiResponseSerializer,
                   tags=['GroupObjectPermission'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterGroupObjectPermissionSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            companies = permission_selector.get_group_object_permissions(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutGroupObjectPermissionSerializer,
                queryset=companies,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GroupObjectPermissionApi(APIView):
    class UpdateGroupObjectPermissionSerializer(GroupObjectPermissionsApi.InputGroupObjectPermissionSerializer):
        pass

    @extend_schema(responses=CustomGroupObjectPermissionSingleResponseSerializer, tags=['GroupObjectPermission'])
    def get(self, request: HttpRequest, group_object_permission_id: int):
        try:
            group_object_permission = permission_selector.get_group_object_permission(request=request, id=group_object_permission_id)
            return Response(CustomGroupObjectPermissionSingleResponseSerializer(group_object_permission, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateGroupObjectPermissionSerializer, responses=CustomGroupObjectPermissionSingleResponseSerializer, tags=['Permission'])
    def put(self, request: HttpRequest, group_object_permission_id: int):
        serializer = self.UpdateGroupObjectPermissionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            group_object_permission = permission_services.update_group_object_permission(request=request, id=group_object_permission_id)
            return Response(CustomGroupObjectPermissionSingleResponseSerializer(group_object_permission, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
