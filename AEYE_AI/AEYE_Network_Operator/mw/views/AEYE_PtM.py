from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_ptm_models
from .serializers import aeye_ptm_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests
import os

def print_log(status, whoami, mw, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[AI NetOper - active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.RED + "[AI NetOper - error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

i_am_mw_ptm = 'MW - PtM'

url = 'http://127.0.0.1:3000/hal/print-log/'
class aeye_ptm_Viewswets(viewsets.ModelViewSet):
    queryset=aeye_ptm_models.objects.all().order_by('id')
    serializer_class=aeye_ptm_serializers

    def create(self, request) :
        serializer = aeye_ptm_serializers(data = request.data)

        if serializer.is_valid() :
            i_am_client    = serializer.validated_data.get('whoami')
            message_form_client   = serializer.validated_data.get('message')
            print_log('active', i_am_client, i_am_mw_ptm, "Succeed to Received Data : {}".format(message_form_client))

            response_from_server = aeye_print_to_maintainer_request()

            if response_from_server.status_code==200:
                return response_from_server
            else:
                return response_from_server
        else:
            print_log('error', i_am_mw_ptm, i_am_mw_ptm, "Failed to Received Data : {}".format(request.data))

            message = "Client Sent Invalid Data"
            data = aeye_create_json_data(message)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



def aeye_print_to_maintainer_request():
    data = {
        'whoami'  : i_am_mw_ptm,
        'message' : 'Request AI Test',
    }

    print_log('active', i_am_mw_ptm, i_am_mw_ptm, "Send Data to : {}".format(url))
    response = requests.post(url, data=data)

    if response.status_code==200:
        response_data = response.json()
        print_log('active', i_am_mw_ptm, i_am_mw_ptm, "Received Data from the Server : {}".format(response_data))
        
        i_am_server  = response_data.get('whoami')
        message_from_server = response_data.get('message')
            
        print_log('active', i_am_server, i_am_mw_ptm, "Succedd to Receive Data : {}".format(message_from_server) )
        data = aeye_create_json_data(message_from_server)

        return  Response(data, status=status.HTTP_200_OK)
    else:
        print_log('error', i_am_mw_ptm, i_am_mw_ptm, "Failed to Receive Data from : {}".format(url))

        message_to_client = "Failed to Receive Response From :".format(url)
        data = aeye_create_json_data(message_to_client)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


def aeye_get_data_from_response(reponse):
    response_data = reponse.json()
    whoami = response_data.get('whoami', '')
    message = response_data.get('message', '')

    if whoami:
        if message:
            return whoami, message
        else:
            print_log('error', i_am_mw_ptm, i_am_mw_ptm, "Failed to Receive message from the server : {}"
                                                                                            .format(message))
            return 400
    else:
        print_log('error', i_am_mw_ptm, i_am_mw_ptm, "Failed to Receive whoami from the server : {}"
                                                                                            .format(whoami))
        return 400
    
def aeye_create_json_data(message):
    data = {
        'whoami'  : i_am_mw_ptm,
        'message' : message
    }

    return data