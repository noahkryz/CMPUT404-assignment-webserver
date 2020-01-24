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

        # Break the request into its parts
        parsedRequest = self.parseClientRequest()

        self.methodName = parsedRequest[0]
        self.pathName = parsedRequest[1]
        self.protocolName = parsedRequest[2]

        # Only check the file/directory if it was a GET request
        result = self.checkMethodName()
        if result == False:
            return
        self.checkFileName()

    # Break the request into it's individual parts
    def parseClientRequest(self):
        fullUserRequest = self.data.decode().split("\r\n")
        requestInformation = fullUserRequest[0].split(' ')

        methodName = requestInformation[0]
        pathName = requestInformation[1]
        protocolName = requestInformation[2]

        return [methodName, pathName, protocolName]

    # Handle 405 request, only allowing GET requests
    def checkMethodName(self):
        if self.methodName != 'GET':
            req = self.protocolName + " 405 Method Not Allowed" + '\r\n\r\n'
            self.request.sendall(req.encode())
            return False

    # Handle the redirect of the 301
    def redirect301(self):
        req = self.protocolName + " 301 Moved Permanently" + '\r\n'
        self.request.sendall(req.encode())

        redirect = 'Location: http://127.0.0.1:8080'+self.pathName+'\r\n\r\n'
        self.request.sendall(redirect.encode())

    # Handle the 200 request, file exists
    def send200(self):
        req = self.protocolName + " 200 OK" + '\r\n'
        self.request.sendall(req.encode())

        contentType = "Content-Type: text/"+self.extension+"; charset=UTF-8\r\n"
        self.request.sendall(contentType.encode("utf-8"))
        
        # Open the file to send the contents
        file_object = open(self.currentPath, "r")
        file_string = file_object.read()
        file_string = file_string + "\r\n"
        
        self.request.sendall(("\r\n"+file_string).encode("utf-8"))

    # Handle the 404, not found
    def send404(self):
        req = self.protocolName + " 404 Not Found" + '\n\r\n'
        self.request.sendall(req.encode())

    def checkFileName(self):
        self.currentPath = os.getcwd() + '/www' + self.pathName

        #Split the path to see if it is a file
        fileExtension = self.pathName.split('.')
        # Length = 2 if it is a file ex) index.html -> ['index', 'html']
        if len(fileExtension) != 2:
            self.extension = "html"
            if self.pathName[-1] != "/":
                self.pathName += "/"
                self.redirect301()
            else:
                # Append the index.html to the end if last character "/"
                self.currentPath += 'index.html'

                # Found the file in the path
                if os.path.isfile(self.currentPath):
                    self.send200()
                # Does not exist
                else:
                    self.send404()
        # A file to serve is provided
        else:
            # Set to css or html for the mime type
            self.extension = fileExtension[1]
            # Found the file in the path
            if os.path.isfile(self.currentPath):
                self.send200()
            # Does not exist
            else:
                self.send404()
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
