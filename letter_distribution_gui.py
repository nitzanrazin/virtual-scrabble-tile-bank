import tkinter as tk

from tkinter import ttk

class LetterDistributionSetting(tk.Frame):
    def __init__(self, master, distribution):
        # distribution = a list of amout of tiles of each type in tile bank, order: aleph - tav, *
        tk.Frame.__init__(self, master)
        self.distribution = distribution
        
        # game version distributions
        self.game_version_distribution = {}
        self.game_version_distribution['2008 JW Spears and Sons'] = \
            [6, 4, 1, 4, 8, 12, 1, 3, 1, 10, 2, 6, 6, 3, 1, 2, 3, 1, 2, 8, 6, 8, 2]
        self.game_version_distribution['1980s JW Spears and Sons'] = \
            [6, 4, 2, 4, 8, 12, 1, 3, 1, 10, 2, 6, 6, 4, 1, 2, 3, 2, 3, 8, 6, 9, 2]
        self.game_version_distribution['1977 JW Spears and Sons'] = \
            [3, 4, 1, 4, 9, 12, 1, 2, 1, 10, 2, 6, 6, 3, 1, 2, 3, 1, 2, 8, 6, 8, 2]
        self.game_version_distribution['1975 Selchow & Righter'] = \
            [4, 4, 1, 4, 8, 12, 1, 2, 1, 10, 2, 6, 6, 3, 1, 2, 3, 1, 2, 8, 6, 9, 2]
        
        
        # label and entry for each tile
        self.ind_to_heb_ord = {0: 1488, 1: 1489, 2: 1490, 3: 1491, 4: 1492, 5: 1493,
                              6: 1494, 7: 1495, 8: 1496, 9: 1497, 10: 1499, 11: 1500,
                              12: 1502, 13: 1504, 14: 1505, 15: 1506, 16: 1508, 17: 1510,
                              18: 1511, 19: 1512, 20: 1513, 21: 1514, 22: 42}
        
        # label with total number of tiles (define before distribution change entry fields so that self.tile_label is already defined when they are changed)
        total_num_tiles = sum(self.distribution)
        total_num_tiles_text = 'Total number of tiles: ' + str(total_num_tiles)
        self.tile_label = tk.Label(master, text=total_num_tiles_text)
        self.tile_label.grid(row=7, column=0, columnspan=8)
        
        num_rows = 6
        num_columns = 4
        self.tile_labels = []
        self.tile_amount_entries = []
        self.string_vars = [None] * 23
        for tile_ind in self.ind_to_heb_ord.keys():
            tile_label = tk.Label(master, text=chr(self.ind_to_heb_ord[tile_ind]), pady=2)
            
            #tile_amount_entry = tk.Entry(master, width=3)
            self.string_vars[tile_ind] = tk.StringVar()
            self.string_vars[tile_ind].trace("w", lambda name, index, mode, var=self.string_vars[tile_ind], tile_ind=tile_ind:self.entry_update(var, tile_ind))
            # registering the observer 
            #self.string_vars[tile_ind].trace_add('write', self.entry_change_callback) 
            # validate that entries of number of tiles are numbers only (or empty field)
            vcmd = master.register(self._validate)
            tile_amount_entry = tk.Entry(master, textvariable=self.string_vars[tile_ind], validate="key", validatecommand=(vcmd, '%P'), width=3)
            tile_amount_entry.insert(0, self.distribution[tile_ind]) # display amount set in distribution
            
            # place tile labels and amount entry fields in a grid
            r = tile_ind % num_rows
            c = tile_ind // num_rows
            tile_label.grid(row=r, column=2*num_columns - 2*c, padx=(0,35))
            tile_amount_entry.grid(row=r, column=2*num_columns - 2*c - 1)
            
            self.tile_labels.append(tile_label)
            self.tile_amount_entries.append(tile_amount_entry)
        
       
        # distribution selection from combobox of game versions
        game_version_selection_label = tk.Label(master, text='Set letter distribution to game version:')
        game_version_selection_label.grid(row=9, column=0, columnspan=8, pady=(20,0))
        
        # function to run when combobox value is changed
        def on_field_change(index, value, op):
            #print("combobox updated to ", v.get()) # DEBUG
            # change letter distribution to the selected game version
            game_version_value = game_version.get()
            
            # if chose a non-blank game version, change tile distribution to the chosen one
            if game_version_value:
                self.distribution = self.game_version_distribution[game_version_value]
                
                # update letter distribution entries
                for tile_ind, tile_amount_entry in enumerate(self.tile_amount_entries):
                    tile_amount_entry.delete(0, tk.END) # delete previous value
                    tile_amount_entry.insert(0, self.distribution[tile_ind]) # enter numer of tiles from chosen distribution
                
                # update total number of tiles
                total_num_tiles = sum(self.distribution)
                total_num_tiles_text = 'Total number of tiles: ' + str(total_num_tiles)
                self.tile_label['text'] = total_num_tiles_text
        
        game_version_list = ['']+list(self.game_version_distribution.keys())
        game_version = tk.StringVar(master)
        game_version.trace('w',on_field_change)
        self.pick_player_combobox = ttk.Combobox(master, textvar=game_version, values=game_version_list)
        self.pick_player_combobox.grid(row=10, column=2, columnspan=6)
               
    def entry_update(self, var, indx): 
        # DEBUG
        #print('var: ', var)
        #print('indx: ', indx)
        #print('var.get(): ', var.get())
        
        # get entered value of tile number, convert from string to int and 
        # if the string is empty use zero
        tile_num_str = var.get()
        if tile_num_str:
            tile_num = int(tile_num_str)
                
            # update distribution
            self.distribution[indx] = tile_num
            
            # update total number of tiles displayed in gui
            total_num_tiles = sum(self.distribution)
            total_num_tiles_text = 'Total number of tiles: ' + str(total_num_tiles)
            self.tile_label['text'] = total_num_tiles_text

    def _validate(self, new_text):
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
            return True

        try:
            _ = int(new_text)
            return True
        except ValueError:
            return False
        
    def setDistribution(self, distribution):
        self.distribution = distribution
        
    def getDistribution(self):
        return self.distribution
    
    
if __name__ == '__main__':
    root = tk.Tk()
    inventory = [6, 4, 1, 4, 8, 12, 1, 2, 1, 10, 2, 6, 6, 3, 1, 2, 3, 1, 2, 8, 6, 8, 2]
    ld = LetterDistributionSetting(root, inventory)
    root.mainloop(  )