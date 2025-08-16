from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ..models import DocumentType
from ..forms import DocumentTypeForm

def document_types_list(request):
    document_types = DocumentType.objects.filter(deleted_at__isnull=True)
    data = [{'id': dt.id, 'name': dt.name, 'description': dt.description} for dt in document_types]
    return JsonResponse({'document_types': data}, status=200)

def document_type_create(request):
    if request.method == 'POST':
        form = DocumentTypeForm(request.POST)
        if form.is_valid():
            dt = form.save()
            return JsonResponse({'message': 'Documento creado correctamente', 'id': dt.id}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def document_type_update(request, pk):
    document_type = get_object_or_404(DocumentType, pk=pk)
    if request.method == 'POST':
        form = DocumentTypeForm(request.POST, instance=document_type)
        if form.is_valid():
            dt = form.save()
            return JsonResponse({'message': 'Documento actualizado correctamente', 'id': dt.id}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def document_type_delete(request, pk):
    document_type = get_object_or_404(DocumentType, pk=pk)
    document_type.soft_delete()
    return JsonResponse({'message': 'Documento eliminado correctamente'}, status=200)
