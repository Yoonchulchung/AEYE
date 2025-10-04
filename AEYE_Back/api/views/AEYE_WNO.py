from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_wno_models
from .serializers import aeye_wno_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests
import asyncio
import aiohttp


def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " +Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

i_am_api_wno = 'Router API - WNO'

url_server       = 'http://127.0.0.1:2000/'
mw_ai_inference  = 'mw/ai-inference/'
mw_database      = 'mw/database/'

class aeye_wno_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_wno_models.objects.all().order_by('id')
    serializer_class=aeye_wno_models

    def create(self, request) :
        serializer = aeye_wno_serializers(data = request.data)

        if serializer.is_valid() :
            i_am_client      = serializer.validated_data.get('whoami')
            operation_client = serializer.validated_data.get('operation')
            message_client   = serializer.validated_data.get('message')

            print_log('active', i_am_api_wno, i_am_api_wno, 'Received Valid Data : {}, Oper: {}'.format(message_client, operation_client))
            
            if operation_client=='Inference' :
                image = request.FILES.get('image')

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response_from_server = loop.run_until_complete(aeye_ai_inference_request(i_am_client, image))
                
                print_log('active', i_am_client, i_am_api_wno, "Succed to Receive Data from : {}{}".format(url_server, mw_ai_inference))

                i_am_server    = response_from_server.get('whoami')
                server_message = response_from_server.get('message')

                data={
                    'whoami' : i_am_api_wno,
                    'message': server_message
                } 
                return Response(data, status=status.HTTP_200_OK)

            elif operation_client=='Train':
                pass
            elif operation_client=='Test':
                pass
            elif operation_client=='DataBase Write' or 'DataBase Read':
                response = aeye_database_requst(operation_client)

                if response.status_code==200:
                    message='succeed to reacive data from : {}{}'.format(url_server, mw_database)
                    print_log("active", i_am_api_wno, i_am_api_wno, message)
                    message="GODD"
                    data={
                        'whoami' : i_am_api_wno,
                        'message': message 
                    }
                    return Response(data, status=status.HTTP_200_OK)  
                else:
                    message="failed to Reacive data from : {}{}".format(url_server, mw_database)
                    data={
                        'whoami' : i_am_api_wno,
                        'message': message
                    } 
                    print('error', i_am_api_wno, i_am_api_wno, message)
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            message="Reacived Invalid data : {}".format(serializer.errors)
            data={
                'whoami' : i_am_api_wno,
                'message': message
            }
            print_log('error', i_am_api_wno, i_am_api_wno, message)
            return Response(data, status = status.HTTP_400_BAD_REQUEST)
    

async def aeye_ai_inference_request(i_am_client : str, image):
    message = "Failed to Receive Data [NetOper - WNO]"
    url='{}{}'.format(url_server, mw_ai_inference)
    print_log('active', i_am_client, i_am_api_wno, "Send Data to : {}".format(url))

    async with aiohttp.ClientSession() as session:
        message='Request AI Inference'
        form_data = aiohttp.FormData()
        form_data.add_field('whoami', i_am_api_wno)
        form_data.add_field('message', message)
        form_data.add_field('image', image.read(), filename=image.name, content_type=image.content_type)
        async with session.post(url, data=form_data) as response_from_server:
            result_from_server = await response_from_server.json()

    return result_from_server


def aeye_database_requst(operation_client):
    message='request data to : {}{}'.format(url_server, mw_database)
    print_log('active', i_am_api_wno, i_am_api_wno, message)

    message='Request DataBase'
    data={
        'whoami'       : i_am_api_wno,
        'message'      : message,
        'operation'    : operation_client,
        'request_data' : "None"
    }
    url='{}{}'.format(url_server, mw_database)
    response_server = requests.post(url, data=data)
    return response_server