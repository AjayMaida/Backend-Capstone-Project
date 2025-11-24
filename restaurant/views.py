import json
import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .models import Booking
from .forms import BookingForm

def book(request):
    form = BookingForm()
    return render(request, 'book.html', {'form': form})

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except Exception:
            return HttpResponse("{'error':1}", content_type='application/json')

        exists = Booking.objects.filter(reservation_date=data.get('reservation_date'))                                         .filter(reservation_slot=data.get('reservation_slot'))                                         .exists()
        if not exists:
            booking = Booking(
                first_name=data.get('first_name'),
                reservation_date=data.get('reservation_date'),
                reservation_slot=int(data.get('reservation_slot'))
            )
            booking.save()
            return JsonResponse({'success':1})
        else:
            return HttpResponse("{'error':1}", content_type='application/json')

    date = request.GET.get('date', datetime.date.today())
    bookings_qs = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings_qs)
    return HttpResponse(booking_json, content_type='application/json')
