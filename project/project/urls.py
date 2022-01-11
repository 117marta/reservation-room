"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from reservation_app.views import (
    AddRoomView,
    RoomListView,
    DeleteRoomView,
    ModifyRoomView,
    ReservationRoomView,
    RoomDetailsView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', TemplateView.as_view(template_name='reservation_app/base.html')),
    path('room/view/', AddRoomView.as_view(), name='add-room'),
    path('room_list/', RoomListView.as_view(), name='room-list'),
    path('room/delete/<int:room_id>/', DeleteRoomView.as_view(), name='delete-view'),
    path('room/modify/<int:room_id>/', ModifyRoomView.as_view(), name='modify-view'),
    path('room/reserve/<int:room_id>/', ReservationRoomView.as_view(), name='reservation-room'),
    path('room/<int:room_id>/', RoomDetailsView.as_view(), name='room-details'),
]
