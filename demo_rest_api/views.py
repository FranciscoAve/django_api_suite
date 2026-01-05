from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        items=[]
        for elem in data_list:
            if(elem.get("is_active", False)):
                items.append(elem)
        return Response(items, status= status.HTTP_200_OK)

    def post(self, request):
        body = request.data
        if "name" not in body or "email" not in body:
            return Response({'error':'Faltan campos'},status=status.HTTP_400_BAD_REQUEST)
        
        body['id']= str(uuid.uuid4())
        body['is_active'] = True
        data_list.append(body)

        return Response({'message':'Dato guardado exitosamente','data':body}, status= status.HTTP_201_CREATED)

class DemoRestApiItem(APIView):
    name = "Demo REST API 2.0"
    def put(self, request):
        data = request.data
        tabien = False
        for elem in data_list:
            if elem["id"] == data['id']:
                elem["name"] = data["name"]
                elem["email"] = data["email"]
                elem["is_active"] = data["is_active"]
                tabien = True
        if not tabien:
            return Response({"error":"errorrrrrrrr"}, status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data_list, status= status.HTTP_200_OK)
        
