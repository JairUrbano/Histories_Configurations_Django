from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Patient
from ..forms import PatientForm

# ----------------------------
# Listar pacientes
# ----------------------------
def patients_list(request):
    patients = Patient.objects.all()
    data = [
        {
            'id': p.id,
            'name': p.name,
            'document_type': p.document_type.name if p.document_type else None,
        } 
        for p in patients
    ]
    return JsonResponse({'patients': data}, status=200)

# ----------------------------
# Crear paciente
# ----------------------------
def patient_create(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    form = PatientForm(request.POST)
    if form.is_valid():
        patient = form.save()
        return JsonResponse({
            'status': 'creado',
            'id': patient.id,
            'name': patient.name
        }, status=201)
    else:
        return JsonResponse({'errors': form.errors}, status=400)

# ----------------------------
# Actualizar paciente
# ----------------------------
def patient_update(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST, instance=patient)
    if form.is_valid():
        updated = False
        for field, value in form.cleaned_data.items():
            if getattr(patient, field) != value:
                setattr(patient, field, value)
                updated = True
        if updated:
            patient.save()
            return JsonResponse({'status': 'actualizado'}, status=200)
        else:
            return JsonResponse({'status': 'sin cambios'}, status=200)
    else:
        return JsonResponse({'errors': form.errors}, status=400)

# ----------------------------
# Eliminar paciente
# ----------------------------
def patient_delete(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return JsonResponse({'status': 'eliminado'}, status=200)
