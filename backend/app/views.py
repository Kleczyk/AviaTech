from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import Ticket
from . import forms
import tempfile
import identity
import base64
import numpy as np

def numpy_array_to_base64(arr):
    arr_bytes = arr.tobytes()
    arr_base64 = base64.b64encode(arr_bytes).decode('utf-8')
    return arr_base64

def base64_to_numpy_array(base64_str):
    arr_bytes = base64.b64decode(str(base64_str).encode('utf-8'))
    arr = np.frombuffer(arr_bytes, dtype=np.float64)
    return arr

def register_ticket(request: HttpRequest):
    form = forms.TicketUploadForm(request.POST, request.FILES)
    if form.is_valid():
        passenger_name = form.cleaned_data['passenger_name']
        flight =         form.cleaned_data['flight_id']
        file =           form.cleaned_data['file']

        encoding = None
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file.flush()
                temp_file.seek(0)
                encoding = identity.extract_face_encodings(temp_file)

        encoding_base64 = numpy_array_to_base64(encoding)
        ticket = Ticket(passenger_name=passenger_name, passenger_state='0', biometrics=encoding_base64, flight=flight);
        ticket.save()
        return HttpResponse('')
    return HttpResponse('Invalid request')


def camera_triggered(request: HttpRequest):
    camera = forms.CameraForm(request.POST)
    if camera.is_valid():
        encoding = base64_to_numpy_array(camera.cleaned_data['passenger_biometrics'])

        for ticket in Ticket.objects.filter(flight=camera.cleaned_data['flight']):
            ticket_encoding = base64_to_numpy_array(ticket.biometrics)

            if identity.compare_faces(encoding, ticket_encoding):
                ticket.passenger_state = camera.cleaned_data['location']
                ticket.save()
                return HttpResponse('')

        return HttpResponse('This person wasn\'t found on this flight')
    return HttpResponse('Invalid request')
    

