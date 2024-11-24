import socket
from os.path import split
from socket import *
import os

serverPort = 5698
#define TCP server
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
# listen for requests
serverSocket.listen(50)
# print for the server is ready
print('Web Server is ready ...')

def sendResponse(res, type):
    if (int(res) == 200):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
    elif (int(res) == 404):
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
    elif (int(res) == 307):
        connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())

    str = "Content-Type: " + type + "; charset=utf-8\r\n"
    connectionSocket.send(str.encode())
    connectionSocket.send("\r\n".encode())

def Error(ip,port):
        sendResponse(404,'text/html')
        error = ('<!DOCTYPE html>'
                '<html lang="en">'
                '<style>'
                '*{text-align: center;padding:10px;}'
                'h1{font-size:50px;}'
                'p{font-size:20px;}'
                '</style>'
                '<head>'
                '<meta charset="UTF-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
                '<title>Error 404</title>'
                '</head>'
                '<body>'
                '<h1 style="color: red;">The file is not found!</h1>'
                '<p>IP Address: ' + str(ip) + ',Port Number: ' + str(port) + '</p>'
                '</body></html>'
        )
        connectionSocket.send(error.encode())


while True:
    # opening all the files and images
    files = os.listdir('.')
    files = [f for f in files if os.path.isfile(f)]

    html = os.listdir('./html')
    html = [f for f in html if os.path.isfile(os.path.join('./html', f))]

    css = os.listdir('./css')
    css = [f for f in css if os.path.isfile(os.path.join('./css', f))]

    images = os.listdir('./images')
    images = [f for f in images if os.path.isfile(os.path.join('./images', f))]

    videos = os.listdir('./videos')
    #accept the connection
    connectionSocket, addr = serverSocket.accept()
    ip = addr[0]
    port = addr[1]
    print('Got connection from', "IP: " + ip + ", Port: " + str(port))
    #receive http reqeust
    sentence = connectionSocket.recv(4096).decode()
    #split the request to get the request line from user input
    try:
        match= sentence.split('\n')[0]
        request = match.split(' ')[1]
        print("The Request is : "+request) # print http request intermanel
        print(sentence)
    except :
        print("BAD REQUEST")
        continue

    #for any of this we handle the request depending on the url
    #English Version
    if(request =="/" or request =="/index.html" or request =="/main_en.html" or request =="/en"):
        if 'main_en.html' in html:
            with open('./html/main_en.html','r') as mainEn:
                mainEn = mainEn.read()
            sendResponse(200,'text/html')
            connectionSocket.send(mainEn.encode())
        else:
            Error(ip,port)
    #Arabic Version
    elif(request == "/ar" or request == "/main_ar.html"):

        if 'main_ar.html' in html:
            with open('./html/main_ar.html','rb') as mainAr:
                mainAr = mainAr.read()
            sendResponse(200,'text/html')
            connectionSocket.send(mainAr)

        else:
            Error(ip,port)
    #supporting material English
    elif(request == "/supporting_material_en.html"):
        if 'supporting_material_en.html' in html:
            with open('./html/supporting_material_en.html','r') as supporting_En:
                supporting_En = supporting_En.read()
            sendResponse(200,'text/html')
            connectionSocket.send(supporting_En.encode())
        else:
            Error(ip,port)
    #supporting material Arabic
    elif (request == "/supporting_material_ar.html"):
        if 'supporting_material_ar.html' in html:
            with open('./html/supporting_material_ar.html','rb') as supporting_Ar:
                supporting_Ar = supporting_Ar.read()
            sendResponse(200,'text/html')
            connectionSocket.send(supporting_Ar)
        else:
            Error(ip,port)

    #for the css file
    elif (request =="/main.css"):
        if 'main.css' in css:
            with open('./css/main.css','r') as css:
                css = css.read()
            sendResponse(200,'text/css')
            connectionSocket.send(css.encode())
        else:
            Error(ip,port)

    #if this statement(/request_handler?material) in the url then the user submit an img/video name in the html form
    elif 'request_handler?material' in request :
        var,type = request.split('=')[1], request.split('=')[2] #to get the image name alone
        object = var.split('&')[0]
        if (type == 'image'):
            object1 = object + '.jpg'
            object2 = object + '.png'
            if (object1 in images):
                object1 = './images/' +object1
                with open(object1,'rb') as image:
                    sendResponse(200,'image/jpg')
                    connectionSocket.send(image.read())
            elif (object2 in images):
                object2 = './images/' + object2
                with open(object2,'rb') as image:
                    sendResponse(200,'image/png')
                    connectionSocket.send(image.read())
            else:
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send('Content-Type: text/html; charset=utf-8\r\n'.encode())
                object = object.replace(" ", "+")
                location = "Location:http://www.google.com/search?q="+object+"&udm=2\r\n"
                connectionSocket.send(location.encode())
                connectionSocket.send('\r\n'.encode())
                print("Redirect to google\r\n")
        else:
            object1 = object + '.mp4'
            if (object1 in videos):
                object1 = './videos/' + object1
                with open(object1,'rb') as video:
                    video = video.read()
                    sendResponse(200, 'video/mp4')
                    connectionSocket.send(video)
            else:
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send('Content-Type: text/html; charset=utf-8\r\n'.encode())
                object = object.replace(" ","+")
                location = "Location:https://www.youtube.com/results?search_query=" + object +"\r\n"
                connectionSocket.send(location.encode())
                connectionSocket.send('\r\n'.encode())
                print("Redirect to Youtube\r\n")

    #for images requests
    elif('/images' in request):
        ob = request.split('/')[2]
        obj = './images/'+ob
        if (ob in images):
            type = 'image/'+obj.split('.')[-1]
            with open(obj,'rb') as image:
                image = image.read()
                sendResponse(200, type)
                connectionSocket.send(image)
        else:
            Error(ip,port)

    #for videos requests
    elif ('/videos' in request):
        obj = request.split('/')[2]
        if (obj in videos):
            type = 'video/' + obj.split('.')[-1]
            obj = './videos/' + obj
            with open(obj, 'rb') as video:
                video = video.read()
                sendResponse(200, type)
                connectionSocket.send(video)
        else:
            Error(ip,port)

    #if the client made any request that dose not exist
    else:
        try:
            obj = request.split('/')[1]
            if(obj in files or obj in html or obj in css or obj in images or obj in videos):
                type = obj.split('.')[-1]
                if obj in html:
                    obj = './html/' + obj
                elif obj in css:
                    obj = './css/' + obj
                elif obj in images:
                    obj = './images/' + obj
                elif obj in videos:
                    obj = './videos/' + obj
                if(type == 'html'):
                    sendResponse(200, 'text/html')
                    with open(obj, 'r') as file:
                        file = file.read()
                    connectionSocket.send(file.encode())
                elif(type == 'css'):
                    sendResponse(200, 'text/css')
                    with open(obj, 'rb') as file:
                        file = file.read()
                    connectionSocket.send(file)
                elif(type == 'jpg'):
                    sendResponse(200, 'image/jpg')
                    with open(obj, 'rb') as file:
                        file = file.read()
                    connectionSocket.send(file)
                elif(type == 'png'):
                    sendResponse(200, 'image/png')
                    with open(obj, 'rb') as file:
                        file = file.read()
                    connectionSocket.send(file)
                elif(type == 'mp4'):
                    sendResponse(200, 'video/mp4')
                    with open(obj, 'rb') as file:
                        file = file.read()
                    connectionSocket.send(file)
                else:
                    sendResponse(200, 'text/html') #default
                    with open(obj, 'rb') as file:
                        file = file.read()
                    connectionSocket.send(file)
            else:
                Error(ip,port)
        except IndexError:
            print('Bad Request')
    connectionSocket.close()