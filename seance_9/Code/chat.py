from textual import on, work
from textual.screen import ModalScreen
from textual.reactive import reactive
from textual.message import Message
from textual.app import App, ComposeResult
from textual.widgets import Input, RichLog, Button
from textual.widgets import Header, Footer
from time import sleep
import asyncio
import json


class MessageWidget(RichLog):
    class NewMessage(Message):
        def __init__(self, msg: str) -> None:
            self.msg = msg
            super().__init__()

async def get_new_message(log: MessageWidget, reader):
    while True:
        message_data = json.loads((await reader.readline()).decode())
        if isinstance(message_data, dict):
            sender = message_data.get("sender", message_data.get("login", "Unknown"))
            msg = message_data.get("message", message_data.get("msg", str(message_data)))
            formatted_message = f"[{sender}] {msg}"
        else:
            formatted_message = str(message_data)
        log.post_message(MessageWidget.NewMessage(formatted_message))

async def send_message(text, writer, log: MessageWidget):
    message_json = json.dumps({"msg": text}, separators=(', ', ':')) + "\n"
    writer.write(message_json.encode())
    await writer.drain()

async def connection(login: str, password: str, log: MessageWidget):
    reader, writer = await asyncio.open_connection('vassor.org', 12345)
    auth_message = json.dumps({"login": login, "password": password}, separators=(', ', ':')) + "\n"
    writer.write(auth_message.encode())
    await writer.drain()
    raw_response = await reader.readline()
    response_str = raw_response.decode()
    response = json.loads(response_str)
    if response == "Failure":
        log.app.exit("Erreur d'authentification")
    elif isinstance(response, dict) and "Success" in response:
        log.post_message(MessageWidget.NewMessage("Authentification réussie"))
    else:
        log.app.exit(f"Erreur d'authentification - réponse inattendue: {response}")
    return (reader, writer)

class ConnectScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Identifiant", id="login")
        yield Input(placeholder="Mot de passe", id="pw", password=True)

    @on(Input.Submitted)
    async def login_submitted(self, event: Input.Submitted) -> None:
        login = self.query_one("#login").value
        pw = self.query_one("#pw").value
        (reader, writer) = await connection(login, pw, self.app.query_one(MessageWidget))
        self.app.socket_snd = writer
        self.app.socket_rcv = reader
        self.app.pop_screen()
        self.app.get_messages()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        login = self.query_one("#login").value
        pw = self.query_one("#pw").value
        (reader, writer) = await connection(login, pw, self.app.query_one(MessageWidget))
        self.app.socket_snd = writer
        self.app.socket_rcv = reader
        self.app.pop_screen()
        self.app.get_messages()

class ChatApp(App[str]): 
    """A small TCP chat App"""

    connected = reactive(False)
    socket_snd = None
    socket_rcv = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield MessageWidget()
        yield Input(placeholder="Message", id="send_msg")
        yield Footer()

    @on(Input.Submitted)
    async def handle_message_request(self, event: Input.Submitted) -> None:
        if event.input.id == "send_msg":
            text_log = self.query_one(MessageWidget)
            await send_message(event.value, self.socket_snd, text_log)
            input_field = self.query_one(Input)
            input_field.clear()
        else:
            # L'évènement vient des champs de connexion.
            self.get_messages()


    @on(MessageWidget.NewMessage)
    def handle_new_message(self, event: MessageWidget.NewMessage) -> None:
        text_log = self.query_one(MessageWidget)
        text_log.write(content=event.msg)


    @on(Button.Pressed)
    def start_connection(self, event: Button.Pressed) -> None:
        self.get_messages()

    @work(exclusive=True)
    async def get_messages(self) -> None:
        log = self.query_one(MessageWidget)
        asyncio.create_task(get_new_message(log, self.socket_rcv))

    def watch_connected(self, value) -> None:
        if not value:
            self.push_screen(ConnectScreen())
            self.connected = True
        else:
            pass

if __name__ == "__main__":
    app = ChatApp()
    msg = app.run()
    if msg:
        print(msg)
