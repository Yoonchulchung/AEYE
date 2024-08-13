from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_hal_print_log_models
from .serializers import aeye_hal_print_log_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests
from django.conf import settings


def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if str(status) == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + str(whoami) + " ] send to : " + Fore.LIGHTBLUE_EX + "[ " + str(api) + " ]" +  
              Fore.RESET + "\n" + Fore.GREEN + "[active] " +  str(message) + Fore.RESET +
              "\n-----------------------------------------")
    elif str(status) == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + str(whoami) + " ] send to : " + Fore.BLUE + "[ " + str(api) + " ]" +  
              Fore.RESET + "\n" + Fore.RED + "[error] " + Fore.RED + str(message) + Fore.RESET +
              "\n-----------------------------------------")

i_am_hw_pl = 'Maintainer HAL - PL'

class aeye_hal_print_log_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_hal_print_log_models.objects.all().order_by('id')
    serializer_class=aeye_hal_print_log_serializers

    def create(self, request) :
        serializer = aeye_hal_print_log_serializers(data = request.data)

        if serializer.is_valid() :
            i_am_client        = serializer.validated_data.get('whoami')
            message_client     = serializer.validated_data.get('message')
            client_name_raw   = serializer.validated_data.get('client_name_raw')
            client_message_raw = serializer.validated_data.get('client_message_raw')
            client_status_raw  = serializer.validated_data.get('client_status_raw')

            if settings.DEBUG:
                print_log('active', i_am_client, i_am_hw_pl, "Received Data Successfully!")


            print_log(client_status_raw, client_name_raw, i_am_hw_pl, client_message_raw)
            message="Printed Well"
            data={
                'whoami' : i_am_hw_pl,
                'message': message
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            message="Received Invalid data : ".format(serializer.errors)
            data={
                'whoami' : i_am_hw_pl,
                'message': message
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

