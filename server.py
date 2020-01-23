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
        file_object = open("www/index.html", "r")
        file_string = file_object.read()
        file_string = file_string + "\r\n"
        # print(file_string)

        self.request.sendall("Content-Type: text/html; charset=UTF-8\r\n".encode("utf-8"))
        self.request.sendall(file_string.encode("utf-8"))

        # print(self.data.decode())
        # print('\n')
        # self.request.sendall("")
        print(self.parseClientRequest(self.data))
        
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

    def parseClientRequest(self, clientRequest):
        fullUserRequest = clientRequest.decode().split("\r\n")
        requestInformation = fullUserRequest[0].split(' ')

        methodName = requestInformation[0]
        pathName = requestInformation[1]
        protocolName = requestInformation[2]

        self.checkMethodName(methodName)
        self.checkFileName(pathName)

        return [methodName, pathName, protocolName]

    def checkMethodName(self, name):
        if name != 'GET':
            print('405 Method Not Allowed')
            status_code = "405 Method Not Allowed"

    def checkFileName(self, name):
        currentPath = os.getcwd() + '/www' + name
        print(currentPath)
        if os.path.exists(currentPath):
            print('exists')
        else:
            print('nope')

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
