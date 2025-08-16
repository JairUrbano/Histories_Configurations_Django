from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ..models import Appointment
from ..forms import AppointmentForm

def appointments_list(request):
    appointments = Appointment.objects.all()
    data = [{
        'id': appt.id,
        'patient': appt.patient.id if hasattr(appt, 'patient') else None,
        'date': appt.date.isoformat() if appt.date else None,
        'notes': getattr(appt, 'notes', '')
    } for appt in appointments]
    return JsonResponse({'appointments': data}, status=200)

def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            return JsonResponse({'message': 'Cita creada correctamente', 'id': appt.id}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appt = form.save()
            return JsonResponse({'message': 'Cita actualizada correctamente', 'id': appt.id}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return JsonResponse({'message': 'Cita eliminada correctamente'}, status=200)
