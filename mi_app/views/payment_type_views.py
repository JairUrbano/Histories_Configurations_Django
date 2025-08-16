from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import PaymentType
from ..forms import PaymentTypeForm
from django.utils import timezone


# ----------------------------
# Listar tipos de pago
# ----------------------------
def payment_types_list(request):
    payment_types = PaymentType.objects.filter(deleted_at__isnull=True)
    data = [
        {
            'id': pt.id,
            'name': pt.name,
        } 
        for pt in payment_types
    ]
    return JsonResponse({'payment_types': data}, status=200)

# ----------------------------
# Crear tipo de pago
# ----------------------------
def payment_type_create(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    form = PaymentTypeForm(request.POST)
    if form.is_valid():
        payment_type = form.save()
        return JsonResponse({
            'status': 'creado',
            'id': payment_type.id,
            'name': payment_type.name
        }, status=201)
    else:
        return JsonResponse({'errors': form.errors}, status=400)

# ----------------------------
# Actualizar tipo de pago
# ----------------------------
def payment_type_update(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    payment_type = get_object_or_404(PaymentType, pk=pk)
    form = PaymentTypeForm(request.POST, instance=payment_type)
    if form.is_valid():
        updated = False
        for field, value in form.cleaned_data.items():
            if getattr(payment_type, field) != value:
                setattr(payment_type, field, value)
                updated = True
        if updated:
            payment_type.save()
            return JsonResponse({'status': 'actualizado'}, status=200)
        else:
            return JsonResponse({'status': 'sin cambios'}, status=200)
    else:
        return JsonResponse({'errors': form.errors}, status=400)

# ----------------------------
# Eliminar tipo de pago (soft delete)
# ----------------------------
def payment_type_delete(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    payment_type = get_object_or_404(PaymentType, pk=pk)
    payment_type.deleted_at = timezone.now()
    payment_type.save()
    return JsonResponse({'status': 'eliminado'}, status=200)
