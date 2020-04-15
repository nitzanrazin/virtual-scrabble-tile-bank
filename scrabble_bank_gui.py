import csv
import itertools # for toggle button of display/hide history

import tkinter as tk
import tkinter.messagebox

from tkinter import filedialog
from tkinter import ttk

import Pmw # foor tooltips (Balloon)

from remote_scrabble_bank import LetterBank


#########
import smtplib

def send_email(to, subject, body):
    gmail_user = '[INPUT MAIL HERE]@gmail.com'
    gmail_password = '[PASSWORD]'
    
    sent_from = gmail_user
    
    fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, fmt.format(sent_from, ", ".join(to), subject, body).encode('utf-8'))
    server.close()
##########

class Player:
    """
    one player data
    """
    def __init__(self, name="", email=""):
        self.name = name
        self.email = email
    

class TileBankGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("950x900")
        self.master.title("בנק אותיות שבץ נא")
        
        self.bank = LetterBank() # initialize the tile bank
        
        #self.history = [] # history of all letters drawn, to allow "back"
        self.players = [] # data of players
        
        self.text_history = [] # write a line of text each time tiles are drawn
        # is a human readable version of history, with player name for each draw documented
        
        self.ind_to_heb_ord = {0: 1488, 1: 1489, 2: 1490, 3: 1491, 4: 1492, 5: 1493,
                      6: 1494, 7: 1495, 8: 1496, 9: 1497, 10: 1499, 11: 1500,
                      12: 1502, 13: 1504, 14: 1505, 15: 1506, 16: 1508, 17: 1510,
                      18: 1511, 19: 1512, 20: 1513, 21: 1514, 22: 42}

        #########
        # put all everything except for the status bar in "interior" (so the status bar can be at the bottom)
        self.interior = tk.Frame(master)
        self.interior.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # game reset
        self.start_new_game_button = tk.Button(self.interior, text="התחל משחק חדש", command=self.reset)
        self.start_new_game_button.grid(row=0, column=3)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.start_new_game_button , 'אפס את בנק האותיות ומחק היסטוריה')

        # player data entry
        self.label_player_subtitle = tk.Label(self.interior, text="שחקנים", font=("Helvetica", 14))
        self.label_player_subtitle.grid(row=1, column=4)
        
        self.label_name = tk.Label(self.interior, text=":שם")
        self.label_name.grid(row=2, column=4)
        
        self.player_name_entry = tk.StringVar()
        self.entry_name = tk.Entry(self.interior, textvariable=self.player_name_entry)
        self.entry_name.grid(row=2, column=3)
        
        self.label_email = tk.Label(self.interior, text=":מייל")
        self.label_email.grid(row=2, column=2)
        
        self.player_email_entry = tk.StringVar()
        self.entry_email = tk.Entry(self.interior, textvariable=self.player_email_entry)
        self.entry_email.grid(row=2, column=1)
        
        self.add_player_button = tk.Button(self.interior, text="+", command=self.add_player)
        self.add_player_button.grid(row=2, column=0)
                
        # listbox of players
        self.listbox = tk.Listbox(self.interior, width=30, height=5)
        self.listbox.grid(row=4, column=3, rowspan=4, columnspan=2)
        
        # remove one player button
        self.remove_player_button = tk.Button(self.interior, text="הסר", command=self.remove_player)
        self.remove_player_button.grid(row=4, column=2)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.remove_player_button , 'הסר את השחקן המסומן')
        
        # delete all players button
        self.delete_all_players_button = tk.Button(self.interior, text="מחק הכל", command=self.delete_all_players)
        self.delete_all_players_button.grid(row=4, column=1)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.delete_all_players_button , 'מחק את כל השחקנים')
        
        # save player data to file button
        self.save_players_button = tk.Button(self.interior, text="שמור לקובץ", command=self.save_players_to_file)
        self.save_players_button.grid(row=5, column=1)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.save_players_button , 'שמור את רשימת השחקנים לקובץ טקסט')
        
        # load player data from file button
        self.load_players_button = tk.Button(self.interior, text="טען מקובץ", command=self.load_players_from_file)
        self.load_players_button.grid(row=6, column=1)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.load_players_button , 'קרא שחקנים מקובץ טקסט והוסף אותם לרשימת השחקנים')
        
        # draw letters for a player
        self.label_draw_title = tk.Label(self.interior, text="הגרלת אותיות", font=("Helvetica", 14))
        self.label_draw_title.grid(row=9, column=4, pady=10)
        
        self.label_tile_number = tk.Label(self.interior, text=":מספר אותיות")
        self.label_tile_number.grid(row=10, column=4)
        
        self.entered_tile_number = 0
        # allow only empty or integer values to be entered by using a validation function
        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry_tile_number = tk.Entry(self.interior, validate="key", validatecommand=(vcmd, '%P'))
        self.entry_tile_number.grid(row=10, column=3)
        #self.entry_tile_number = tk.Entry(self.interior)
        ##self.tile_number = self.entry_tile_number.get()
        
        self.label_player = tk.Label(self.interior, text=":שחקן")
        self.label_player.grid(row=10, column=2)
        
        ## combobox
        player_list = [p.name for p in self.players]
        self.pick_player_combobox = ttk.Combobox(self.interior, values=player_list)
        self.pick_player_combobox.grid(row=10, column=1)
        ## combobox
               
        self.draw_tiles_button = tk.Button(self.interior, text="הגרל", command=self.draw)
        self.draw_tiles_button.grid(row=10,column=0, padx=10)
        self.undo_button = tk.Button(self.interior, text="בטל", command=self.undo_last_draw)
        self.undo_button.grid(row=11,column=0)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.undo_button, 'בטל את ההגרלה האחרונה')
        
        # send email checkbox - can untick to not send emails to players
        # upon drawing letters
        self.send_email = tk.IntVar()
        self.send_email_checkbutton = tk.Checkbutton(self.interior, text="שלח מייל", variable=self.send_email)
        self.send_email_checkbutton.grid(row=11, column=2, columnspan=2)
        self.send_email_checkbutton.select() # set checkbox to on at startup
        
        # show / hide tile draw history
        self.show_history_button = tk.Button(self.interior, text="הסתר היסטוריה", command=self.toggle_display_history)
        self.show_history_button.grid(row=12,column=3)
        
        # print history log
        #self.save_log_button = tk.Button(self.interior, text="הצג היסטוריה", command=self.save_log)
        #self.save_log_button.grid(row=12,column=3)
        
        # display textbox with letters drawn log
        self.text = tk.Text(self.interior, height=4, width=40)
        self.text.grid(row=13, column=0, columnspan=5, pady=10, sticky=tk.N+tk.S)
        self.interior.grid_rowconfigure(13, weight=1) # make row 13 (which contains the Text) extend with window
        # lock writing to text box - so it can't be written into from GUI
        self.text.configure(state='disabled')
        #self.text.configure(font=("Tahoma", 11))

        # status bar
        self.status = tk.Label(master, text="Ready...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X) # put status bar in entire bottom line
        
    def validate(self, new_text):
        '''
        verifies that the input string is a valid integer

        Parameters
        ----------
        new_text : string
            string to validate.

        Returns
        -------
        bool
            True if new_string is an integer, False otherwise.

        '''
        if not new_text: # the field is being cleared
            self.entered_tile_number = 0
            return True

        try:
            self.entered_tile_number = int(new_text)
            return True
        except ValueError:
            return False
   
    # event functions
    def reset(self):
        '''
        reset letter bank to include all letters (and 2 blank tiles),
        reset history

        '''
        # ask if sure that want to reset the tile bank
        answer = tk.messagebox.askquestion(title="איפוס בנק האותיות", message="האם את בטוחה שברצונך לאפס את בנק האותיות?")

        if answer=='yes':
            # reset inventory and history
            self.bank.reset()
            
            # reset text
            self.text.configure(state='normal') # allow writing to text box
            self.text.delete('1.0', tk.END) # delete all the text
            self.text.configure(state='disabled') # lock writing to text box
            
            # write update to status bar
            self.status.config(text="Reset the tile bank.")
            
    def add_player(self):
        self.players.append(Player(name=self.player_name_entry.get(), email=self.player_email_entry.get()))
        line = self.players[-1].name + " " + self.players[-1].email
        self.listbox.insert(tk.END, line) # add player line to list
        # clear player data entry fields
        self.entry_name.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        
        self.update_player_selection() # update player selection combobox

    
    def remove_player(self):
        '''
        Delete the selected player

        '''
        selected_ind = self.listbox.curselection()[0]
        #selected = self.listbox.get(self.listbox.curselection())
        self.listbox.delete(tk.ANCHOR) # delete selected line from list
        # delete player from players list
        self.players.pop(selected_ind)
        
        self.update_player_selection() # update player selection combobox
    
    def delete_all_players(self):
        '''
        Delete the entire player list

        '''
        self.listbox.delete(0, tk.END)
        self.players = []
        
        self.update_player_selection() # update player selection combobox

    def save_players_to_file(self):
        '''
        Save the player details to a tab delimited text file.
        Each player data is saved to a line with the format: name \t mail \n

        '''
        filename = filedialog.asksaveasfilename(initialdir = "C:/Users/nitza/OneDrive/Documents",title = "Select file",filetypes = (("text file","*.txt"),("all files","*.*")))
        # save the players to file
        with open(filename, "w", encoding="utf-8") as file:
            for p in self.players:
                file.write(p.name + "\t" + p.email + "\n")
         
        # write status bar update
        self.status.config(text="Saved player data to file.")
    
    def load_players_from_file(self):
        filename =  filedialog.askopenfilename(initialdir = "C:/Users/nitza/OneDrive/Documents",title = "Select file",filetypes = (("text file","*.txt"),("all files","*.*")))
        
        with open(filename, newline = '', encoding="utf-8") as players:
            player_reader = csv.reader(players, delimiter='\t')
            for player in player_reader:
                p = Player(name=player[0], email=player[1])
                self.players.append(p)
                self.listbox.insert(tk.END, player) # add player line to list
        
        self.update_player_selection() # update player selection combobox
                
        # write status bar update
        self.status.config(text="Loaded player data from file.")
    
    def draw(self):
        #tile_number = int(self.entry_tile_number.get()) # get number of tiles to draw 
        tile_number = self.entered_tile_number

        # change default player for next draw to be the next one
        player_selected_ind = self.pick_player_combobox.current()
        
        # verify that the number of tiles entered is 1-7, and a player to draw them was selected
        if tile_number not in [1,2,3,4,5,6,7]:
            self.status.config(text="ERROR: Number of tiles must be 1-7.")
            return
        elif player_selected_ind==-1:
            self.status.config(text="ERROR: Must select player for which to draw tiles.")
            return
        
        # draw tiles for currently chosen player
        tiles_drawn, inds_drawn = self.bank.draw(tile_number)
        #print(tiles_drawn) # DEBUG
        heb_tiles = [chr(self.ind_to_heb_ord[i]) for i in inds_drawn]
        #print(heb_tiles)
            
        # save drawn letters to string for email and textbox update
        player_text = self.players[player_selected_ind].name + ": "
        tiles_text = " ".join(heb_tiles)
 
        # send email to player
        if self.send_email.get():
            to = self.players[player_selected_ind].email
            subject = "אותיות שהוגרלו"
            body = tiles_text
            send_email([to], subject, body)

        # set selected player to next one in list
        num_players = len(self.players)
        next_player_ind = (player_selected_ind + 1) % num_players
        self.pick_player_combobox.current(next_player_ind)

        # write to status bar and history text box
        self.text.configure(state='normal') # allow writing to text box
        num_tiles_left = sum(self.bank.inventory)
        num_tiles_drawn = len(heb_tiles)
        if num_tiles_drawn>0:
            # text for status bar
            text = str(num_tiles_drawn) + " tiles drawn for " + self.players[player_selected_ind].name + \
                ", number of tiles left in bank: " + str(num_tiles_left) + "."
            
            textbox_message = player_text + tiles_text
            # write to history text box
            #self.text.insert(tk.INSERT, player_text + tiles_text) # write drawn letters to text box

        else:
            text = "Bank is empty!"
            # write to history text box
            textbox_message = text
            #self.text.insert(tk.INSERT, text + "\n")
            
        self.status.config(text=text) # write to status bar
        
        self.text_history.append(textbox_message)
        # write which tiles were drawn to the text box
        self.text.insert(tk.INSERT, textbox_message + "\n")
        #self.text.insert(tk.END, "\n" + textbox_message) # write to end of text
        # use leading instead of trailing \n to allow deletion with undo
        # https://stackoverflow.com/questions/43561558/using-tkinter-text-indexing-expressions-to-delete-last-line-of-text
        # lock writing to text box - so it can't be written into from GUI
        self.text.configure(state='disabled')
        self.text.yview_pickplace(tk.END) # scroll to end

    
    def undo_last_draw(self):
        '''
        Undo the last drawing of letters - return letters to the bank, delete from history

        '''
        message = self.bank.back()
        # write to status bar
        self.status.config(text=message)
        
        # TO DO: DON'T NEED THIS CHECK, JUST RETURN A FLAG FROM BANK.BACK
        if self.text.compare("end-1c", "==", "1.0"): # check if the textbox is empty
            print("the widget is empty")
        
        # TO DO: REMOVE THE UNNECESSARY TEXT_HISTORY (SINCE HAVE SELF.TEXT), REPLACE THIS IF WITH IF OVER THAT
        if self.text_history: # if there is a draw step to undo, delete it
            self.text_history.pop() # delete last draw from draw history
        
            # set selected player in combobox 1 back (assuming want to redraw what was undone)
            player_selected_ind = self.pick_player_combobox.current()
            # set selected player to next one in list
            num_players = len(self.players)
            prev_player_ind = (player_selected_ind - 1) % num_players
            self.pick_player_combobox.current(prev_player_ind)
            
        # delete the last line from the textbox
        self.text.configure(state='normal') # allow writing to text box
        #self.text.delete("end-1c linestart", "end") # wrong because there is a \n at the end which should keep (is there since the beginning, all text inserted before it)
        self.text.delete("end-2c linestart", "end-1c") # trying this
        self.text.configure(state='disabled') # lock writing to text box
            
    
    def update_player_selection(self):
        '''
        call this function whenever players are added or deleted, to update
        the player selection combobox

        '''
        player_list = [p.name for p in self.players]
        self.pick_player_combobox["values"] = player_list
        
    def save_log(self):
        # for now, print history to console
        print(self.bank.history)
        
    def toggle_display_history(self, icycle=itertools.cycle([False, True])):
        disp_history = next(icycle)
        if disp_history:
            self.show_history_button['text'] = 'הסתר היסטוריה'
            self.text.grid(row=13, column=0, columnspan=5, pady=10, sticky=tk.N+tk.S) # display history text box
        else:
            self.show_history_button['text'] = 'הצג היסטוריה'
            self.text.grid_forget() # hide history text box
        

###########
root = tk.Tk()
tile_bank_gui = TileBankGUI(root)
root.mainloop()
