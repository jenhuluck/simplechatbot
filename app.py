# -*- coding: utf-8 -*-
from tkinter import *
from chat import get_response, bot_name

head_color = '#5680e9'
bg_color = '#5ab9ea'
text_bg_color = '#84ceeb'
send_bg_color = '#c1c8e4'
send_button_color = '#5680e9'
TEXT_COLOR = '#05386b'

HEAD = 'Helvetica 11 bold'
FONT = 'Helvetica 9'
FONT_BOLD = 'Helvetica 8 bold'

class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
    
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title('Chat')
        self.window.resizable(width=False, height=False)
        self.window.configure(width=600, height=720, bg=bg_color)
        #head label
        head_label = Label(self.window, bg=head_color, fg=TEXT_COLOR, text="CHAT BOT", font=HEAD, pady=10)       
        head_label.place (relwidth=1)
        #divider
        line = Label(self.window, width=600, bg=head_color)
        line.place(relwidth=1, rely=0.11, relheight=0.002)
        #text
        self.text_widget = Text(self.window, width=15, height=1, bg=text_bg_color, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.705, relwidth=1, rely=0.11)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        #scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.93)
        scrollbar.configure(command=self.text_widget.yview)
        
        #bottom label
        bottom_label = Label(self.window, bg=send_bg_color, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        #message entry box
        self.msg_entry = Entry(bottom_label, bg=send_bg_color, fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.8, relheight=0.030, rely=0.001, relx=0.011)
        self.msg_entry.focus() #focus on the message entry box when the app starts
        self.msg_entry.bind("<Return>", self._on_enter_pressed) #bind the return action to a function
    
        #send button
        send_button = Button(bottom_label, text='Send', font=FONT_BOLD, width=18, bg=send_button_color,
                             command=lambda:self._on_enter_pressed(None))
        send_button.place(relx=0.81, rely=0.001, relheight=0.03, relwidth=0.17)
        
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}:{msg}\n\n"
        self.text_widget.configure(state=NORMAL)    
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
        msg2 = f"{bot_name}:{get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)    
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)
             
        
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()