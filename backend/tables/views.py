from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import table
from .serializers import tableSerializer

@api_view(['POST'])
def addTable(request):
    serializer = tableSerializer(data = {})
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    return Response("la mesa fue agregada")

@api_view(['GET'])
def getStatusPerTable(request,id):
    tableObj = get_object_or_404(table, pk=id)
    serializer = tableSerializer (tableObj)
    return Response(serializer.data)

@api_view(['Get'])
def getAllStatus(resquet):
    all_tables = table.objects.all()
    serializar = tableSerializer(all_tables, many=True)
    return Response(serializar.data)

@api_view(['POST'])
def updateStatusPerTable(request):
    id = request.data.get('id')
    new_status = request.data.get('new_status')
    tableObj = get_object_or_404(table, pk=id)
    tableObj.status = new_status
    tableObj.save()
    serializar = tableSerializer(tableObj)
    return Response(serializar.data)