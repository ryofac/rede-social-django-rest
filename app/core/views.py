from django.http import JsonResponse
from rest_framework import status


def custom_404(request, exception):
    return JsonResponse({"error": "(404) Resource not found"}, status=status.HTTP_404_NOT_FOUND)
