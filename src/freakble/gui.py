import asyncio
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from .ble import BLE_interface
from .ble import connect as ble_connect


class App:
    def config(self, adapter, device, ble_connection_timeout):
        self.adapter = adapter
        self.device = device
        self.ble_connection_timeout = ble_connection_timeout

    async def run(self):
        self.window = Window(self, asyncio.get_event_loop())
        await self.window.show()


class Window(tk.Tk):
    def __init__(self, app, loop):
        self.app = app
        self.loop = loop
        self.root = tk.Tk()
        self.root.title("freakble")
        self.root.geometry("640x480")

        self.make_ui()

        self.task1 = self.loop.create_task(self.ble_loop())

        self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def make_ui(self):
        self.entry = ttk.Entry(self.root)
        self.entry.pack(side=tk.TOP, fill=tk.X)
        self.entry.focus_set()
        self.entry.bind("<Return>", self.on_entry_return)

        self.frame = ttk.Frame(self.root, borderwidth=5, relief="ridge", height=100)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.v_scrollbar = ttk.Scrollbar(self.frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text = tk.Text(
            self.frame,
            bg="white",
            width=640,
            height=300,
            yscrollcommand=self.v_scrollbar.set,
            state=tk.DISABLED,
        )
        self.text.pack(side=tk.TOP, fill=tk.BOTH)
        self.v_scrollbar.config(command=self.text.yview)

    async def ble_loop(self):
        self.ble = BLE_interface(self.app.adapter, None)
        self.ble.set_receiver(self.on_ble_data_received)
        await ble_connect(self.ble, self.app.device, self.app.ble_connection_timeout)
        await self.ble.send_loop()

    def send_over_ble(self, data):
        self.ble.queue_send(bytes(data, "utf-8"))

    def on_ble_data_received(self, data):
        data = data.decode("utf-8")
        self.insert_text(data)

    def insert_text(self, text):
        now = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        self.text["state"] = tk.NORMAL
        self.text.insert(tk.END, f"[{now}] {text}")
        self.text["state"] = tk.DISABLED

    def on_entry_return(self, e):
        text = e.widget.get()
        self.send_over_ble(text)
        self.insert_text(f"{text}\n")
        e.widget.delete(0, len(text))

    def quit(self):
        self.root.destroy()
        # TODO: properly close using an asyncio.Event: using click is hard to
        # pass it from main. One possible solution is to stop using click.
        self.loop.stop()

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(0.1)
