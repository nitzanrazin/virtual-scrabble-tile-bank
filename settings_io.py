'''
functions for saving and loading settings from files
'''

import csv # for writing and reading from file
# TO DO: change naming convension so it is clear where the variable stores the full email, and where just the gmail username
def save_email(filename, email, password):
    with open(filename, 'w') as file:
        file.write(email + '@gmail.com\n' + password)

def load_email(filename):
    try:
        f = open(filename, "r")
        gmail_user = f.readline()
        gmail_password = f.readline()
        f.close()
        return gmail_user, gmail_password
    except FileNotFoundError:
        print(filename, " not found")
        return None, None


def save_tile_distribution(filename, tile_distribution):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(tile_distribution)
            

def load_tile_distribution(filename):
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # read just the first row (file is expected to have one row containing 23 comma separated integers)
            row1 = next(reader)  # gets the first line
            tile_distribution = [int(x) for x in row1] # convert to integer
            return tile_distribution
    except FileNotFoundError:
        print(filename, " not found, default tile distribution used")
        return None
    
    