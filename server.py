#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import os


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()

        parsedRequest = self.parseClientRequest()

        self.methodName = parsedRequest[0]
        self.pathName = parsedRequest[1]
        self.protocolName = parsedRequest[2]

        self.checkMethodName()
        self.checkFileName()

        # file_object = open("www/index.html", "r")
        # file_string = file_object.read()
        # file_string = file_string + "\r\n"
        # # print(file_string)

        # self.request.sendall("HTTP/1.1 200 OK\n".encode("utf-8"))
        # self.request.sendall("Content-Type: text/html; charset=UTF-8\r\n".encode("utf-8"))
        # self.request.sendall(file_string.encode("utf-8"))

        
        
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

    def parseClientRequest(self):
        fullUserRequest = self.data.decode().split("\r\n")
        requestInformation = fullUserRequest[0].split(' ')

        methodName = requestInformation[0]
        pathName = requestInformation[1]
        protocolName = requestInformation[2]

        # print(pathName, methodName, protocolName)

        # self.checkMethodName()
        # self.checkFileName()

        return [methodName, pathName, protocolName]

    def checkMethodName(self):
        if self.methodName != 'GET':
            print(' 405 Method Not Allowed')
            status_code = " 405 Method Not Allowed"
            self.sendRequest(status_code)
        return

    def redirect301(self):
        status_code = " 301 Moved Permanently"
        self.sendRequest(status_code)

    def checkFileName(self):
        self.currentPath = os.getcwd() + '/www' + self.pathName

        #Append the index.html to the end if last character "/"
        if self.pathName[-1] == "/":
            self.currentPath += 'index.html'

        print('above')
        print(self.currentPath)
        if os.path.isfile(self.currentPath):
            status_code = " 200 OK"
            self.sendRequest(status_code)
        else:
            status_code = " 404 Not Found"
            self.sendRequest(status_code)

    def sendRequest(self, statusCode):
        print("Status Code:", statusCode)

        if statusCode == " 404 Not Found":
            print('in 404')
            req = self.protocolName + statusCode + '\n\r\n'
            print("Request:", req)
            self.request.sendall(req.encode())

        if statusCode == " 200 OK":
            print('in 200')
            req = self.protocolName + statusCode + '\r\n'
            print("Request:", req)
            self.request.sendall(req.encode())
            file_object = open(self.currentPath, "r")
            file_string = file_object.read()
            file_string = file_string + "\r\n"

            # self.request.sendall("HTTP/1.1 200 OK\n".encode("utf-8"))
            self.request.sendall("Content-Type: text/html; charset=UTF-8\r\n".encode("utf-8"))
            self.request.sendall(("\r\n"+file_string).encode("utf-8"))
        
        if statusCode == " 301 Moved Permanently":
            print("301")
            req = self.protocolName + statusCode + '\n'
            
            print("Request:", req)
            self.request.sendall(req.encode())

            redirect = 'Location: http://127.0.0.1:8080/index.html\r\n\r\n'
            print("Redirect:", redirect)
            self.request.sendall(redirect.encode())

            return
            # self.request.sendall(redirect.encode())
            # print("Redirect: ", redirect)

        if statusCode == " 405 Method Not Allowed":
            req = self.protocolName + statusCode + '\r\n\r\n'
            print("Request:", req)
            self.request.sendall(req.encode())
            return
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
