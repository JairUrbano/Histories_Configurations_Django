import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models import PaymentType

@csrf_exempt
def payment_types_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    qs = PaymentType.objects.filter(deleted_at__isnull=True)
    data = [{"id": p.id, "name": p.name, "description": p.description} for p in qs]
    return JsonResponse({"payment_types": data})

@csrf_exempt
def payment_type_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    name = payload.get("name")
    description = payload.get("description", "")
    if not name:
        return JsonResponse({"error": "El campo name es obligatorio"}, status=400)
    
    p = PaymentType.objects.create(name=name, description=description)
    return JsonResponse({"id": p.id}, status=201)

@csrf_exempt
def payment_type_update(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        p = PaymentType.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except PaymentType.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)
    
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    p.name = payload.get("name", p.name)
    p.description = payload.get("description", p.description)
    p.save()
    return JsonResponse({"status": "updated"})

@csrf_exempt
def payment_type_delete(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        p = PaymentType.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except PaymentType.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)
    
    p.soft_delete()
    return JsonResponse({"status": "deleted"})