from django.shortcuts import render
from .models import Room

# rooms = [
#     {"id": 1, "name": "Let's learn python"},
#     {"id": 2, "name": "Design with me"},
#     {"id": 3, "name": "Frontend Developers"},
# ]


def home(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "base/home.html", context)


def room(request, id):
    room = Room.objects.get(id=id)

    context = {"room": room}
    return render(request, "base/room.html", context)
