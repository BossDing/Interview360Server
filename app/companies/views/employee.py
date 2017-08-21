from . import (
    viewsets, status, Response, Company, CompanyMember, get_object_or_404,
    EmployeeSerializer, User, IsAuthenticated,  TokenAuthentication, User
)
from rest_framework.decorators import list_route

class EmployeesViewSet(viewsets.ViewSet):
    """ View class for employee's actions """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def list(self, request, company_pk=None):
        """ Return list of employees for the company """

        company = self.get_company(company_pk)
        serializer = EmployeeSerializer(
            company.employees.all(), many=True, context={'company_id': company.id})
        return Response({'employees': serializer.data}, status=status.HTTP_200_OK);

    def create(self, request, company_pk=None):
        """ Create new user and send it a letter """

        company = self.get_company(company_pk)
        serializer = EmployeeSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid() and serializer.save():
            return Response(
                { 'message': 'Users were succesfully added as an employee' },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                { 'errors': serializer.errors },
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, company_pk=None, pk=None):
        """ Destroys the CompanyMember object  """

        company = self.get_company(company_pk)
        employee = get_object_or_404(User, pk=pk)
        company_member = CompanyMember.objects.get(
            user_id=employee.id, company_id=company.id
        )
        company_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def get_company(self, id):
        return get_object_or_404(Company, pk=id)