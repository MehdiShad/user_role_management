from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from django.core.validators import MinLengthValidator
from user_role_management.api.mixins import ApiAuthMixin
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from user_role_management.manage.services import user as user_services
from user_role_management.manage.selectors import user as user_selector
from user_role_management.manage.models import BaseUser, UserTypesChoices
from user_role_management.api.pagination import LimitOffsetPagination, get_paginated_response_context
from user_role_management.manage.validators import number_validator, special_char_validator, letter_validator
from user_role_management.core.exceptions import handle_validation_error, error_response, success_response


class OutPutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'


class CustomUserSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutUserSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomUserMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutUserSerializer())

    class Meta:
        fields = ('is_success', 'data')


class UsersApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputUserSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        first_name = serializers.CharField(max_length=255)
        last_name = serializers.CharField(max_length=255)
        type = serializers.CharField(max_length=2)
        last_company_logged_in = serializers.IntegerField(required=False)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email Already Taken")
            return email

        # def validate_type(self, value):
        #     if value not in [choice[0] for choice in UserTypesChoices.choices]:
        #         raise serializers.ValidationError(f"'{value}' is not a valid user type.")
        #     return value

    class FilterUserSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255, required=False)
        first_name = serializers.CharField(max_length=255, required=False)
        last_name = serializers.CharField(max_length=255, required=False)
        type = serializers.CharField(max_length=2, required=False)
        last_company_logged_in_id = serializers.IntegerField(required=False)


    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(
            validators=[
                number_validator,
                letter_validator,
                special_char_validator,
                MinLengthValidator(limit_value=10)
            ]
        )
        confirm_password = serializers.CharField(max_length=255)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email Already Taken")
            return email

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data

    class OutPutRegisterSerializer(serializers.ModelSerializer):

        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BaseUser
            fields = ("email", "token", "created_at", "updated_at")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer, tags=['User'])
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = user_services.register(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutPutRegisterSerializer(user, context={"request": request}).data)


    @extend_schema(parameters=[FilterUserSerializer], responses=CustomUserMultiResponseSerializer, tags=['User'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterUserSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            users = user_selector.get_users(request, **filter_serializer.validated_data)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutUserSerializer,
                queryset=users,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserApi(APIView):
    class UpdateUserSerializer(UsersApi.InputUserSerializer):
        email = serializers.EmailField(max_length=255, required=False)
        first_name = serializers.CharField(max_length=255, required=False)
        last_name = serializers.CharField(max_length=255, required=False)
        type = serializers.CharField(max_length=2, required=False)
        last_company_logged_in_id = serializers.IntegerField(required=False)


    @extend_schema(responses=CustomUserSingleResponseSerializer, tags=['User'])
    def get(self, request: HttpRequest, user_id: int):
        try:
            user = user_selector.get_user(request=request, id=user_id)
            if not user['is_success']:
                raise Exception(user['message'])
            return Response(CustomUserSingleResponseSerializer(user, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateUserSerializer, responses=CustomUserSingleResponseSerializer, tags=['User'])
    def put(self, request: HttpRequest, user_id: int):
        serializer = self.UpdateUserSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = user_services.update_user(request=request, id=user_id, **serializer.validated_data)
            if not user['is_success']:
                raise Exception(user['message'])
            return Response(CustomUserSingleResponseSerializer(user, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class AssignPermission(APIView):
    pass
