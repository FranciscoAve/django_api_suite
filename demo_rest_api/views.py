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
    name = "Demo REST API Item"

    def put(self, request, id):
        data = request.data
        tabien = False

        if len(data) < len(data_list[0]) - 1:
            return Response({"error": "Campos incompletos"}, status=status.HTTP_400_BAD_REQUEST)
        
        for elem in data_list:
            if elem["id"] == id:
                elem["name"] = data["name"]
                elem["email"] = data["email"]
                elem["is_active"] = data["is_active"]
                tabien = True

        if not tabien:
            return Response({"error":"Elemento no encontrado con el id proporcionado"}, status= status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Elemento actualizado exitosamente","data":data_list}, status= status.HTTP_200_OK)
        
    def patch(self, request, id):
        data = request.data
        tabien = False
        
        for elem in data_list:
            if elem["id"] == id:
                for clave in data:
                    if clave != "id": #no reemplazo del id
                        elem[clave] = data[clave]
                tabien = True

        if not tabien:
            return Response({"error":"Elemento no encontrado con el id proporcionado"}, status= status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":"Elemento actualizado parcialmente","data":data_list}, status= status.HTTP_200_OK)
    
    def delete(self,request, id):
        data = request.data
        tabien=False

        for elem in data_list:
            if elem.get("id") == id:
                elem["is_active"] = False
                tabien = True
        
        if not tabien:
            return Response({"error":"Elemento no encontrado con el id proporcionado"}, status= status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message":"Elemento eliminado lógicamente","data":data_list}, status= status.HTTP_200_OK)



