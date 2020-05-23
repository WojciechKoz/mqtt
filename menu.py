from utils import clear, getchar

def choice(choices):
    if not choices: 
        input("There are no option to choose from. First you need to add some cards or terminals")
        return None

    index = 0
    while True:
        clear()
        print('\tMENU')
        for i, text in enumerate(choices):
            print(('* ' if i == index else '  ')+str(text))
        print("\n\npress 'j' and 'k' to go up and down and space or enter to confirm choice")
        ch = getchar()
        if ch == 'j':
            index = min(index+1, len(choices)-1)
        elif ch == 'k':
            index = max(index-1, 0)
        elif ch == 'G':
            index = len(choices)-1
        elif ch == 'g':
            index = 0
        elif ch == ' ' or ord(ch) == 13: # space or enter
            return choices[index]

