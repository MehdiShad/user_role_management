from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from user_role_management.api.mixins import ApiAuthMixin
from user_role_management.manage.models import Company, Company_group, Company_branch
from user_role_management.manage.services import company as company_services
from user_role_management.manage.selectors import company as company_selector
from user_role_management.api.pagination import LimitOffsetPagination, get_paginated_response_context
from user_role_management.core.exceptions import handle_validation_error, error_response, success_response
from user_role_management.utils.serializer_handler import CustomSingleResponseSerializerBase, \
    CustomMultiResponseSerializerBase, FilterWithSearchSerializerBase


class OutPutCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CustomCompanySingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutCompanySerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomCompanyMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutCompanySerializer())

    class Meta:
        fields = ('is_success', 'data')


class CompaniesApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputCompanySerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155)

    class FilterCompanySerializer(FilterWithSearchSerializerBase):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(request=InputCompanySerializer, responses=CustomCompanySingleResponseSerializer, tags=['Company'])
    def post(self, request: HttpRequest):
        serializer = self.InputCompanySerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = company_services.create_company(request=request, **serializer.validated_data)
            if not company['is_success']:
                raise Exception(company['message'])
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


class CompanyApi(ApiAuthMixin, APIView):
    class UpdateCompanySerializer(CompaniesApi.InputCompanySerializer):
        pass

    @extend_schema(responses=CustomCompanySingleResponseSerializer, tags=['Company'])
    def get(self, request: HttpRequest, company_id: int):
        try:
            company = company_selector.get_company(request=request, id=company_id)
            if not company['is_success']:
                raise Exception(company['message'])
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
            company = company_services.update_company(request=request, id=company_id, **serializer.validated_data)
            if not company['is_success']:
                raise Exception(company['message'])
            return Response(CustomCompanySingleResponseSerializer(company, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# =================================================================

class OutPutGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CustomGroupSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutGroupSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomGroupMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutGroupSerializer())

    class Meta:
        fields = ('is_success', 'data')


class GroupsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputGroupSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=150)

    class FilterGroupSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=150, required=False)

    @extend_schema(request=InputGroupSerializer, responses=CustomGroupSingleResponseSerializer, tags=['Group'])
    def post(self, request: HttpRequest):
        serializer = self.InputGroupSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = company_services.create_group(request=request, **serializer.validated_data)
            if not group['is_success']:
                raise Exception(group['message'])
            return Response(CustomGroupSingleResponseSerializer(group, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterGroupSerializer], responses=CustomGroupMultiResponseSerializer,
                   tags=['Group'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterGroupSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            groups = company_selector.get_groups(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutGroupSerializer,
                queryset=groups,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GroupApi(ApiAuthMixin, APIView):
    class UpdateGroupSerializer(GroupsApi.InputGroupSerializer):
        name = serializers.CharField(max_length=150, required=False)

    @extend_schema(responses=CustomGroupSingleResponseSerializer, tags=['Group'])
    def get(self, request: HttpRequest, group_id: int):
        try:
            group = company_selector.get_group(request=request, id=group_id)
            if not group['is_success']:
                raise Exception(group['message'])
            return Response(CustomGroupSingleResponseSerializer(group, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateGroupSerializer, responses=CustomGroupSingleResponseSerializer, tags=['Group'])
    def put(self, request: HttpRequest, group_id: int):
        serializer = self.UpdateGroupSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = company_services.update_group(request=request, id=group_id, **serializer.validated_data)
            if not group['is_success']:
                raise Exception(group['message'])
            return Response(CustomGroupSingleResponseSerializer(group, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# =================================================================


class OutPutCompanyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company_group
        fields = '__all__'


class CustomCompanyGroupSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutCompanyGroupSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomCompanyGroupMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutCompanyGroupSerializer())

    class Meta:
        fields = ('is_success', 'data')


class CompanyGroupsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputCompanyGroupSerializer(serializers.Serializer):
        company_id = serializers.IntegerField()
        group_id = serializers.IntegerField()

    class FilterCompanyGroupSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(request=InputCompanyGroupSerializer, responses=CustomCompanyGroupSingleResponseSerializer,
                   tags=['Group'])
    def post(self, request: HttpRequest):
        serializer = self.InputCompanyGroupSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            company_group = company_services.create_company_group(request=request, **serializer.validated_data)
            if not company_group['is_success']:
                raise Exception(company_group['message'])
            return Response(
                CustomCompanyGroupSingleResponseSerializer(company_group, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterCompanyGroupSerializer], responses=CustomCompanyGroupMultiResponseSerializer,
                   tags=['Group'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterCompanyGroupSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_groups = company_selector.get_company_groups(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutCompanyGroupSerializer,
                queryset=company_groups,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CompanyGroupApi(ApiAuthMixin, APIView):
    class UpdateCompanyGroupSerializer(CompanyGroupsApi.InputCompanyGroupSerializer):
        company_id = serializers.IntegerField(required=False)
        group_id = serializers.IntegerField(required=False)

    @extend_schema(responses=CustomCompanyGroupSingleResponseSerializer, tags=['Group'])
    def get(self, request: HttpRequest, company_group_id: int):
        try:
            company_group = company_selector.get_company_group(request=request, id=company_group_id)
            if not company_group['is_success']:
                raise Exception(company_group['message'])
            return Response(
                CustomCompanyGroupSingleResponseSerializer(company_group, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateCompanyGroupSerializer, responses=CustomCompanyGroupSingleResponseSerializer,
                   tags=['Group'])
    def put(self, request: HttpRequest, company_group_id: int):
        serializer = self.UpdateCompanyGroupSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_group = company_services.update_company_group(request=request, id=company_group_id,
                                                                  **serializer.validated_data)
            if not company_group['is_success']:
                raise Exception(company_group['message'])
            return Response(
                CustomCompanyGroupSingleResponseSerializer(company_group, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# ===============================================================
class OutPutCompanyBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company_branch
        fields = '__all__'


class CustomCompanyBranchSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutCompanyBranchSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomCompanyBranchMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutCompanyBranchSerializer())

    class Meta:
        fields = ('is_success', 'data')


class CompanyBranchesApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputCompanyBranchSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155)

    class FilterCompanyBranchSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(request=InputCompanyBranchSerializer, responses=CustomCompanyBranchSingleResponseSerializer,
                   tags=['Branch'])
    def post(self, request: HttpRequest):
        serializer = self.InputCompanyBranchSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = company_services.create_company_branch(request=request, **serializer.validated_data)
            if not company['is_success']:
                raise Exception(company['message'])
            return Response(CustomCompanyBranchSingleResponseSerializer(company, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterCompanyBranchSerializer], responses=CustomCompanyBranchMultiResponseSerializer,
                   tags=['Branch'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterCompanyBranchSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            companies = company_selector.get_company_branches(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutCompanyBranchSerializer,
                queryset=companies,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CompanyBranchApi(ApiAuthMixin, APIView):
    class UpdateCompanyBranchSerializer(CompanyBranchesApi.InputCompanyBranchSerializer):
        pass

    @extend_schema(responses=CustomCompanyBranchSingleResponseSerializer, tags=['Branch'])
    def get(self, request: HttpRequest, company_id: int):
        try:
            company = company_selector.get_company_branch(request=request, id=company_id)
            if not company['is_success']:
                raise Exception(company['message'])
            return Response(CustomCompanyBranchSingleResponseSerializer(company, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateCompanyBranchSerializer, responses=CustomCompanyBranchSingleResponseSerializer,
                   tags=['Branch'])
    def put(self, request: HttpRequest, company_id: int):
        serializer = self.UpdateCompanyBranchSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = company_services.update_company_branch(request=request, id=company_id,
                                                             **serializer.validated_data)
            if not company['is_success']:
                raise Exception(company['message'])
            return Response(CustomCompanyBranchSingleResponseSerializer(company, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
