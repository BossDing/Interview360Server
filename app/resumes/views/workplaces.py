from . import viewsets, list_route, Response, status
from rest_framework.views import APIView
from resumes.forms import WorkplaceForm
from resumes.serializers import WorkplaceSerializer
import ipdb

class WorkplacesApiView(APIView):
    """ Views for workplace resource """

    def put(self, request, resume_id=None):
        """ Create new workplaces for resume; Update existing ones """

        form = WorkplaceForm(params=request.data)
        if form.submit():
            return Response(
                { 'workplaces': WorkplaceSerializer(form.objects, many=True).data }
            )
        else:
            return Response(
                { 'errors': form.errors }, status=status.HTTP_400_BAD_REQUEST
            )
