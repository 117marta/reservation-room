from django.shortcuts import render, redirect
from django.views import View
from .models import Room, RoomReservation
import datetime


# Dodaj salę konferencyjną
class AddRoomView(View):

    def get(self, request):
        return render(request, 'reservation_app/add_room.html')

    def post(self, request):
        name = request.POST.get('room-name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector') == 'on'  # rzutowanie na typ logiczny, sprawdzając czy wartość (on) jest ustawiona

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


# Wyświetl listę wszystkich sal
class RoomListView(View):

    def get(self, request):
        rooms = Room.objects.all().order_by('name')
        return render(request, 'reservation_app/room_list.html', context={'rooms': rooms})


# Usunięcie sali konferencyjnej z bazy
class DeleteRoomView(View):

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        room.delete()
        return redirect('/room_list/')


# Modyfikacja sali konferencyjnej
class ModifyRoomView(View):

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        return render(request, 'reservation_app/modify_room.html', context={'room': room})

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        name = request.POST.get('room-name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector') == 'on'

        # Błędy
        if not name:  # Czy nazwa nie jest pusta
            ctx = {'room': room, 'error': 'Nie podano nazwy sali!'}
            return render(request, 'reservation_app/modify_room.html', context=ctx)
        if capacity <= 0:  # Czy pojemność sali jest dodatnia
            ctx = {'room': room, 'error': 'Pojemność musi być dodatnia!'}
            return render(request, 'reservation_app/modify_room.html', context=ctx)
        if name != room.name and Room.objects.filter(name=name).first():  # czy nazwa została zmieniona i nie pokrywa się z inną salą
            ctx = {'room': room, 'error': 'Podana nazwa sali już istnieje!'}
            return render(request, 'reservation_app/modify_room.html', context=ctx)

        # Modyfikacja obiektu
        room.name = name
        room.capacity = capacity
        room.projector_availability = projector
        room.save()
        return redirect('room-list')


# Rezerwacja sali konferencyjnej
class ReservationRoomView(View):

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        return render(request, 'reservation_app/reservation_room.html', context={'room': room})

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        date = request.POST.get('reservation-date')
        comment = request.POST.get('comment')

        # Czy sala nie jest już zarezerwowana
        if RoomReservation.objects.filter(room_id=room, date=date):
            ctx = {'room': room, 'error': 'Sala jest już zarezerwowana!'}
            return render(request, 'reservation_app/reservation_room.html', context=ctx)

        # Czy użytkownik nie wprowadził daty z przeszłości
        if date < str(datetime.date.today()):
            ctx = {'room': room, 'error': 'Nie możesz rezerwować wstecz!'}
            return render(request, 'reservation_app/reservation_room.html', context=ctx)

        # Zapisanie nowej rezerwacji do bazy
        RoomReservation.objects.create(room_id=room, date=date, comment=comment)
        return redirect('room-list')


# Szczegółowy widok sali
class RoomDetailsView(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        # Wszystkie terminy rezerwacji (z obiektu naszej sali) posortowane od najstarszej
        reservations = room.roomreservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, 'reservation_app/room_details.html', context={'room': room, 'reservations': reservations})
