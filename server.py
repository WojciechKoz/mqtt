import csv
from datetime import datetime

class Server:
    def __init__(self, terminals_filename, logs_filename, cards_filename):
        self.term_file = terminals_filename
        self.logs_file = logs_filename
        self.card_file = cards_filename
        self.terminals = []
        self.cards = []
        
        self.load_cards_from_file()
        self.load_term_from_file()
        self.get_logs() # appends header if there is no such a file


    def load_cards_from_file(self):
        try:
            file = open(self.card_file, newline='')
            csvreader = csv.reader(file)
            next(csvreader)
            for row in csvreader:
                self.cards.append([str(row[0]), row[1], row[2]]) 
            file.close()
        except:
            with open(self.card_file, 'w') as file:
                file.write('RFIDnum,name,surname\n')


    def load_term_from_file(self):
        try:
            file = open(self.term_file, newline='')
            csvreader = csv.reader(file)
            next(csvreader) # header
            for row in csvreader:
                self.terminals.append([row[0], row[1]])
            file.close()
        except:
            with open(self.term_file, 'w') as file:
                file.write('ID,place\n')


    def append_new_card_to_file(self):
        ''' saves new card - tuple like (num, name, surname) into file with csv format '''
        ''' the new card is the last element of the list '''

        with open(self.card_file, 'a') as file:
            file.write(','.join(tuple(str(val) for val in self.cards[-1]))+'\n')


    def append_new_term_to_file(self):
        with open(self.term_file, 'a') as file:
            file.write(self.terminals[-1][0]+','+self.terminals[-1][1]+'\n')


    def rewrite_cards_in_file(self):
        ''' Since we have all the cards except the one to be removed 
        from the list, the easiest way is to rewrite the entire list to a file '''

        with open(self.card_file, 'w') as file:
            # header
            file.write('RFIDnum,name,surname\n')

            # stuff
            for card in self.cards:
                file.write(','.join(map(str, card))+'\n')


    def rewrite_terms_in_file(self):
        ''' the same as in remove_card_in_file '''

        with open(self.term_file, 'w') as file:
            file.write('ID,place\n')
            for term in self.terminals:
                file.write(','.join(term)+'\n')


    def add_card(self, card_num, username='', usersurname=''):
        if card_num in [card[0] for card in self.cards]: return None
        self.cards.append((card_num, username, usersurname))
        self.append_new_card_to_file()


    def remove_card(self, card_num):
        ''' removes a tuple which has a card with a given number value '''

        # that line finds index of that tuple and removes it
        self.cards.pop(list(map(lambda vals: vals[0], self.cards)).index(card_num))

        self.rewrite_cards_in_file()


    def add_terminal(self, ID, place):
        if ID in [term[0] for term in self.terminals]: 
            return None 
        self.terminals.append([ID, place])
        self.append_new_term_to_file()


    def remove_terminal(self, terminalID):
        self.terminals.pop(list(map(lambda vals: vals[0], self.terminals)).index(terminalID))
        self.rewrite_terms_in_file()


    def find_person(self, RFIDnum):
        ''' finds the name and surname of the card owner '''

        data = list(filter(lambda vals: vals[0] == RFIDnum, self.cards))
        if len(data) != 1: assert("something went wrong")
        return data[0][1], data[0][2]


    def gate_update(self, ID, RFIDnum):
        def find_place(): return list(filter(lambda pair: pair[0] == ID, self.terminals))[0][1]

        if ID not in [term[0] for term in self.terminals]:
            return None

        name, surname = "", ""
        if RFIDnum in [num for num,_,_ in self.cards]:
            name, surname = self.find_person(RFIDnum)

        with open(self.logs_file, 'a') as file:
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")            
            line = [date, RFIDnum, name, surname, ID, find_place()]
            file.write(','.join(line)+'\n')
        
    def get_logs(self):
        output = []
        try:
            file = open(self.logs_file, newline='')
            csvreader = csv.reader(file)
            for row in csvreader:
                output.append(row)
            file.close()
        except:
            with open(self.logs_file, 'w') as file:
                file.write('date,RFIDnum,name,surname,terminalID,action\n')
        return output

    def debug(self, msg):
        with open("data/debug.log", "a") as file:
            file.write(msg+'\n')



