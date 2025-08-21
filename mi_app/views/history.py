import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models import History, DocumentType

@csrf_exempt
def histories_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    qs = History.objects.filter(deleted_at__isnull=True).select_related("document_type")
    data = [{
        "id": h.id,
        "document_type": h.document_type_id,
        "document_number": h.document_number
    } for h in qs]
    return JsonResponse({"histories": data})


@csrf_exempt
def history_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    dt_id = payload.get("document_type")
    document_number = payload.get("document_number")

    if dt_id is None or not document_number:
        return JsonResponse({"error": "Campos obligatorios faltantes"}, status=400)

    try:
        dt = DocumentType.objects.get(pk=dt_id)
    except DocumentType.DoesNotExist:
        return JsonResponse({"error": "document_type inválido"}, status=400)
    
    h = History.objects.create(document_type=dt, document_number=document_number)
    return JsonResponse({"id": h.id}, status=201)


@csrf_exempt
def history_update(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        h = History.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except History.DoesNotExist:
        return JsonResponse({"error": "No encontrado"}, status=404)

    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    dt_id = payload.get("document_type")
    document_number = payload.get("document_number")

    if dt_id is None or not document_number:
        return JsonResponse({"error": "Campos obligatorios faltantes"}, status=400)

    try:
        dt = DocumentType.objects.get(pk=dt_id)
    except DocumentType.DoesNotExist:
        return JsonResponse({"error": "document_type inválido"}, status=400)
    
    h.document_type = dt
    h.document_number = document_number
    h.save()

    return JsonResponse({"status": "updated"})


@csrf_exempt
def history_delete(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        h = History.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except History.DoesNotExist:
        return JsonResponse({"error":"No encontrado"}, status=404)
    
    h.soft_delete()
    return JsonResponse({"status": "deleted"})
