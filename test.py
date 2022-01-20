import curses
from random import randint

#IMPORTANT: to run the code, alt-cmd-t, then type python test.py

#set the window/map
curses.initscr()
win = curses.newwin(20, 60, 0, 0) #creates new window of given size 20 lines(y 1st) 60 columns (x 2nd), starts 0 0
win.keypad(1) #true for keypad
curses.noecho() #doesn't let other keys do anything
curses.curs_set(0)
win.border(0) #creates border
win.nodelay(1) #no delay, doesn't wait for user input

#snake & food
snake = [(4,10), (4,9), (4,8)] #where the snake start (y,x) in tuple
food = (randint(1, 18), randint(1,58)) #random into between (1,18) and (1,58) (y,x)
esc = 27 #exit for curses
key = curses.KEY_RIGHT
intoself = 0
score = 0
win.addch(food[0], food[1], 'π')

while key != esc:
    win.addstr(0, 2, 'Score ' + str(score) + ' ') #puts score on top left
    win.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120) #curses speed of snake
    prevKey = key
    event = win.getch() #waits for next user input

    if event != -1:
        key = event
    else:
        prevKey #continues going in the key direction

    if key == ord(' '): #space bar pause
        key = -1
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, esc]: #if invalid key is pressed
        key = prevKey #just continue


    #calculate the next coordinates
    y = snake[0][0] #remember, coordinates are (y,x) so [1st tuple][1st index/y coordinate] which is head
    x = snake[0][1] #[1st tuple][2nd index/x coordinate]


    if key == curses.KEY_DOWN and intoself == 2: #snake can't go backwards into itself
        key = prevKey
    if key == curses.KEY_UP and intoself == 3:
        key = prevKey
    if key == curses.KEY_LEFT and intoself == 0:
        key = prevKey
    if key == curses.KEY_RIGHT and intoself == 1:
        key = prevKey

    if key == curses.KEY_DOWN: #y coordinates increases as going down
        y += 1
        intoself = 3
    if key == curses.KEY_UP:
        y -= 1
        intoself = 2
    if key == curses.KEY_LEFT:
        x -= 1
        intoself = 1
    if key == curses.KEY_RIGHT:
        x += 1
        intoself = 0

    snake.insert(0, (y,x))

    #case: border hit
    if y == 0:
        break
    if y == 19:
        break
    if x == 0:
        break
    if x == 59:
        break

    #case: snake hits itself
    if snake[0] in snake[1:]: #if the snake head is in from 1 to end
        break
    #snake hits food
    if snake[0] == food:
        food = () #food is gone/eaten
        while food == (): #so generate a new food random place
            food = (randint(1, 18), randint(1,58))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], 'π')
        score += 1
    else:
        last = snake.pop()
        win.addch(last[0], last[1], ' ') #addch(y, x, ch[, attr]) Paint character ch at (y, x)
    win.addch(snake[0][0], snake[0][1], '∞')


curses.endwin() #closes window
print(f"Final Score = {score}")
