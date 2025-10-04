from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_inference_models
from .serializers import aeye_inference_serializers
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

i_am_hal_infer = 'Router HAL - Inference'

server_url=''
api_ano=''

class aeye_inference_Viewswets(viewsets.ModelViewSet):
    queryset=aeye_inference_models.objects.all().order_by('id')
    serializer_class=aeye_inference_serializers

    def create(self, request) :
        serializer = aeye_inference_serializers(data = request.data)

        if serializer.is_valid() :
            whoami    = serializer.validated_data.get('whoami')
            message   = serializer.validated_data.get('message')
            print_log('active', whoami, i_am_hal_infer, "Succeed to Received Data : {}".format(message))

            image = request.FILES.get('image')
            data={
                'whoami' : i_am_hal_infer,
                'message': "GG"
            }
            return Response(data, status=status.HTTP_200_OK)
            # response = aeye_ai_inference_request(image, url)
            '''
            if response.status_code==200:
                return response
            else:
                return response
            '''
            
        else:
            message = "Client Sent Invalid Data : {}".format(serializer.errors)
            print_log('error', i_am_hal_infer, i_am_hal_infer, message)
            data={
                'whoami' : i_am_hal_infer,
                'message': message
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



def aeye_ai_inference_request(image, url)->Response:

    files = {
            'image': (image.name, image.read(), image.content_type),
        }
    
    data = {
        'whoami' : i_am_hal_infer,
        'operation' : 'Inference',
        'message' : 'Request AI Inference',
    }

    print_log('active', whoami, i_am_hal_infer, "Send Data to : {}".format(url))
    response = requests.post(url, data=data, files=files)

    if response.status_code==200:
        response_data = response.json()
        print_log('active', whoami, i_am_hal_infer, "Received Data from the Server : {}".format(response_data))
        whoami  = response_data.get('whoami')
        message = response_data.get('message')
        
        print_log('active', whoami, i_am_hal_infer, "Succedd to Receive Data : {}".format(message) )
        data={
            'whoami' : i_am_hal_infer,
            'message': message
        }
        return  Response(data, status=status.HTTP_200_OK)
    else:
        print_log('error', whoami, i_am_hal_infer, "Failed to Receive Data : {}".format(message) )

        message = "Failed to Get Response from : {}".format(url)
        data={
            'whoami' : i_am_hal_infer,
            'message': message
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)