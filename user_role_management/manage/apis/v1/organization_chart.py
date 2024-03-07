from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from user_role_management.manage import models
from user_role_management.api.mixins import ApiAuthMixin
from user_role_management.manage.services import organization_chart as organization_chart_services
from user_role_management.manage.selectors import organization_chart as organization_chart_selector
from user_role_management.api.pagination import LimitOffsetPagination, get_paginated_response_context
from user_role_management.core.exceptions import handle_validation_error, error_response, success_response
from user_role_management.utils.serializer_handler import CustomSingleResponseSerializerBase, CustomMultiResponseSerializerBase


class OutPutEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class CustomEmployeeSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutEmployeeSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomEmployeeMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutEmployeeSerializer())

    class Meta:
        fields = ('is_success', 'data')


class EmployeesApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputEmployeeSerializer(serializers.Serializer):
        company_id = serializers.IntegerField()
        personnel_code = serializers.CharField(max_length=45)
        user_id = serializers.IntegerField()

    class FilterEmployeeSerializer(serializers.Serializer):
        personnel_code = serializers.CharField(max_length=15, required=False)

    @extend_schema(request=InputEmployeeSerializer, responses=CustomEmployeeSingleResponseSerializer, tags=['Employee'])
    def post(self, request: HttpRequest):
        serializer = self.InputEmployeeSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = organization_chart_services.create_employee(request, **serializer.validated_data)
            if not employee['is_success']:
                raise Exception(employee['message'])
            return Response(CustomEmployeeSingleResponseSerializer(employee, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterEmployeeSerializer], responses=CustomEmployeeMultiResponseSerializer,
                   tags=['Employee'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterEmployeeSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            employees = organization_chart_selector.get_employees(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutEmployeeSerializer,
                queryset=employees,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class EmployeeApi(ApiAuthMixin, APIView):
    class UpdateEmployeeSerializer(EmployeesApi.InputEmployeeSerializer):
        company_id = serializers.IntegerField(required=False)
        personnel_code = serializers.CharField(max_length=15, required=False)
        user_id = serializers.IntegerField(required=False)

    @extend_schema(responses=CustomEmployeeSingleResponseSerializer, tags=['Employee'])
    def get(self, request: HttpRequest, employee_id: int):
        try:
            employee = organization_chart_selector.get_employee(request=request, id=employee_id)
            if not employee['is_success']:
                raise Exception(employee['message'])
            return Response(CustomEmployeeSingleResponseSerializer(employee, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateEmployeeSerializer, responses=CustomEmployeeSingleResponseSerializer,
                   tags=['Employee'])
    def put(self, request: HttpRequest, employee_id: int):
        serializer = self.UpdateEmployeeSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = organization_chart_services.update_employee(request=request, id=employee_id,
                                                                   **serializer.validated_data)
            if not employee['is_success']:
                raise Exception(employee['message'])
            return Response(CustomEmployeeSingleResponseSerializer(employee, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# =====================================================


class OutPutPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = '__all__'


class CustomPositionSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutPositionSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomPositionMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutPositionSerializer())

    class Meta:
        fields = ('is_success', 'data')


class PositionsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputPositionSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155)
        abbreviation = serializers.CharField(max_length=55, required=False)

    class FilterPositionSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(request=InputPositionSerializer, responses=CustomPositionSingleResponseSerializer, tags=['Position'])
    def post(self, request: HttpRequest):
        serializer = self.InputPositionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            position = organization_chart_services.create_position(request, **serializer.validated_data)
            if not position['is_success']:
                raise Exception(position['message'])
            return Response(CustomPositionSingleResponseSerializer(position, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterPositionSerializer], responses=CustomPositionMultiResponseSerializer,
                   tags=['Position'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterPositionSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            positions = organization_chart_selector.get_positions(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutPositionSerializer,
                queryset=positions,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PositionApi(ApiAuthMixin, APIView):
    class UpdatePositionSerializer(PositionsApi.InputPositionSerializer):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(responses=CustomPositionSingleResponseSerializer, tags=['Position'])
    def get(self, request: HttpRequest, position_id: int):
        try:
            position = organization_chart_selector.get_position(request=request, id=position_id)
            if not position['is_success']:
                raise Exception(position['message'])
            return Response(CustomPositionSingleResponseSerializer(position, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdatePositionSerializer, responses=CustomPositionSingleResponseSerializer,
                   tags=['Position'])
    def put(self, request: HttpRequest, position_id: int):
        serializer = self.UpdatePositionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            position = organization_chart_services.update_position(request=request, id=position_id,
                                                                   **serializer.validated_data)
            if not position['is_success']:
                raise Exception(position['message'])
            return Response(CustomPositionSingleResponseSerializer(position, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class OutPutDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'


class CustomDepartmentSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutDepartmentSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomDepartmentMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutDepartmentSerializer())

    class Meta:
        fields = ('is_success', 'data')


class DepartmentsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class FilterDepartmentSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155, required=False)

    class InputDepartmentSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155)
        abbreviation = serializers.CharField(max_length=55, required=False)

    @extend_schema(request=InputDepartmentSerializer, responses=CustomDepartmentSingleResponseSerializer,
                   tags=['Department'])
    def post(self, request: HttpRequest):
        serializer = self.InputDepartmentSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            department = organization_chart_services.create_department(request, **serializer.validated_data)
            if not department['is_success']:
                raise Exception(department['message'])
            return Response(CustomDepartmentSingleResponseSerializer(department, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterDepartmentSerializer], responses=CustomDepartmentMultiResponseSerializer,
                   tags=['Department'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterDepartmentSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            departments = organization_chart_selector.get_departments(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutDepartmentSerializer,
                queryset=departments,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class DepartmentApi(ApiAuthMixin, APIView):
    class UpdateDepartmentSerializer(DepartmentsApi.InputDepartmentSerializer):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(responses=CustomDepartmentSingleResponseSerializer, tags=['Department'])
    def get(self, request: HttpRequest, department_id: int):
        try:
            department = organization_chart_selector.get_department(request=request, id=department_id)
            if not department['is_success']:
                raise Exception(department['message'])
            return Response(CustomDepartmentSingleResponseSerializer(department, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateDepartmentSerializer, responses=CustomDepartmentSingleResponseSerializer,
                   tags=['Department'])
    def put(self, request: HttpRequest, department_id: int):
        serializer = self.UpdateDepartmentSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            department = organization_chart_services.update_department(request=request, id=department_id,
                                                                       **serializer.validated_data)
            if not department['is_success']:
                raise Exception(department['message'])
            return Response(CustomDepartmentSingleResponseSerializer(department, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# =============================================================


class OutPutCompanyDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company_department
        fields = '__all__'


class CustomCompanyDepartmentSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutCompanyDepartmentSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomCompanyDepartmentMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutCompanyDepartmentSerializer())

    class Meta:
        fields = ('is_success', 'data')


class CompanyDepartmentsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputCompanyDepartmentSerializer(serializers.Serializer):
        company_id = serializers.IntegerField()
        department_id = serializers.IntegerField()
        parent_department_id = serializers.IntegerField(required=False)
        manager_id = serializers.IntegerField(required=False)

    class FilterCompanyDepartmentSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(request=InputCompanyDepartmentSerializer, responses=CustomCompanyDepartmentSingleResponseSerializer,
                   tags=['CompanyDepartment'])
    def post(self, request: HttpRequest):
        serializer = self.InputCompanyDepartmentSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            company_department = organization_chart_services.create_company_department(request,
                                                                                       **serializer.validated_data)
            if not company_department['is_success']:
                raise Exception(company_department['message'])
            return Response(
                CustomCompanyDepartmentSingleResponseSerializer(company_department, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterCompanyDepartmentSerializer],
                   responses=CustomCompanyDepartmentMultiResponseSerializer,
                   tags=['CompanyDepartment'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterCompanyDepartmentSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_departments = organization_chart_selector.get_company_departments(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutCompanyDepartmentSerializer,
                queryset=company_departments,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CompanyDepartmentApi(ApiAuthMixin, APIView):
    class UpdateCompanyDepartmentSerializer(CompanyDepartmentsApi.InputCompanyDepartmentSerializer):
        company_id = serializers.IntegerField(required=False)
        department_id = serializers.IntegerField(required=False)
        manager_id = serializers.IntegerField(required=False)

    @extend_schema(responses=CustomCompanyDepartmentSingleResponseSerializer, tags=['CompanyDepartment'])
    def get(self, request: HttpRequest, company_department_id: int):
        try:
            company_department = organization_chart_selector.get_company_department(request=request,
                                                                                    id=company_department_id)
            if not company_department['is_success']:
                raise Exception(company_department['message'])
            return Response(
                CustomCompanyDepartmentSingleResponseSerializer(company_department, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateCompanyDepartmentSerializer, responses=CustomCompanyDepartmentSingleResponseSerializer,
                   tags=['CompanyDepartment'])
    def put(self, request: HttpRequest, company_department_id: int):
        serializer = self.UpdateCompanyDepartmentSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_department = organization_chart_services.update_company_department(request=request,
                                                                                       id=company_department_id,
                                                                                       **serializer.validated_data)
            if not company_department['is_success']:
                raise Exception(company_department['message'])
            return Response(
                CustomCompanyDepartmentSingleResponseSerializer(company_department, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# ========================================================================

class OutPutCompanyDepartmentEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company_department_employee
        fields = '__all__'


class CustomCompanyDepartmentEmployeeSingleResponseSerializer(CustomSingleResponseSerializerBase):
    data = OutPutCompanyDepartmentEmployeeSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomCompanyDepartmentEmployeeMultiResponseSerializer(CustomMultiResponseSerializerBase):
    data = serializers.ListSerializer(child=OutPutCompanyDepartmentEmployeeSerializer())

    class Meta:
        fields = ('is_success', 'data')


class CompanyDepartmentEmployeesApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputCompanyDepartmentEmployeeSerializer(serializers.Serializer):
        company_department_id = serializers.IntegerField()
        employee_id = serializers.IntegerField()
        supervisor_id = serializers.IntegerField(required=False)

    class FilterCompanyDepartmentEmployeeSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155, required=False)

    @extend_schema(request=InputCompanyDepartmentEmployeeSerializer,
                   responses=CustomCompanyDepartmentEmployeeSingleResponseSerializer,
                   tags=['CompanyDepartmentEmployee'])
    def post(self, request: HttpRequest):
        serializer = self.InputCompanyDepartmentEmployeeSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            company_department_employee = organization_chart_services.create_company_department_employee(request,
                                                                                                         **serializer.validated_data)
            if not company_department_employee['is_success']:
                return Response(company_department_employee, status=status.HTTP_400_BAD_REQUEST)
                # raise Exception(company_department_employee['message'])
            return Response(CustomCompanyDepartmentEmployeeSingleResponseSerializer(company_department_employee,
                                                                                    context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterCompanyDepartmentEmployeeSerializer],
                   responses=CustomCompanyDepartmentEmployeeMultiResponseSerializer,
                   tags=['CompanyDepartmentEmployee'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterCompanyDepartmentEmployeeSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_department_employees = organization_chart_selector.get_company_department_employees(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutCompanyDepartmentEmployeeSerializer,
                queryset=company_department_employees,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CompanyDepartmentEmployeeApi(ApiAuthMixin, APIView):
    class UpdateCompanyDepartmentEmployeeSerializer(CompanyDepartmentEmployeesApi.InputCompanyDepartmentEmployeeSerializer):
        company_department_id = serializers.IntegerField(required=False)
        employee_id = serializers.IntegerField(required=False)
        supervisor_id = serializers.IntegerField(required=False)

    @extend_schema(responses=CustomCompanyDepartmentEmployeeSingleResponseSerializer,tags=['CompanyDepartmentEmployee'])
    def get(self, request: HttpRequest, company_department_employee_id: int):
        try:
            company_department_employee = organization_chart_selector.get_company_department_employee(request=request, id=company_department_employee_id)
            if not company_department_employee['is_success']:
                raise Exception(company_department_employee['message'])
            return Response(CustomCompanyDepartmentEmployeeSingleResponseSerializer(company_department_employee, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateCompanyDepartmentEmployeeSerializer, responses=CustomCompanyDepartmentEmployeeSingleResponseSerializer, tags=['CompanyDepartmentEmployee'])
    def put(self, request: HttpRequest, company_department_employee_id: int):
        serializer = self.UpdateCompanyDepartmentEmployeeSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_department_employee = organization_chart_services.update_company_department_employee(
                request=request, id=company_department_employee_id, **serializer.validated_data)
            if not company_department_employee['is_success']:
                raise Exception(company_department_employee['message'])
            return Response(CustomCompanyDepartmentEmployeeSingleResponseSerializer(company_department_employee,
                                                                                    context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
