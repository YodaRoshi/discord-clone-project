from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
# This view can only take in GET request 
# @api_view(['GET','PUT','POST'])
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    # safe=False means you can use more than just python dictionary
    # will convert it to json data
    return Response(routes)
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # since we are serialzing a query set
    serializer = RoomSerializer(rooms,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    # since we are serialzing a query set
    serializer = RoomSerializer(room,many=False)
    return Response(serializer.data)