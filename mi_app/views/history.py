import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models import History, DocumentType

@csrf_exempt
def histories_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    qs = History.active.select_related("document_type")
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
    payload = json.loads(request.body.decode() or "{}")
    dt_id = payload.get("document_type")
    try:
        dt = DocumentType.objects.get(pk=dt_id)
    except DocumentType.DoesNotExist:
        return JsonResponse({"error": "document_type inválido"}, status=400)
    h = History.objects.create(document_type=dt, document_number=payload.get("document_number",""))
    return JsonResponse({"id": h.id}, status=201)

@csrf_exempt
def history_delete(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        h = History.active.get(pk=pk)
    except History.DoesNotExist:
        return JsonResponse({"error":"No encontrado"}, status=404)
    h.soft_delete()
    return JsonResponse({"status": "deleted"})
