import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models import DocumentType

@csrf_exempt
def document_types_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    qs = DocumentType.objects.filter(deleted_at__isnull=True)
    data = [{"id": d.id, "name": d.name, "description": d.description} for d in qs]
    return JsonResponse({"document_types": data})

@csrf_exempt
def document_type_create(request):
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
    
    d = DocumentType.objects.create(name=name, description=description)
    return JsonResponse({"id": d.id}, status=201)

@csrf_exempt
def document_type_update(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        d = DocumentType.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except DocumentType.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)
    
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    d.name = payload.get("name", d.name)
    d.description = payload.get("description", d.description)
    d.save()
    return JsonResponse({"status": "updated"})

@csrf_exempt
def document_type_delete(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        d = DocumentType.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except DocumentType.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)
    
    d.soft_delete()
    return JsonResponse({"status": "deleted"})
