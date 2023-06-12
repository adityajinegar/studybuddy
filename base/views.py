from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {"id": 1, "name": "Let's learn python"},
#     {"id": 2, "name": "Design with me"},
#     {"id": 3, "name": "Frontend Developers"},
# ]


def home(request):
    # expression_if_true if condition else expression_if_false
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    # topic__name, to query upwards to the parent
    # topic__name__icontains - contains means it will check if it contains letters in query string. i.e. Py for Python. i stands for case insensitive
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
    return render(request, "base/home.html", context)


def room(request, id):
    room = Room.objects.get(id=id)

    context = {"room": room}
    return render(request, "base/room.html", context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"obj": room})
