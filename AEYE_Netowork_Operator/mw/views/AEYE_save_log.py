from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_print_log_models
from .serializers import aeye_print_log_serializers
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
              current_time + " [ " + whoami + " ] send to : " + Fore.BLUE + "[ " + api + " ]" +  
              Fore.RESET + "\n" + Fore.RED + "[error] " + Fore.RED + message + Fore.RESET +
              "\n-----------------------------------------")

server_url    = 'http://127.0.0.1:2000/'
hal_print_log = 'hal/print-log/'
i_am_mw_pl = 'Maintainer MW - PL'

class aeye_print_log_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_print_log_models.objects.all().order_by('id')
    serializer_class=aeye_print_log_serializers

    def create(self, request) :
        serializer = aeye_print_log_serializers(data = request.data)

        if serializer.is_valid() :
            i_am_client        = serializer.validated_data.get('whoami')
            message_client     = serializer.validated_data.get('message')
            cllient_name_raw   = serializer.validated_data.get('client_name_raw')
            client_message_raw = serializer.validated_data.get('client_message_raw')
            client_status_raw  = serializer.validated_data.get('client_status_raw')

            if settings.DEBUG:
                print_log('active', i_am_client, i_am_mw_pl, "Received Data Successfully!")

            response_server = request_print_log(cllient_name_raw, client_message_raw, client_status_raw)
            
            if response_server.status_code==200:
                
                if settings.DEBUG:
                    print_log('active', i_am_mw_pl, i_am_mw_pl, "Received Data From: {}{}".format(server_url, hal_print_log))
                message="Printed Log Successfully!"
                data={
                    'whoami' : i_am_mw_pl,
                    'message':message
                }
                return Response(data, status=status.HTTP_200_OK)
            else:

                if settings.DEBUG:
                    message="Failed receive Data From: {}{}".format(server_url, hal_print_log)
                    print_log('error', i_am_mw_pl, i_am_mw_pl, message)
                data={
                    'whoami' : i_am_mw_pl,
                    'message': message
                }

                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            message="Received Invalid data : {}".format(serializer.errors)
            print_log('error', i_am_mw_pl, i_am_mw_pl, message)
            data={
                'whoami' : i_am_mw_pl,
                'message': message
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def request_print_log(name_client : str, message_client : str, client_status_raw : str)->Response:
    
    if settings.DEBUG:
        message="Request Print Log to : {}{}".format(server_url, hal_print_log)
        print_log("active", i_am_mw_pl, i_am_mw_pl, message)

    message="Request Print Log"
    data={
        'whoami'             : i_am_mw_pl,
        'message'            : message,
        'client_name_raw'    : name_client,
        'client_message_raw' : message_client,
        'client_status_raw'  : client_status_raw
    }

    url='{}{}'.format(server_url, hal_print_log)
    response_server=requests.post(url, data=data)

    if response_server.status_code==200:
        
        if settings.DEBUG:
            message="Received From Server Well from : {}{}".format(server_url, hal_print_log)
            print_log("active", i_am_mw_pl, i_am_mw_pl, message)
        
        
        return response_server
    else:
        message="Failed to receive Data from : {}{}".format(server_url, hal_print_log)
        data={
            'whoami' : i_am_mw_pl,
            'message': message
        }
        
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


