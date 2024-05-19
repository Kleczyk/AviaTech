from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import Ticket
from . import forms

# def flight(request: HttpRequest):
#     flight_airport = request.POST["airport"]
#     flight_terminal = request.POST["terminal"]
#     if flight_airport is None or flight_terminal is None:
#         return
#
#     flight = Flight(airport=flight_airport, terminal=flight_terminal)
#     flight.save()
#
#     return JsonResponse({'id' : flight.id})
#
# def flight_delete(request: HttpRequest):
#     flight_id = request.POST["id"]
#     if flight_id is None:
#         return
#
#     Flight.objects.get(id=flight_id).delete()
#     return HttpResponse('ok')
#

def register_ticket(request: HttpRequest):
    form = forms.TicketUploadForm(request.POST, request.FILES)
    if form.is_valid():
        passenger_name = form.cleaned_data['passenger_name']
        flight =         form.cleaned_data['flight_id']
        file =           form.cleaned_data['file']
        # todo download attached file
        # dispatch file for AI stuff
        # dump vector data to db
        ticket = Ticket(passenger_name=passenger_name, passenger_state='0', biometrics="A", flight=flight);
        ticket.save()
        return HttpResponse('ok')
    return HttpResponse('Invalid request')


def camera_triggered(request: HttpRequest):
    camera = forms.CameraForm(request.POST)
    if camera.is_valid():
        biometrics = camera.cleaned_data['passenger_biometrics']
        for ticket in Ticket.objects.filter(flight=camera.cleaned_data['flight']):
            if ticket.biometrics == biometrics: # todo actual comparation
                ticket.passenger_state = camera.cleaned_data['location']
                ticket.save()
                return HttpResponse('ok')
        return HttpResponse('This person wasn\'t found on this flight')
    return HttpResponse('Invalid request')
    

