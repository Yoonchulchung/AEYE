from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_database_write_models
from .serializers import aeye_database_write_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests
import os

def print_log(status, whoami, hal, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + Fore.BLUE + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + "[ " + hal + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

i_am_hal_write_data = 'Router HAL - DataBase Write'


class aeye_database_write_Viewswets(viewsets.ModelViewSet):
    queryset=aeye_database_write_models.objects.all().order_by('id')
    serializer_class=aeye_database_write_serializers

    def create(self, request) :
        serializer = aeye_database_write_serializers(data = request.data)

        if serializer.is_valid() :
            i_am_client      = serializer.validated_data.get('whoami')
            message_client   = serializer.validated_data.get('message')
            request_data     = serializer.validated_data.get('request_data')

            ##############################################
            # MySQL Connection
            
            message="GOOD"
            data={
                'whoami' : i_am_hal_write_data,
                'message': message
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            message = serializer.errors
            print_log('error', i_am_hal_write_data, i_am_hal_write_data, "Failed to Received Data : {}".format(message))

            message = "Failed to Write Data in DataBase"
            data={
                'whoami'  : i_am_hal_write_data,
                'message' : message
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)