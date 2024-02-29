from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from user_role_management.manage.models import Company
from user_role_management.api.mixins import ApiAuthMixin
from user_role_management.manage.services import company as company_service
from user_role_management.manage.selectors import company as company_selector
from user_role_management.api.pagination import LimitOffsetPagination, get_paginated_response_context
from user_role_management.core.exceptions import handle_validation_error, error_response, success_response


class OutPutCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CustomCompanySingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutCompanySerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomCompanyMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutCompanySerializer())

    class Meta:
        fields = ('is_success', 'data')
        

class CompaniesApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputCompanySerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155)

    class FilterCompanySerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(request=InputCompanySerializer, responses=CustomCompanySingleResponseSerializer, tags=['Company'])
    def post(self, request: HttpRequest):
        serializer = self.InputCompanySerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = company_service.create_company(request, **serializer.validated_data)
            return Response(CustomCompanySingleResponseSerializer(company, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterCompanySerializer], responses=CustomCompanyMultiResponseSerializer,
                   tags=['Company'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterCompanySerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            companies = company_selector.get_companies(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutCompanySerializer,
                queryset=companies,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CompanyApi(APIView):
    class UpdateCompanySerializer(CompaniesApi.InputCompanySerializer):
        pass

    @extend_schema(responses=CustomCompanySingleResponseSerializer, tags=['Company'])
    def get(self, request: HttpRequest, company_id: int):
        try:
            company = company_selector.get_company(request=request, id=company_id)
            return Response(CustomCompanySingleResponseSerializer(company, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateCompanySerializer, responses=CustomCompanySingleResponseSerializer, tags=['Company'])
    def put(self, request: HttpRequest, company_id: int):
        serializer = self.UpdateCompanySerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = company_service.update_company(request=request, id=company_id)
            return Response(CustomCompanySingleResponseSerializer(company, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
