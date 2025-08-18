from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from ..models import History
from ..forms import HistoryForm

# ----------------------------
# Crear historial
# ----------------------------
def history_create(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    form = HistoryForm(request.POST)
    if form.is_valid():
        patient = form.cleaned_data['patient']
        existing_history = History.objects.filter(patient=patient, deleted_at__isnull=True).first()

        if existing_history:
            return JsonResponse({'error': 'Ya existe historial activo'}, status=400)

        # Restaurar historial soft-deleted si existe
        soft_deleted = History.objects.filter(patient=patient, deleted_at__isnull=False).first()
        if soft_deleted:
            for field, value in form.cleaned_data.items():
                setattr(soft_deleted, field, value)
            soft_deleted.deleted_at = None
            soft_deleted.save()
            return JsonResponse({'status': 'restaurado'}, status=200)

        form.save()
        return JsonResponse({'status': 'creado'}, status=201)
    else:
        return JsonResponse({'errors': form.errors}, status=400)


# ----------------------------
# Listar historiales (paginado)
# ----------------------------
def histories_list(request):
    search_query = request.GET.get('q', '')
    histories = History.objects.filter(deleted_at__isnull=True)

    if search_query:
        histories = histories.filter(
            Q(patient__name__icontains=search_query) |
            Q(testimony__icontains=search_query)
        )

    paginator = Paginator(histories, 10)
    page = request.GET.get('page')
    histories_paginated = paginator.get_page(page)

    data = [
        {
            'id': h.id,
            'patient': h.patient.name,
            'testimony': h.testimony,
            'created_at': h.created_at.isoformat() if h.created_at else None,
        }
        for h in histories_paginated
    ]

    return JsonResponse({
        'histories': data,
        'page': histories_paginated.number,
        'num_pages': histories_paginated.paginator.num_pages
    }, status=200)


# ----------------------------
# Actualizar historial
# ----------------------------
def history_update(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        history = History.objects.get(pk=pk, deleted_at__isnull=True)
    except History.DoesNotExist:
        return JsonResponse({'error': 'Historial no encontrado'}, status=404)

    form = HistoryForm(request.POST, instance=history)
    if form.is_valid():
        updated = False
        for field, value in form.cleaned_data.items():
            if getattr(history, field) != value:
                setattr(history, field, value)
                updated = True

        if updated:
            history.save()
            return JsonResponse({'status': 'actualizado'}, status=200)
        else:
            return JsonResponse({'status': 'sin cambios'}, status=200)
    else:
        return JsonResponse({'errors': form.errors}, status=400)


# ----------------------------
# Eliminar historial (soft delete)
# ----------------------------
def history_delete(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        history = History.objects.get(pk=pk, deleted_at__isnull=True)
    except History.DoesNotExist:
        return JsonResponse({'error': 'Historial no encontrado'}, status=404)

    history.deleted_at = timezone.now()
    history.save()
    return JsonResponse({'status': 'eliminado'}, status=200)


# ----------------------------
# Detalle de historial por paciente
# ----------------------------
def history_detail(request, patient_id):
    try:
        history = History.objects.get(patient_id=patient_id, deleted_at__isnull=True)
    except History.DoesNotExist:
        return JsonResponse({'error': 'Historial no encontrado'}, status=404)

    data = {
        'id': history.id,
        'patient': history.patient.name,
        'testimony': history.testimony,
        'created_at': history.created_at.isoformat() if history.created_at else None,
        'height': history.height,
        'weight': history.weight,
        'observations': history.observations
    }
    return JsonResponse(data, status=200)
