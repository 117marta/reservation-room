from django.db import models


# Sala konferencyjna
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector_availability = models.BooleanField(default=False)


# Rezerwacji sali konferencyjnej
class RoomReservation(models.Model):
    date = models.DateField()  # rezerwacja na dany dzień
    comment = models.TextField()
    # 1 sala może mieć wiele całodniowych rezerwacji. Przy usunięciu sali, usuwane są też jej rezerwacje
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)

    # Dwa pola razem będą unikalne (sala i dzień)
    class Meta:
        unique_together = ('room_id', 'date')
