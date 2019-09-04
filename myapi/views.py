from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets

from .serializers import HeroSerializer
from .models import Hero


from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
import json
import socket
import sys
import  PIL
from PIL import Image
from io import BytesIO
import base64

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer
    
    
# def get(self, request):
#     a = 1+1
#     return HttpResponse('Albinos'+a) # Redirect after POST
@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Your code for POST
        a = json.loads(request.body)
        stringImagen = str(a['base64'])

        # ------------------------ RESIZE IMAGEN -------------------#
        # adjust width and height to your needs
        width = 240
        height = 320

        im1 = PIL.Image.open(BytesIO(base64.b64decode(stringImagen)))

        im1.save("imagenBase64.jpg")

        # use one of these filter options to resize the image
        im2 = im1.resize((width, height), PIL.Image.NEAREST)      # use nearest neighbour
        
        im2.save("resized.jpg")

        # ------------------------ MAPEO RGB -----------------------#

        rojo = list(im2.getdata(band=0))
        verde = list(im2.getdata(band=1))
        azul = list(im2.getdata(band=2))

        file = open("rgb.txt","w+")
        posX = 0
        posY = 1
        lista = []

        for x in range(0,len(rojo)):

            posX += 1

            if rojo[x] > verde[x] and rojo[x] > azul[x]:
                file.write("R")
                lista.insert(x, str(posX)+"R"+str(posY)+"\n")
            elif verde[x] > rojo[x] and verde[x] > azul[x]:
                file.write("G")
                lista.insert(x, str(posX)+"G"+str(posY)+"\n")
            elif azul[x] > verde[x] and azul[x] > rojo[x]:
                file.write("B")
                lista.insert(x, str(posX)+"B"+str(posY)+"\n")
            else:
                file.write(" ")

            if posX == 240:
                file.write("\n")
                lista.insert(x, "|\n")
                posY +=1
                posX = 0

                
        #file.write('\n'.join(map(str, pixels)))

        file.close()
        
        file2 = open("listaRGB.txt","w+")

        file2.write(''.join(map(str, lista)))

        file2.close()

        with open('listaRGB.txt', 'r') as file:
            data = file.read()


        # ------------------------ ENVÍO POR UPD ------------------ #

        # UPD_IP = "192.168.1.9"
        # UPD_PORT = 4210
        # MESSAGE = stringImagen

        # chunks, chunk_size = len(stringImagen), len(stringImagen)//4
        # [ stringImagen[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.sendto(bytes(MESSAGE, "utf-8"), (UPD_IP, UPD_PORT))

        # ------------------------ ENVÍO POR TCP ------------------ #
        TCP_IP = '192.168.1.13'
        TCP_PORT = 5005
        BUFFER_SIZE = 2
        #MESSAGE = data;
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        for x in range(0,len(lista)):
            s.send(lista[x].encode('utf-8'))
            if x != (len(lista)-1) :
                dataRcv = s.recv(BUFFER_SIZE)
                print((""+str(dataRcv)), file=sys.stderr)

        
        #print("Goodbye cruel world!", file=sys.stderr)
        
        print(("Texto Correcto"), file=sys.stderr)
        
        s.close()

        return HttpResponse('Recibio POST : '+str(a['base64']))
    else:
        # Your code for GET
        return HttpResponse('Recibio GET')
    

from .serializers import ImagenSerializer
from .models import Image


class ImagenViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImagenSerializer
    #return HttpResponse("Entro Imagen.")


