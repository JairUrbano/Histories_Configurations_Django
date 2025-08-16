import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from ..models import History, Patient
from ..forms import HistoryForm

def history_create(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    form = HistoryForm(data)
    if form.is_valid():
        patient = form.cleaned_data['patient']
        existing_history = History.objects.filter(patient=patient).first()

        if existing_history:
            if existing_history.deleted_at:  # soft deleted
                existing_history.testimony = form.cleaned_data.get('testimony', existing_history.testimony)
                existing_history.height = form.cleaned_data.get('height', existing_history.height)
                existing_history.weight = form.cleaned_data.get('weight', existing_history.weight)
                existing_history.observations = form.cleaned_data.get('observations', existing_history.observations)
                existing_history.deleted_at = None
                existing_history.save()
                return JsonResponse({'status': 'restaurado'}, status=200)
            else:
                return JsonResponse({'error': 'Ya existe historial activo'}, status=400)

        form.save()
        return JsonResponse({'status': 'creado'}, status=201)
    else:
        return JsonResponse({'errors': form.errors}, status=400)


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
            'patient': {'id': h.patient.id, 'name': h.patient.name},
            'testimony': h.testimony,
            'created_at': h.created_at,
            'height': h.height,
            'weight': h.weight,
            'observations': h.observations,
        }
        for h in histories_paginated
    ]

    return JsonResponse({
        'histories': data,
        'page': histories_paginated.number,
        'num_pages': histories_paginated.paginator.num_pages
    })


def history_update(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    try:
        history = History.objects.get(pk=pk, deleted_at__isnull=True)
    except History.DoesNotExist:
        return JsonResponse({'error': 'Historial no encontrado'}, status=404)

    form = HistoryForm(data, instance=history)
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


def history_detail(request, patient_id):
    try:
        history = History.objects.get(patient_id=patient_id, deleted_at__isnull=True)
    except History.DoesNotExist:
        return JsonResponse({'error': 'Historial no encontrado'}, status=404)

    data = {
        'id': history.id,
        'patient': {'id': history.patient.id, 'name': history.patient.name},
        'testimony': history.testimony,
        'created_at': history.created_at,
        'height': history.height,
        'weight': history.weight,
        'observations': history.observations
    }
    return JsonResponse(data, status=200)
