import csv # for writing and reading from file
import itertools # for toggle button of display/hide history

import tkinter as tk
import tkinter.messagebox

from tkinter import filedialog # for saving to / reading from file of player list
from tkinter import ttk

import Pmw # foor tooltips (Balloon)

from remote_scrabble_bank import LetterBank
from send_email import send_from_gmail
from dnd_multilistbox import MultiListbox # class of listbox with multiple columns, drag and drop reordering, that is used to store and display player data
from letter_distribution_gui import LetterDistributionSetting
from settings_io import load_tile_distribution, save_tile_distribution, load_email, save_email

class TileBankGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("950x900")
        self.master.title("בנק אותיות שבץ נא")
        
        # read the tile distribution from a settings file, if it exists
        # set tile_distribution to default value of 2008 game version
        self.tile_distribution = [6, 4, 1, 4, 8, 12, 1, 3, 1, 10, 2, 6, 6, 3, 1, 2, 3, 1, 2, 8, 6, 8, 2]
        
        # load tile distribution from file, if found
        tile_distribution = load_tile_distribution('letter_distribution.csv')
        if tile_distribution is not None: # if file not found, tile_distribution==None here (returned from load_tile_distribution)
            self.tile_distribution = tile_distribution
        
        self.bank = LetterBank(tile_distribution=self.tile_distribution) # initialize the tile bank
               
        self.ind_to_heb_ord = {0: 1488, 1: 1489, 2: 1490, 3: 1491, 4: 1492, 5: 1493,
                      6: 1494, 7: 1495, 8: 1496, 9: 1497, 10: 1499, 11: 1500,
                      12: 1502, 13: 1504, 14: 1505, 15: 1506, 16: 1508, 17: 1510,
                      18: 1511, 19: 1512, 20: 1513, 21: 1514, 22: 42}
        
        # get gmail account details for drawn letters message sending from mail_settings.txt file
        self.gmail_address, self.gmail_password = load_email('mail_settings.txt')
        
        ## GUI elements
        # put all everything except for the status bar in "interior" (so the status bar can be at the bottom)
        self.interior = tk.Frame(master)
        self.interior.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # game reset
        self.start_new_game_button = tk.Button(self.interior, text="התחל משחק חדש", command=self.reset, bg='#e1e1e1')
        self.start_new_game_button.grid(row=0, column=3)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.start_new_game_button , 'אפס את בנק האותיות ומחק היסטוריה')

        # settings button
        cog_img = tk.PhotoImage(master=master, file = r".\cog64.png") # read image from file
        #photoimage = cog_img.subsample(2, 2)         # Resizing image to fit on button 
        self.settings_button = tk.Button(self.interior, image=cog_img, command=self.create_settings_window)
        self.settings_button.image = cog_img # needed to avoid garbage collection of image
        self.settings_button.grid(row=0, column=0)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.settings_button , 'הגדרות')

        # player data entry
        self.label_player_subtitle = tk.Label(self.interior, text="שחקנים", font=("Helvetica", 14))
        self.label_player_subtitle.grid(row=1, column=4, sticky=tk.E)
        
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
        
        self.add_player_button = tk.Button(self.interior, text="+", command=self.add_player, bg='#e1e1e1')
        self.add_player_button.grid(row=2, column=0)
                
        # multicolumn listbox of players
        self.listbox = MultiListbox(self.interior, (('מייל', 20),('שם', 10)), height=5) # careful, Hebrew makes the order of columns appear funny in this line
        self.listbox.grid(row=4, column=3, rowspan=4, columnspan=2)
        
        # remove one player button
        self.remove_player_button = tk.Button(self.interior, text="הסר", command=self.remove_player, bg='#e1e1e1')
        self.remove_player_button.grid(row=4, column=2)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.remove_player_button , 'הסר את השחקן המסומן')
        
        # delete all players button
        self.delete_all_players_button = tk.Button(self.interior, text="מחק הכל", command=self.delete_all_players, width=10, bg='#e1e1e1')
        self.delete_all_players_button.grid(row=4, column=1)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.delete_all_players_button , 'מחק את כל השחקנים')
        
        # save player data to file button
        self.save_players_button = tk.Button(self.interior, text="שמור לקובץ", command=self.save_players_to_file, width=10, bg='#e1e1e1')
        self.save_players_button.grid(row=5, column=1)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.save_players_button , 'שמור את רשימת השחקנים לקובץ טקסט')
        
        # load player data from file button
        self.load_players_button = tk.Button(self.interior, text="טען מקובץ", command=self.load_players_from_file, width=10, bg='#e1e1e1')
        self.load_players_button.grid(row=6, column=1)
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.load_players_button , 'קרא שחקנים מקובץ טקסט והוסף אותם לרשימת השחקנים')
        
        # draw letters for a player
        self.label_draw_title = tk.Label(self.interior, text="הגרלת אותיות", font=("Helvetica", 14))
        self.label_draw_title.grid(row=9, column=4, pady=(25,0), sticky=tk.E)
        
        self.label_tile_number = tk.Label(self.interior, text=":מספר אותיות")
        self.label_tile_number.grid(row=10, column=4)
        
        self.entered_tile_number = 0
        # allow only empty or integer values to be entered by using a validation function
        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry_tile_number = tk.Entry(self.interior, validate="key", validatecommand=(vcmd, '%P'))
        self.entry_tile_number.grid(row=10, column=3)
        
        self.label_player = tk.Label(self.interior, text=":שחקן")
        self.label_player.grid(row=10, column=2)
        
        # combobox for player selection (choose player to draw tiles)
        players_data = self.listbox.get(0,tk.END) # get player data from multilistbox
        player_list = [p[1] for p in players_data] # list of player names
        self.pick_player_combobox = ttk.Combobox(self.interior, values=player_list, postcommand=self.update_player_selection) #postcommand - function to run when the dropdown button is pressed
        self.pick_player_combobox.grid(row=10, column=1)
               
        self.draw_tiles_button = tk.Button(self.interior, text="הגרל", command=self.draw, width=4, bg='#e1e1e1')
        self.draw_tiles_button.grid(row=10,column=0, padx=10)
        self.undo_button = tk.Button(self.interior, text="בטל", command=self.undo_last_draw, width=4, bg='#e1e1e1')
        self.undo_button.grid(row=11,column=0, pady=(3,0))
        self.balloon = Pmw.Balloon(self.interior)
        self.balloon.bind(self.undo_button, 'בטל את ההגרלה האחרונה')
        
        # send email checkbox - can untick to not send emails to players
        # upon drawing letters
        self.send_email = tk.IntVar()
        self.send_email_checkbutton = tk.Checkbutton(self.interior, text="שלח מייל", variable=self.send_email)
        self.send_email_checkbutton.grid(row=11, column=2, columnspan=2)
        self.send_email_checkbutton.select() # set checkbox to on at startup
        
        # show / hide tile draw history
        self.show_history_button = tk.Button(self.interior, text="הסתר היסטוריה", command=self.toggle_display_history, bg='#e1e1e1')
        self.show_history_button.grid(row=12,column=3)
           
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
        # get player name and email from entry fields
        name = self.player_name_entry.get()
        email = self.player_email_entry.get()
        self.listbox.insert(tk.END,(email, name)) # add player line to listbox

        # clear player data entry fields
        self.entry_name.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        
        self.update_player_selection() # update player selection combobox

    
    def remove_player(self):
        '''
        Delete the selected player

        '''
        selected_ind = self.listbox.curselection()[0]
        self.listbox.delete(selected_ind) # delete selected line from list
        
        self.update_player_selection() # update player selection combobox
    
    def delete_all_players(self):
        '''
        Delete the entire player list

        '''
        self.listbox.delete(0, tk.END) # delete all player data from the multilistbox       
        self.update_player_selection() # update player selection combobox

    def save_players_to_file(self):
        '''
        Save the player details to a tab delimited text file.
        Each player data is saved to a line with the format: name \t mail \n

        '''
        filename = filedialog.asksaveasfilename(initialdir = "./",title = "Select file",filetypes = (("text file","*.txt"),("all files","*.*")))
        # save the players to file
        with open(filename, "w", encoding="utf-8") as file:
            players_data = self.listbox.get(0,tk.END)
            for p in players_data:
                file.write(p[1] + "\t" + p[0] + "\n") # name \t email \n
         
        # write status bar update
        self.status.config(text="Saved player data to file.")
    
    def load_players_from_file(self):
        filename =  filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("text file","*.txt"),("all files","*.*")))
        
        with open(filename, newline = '', encoding="utf-8") as players:
            player_reader = csv.reader(players, delimiter='\t') # read player data from tab delimited text file
            for player in player_reader:
                name = player[0]
                email = player[1]
                self.listbox.insert(tk.END,(email, name)) # add player line to listbox
       
        self.update_player_selection() # update player selection combobox
                
        # write status bar update
        self.status.config(text="Loaded player data from file.")
    
    def draw(self):
        # first, update combobox
        self.update_player_selection() # update player selection combobox

        tile_number = self.entered_tile_number # get number of tiles to draw

        # change default player for next draw to be the next one
        player_selected_ind = self.pick_player_combobox.current()
        
        # get the selected player data from multilistbox
        player_data = self.listbox.get(player_selected_ind)
        player_name = player_data[1]
        player_email = player_data[0]
        
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
        player_text = player_name + ": "
        tiles_text = " ".join(heb_tiles)
 
        # send email to player
        if self.send_email.get():
            to = player_email
            subject = "אותיות שהוגרלו"
            body = tiles_text
            send_from_gmail(self.gmail_address, self.gmail_password, [to], subject, body)

        # set selected player to next one in list
        num_players = self.listbox.size()
        next_player_ind = (player_selected_ind + 1) % num_players
        self.pick_player_combobox.current(next_player_ind)

        # write to status bar and history text box
        self.text.configure(state='normal') # allow writing to text box
        num_tiles_left = sum(self.bank.inventory)
        num_tiles_drawn = len(heb_tiles)
        if num_tiles_drawn>0:
            # text for status bar
            text = str(num_tiles_drawn) + " tiles drawn for " + player_name + \
                ", number of tiles left in bank: " + str(num_tiles_left) + "."
            
            textbox_message = player_text + tiles_text
        else:
            text = "Bank is empty!"
            # write to history text box
            textbox_message = text
            
        self.status.config(text=text) # write to status bar
        
        # write which tiles were drawn to the text box
        self.text.insert(tk.INSERT, textbox_message + "\n")
        #self.text.insert(tk.END, "\n" + textbox_message) # write to end of text
        # use leading instead of trailing \n to allow deletion with undo
        # https://stackoverflow.com/questions/43561558/using-tkinter-text-indexing-expressions-to-delete-last-line-of-text
        
        self.text.configure(state='disabled') # lock writing to text box - so it can't be written into from GUI
        self.text.yview_pickplace(tk.END) # scroll to end
        
    
    def undo_last_draw(self):
        '''
        Undo the last drawing of letters - return letters to the bank, delete from history

        '''
        message = self.bank.back()
        # write to status bar
        self.status.config(text=message)
        
        # TO DO: replace this check - more reliable to modify bank.back to RETURN A FLAG
        # instead of relying on text box state which may be buggy
        if self.text.compare("end-1c", "==", "1.0"): # check if the textbox is empty
            #print("the widget is empty") # DEBUG
        
            # set selected player in combobox 1 back (assuming want to redraw what was undone)
            player_selected_ind = self.pick_player_combobox.current()
            num_players = self.listbox.size()
            prev_player_ind = (player_selected_ind - 1) % num_players
            self.pick_player_combobox.current(prev_player_ind)
            
        # delete the last line from the textbox
        self.text.configure(state='normal') # allow writing to text box
        #self.text.delete("end-1c linestart", "end") # wrong because there is a \n at the end which should keep (is there since the beginning, all text inserted before it)
        self.text.delete("end-2c linestart", "end-1c") # this works!
        self.text.configure(state='disabled') # lock writing to text box
            
    
    def update_player_selection(self):
        '''
        call this function whenever players are added or deleted, to update
        the player selection combobox

        '''
        players_data = self.listbox.get(0,tk.END)
        player_list = [p[1] for p in players_data] # list of player names
        self.pick_player_combobox["values"] = player_list
        
    def print_log(self):
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
            
        ### FOR DEBUG - use this button to print out some variable values
        #print('current values of TileBankGUI class variables:')
        #print('tile distribution: ')
        #print(self.tile_distribution)
        #print('mail: ', self.gmail_address, ', password: ', self.gmail_password)
        ### END FOR DEBUG SECTION
    
    def create_settings_window(self):
        window = tk.Toplevel(self.master) # or tk.Toplevel()? Is it necessary to give an input?
        window.grab_set() # disable main menu while settings window is open
        window.title('הגדרות')
        ## settings title
        title_label = tk.Label(window, text='הגדרות', font=("Helvetica", 14))
        title_label.pack(side=tk.TOP)
        
        ## gmail account settings
        mail_labelframe = tk.LabelFrame(window, text="Gmail Account")
        mail_labelframe.pack(fill="both", expand="yes", padx=10, pady=10)
               
        email_label = tk.Label(mail_labelframe, text="E-mail")
        password_label = tk.Label(mail_labelframe, text="Password")
        email_entry = tk.Entry(mail_labelframe)
        password_entry = tk.Entry(mail_labelframe, show="*")
       
        if self.gmail_address is not None:
            full_gmail = self.gmail_address.rstrip() # remove trailing EOL character with rstrip
            if full_gmail[-10:]=='@gmail.com':
                gmail_username = full_gmail[:-10]
            else:
                gmail_username = ''
            email_entry.insert(0, gmail_username)

            password_entry.insert(0, self.gmail_password)

        email_label.grid(row=0, sticky=tk.E)
        password_label.grid(row=1, sticky=tk.E)
        
        email_entry.grid(row=0, column=1)
        password_entry.grid(row=1, column=1)
        
        gmail_label = tk.Label(mail_labelframe, text="@gmail.com")
        gmail_label.grid(row=0, column=2)
        
        ## set letter distribution
        letter_distribution_labelframe = tk.LabelFrame(window, text="Letter Distribution")
        letter_distribution_labelframe.pack(fill="both", expand="yes", padx=10, pady=10)
        
        # setup tile distribution frame which displays the tile_distribution
        ld = LetterDistributionSetting(letter_distribution_labelframe, self.tile_distribution.copy())
        ld.grid(row=0,column=0)
        
        
        ## exit buttons (for exit with and without saving changes)
        def save_settings():
            ## save email config to file
            # get entries
            email = email_entry.get()
            password = password_entry.get()
            
            ## save to file
            save_email('mail_settings.txt', email, password)
            # save to main GUI variables
            self.gmail_address, self.gmail_password = email+'@gmail.com', password
            
            ## save tile distribution to file
            # get the tile distribution set in the gui
            new_tile_distribution = ld.getDistribution()
            
            # save the new distribution to file and to main GUI variable, and to bank class
            save_tile_distribution('letter_distribution.csv', new_tile_distribution) # save the new tile distribution to file
            self.tile_distribution = new_tile_distribution.copy() # save to GUI parameter
            self.bank.set_tile_distribution(new_tile_distribution.copy()) # save to tile bank class
                      
            # write status bar update
            self.status.config(text="Saved changes to game settings.")
            
            ## quit the settings window
            window.destroy()
        
        buttons_frame = tk.Frame(window)
        buttons_frame.pack(side=tk.BOTTOM)
        
        ok_button = tk.Button(buttons_frame, text='אישור', command=save_settings, bg='#e1e1e1')
        ok_button.grid(row=0, column=1, padx=40)
        balloon = Pmw.Balloon(buttons_frame)
        balloon.bind(ok_button , 'שמור שינויים. התפלגות האותיות החדשה תיכנס לשימוש כשיתחיל משחק חדש.')
        
        cancel_button = tk.Button(buttons_frame, text='ביטול', command=window.destroy, bg='#e1e1e1')
        cancel_button.grid(row=0, column=0, padx=40)   
       


## create GUI object, run main loop
root = tk.Tk()
tile_bank_gui = TileBankGUI(root)
root.mainloop()