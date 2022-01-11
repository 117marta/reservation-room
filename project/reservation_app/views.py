from django.shortcuts import render, redirect
from django.views import View
from .models import Room


class AddRoomView(View):

    def get(self, request):
        return render(request, 'reservation_app/add_room.html')

    def post(self, request):
        name = request.POST.get('room-name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector')  == 'on'  # rzutowanie na typ logiczny, sprawdzając czy wartość (on) jest ustawiona

        # Błędy
        if not name:  # Czy nazwa nie jest pusta
            return render(request, 'reservation_app/add_room.html', context={'error': 'Nie podano nazwy sali!'})
        if capacity <= 0:  # Czy pojemność sali jest dodatnia
            return render(request, 'reservation_app/add_room.html', context={'error': 'Pojemność musi być dodatnia!'})
        if Room.objects.filter(name=name).first():
            return render(request, 'reservation_app/add_room.html', context={'error': 'Podana nazwa sali już istnieje!'})

        # Dodanie nowego obiektu
        Room.objects.create(name=name, capacity=capacity, projector_availability=projector)
        return redirect('room-list')
