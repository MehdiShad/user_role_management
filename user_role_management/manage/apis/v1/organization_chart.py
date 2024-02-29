from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from user_role_management.manage import models
from user_role_management.api.mixins import ApiAuthMixin
from user_role_management.manage.services import organization_chart as organization_chart_service
from user_role_management.manage.selectors import organization_chart as organization_chart_selector
from user_role_management.api.pagination import LimitOffsetPagination, get_paginated_response_context
from user_role_management.core.exceptions import handle_validation_error, error_response, success_response


class OutPutEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class CustomEmployeeSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutEmployeeSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomEmployeeMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutEmployeeSerializer())

    class Meta:
        fields = ('is_success', 'data')

class EmployeesApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class InputEmployeeSerializer(serializers.Serializer):
        company = serializers.IntegerField()
        personnel_code = serializers.CharField(max_length=15)
        user = serializers.IntegerField()

    class FilterEmployeeSerializer(serializers.Serializer):
        personnel_code = serializers.CharField(max_length=15, required=False)

    @extend_schema(request=InputEmployeeSerializer, responses=CustomEmployeeSingleResponseSerializer, tags=['Employee'])
    def post(self, request: HttpRequest):
        serializer = self.InputEmployeeSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = organization_chart_service.create_employee(request, **serializer.validated_data)
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
            companies = organization_chart_selector.get_employees(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutEmployeeSerializer,
                queryset=companies,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class EmployeeApi(APIView):

    class UpdateEmployeeSerializer(EmployeesApi.InputEmployeeSerializer):
        pass

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

    @extend_schema(request=UpdateEmployeeSerializer, responses=CustomEmployeeSingleResponseSerializer, tags=['Employee'])
    def put(self, request: HttpRequest, employee_id: int):
        serializer = self.UpdateEmployeeSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = organization_chart_service.update_employee(request=request, id=employee_id, **serializer.validated_data)
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


class CustomPositionSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutPositionSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomPositionMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutPositionSerializer())

    class Meta:
        fields = ('is_success', 'data')


class PositionsApi(APIView):
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
            position = organization_chart_service.create_position(request, **serializer.validated_data)
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
            companies = organization_chart_selector.get_positions(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutPositionSerializer,
                queryset=companies,
                view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PositionApi(APIView):

    class UpdatePositionSerializer(PositionsApi.InputPositionSerializer):
        pass

    @extend_schema(responses=CustomPositionSingleResponseSerializer, tags=['Position'])
    def get(self, request: HttpRequest, position_id: int):
        try:
            position = organization_chart_selector.get_position(request=request, id=position_id)
            if not position['is_success']:
                raise Exception(position['message'])
            return Response(CustomPositionSingleResponseSerializer(success_response(data=position), context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdatePositionSerializer, responses=CustomPositionSingleResponseSerializer, tags=['Position'])
    def put(self, request: HttpRequest, company_id: int):
        serializer = self.UpdatePositionSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            position = organization_chart_service.update_position(request=request, id=company_id, **serializer.validated_data)
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


class CustomDepartmentSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutDepartmentSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomDepartmentMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutDepartmentSerializer())

    class Meta:
        fields = ('is_success', 'data')

class DepartmentsApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class FilterDepartmentSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155, required=False)


    class InputDepartmentSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=155)
        abbreviation = serializers.CharField(max_length=55, required=False)

    @extend_schema(request=InputDepartmentSerializer, responses=CustomDepartmentSingleResponseSerializer, tags=['Department'])
    def post(self, request: HttpRequest):
        serializer = self.InputDepartmentSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            department = organization_chart_service.create_department(request, **serializer.validated_data)
            if not department['is_success']:
                raise Exception(department['message'])
            return Response(CustomDepartmentSingleResponseSerializer(department, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=[FilterDepartmentSerializer], responses=CustomDepartmentMultiResponseSerializer, tags=['Department'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterDepartmentSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            companies = organization_chart_selector.get_departments(request)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutDepartmentSerializer,
                queryset=companies,
                  view=self,
            )
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class DepartmentApi(APIView):

    class UpdateDepartmentSerializer(DepartmentsApi.InputDepartmentSerializer):
        pass


    @extend_schema(responses=CustomDepartmentSingleResponseSerializer, tags=['Department'])
    def get(self, request: HttpRequest, department_id: int):
        try:
            department = organization_chart_selector.get_department(request=request, id=department_id)
            if not department['is_success']:
                raise Exception(department['message'])
            return Response(CustomDepartmentSingleResponseSerializer(success_response(data=department), context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UpdateDepartmentSerializer, responses=CustomDepartmentSingleResponseSerializer, tags=['Department'])
    def put(self, request: HttpRequest, department_id: int):
        serializer = self.UpdateDepartmentSerializer(data=request.data)
        validation_result = handle_validation_error(serializer=serializer)
        if not isinstance(validation_result, bool):
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            department = organization_chart_service.update_department(request=request, id=department_id, **serializer.validated_data)
            if not department['is_success']:
                raise Exception(department['message'])
            return Response(CustomDepartmentSingleResponseSerializer(department, context={"request": request}).data)
        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

