from django.http import JsonResponse
from django.utils import timezone
from ..models import PredeterminedPrice
from ..forms import PredeterminedPriceForm

def predetermined_prices_list(request):
    prices = PredeterminedPrice.objects.filter(deleted_at__isnull=True)
    data = [
        {
            'id': p.id,
            'name': getattr(p, 'name', ''),
            'price': getattr(p, 'price', 0),
            'created_at': p.created_at,
        }
        for p in prices
    ]
    return JsonResponse({'prices': data}, status=200)

def predetermined_price_create(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    form = PredeterminedPriceForm(request.POST)
    if form.is_valid():
        price = form.save()
        return JsonResponse({
            'status': 'creado',
            'id': price.id,
            'name': getattr(price, 'name', ''),
            'price': getattr(price, 'price', 0),
        }, status=201)
    else:
        return JsonResponse({'errors': form.errors}, status=400)

def predetermined_price_update(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        price = PredeterminedPrice.objects.get(pk=pk, deleted_at__isnull=True)
    except PredeterminedPrice.DoesNotExist:
        return JsonResponse({'error': 'Precio no encontrado'}, status=404)

    form = PredeterminedPriceForm(request.POST, instance=price)
    if form.is_valid():
        updated = False
        for field, value in form.cleaned_data.items():
            if getattr(price, field) != value:
                setattr(price, field, value)
                updated = True
        if updated:
            price.save()
            return JsonResponse({'status': 'actualizado'}, status=200)
        else:
            return JsonResponse({'status': 'sin cambios'}, status=200)
    else:
        return JsonResponse({'errors': form.errors}, status=400)

def predetermined_price_delete(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        price = PredeterminedPrice.objects.get(pk=pk, deleted_at__isnull=True)
    except PredeterminedPrice.DoesNotExist:
        return JsonResponse({'error': 'Precio no encontrado'}, status=404)

    price.deleted_at = timezone.now()
    price.save()
    return JsonResponse({'status': 'eliminado'}, status=200)
