from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_ano_models
from .serializers import aeye_ano_serializers
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
              current_time + " [ " + whoami + " ] send to : " + Fore.LIGHTBLUE_EX + "[ " + api + " ]" +  
              Fore.RESET + "\n" + Fore.GREEN + "[active] " +  message + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + Fore.BLUE + "[ " + api + " ]" +  
              Fore.RESET + "\n" + Fore.RED + "[error] " + Fore.RED + message + Fore.RESET +
              "\n-----------------------------------------")

i_am_api_ano = 'NetOper API - ANO'

url = 'http://127.0.0.1:3000/mw/ai-inference/'

class aeye_ano_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_ano_models.objects.all().order_by('id')
    serializer_class=aeye_ano_serializers

    def create(self, request) :
        serializer = aeye_ano_serializers(data = request.data)

        if serializer.is_valid() :
            i_am_client    = serializer.validated_data.get('whoami')
            operation_client = serializer.validated_data.get('operation')
            message_client   = serializer.validated_data.get('message')

            message='received message  : {}\n         received operation: {}'\
                                            .format(message_client, operation_client)
            print_log('active', i_am_client, i_am_api_ano, message)
            
            if operation_client=='Inference' :
                image = request.FILES.get('image')

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response_from_server = loop.run_until_complete(aeye_ai_inference_request(image, url))
                
                if response_from_server.status_code==200:
                    i_am_server, message = aeye_get_data_from_response(response_from_server)
                    data = aeye_create_json_file(message)

                    return Response(data, status=status.HTTP_200_OK)
                else:
                    message = 'Failed to Receive Data From Server'
                    data = aeye_create_json_file(message)

                    return Response(data, status = status.HTTP_400_BAD_REQUEST)
                
            elif operation_client=='Train':
                pass
            elif operation_client=='Test':
                pass
            else:
                pass
        else :
            message='Sent Invalide Data : {}'.format(serializer.errors)
            data={
                'whoami' : i_am_api_ano,
                'message': message
            }
            print_log('active', i_am_client, i_am_api_ano, message)

            return Response(data, status = status.HTTP_400_BAD_REQUEST)
    

async def aeye_ai_inference_request(image, url):

    print_log('active', i_am_api_ano, i_am_api_ano, "send data to : {}".format(url))

    async with aiohttp.ClientSession() as session:
        message='Request AI Inference'
        form_data = aiohttp.FormData()
        form_data.add_field('whoami', i_am_api_ano)
        form_data.add_field('message', message)
        form_data.add_field('image', image.read(), filename=image.name, content_type=image.content_type)
        async with session.post(url, data=form_data) as response_from_server:
            result_from_server = await response_from_server


    if result_from_server.status_code==200:

        whoami, message = aeye_get_data_from_response(result_from_server)
        print_log('active', whoami, i_am_api_ano, "received data from : {}".format(url))

        return result_from_server
    else:
        message="failed to send data to : {}\n" + \
                "received message from the server: {}".formaturl, message
        print_log('error', whoami, i_am_api_ano, message)
        return result_from_server


def aeye_get_data_from_response(reponse):
    response_data = reponse.json()
    whoami = response_data.get('whoami', '')
    message = response_data.get('message', '')

    if whoami:
        if message:
            return whoami, message
        else:
            print_log('error', i_am_api_ano, i_am_api_ano, "Failed to Receive message from the server : {}"
                                                                                            .format(message))
            return 400
    else:
        print_log('error', i_am_api_ano, i_am_api_ano, "Failed to Receive whoami from the server : {}"
                                                                                            .format(whoami))
        return 400
    
def aeye_create_json_file(message):
    data = {
        'whoami' : i_am_api_ano,
        'message' : message
        }

    return data