from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_inference_models
from .serializers import aeye_inference_serializers
from .forms import aeye_image_form
from colorama import Fore, Back, Style, init
from datetime import datetime
import requests
import os
import hashlib
import AEYE_LangChain as LLM


def print_log(status, whoami , mw , message):
    
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] Send to : " + Fore.LIGHTBLUE_EX + "[ " + mw + " ]" +  Fore.RESET + "\n" +
              Fore.GREEN + "[active] " + Fore.GREEN + message +" " + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + "] Send to : " + Fore.LIGHTBLUE_EX + "[ " + mw + " ]" +  Fore.RESET + "\n" +
              Fore.RED + "[error] " + Fore.RED + message +" " + Fore.RESET +
              "\n-----------------------------------------")

i_am_mw_infer = 'NetOper MW - Inference'

server_url   = 'http://opticnet_container:2000'
url_ai       = '/api/ai-toolkit/'
url_upload   = '/api/upload-file-chunk/'
url_start    = '/api/start-upload-file/' 
url_assemble = '/api/data-assemble/'

class aeye_inference_Viewswets(viewsets.ModelViewSet):
    queryset=aeye_inference_models.objects.all().order_by('id')
    serializer_class=aeye_inference_serializers

    def create(self, request) :
        serializer=aeye_inference_serializers(data = request.data)
        form=aeye_image_form(request.POST, request.FILES)

        if serializer.is_valid() :
            whoami_client       = serializer.validated_data.get('whoami')
            message_from_client = serializer.validated_data.get('message')
            
            if form.is_valid() :
                form.save()
            
            print_log('active', whoami_client, i_am_mw_infer, "MW - Inference received message : {}".format(message_from_client))

            image = request.FILES.get('image')
            response_from_server = aeye_ai_inference_request(image)
            
            #####################################################
            message_server = response_from_server.get('message')
            llm_response   = LLM.aeye_langchain(message_server)
            data = aeye_create_json_data(llm_response)

            return Response(data, status=status.HTTP_200_OK)
           #####################################################
        else:
            print_log('error', i_am_mw_infer, i_am_mw_infer, "Received Invalid Data : {}".format(serializer.errors))

            message = "Client Sent Invalid Data"
            data = aeye_create_json_data(message)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def aeye_upload_data(file_path, chunk_size):

    file_name = file_path.split('/')[-1]
    file_size = os.path.getsize(file_path)
    
    # Read Hash
    with open(file_path, 'rb') as f:
        file_hash = calculate_hash(f.read())
    
    message  = 'check server status : {}{}'.format(server_url, url_start)
    metadata = {
        'whoami'    : i_am_mw_infer,
        'message'   : message,
        'file_name'  : file_name,
        'file_size' : file_size,
        'file_hash' : file_hash
    }
    
    # Request for TCP Protocol.
    print_log('active', i_am_mw_infer, i_am_mw_infer, message)
    response = requests.post("{}{}".format(server_url, url_start), data=metadata)
    if response.status_code != 200:
        message = 'Failed to receive ok from : {}{}'.format(server_url, url_start)
        data = {
            'whoami'  : i_am_mw_infer,
            'message' : message
        }
        print_log('error', i_am_mw_infer, i_am_mw_infer, message)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    message = 'server is ok : {}{}'.format(server_url, url_start)
    print_log('active', i_am_mw_infer, i_am_mw_infer, message)

    # Split File into chunks
    with open(file_path, 'rb') as tmp_file:
        chunk_index=0
        while True:
            chunk=tmp_file.read(chunk_size)
            if not chunk:
                break
            chunk_hash=calculate_hash(chunk)
            files={'file' : (file_name, chunk)}
            data={
                'whoami'      : i_am_mw_infer,
                'message'     : 'send files in chunk',
                'chunk_index' : chunk_index,
                'chunk_hash'  : chunk_hash
            }
            response=requests.post("{}{}".format(server_url, url_upload), files=files, data=data)
            
            if response.status_code!=200:
                data = "Failed to send data to : {}{}".format(server_url, url_upload)
                print_log('error', i_am_mw_infer, i_am_mw_infer, message)
                
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            chunk_index += 1
    
    total_chunk_index = chunk_index
    
    # Request Assemble
    message='request to assmble files to : {}{}'.format(server_url, url_assemble)
    data={
        'whoami'            : i_am_mw_infer,
        'message'           : message,
        'file_name'         : file_name,
        'total_chunk_index' : total_chunk_index,
        'total_chunk_hash'  : file_hash
    }
    response_from_server = requests.post("{}{}".format(server_url, url_assemble), data=data)

    if response_from_server.status_code==200:
        message_to_client='succeed to assemble files from : {}{}'.format(server_url, url_assemble)
        data={
            'whoami'  : i_am_mw_infer,
            'message' : message_to_client
        }
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        message_to_client='Failed to assemble files from : {}{}'.format(server_url, url_assemble)
        data={
            'whoami'  : i_am_mw_infer,
            'message' : message_to_client
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            
        
def calculate_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()



def aeye_ai_inference_request(image)->Response:
    operation = 'Inference'
    
    chunk_size = 5 * 1024 * 1024  # 5MB 

    img_file_path = os.path.join(os.path.dirname(__file__), 'images', image.name)
    response_image  = aeye_upload_data(file_path=img_file_path, chunk_size=chunk_size)
    
    h5_file_path = os.path.join(os.path.dirname(__file__), 'weight', 'Srinivasan2014.h5')
    response_weight = aeye_upload_data(h5_file_path, chunk_size=chunk_size)

    if response_image.status_code==200:
        if response_weight.status_code==200:
            message='request AI Inference to : {}{}'.format(server_url, url_ai)
            data = {
                'whoami'    : i_am_mw_infer,
                'operation' : operation,
                'message'   : message,
            }
            print_log('active', i_am_mw_infer, i_am_mw_infer, message)
            response = requests.post("{}{}".format(server_url, url_ai), data=data)

            if response.status_code==200:
                response_data = response.json()
                message="Received Data from the Server : {}".format(response_data)
                print_log('active', i_am_mw_infer, i_am_mw_infer, message)
                #whoami, message = aeye_get_data_from_response(response_data)
                
                i_am_server    = response_data.get('whoami')
                message_server = response_data.get('message')
                
                print_log('active', i_am_mw_infer, i_am_mw_infer, "Succedd to Receive Data : {}".format(message_server) )
                data = aeye_create_json_data(message)

                return  Response(data, status=status.HTTP_200_OK)
            else:
                print_log('error', i_am_mw_infer, i_am_mw_infer, "Failed to Receive Data : {}".format(message) )

                message = 'Failed to Get Response For the Server'
                data = aeye_create_json_data(message)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            print_log('error', i_am_mw_infer, i_am_mw_infer, "Failed to Upload Weight")

            message = 'Failed to Upload image and files to Json files'
            data = aeye_create_json_data(message)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        pass
    

def aeye_create_json_files(whoami, image):
    
    h5_file_path = os.path.join(os.path.dirname(__file__), 'weight', 'Srinivasan2014.h5')

    try:
        h5_file = open(h5_file_path, 'rb')
        files = {
            'image' : (image.name, image.read(), image.content_type),
            'weight': ('model.h5', h5_file, 'application/octet-stream'),
        }
        print_log('active', i_am_mw_infer, i_am_mw_infer, "Succeeded to add image and h5 files to JSON files")
        return files
    except Exception as e:
        message='Failed to add image and h5 files to JSON files: {}'.format(str(e))
        print_log('error', i_am_mw_infer, i_am_mw_infer, message)
        return 400


def aeye_get_data_from_response(reponse):
    response_data = reponse.json()
    whoami = response_data.get('whoami', '')
    message = response_data.get('message', '')

    if whoami:
        if message:
            return whoami, message
        else:
            print_log('error', i_am_mw_infer, i_am_mw_infer, "Failed to Receive message from the server : {}"
                                                                                            .format(message))
            return 400
    else:
        print_log('error', i_am_mw_infer, i_am_mw_infer, "Failed to Receive whoami from the server : {}"
                                                                                            .format(whoami))
        return 400
    
def aeye_create_json_data(message : str):
    data = {'whoami' : 'AEYE NetOper MW Inference', 'message' : message}

    return data