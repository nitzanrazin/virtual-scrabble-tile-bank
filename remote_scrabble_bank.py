# scrabble letter bank
import numpy as np

class LetterBank:
    def __init__(self):
        '''
        initialize letter bank to include all letters (and 2 blank tiles)

        '''
        #self.all_tiles = [6, 4, 1, 4, 8, 12, 1, 3, 1, 10, 2, 6, 6, 3, 1, 2, 3, 1, 2, 8, 6, 8, 2] # 2008 game version
        self.all_tiles = [6, 4, 1, 4, 8, 12, 1, 2, 1, 10, 2, 6, 6, 3, 1, 2, 3, 1, 2, 8, 6, 8, 2] # 2008 version - 1 chet for more compatibility with 70s version
        # number of tiles in the bank for each type: aleph - tav, blank
        self.inventory = self.all_tiles.copy()
        
        self.ind_to_letter = {0: 'aleph', 1: 'bet', 2: 'gimel', 3: 'dalet', 4: 'he', 5: 'vav',
                              6: 'zayin', 7: 'het', 8: 'tet', 9: 'yod', 10: 'kaf', 11: 'lamed',
                              12: 'mem', 13: 'nun', 14: 'samekh', 15: 'ayin', 16: 'pe', 17: 'tsadi',
                              18: 'qof', 19: 'resh', 20: 'shin', 21: 'tav', 22: 'blank'}
        
        self.letter_to_ind = {'aleph': 0, 'bet': 1, 'gimel': 2, 'dalet': 3, 'he': 4, 'vav': 5, 'zayin': 6,
                              'het': 7, 'tet': 8, 'yod': 9, 'kaf': 10, 'lamed': 11, 'mem': 12, 'nun': 13,
                              'samekh': 14, 'ayin': 15, 'pe': 16, 'tsadi': 17, 'qof': 18, 'resh': 19, 'shin': 20,
                              'tav': 21, 'blank': 22}
        
        self.ind_to_heb_ord = {0: 1488, 1: 1489, 2: 1490, 3: 1491, 4: 1492, 5: 1493,
                              6: 1494, 7: 1495, 8: 1496, 9: 1497, 10: 1499, 11: 1500,
                              12: 1502, 13: 1504, 14: 1505, 15: 1506, 16: 1508, 17: 1510,
                              18: 1511, 19: 1512, 20: 1513, 21: 1514, 22: 42}
        
        self.history = [] # history of all letters drawn, to allow "back"
        
    def reset(self):
        '''
        reset letter bank to include all letters (and 2 blank tiles),
        reset history

        '''
        self.inventory = self.all_tiles.copy() # reset tile bank to include all game tiles
        self.history = [] # history of all letters drawn, to allow "back"
        
    def draw(self, n):
        '''
        Draw n tiles from the letter bank.
        
        Parameters
        ----------
        n : integer between 1 and 7
            the number of tiles to be randomly drawn from the letter bank

        Returns
        -------
        the letters

        '''
        assert n in [1,2,3,4,5,6,7], "must draw 1-7 tiles"
        
        tiles_drawn = []
        inds_drawn = []
        
        for t in range(n):
            num_tiles = sum(self.inventory) # total number of tiles currently in inventory
            
            if num_tiles==0:
                print('Bank is empty!')
                break
            
            prob = np.array(self.inventory) / num_tiles
            
            chosen_tile_ind = np.random.choice(len(self.inventory), p=prob)
            
            self.inventory[chosen_tile_ind] -= 1 # remove tile from inventory
            tiles_drawn.append(self.ind_to_letter[chosen_tile_ind])
            inds_drawn.append(chosen_tile_ind)
            
        self.history.append(tiles_drawn)
        
        return tiles_drawn, inds_drawn
    
    def back(self):
        '''
        go back one step - return last drawn tiles into the letter bank.

        Returns
        -------
        None.

        '''
        if len(self.history) == 0:
            #print('Cannot undo last draw, no tiles were drawn yet.')
            message = 'Cannot undo last draw, no tiles were drawn yet.'
        else:
            last_drawn = self.history.pop()
            for tile in last_drawn: # return all tiles in last draw to inventory
                tile_ind = self.letter_to_ind[tile]
                self.inventory[tile_ind] += 1
                
            #print('Returned the last drawn tiles to the bank.')
            num_tiles_returned = len(last_drawn)
            num_tiles = sum(self.inventory)
            message = 'Returned the last ' + str(num_tiles_returned) + \
                ' drawn tiles to the bank, number of tiles in bank: ' + \
                str(num_tiles) + '.'
            print('last_drawn: ', last_drawn) #DEBUG
            print('inv: ', self.inventory)
                
        return message
        
        
            
### test
# bank = LetterBank()

# print(bank.draw(7))
# print(bank.draw(4))
# print(bank.inventory)
# print(bank.history)
# bank.back()
# print(bank.inventory)
# print(bank.history)            
