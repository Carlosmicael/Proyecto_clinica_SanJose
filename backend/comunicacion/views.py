from django.http import JsonResponse

def my_view(request):
    data = {"message": "¡Mensaje enviado desde Djangg Ingneiria!"}
    return JsonResponse(data)
