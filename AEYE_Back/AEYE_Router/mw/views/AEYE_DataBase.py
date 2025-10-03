from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_database_models
from .serializers import aeye_database_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests
import os

def print_log(status, whoami, mw, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + str(whoami) + " ] send to : " + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + str(message) +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + str(whoami) + " ] send to : " + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + str(message) +" ]" + Fore.RESET +
              "\n-----------------------------------------")

i_am_mw_database = 'Router MW - DataBase'

server_url     = 'http://127.0.0.1:2000/'
hal_data_write = 'hal/database-write/'
hal_data_read  = 'hal/database-read/'


class aeye_database_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_database_models.objects.all().order_by('id')
    serializer_class=aeye_database_serializers

    def create(self, request) :
        serializer = aeye_database_serializers(data = request.data)

        if serializer.is_valid():
            i_am_client         = serializer.validated_data.get('whoami')
            message_client      = serializer.validated_data.get('message')
            operation_client    = serializer.validated_data.get('operation')
            request_data_client = serializer.validated_data.get('request_data')


            # save Image

            if operation_client=='DataBase Write':
                message="Client Requested : {}".format(operation_client)
                print_log('active', i_am_client, i_am_mw_database, message)

                reponse_server = aeye_request_database_write(request_data_client)

                if reponse_server.status_code==200:
                    response_data  = reponse_server.json()
                    i_am_server    = response_data.get('whoami')
                    message_server = response_data.get('message')

                    print_log('active', i_am_mw_database, i_am_mw_database, "Succeed to Reacive data from : {}{}".format(server_url, hal_data_write))

                    message='Succedd to read_data'
                    data={
                        'whoami' : i_am_mw_database,
                        'message': message
                    }

                    return Response(data, status=status.HTTP_200_OK)
                else:
                    message="Failed to Reacive data from : {}{}".format(server_url, hal_data_write)
                    print_log('active', i_am_mw_database, i_am_mw_database, message)
                    data={
                        'whoami' : i_am_mw_database,
                        'message': message
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

            elif operation_client=='DataBase Read':
                message="Client Requested : {}".format(operation_client)
                print_log('active', i_am_client, i_am_mw_database, message)

                reponse_server = aeye_request_database_read(request_data_client)

                if reponse_server.status_code==200:
                    response_data  = reponse_server.json()

                    print_log('active', i_am_mw_database, i_am_mw_database, "Succeed to Reacive data from : {}{}".format(server_url, hal_data_read))

                    return Response(response_data, status=status.HTTP_200_OK)
                
                else:
                    message="Failed to Reacive data from : {}{}".format(server_url, hal_data_read)
                    print_log('active', i_am_mw_database, i_am_mw_database, message)
                    data={
                        'whoami' : i_am_mw_database,
                        'message': message
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

            else:
                message="Client Requested Invalid : {}".format(operation_client)
                print_log('error', i_am_client, i_am_mw_database, message)
                data={
                    'whoami' : i_am_mw_database,
                    'message': message
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            message='Server Received Invalid Data : {}'.format(serializer.errors)
            data={
                'whoami'        : i_am_client,
                'message'       : message,
                'operation'     : 'None',
                'reponse__data' : 'None'
            }
            print_log('error', i_am_mw_database, i_am_mw_database, message)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def aeye_request_database_write(request_data_client : str):
    message='Request to write data in SQL'
    data={
        'whoami'       : i_am_mw_database,
        'message'      : message,
        'request_data' : request_data_client
    }
    url='{}{}'.format(server_url, hal_data_read)
    reponse_server=requests.post(url, data=data)

    return reponse_server


def aeye_request_database_read(request_data_client : str):
    message='Request to read data from SQL'
    data={
        'whoami'       : i_am_mw_database,
        'message'      : message,
        'request_data' : request_data_client
    }
    url='{}{}'.format(server_url, hal_data_read)
    reponse_server=requests.post(url, data=data)

    return reponse_server

