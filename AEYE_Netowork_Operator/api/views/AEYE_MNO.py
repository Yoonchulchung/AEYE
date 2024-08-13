from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_mno_models
from .serializers import aeye_mno_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests
from django.conf import settings


def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + Fore.LIGHTBLUE_EX + "[ " + api + " ]" +  
              Fore.RESET + "\n" + Fore.GREEN + "[active] " +  message + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + Fore.BLUE + "[ " + api + " ]" +  
              Fore.RESET + "\n" + Fore.RED + "[error] " + Fore.RED + message + Fore.RESET +
              "\n-----------------------------------------")

server_url    = '127.0.0.1:2000/'
mw_print_log = '/mw/print-log/'
mw_save_log  = '/mw/save-log/'
i_am_api_ano = 'Maintainer API - MNO'

class aeye_mno_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_mno_models.objects.all().order_by('id')
    serializer_class=aeye_mno_serializers

    def create(self, request) :
        serializer = aeye_mno_serializers(data = request.data)

        if serializer.is_valid() :
            i_am_client      = serializer.validated_data.get('whoami')
            operation_client = serializer.validated_data.get('operation')
            message_client   = serializer.validated_data.get('message')
            status_client    = serializer.validated_data.get('status')
            name_client      = i_am_client

            if operation_client=='print_log':
                response_server = aeye_print_log(message_client, name_client, status_client)

                if response_server.status_code==200:
                    response_server = aeye_save_log(message_client, name_client)

                    return response_server
                else:
                    message="Failed to receive response from: {}{}".format(server_url, mw_save_log)
                    data={
                        'whoami' : i_am_api_ano,
                        'message': message
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
        else:
            message="Received Invalid data : ".format(serializer.errors)
            data={
                'whoami' : i_am_api_ano,
                'message': message
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def aeye_print_log(message_client : str, name_client : str, status_client : str)->Response:
    message="Request Print Log"
    data={
        'whoami'             : i_am_api_ano,
        'message'            : message,
        'client_name_raw'    : name_client,
        'client_message_raw' : message_client,
        'client_status_raw'  : status_client
    }
    url='{}{}'.format(server_url, mw_print_log)

    if settings.DEBUG:
        message="Send Data to : {}{}".format(server_url, mw_print_log)
        print_log('active', i_am_api_ano,i_am_api_ano, message)

    response_print_log=requests.post(url, data=data)
    
    if response_print_log.statu_code==200:
        response_data=response_print_log.json()
        whoami_server  = response_data.get('whoami', '')
        message_server = response_data.get('message', '')

        if settings.DEBUG:
            message="Reaceived response_print_log: {}".format(message_server)
            print_log('active', whoami_server, i_am_api_ano, message)

        return response_print_log
    else:
        message="Failed to Received Data from : {}{}".fromat(server_url, mw_print_log)
        data={
            'whoami' : i_am_api_ano,
            'message': message
        }
        Response(data, status=status.HTTP_400_BAD_REQUEST)

def aeye_save_log(message_client : str, name_client : str)->Response:
    data={
        'whoami'      : i_am_api_ano,
        'message'     : message_client,
        'name_client' : name_client
    }
    url='{}{}'.format(server_url, mw_save_log)
    response_save_log=requests.post(url, data=data)
    
    if response_save_log.statu_code==200:
        response_data=response_save_log.json()
        whoami_server  = response_data.get('whoami', '')
        message_server = response_data.get('message', '')

        if settings.DEBUG:
            message="Reaceived response_print_log: {}".format(message_server)
            print_log('active', whoami_server, i_am_api_ano, message)

        return response_save_log
    else:
        message="Failed to Received Data from : {}{}".fromat(server_url, mw_save_log)
        data={
            'whoami' : i_am_api_ano,
            'message': message
        }
        Response(data, status=status.HTTP_400_BAD_REQUEST)
    