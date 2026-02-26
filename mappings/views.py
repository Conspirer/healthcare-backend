from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient

# Create your views here.

class MappingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only show mappings for user's patients
        mappings = PatientDoctorMapping.objects.filter(
            patient__created_by=request.user
        )
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def post(self, request):
        patient_id = request.data.get('patient')

        # Check patient belongs to user
        try:
            patient = Patient.objects.get(id=patient_id, created_by=request.user)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found or not authorized"},
                status=404
            )

        serializer = PatientDoctorMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PatientMappingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(
                id=patient_id,
                created_by=request.user
            )
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=404)

        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)

class MappingDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            mapping = PatientDoctorMapping.objects.get(
                id=pk,
                patient__created_by=request.user
            )
        except PatientDoctorMapping.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        mapping.delete()
        return Response(status=204)