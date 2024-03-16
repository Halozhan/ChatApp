import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    # 접속 유저 관리
    users = {}

    def send_to_all(self, msg):
        for socket, address in self.users.values():
            socket.send(msg.encode())

    def add_user(self, username, client_socket, address):
        # 이미 등록된 닉네임인 경우
        if username in self.users:
            client_socket.send("이미 등록된 닉네임입니다.".encode())
            return None
        # 새로운 유저인 경우
        self.users[username] = (client_socket, address)
        self.send_to_all(f"{username}님이 입장했습니다.")
        print(f"현재 참여자: {list(self.users.keys())}")
        return username

    def remove_user(self, username):
        if username in self.users:
            del self.users[username]

    def handle(self):
        print("Connection from", self.client_address)

        while True:
            self.request.send("채팅 닉네임을 입력하세요: ".encode())
            username = self.request.recv(1024).decode()
            if username == "exit":
                self.request.close()
                break
            if self.add_user(username, self.request, self.client_address):
                break

        while True:
            msg = self.request.recv(1024).decode()
            print(username + ": " + msg)
            if msg == "exit":
                self.remove_user(username)
                self.request.close()
                self.send_to_all(username + "님이 퇴장했습니다.")
                print(f"현재 참여자: {list(self.users.keys())}")
                break
            self.send_to_all(username + ": " + msg)


class ChatServer(socketserver.ThreadingMixIn,
                 socketserver.TCPServer):
    pass


chat_server = ChatServer(("localhost", 14949), MyTCPHandler)
chat_server.serve_forever()
chat_server.shutdown()
chat_server.server_close()
