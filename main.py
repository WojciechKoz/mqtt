from server import Server
from menu import choice
from utils import clear
from listener import Listener

server = Server('data/terminals.csv', 'data/logs.csv', 'data/cards.csv')
menu = ['add card', 'change card owner', \
        'print terminals', 'print cards', 'print logs', 'quit']

listener = Listener(server) # creates server listener

while True:
    output = choice(menu)    
    if output == 'quit':
        break;
    elif output == 'add card':
        server.add_card(input("Card ID > "), input("owners name > "), input("owners surname > "))
    elif output == 'change card owner':
        card = choice(server.cards)
        if not card: continue
        server.remove_card(card[0])
        server.add_card(card[0], input("owners name > "), input("owners surname > "))
    elif output == 'print terminals':
        clear()
        print("Terminals:")
        for term in server.terminals:
            print(str(term))
        input("press enter to continue ... ")
    elif output == 'print cards':
        clear()
        print("Cards:")
        for card in server.cards:
            print(' '.join(map(str, card)))
        input("press enter to continue ... ")
    elif output == 'print logs':
        clear()
        data = server.get_logs()
        for row in data:
            print(','.join(row))
        input("press enter to continue ... ")
        
listener.disconnect()
        
