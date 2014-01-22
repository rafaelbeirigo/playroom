#!/usr/bin/python
# coding=UTF-8

import Tkinter as tk
from Board import *
from Piece import *
from random import randint
from PIL.ImageTk import PhotoImage
from random import choice
from time import sleep

def update_light_state():
    pass

def update_music_state():
    pass

def update_bell_sound_state():
    # only turns of, it is turned on using
    # kick_ball function
    global bell_sound
    global step

    print 'Updating bell state...'
    print 'Bell state: ' + bell_sound['state']
    print 'Bell step: ' + str(bell_sound['step'])
    print 'Step: ' + str(step)
    if bell_sound['state'] == 'ON':
        print 'Bell was on'
        if step > bell_sound['step']:
            print 'It was turned on the step: ' + str(bell_sound['step'])
            print 'The current step is: ' + str(step)
            turn_bell('OFF')
        else:
            print 'It was turned on this same step'
    else:
        print 'Bell was off'

def update_toy_monkey_sound_state():
    global toy_monkey_sound
    if toy_monkey_sound['state'] == 'ON':
        if light['state'] == 'ON' or \
           music['state'] == 'OFF':
           turn_toy_monkey('OFF')
    else:
        if light['state'] == 'OFF' and \
           music['state'] == 'ON' and \
           bell_sound['state'] == 'ON':
           turn_toy_monkey('ON')

# Environment variables
light = {'state':'ON', 'step':0, 'update_function':update_light_state}
music = {'state':'ON', 'step':0, 'update_function':update_music_state}
bell_sound = {'state':'ON', 'step':0, 'update_function':update_bell_sound_state}
toy_monkey_sound = {'state':'ON', 'step':0, 'update_function':update_toy_monkey_sound_state}
environment_variables = [light, bell_sound, music, toy_monkey_sound]

step = 0

def turn_light(new_light_state):
    global light
    light['state'] = new_light_state
    light['step'] = step

def flick_switch():
    global light
    if light['state'] == 'ON':
        turn_light('OFF')
    else:
        turn_light('ON')

def square_is_occuppied(square):
    for piece in non_agent_pieces:
        if piece.row == square[0] and \
          piece.column == square[1]:
          return True
    return False

def get_adj_squares(piece):
    adj_squares = []
    for row_inc in range(-1, 2):
        for col_inc in range(-1, 2):
            row = piece.row + row_inc
            column = piece.column + col_inc

            # only legal rows
            if ( row >= 0 and row < board.rows ):

                # only legal columns
                if ( column >= 0 and column < board.columns ):

                    # not the piece square
                    if ( row_inc != 0 or col_inc != 0 ):

                        # only unnoccupied squares count
                        if not ( square_is_occuppied ( ( row, column ) ) ):
                            adj_squares.append( (row, column ) )
    return adj_squares

def move_piece_to_square(piece, square):
    piece.row = square[0]
    piece.column = square[1]
    board.placepiece(piece)

def push_block(block):
    adj_squares = get_adj_squares(block)
    if len(adj_squares) > 0:
        random_index = randint(0, len(adj_squares) - 1)
        move_piece_to_square(block, adj_squares[random_index])

def push_blue_block():
    push_block(play)

def push_red_block():
    push_block(stop)

def turn_music_on():
    global music
    global step
    music['state'] = 'ON'
    music['step'] = step

def turn_music_off():
    global music
    global step
    music['state'] = 'OFF'
    music['step'] = step

def press_blue_block():
    turn_music_on()

def press_red_block():
    turn_music_off()

def kick_ball():
    move_piece_to_piece(ball, marker)
    if on_same_cell(ball, bell):
        turn_bell('ON')

def on_same_cell(piece1, piece2):
    return piece1.row == piece2.row and \
           piece1.column == piece2.column

def get_actions_from_agent():
    return [
        'move_eye_to_hand',
        'move_eye_to_marker',
        'move_eye_one_step_north',
        'move_eye_one_step_south',
        'move_eye_one_step_east',
        'move_eye_one_step_west',
        'move_eye_to_random_object',
        'move_hand_to_eye',
        'move_marker_to_eye'
        ]

def get_actions_from_pieces():
    if on_same_cell(eye, hand):
        for piece in non_agent_pieces:
            if on_same_cell(piece, eye):
                return piece.get_actions()
    return []

def turn_bell(new_state):
    global bell
    global step
    bell_sound['state'] = new_state
    bell_sound['step'] = step

def turn_toy_monkey(new_state):
    global toy_monkey_sound
    toy_monkey_sound['state'] = new_state
    toy_monkey_sound['step'] = step

def update_state():
    pass

def move_piece_to_piece(piece_to_move, destination_piece):
    piece_to_move.row = destination_piece.row
    piece_to_move.column = destination_piece.column

    board.placepiece(piece_to_move)

def move_eye_to_random_object():
    random_index = randint(0, len(non_agent_pieces) - 1)
    move_piece_to_piece(eye, non_agent_pieces[random_index])

def move_hand_to_eye():
    move_piece_to_piece(hand, eye)

def move_marker_to_eye():
    move_piece_to_piece(marker, eye)

def move_eye_to_marker():
    move_piece_to_piece(eye, marker)

def move_eye_to_hand():
    move_piece_to_piece(eye, hand)

def move_eye_one_step_north():
    move_piece(eye, 'north')

def move_eye_one_step_south():
    move_piece(eye, 'south')

def move_eye_one_step_east():
    move_piece(eye, 'east')

def move_eye_one_step_west():
    move_piece(eye, 'west')

def move_piece(piece, direction):
    if direction == 'north':
        piece.row -= 1
    elif direction == 'south':
        piece.row += 1
    elif direction == 'east':
        piece.column += 1
    elif direction == 'west':
        piece.column -= 1

    if piece.row < 0:
        piece.row = 0
    if piece.row > board.rows - 1:
        piece.row = board.rows - 1
    if piece.column < 0:
        piece.column = 0
    if piece.column > board.columns - 1:
        piece.column = board.columns - 1

    board.placepiece(piece)

def move_piece_by_name(name, direction):
    if name == 'eye':
        move_piece(eye, direction)
    elif name == 'hand':
        move_piece(hand, direction)
    elif name == 'marker':
        move_piece(marker, direction)

current_piece_to_move_using_keys = 'marker'
def key(event):
    global current_piece_to_move_using_keys
    if event.keysym == 'e':
        current_piece_to_move_using_keys = 'eye'
    if event.keysym == 'h':
        current_piece_to_move_using_keys = 'hand'
    if event.keysym == 'm':
        current_piece_to_move_using_keys = 'marker'

    direction = ''
    if event.keysym in ['Up', 'Down', 'Left', 'Right']:
        if event.keysym == 'Up':
            direction = 'north'
        if event.keysym == 'Down':
            direction = 'south'
        if event.keysym == 'Left':
            direction = 'west'
        if event.keysym == 'Right':
            direction = 'east'
        move_piece_by_name(current_piece_to_move_using_keys, direction)

    if event.keysym == '1':
        move_eye_to_marker()
    if event.keysym == '2':
        move_eye_to_hand()
    if event.keysym == '4':
        move_eye_to_random_object()
    if event.keysym == '5':
        move_hand_to_eye()
    if event.keysym == '6':
        move_marker_to_eye()
    if event.keysym == 'p':
        adj_squares = get_adj_squares(eye)
        print 'entrei'
        for adj_square in adj_squares:
            print adj_square
    if event.keysym == 'b':
        push_blue_block()
    if event.keysym == 'r':
        push_red_block()
    if event.keysym == 'f':
        flick_switch()
    if event.keysym == 'a':
        print 'Actions from agent: '
        print get_actions_from_agent()

        print 'Actions from pieces: '
        print get_actions_from_pieces()
    if event.keysym == 'A':
        print 'All available actions: '
        print get_available_actions()
    if event.keysym == 'z':
        for action in all_possible_actions:
            print 'Executing action: ' + action
            execute_action(action)
    if event.keysym == 'B':
        update_available_actions()
        update_action_buttons_state()
    if event.keysym == 'l':
        update_environment_variables()
        update_environment_labels()
        execute_action
    if event.keysym == 't':
        update_toy_monkey_sound_state()
    if event.keysym == 'E':
        update_bell_sound_state()
        update_environment_labels()
        root.update_idletasks()

        global step
        step += 1
        print 'Sleeping for 1 sec...'
        sleep(1)
        print 'Woke up'

        update_bell_sound_state()
        print 'New Bell state: ' + bell_sound['state']

        update_environment_labels()
    update_screen()

def update_environment_variables():
    global environment_variables
    for variable in environment_variables:
        variable['update_function']()

def update_environment_labels():
    global step

    light_label_text.set('Light: ' + light['state'] + ', ' +
                         'step: ' + str(light['step']))
    light_label['image'] = light_label_images[light['state']]

    music_label_text.set('Music: ' + music['state'] + ', ' +
                         'step: ' + str(music['step']))
    music_label['image'] = music_label_images[music['state']]

    bell_sound_label_text.set('Bell: ' + bell_sound['state'] + ', ' +
                              'step: ' + str(bell_sound['step']))
    bell_sound_label['image'] = bell_sound_label_images[bell_sound['state']]

    toy_monkey_sound_label_text.set('Toy Monkey: ' + toy_monkey_sound['state'] + ', ' +
                                    'step: ' + str(toy_monkey_sound['step']))
    toy_monkey_sound_label['image'] = toy_monkey_sound_label_images[toy_monkey_sound['state']]

    step_count_label_text.set('Steps: ' + str(step))

def update_screen():
    update_environment_variables()
    update_environment_labels()
    update_action_buttons_state()
    root.update_idletasks()

def create_action_buttons():
    action_buttons_frame = tk.Frame(central_frame)
    action_buttons_frame.pack(side=tk.RIGHT)

    # Agent
    move_eye_one_step_north_button = tk.Button(action_buttons_frame, text='move_eye_one_step_north', command=move_eye_one_step_north)
    move_eye_one_step_north_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_one_step_north_button)

    move_eye_one_step_south_button = tk.Button(action_buttons_frame, text='move_eye_one_step_south', command=move_eye_one_step_south)
    move_eye_one_step_south_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_one_step_south_button)

    move_eye_one_step_east_button = tk.Button(action_buttons_frame, text='move_eye_one_step_east', command=move_eye_one_step_east)
    move_eye_one_step_east_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_one_step_east_button)

    move_eye_one_step_west_button = tk.Button(action_buttons_frame, text='move_eye_one_step_west', command=move_eye_one_step_west)
    move_eye_one_step_west_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_one_step_west_button)

    move_eye_to_marker_button = tk.Button(action_buttons_frame, text='move_eye_to_marker', command=move_eye_to_marker)
    move_eye_to_marker_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_to_marker_button)

    move_eye_to_random_object_button = tk.Button(action_buttons_frame, text='move_eye_to_random_object', command=move_eye_to_random_object)
    move_eye_to_random_object_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_to_random_object_button)

    move_hand_to_eye_button = tk.Button(action_buttons_frame, text='move_hand_to_eye', command=move_hand_to_eye)
    move_hand_to_eye_button.pack(side=tk.TOP)
    action_buttons.append(move_hand_to_eye_button)

    move_marker_to_eye_button = tk.Button(action_buttons_frame, text='move_marker_to_eye', command=move_marker_to_eye)
    move_marker_to_eye_button.pack(side=tk.TOP)
    action_buttons.append(move_marker_to_eye_button)

    kick_ball_button = tk.Button(action_buttons_frame, text='kick_ball', command=kick_ball)
    kick_ball_button.pack(side=tk.TOP)
    action_buttons.append(kick_ball_button)

    press_blue_block_button = tk.Button(action_buttons_frame, text='press_blue_block', command=press_blue_block)
    press_blue_block_button.pack(side=tk.TOP)
    action_buttons.append(press_blue_block_button)

    push_blue_block_button = tk.Button(action_buttons_frame, text='push_blue_block', command=push_blue_block)
    push_blue_block_button.pack(side=tk.TOP)
    action_buttons.append(push_blue_block_button)

    press_red_block_button = tk.Button(action_buttons_frame, text='press_red_block', command=press_red_block)
    press_red_block_button.pack(side=tk.TOP)
    action_buttons.append(press_red_block_button)

    push_red_block_button = tk.Button(action_buttons_frame, text='push_red_block', command=push_red_block)
    push_red_block_button.pack(side=tk.TOP)
    action_buttons.append(push_red_block_button)

    flick_switch_button = tk.Button(action_buttons_frame, text='flick_switch', command=flick_switch)
    flick_switch_button.pack(side=tk.TOP)
    action_buttons.append(flick_switch_button)

def update_available_actions():
    global available_actions
    available_actions = get_available_actions()

def get_available_actions():
    available_actions = []
    available_actions_agent = get_actions_from_agent()
    available_actions_piece = get_actions_from_pieces()
    return available_actions_agent + available_actions_piece

def execute_action(action):
    all_possible_actions[action]()

def update_action_buttons_state():
    update_available_actions()
    for button in action_buttons:
        if button['text'] in available_actions:
            button['state'] = 'normal'
        else:
            button['state'] = 'disabled'

def random_actions():
    global step
    num_steps = 1000
    for cur_step in range(num_steps):
        step += 1
        update_environment_labels()
        update_action_buttons_state()
        update_available_actions()
        action = choice(available_actions)
        execute_action(action)
        root.update_idletasks()
        sleep(.1)

root = tk.Tk()

# bottomframe = Frame(root)
# bottomframe.pack( side = BOTTOM )

# redbutton = Button(frame, text="Red", fg="red")
# redbutton.pack( side = LEFT)

# greenbutton = Button(frame, text="Brown", fg="brown")
# greenbutton.pack( side = LEFT )

# bluebutton = Button(frame, text="Blue", fg="blue")
# bluebutton.pack( side = LEFT )

# blackbutton = Button(bottomframe, text="Black", fg="black")
# blackbutton.pack( side = BOTTOM)

# Enviroment characteristics
env_charact_frame = tk.Frame(root)
env_charact_frame.pack(side = tk.TOP)

light_label_text = tk.StringVar()
light_label_image_on = tk.PhotoImage(file='/home/rafaelbeirigo/ciencia/playroom/img/labels/light_on.gif')
light_label_image_off = tk.PhotoImage(file='/home/rafaelbeirigo/ciencia/playroom/img/labels/light_off.gif')
light_label_images = {'ON':light_label_image_on, 'OFF':light_label_image_off}
light_label = tk.Label( env_charact_frame, textvariable=light_label_text, relief=tk.RAISED, borderwidth=4, image = light_label_image_on )
light_label.pack(side = tk.LEFT)

bell_sound_label_text = tk.StringVar()
bell_sound_label_image_on = tk.PhotoImage(file='/home/rafaelbeirigo/ciencia/playroom/img/labels/bell_on.gif')
bell_sound_label_image_off = tk.PhotoImage(file='/home/rafaelbeirigo/ciencia/playroom/img/labels/bell_off.gif')
bell_sound_label_images = {'ON':bell_sound_label_image_on, 'OFF':bell_sound_label_image_off}
bell_sound_label = tk.Label( env_charact_frame, textvariable=bell_sound_label_text, relief=tk.RAISED, borderwidth=4 )
bell_sound_label.pack(side = tk.LEFT)

music_label_text = tk.StringVar()
music_label_image_on = tk.PhotoImage(file='/home/rafaelbeirigo/ciencia/playroom/img/labels/music_on.gif')
music_label_image_off = tk.PhotoImage(file='/home/rafaelbeirigo/ciencia/playroom/img/labels/music_off.gif')
music_label_images = {'ON':music_label_image_on, 'OFF':music_label_image_off}
music_label = tk.Label( env_charact_frame, textvariable=music_label_text, relief=tk.RAISED, borderwidth=4 )
music_label.pack(side = tk.LEFT)

toy_monkey_sound_label_text = tk.StringVar()
toy_monkey_sound_label_image_on = tk.PhotoImage(file='/home/rafaelbeirigo/ciencia/playroom/img/labels/toy-monkey_on.gif')
toy_monkey_sound_label_image_off = tk.PhotoImage(file='/home/rafaelbeirigo/ciencia/playroom/img/labels/toy-monkey_off.gif')
toy_monkey_sound_label_images = {'ON':toy_monkey_sound_label_image_on, 'OFF':toy_monkey_sound_label_image_off}
toy_monkey_sound_label = tk.Label( env_charact_frame, textvariable=toy_monkey_sound_label_text, relief=tk.RAISED, borderwidth=4 )
toy_monkey_sound_label.pack(side = tk.LEFT)

step_count_label_text = tk.StringVar()
step_count_label = tk.Label( env_charact_frame, textvariable=step_count_label_text, relief=tk.RAISED, borderwidth=4 )
step_count_label.pack(side = tk.LEFT)

central_frame = tk.Frame(root)
central_frame.pack()

board = Board(central_frame)
board.pack(side="left", fill="both", expand="true", padx=4, pady=4)

ball = Piece(name = "ball", image=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/ball.gif"), actions=['kick_ball'])
bell = Piece(name = "bell", image=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/bell.gif"), row=0, column=1)
play = Piece(name = "play", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/play.gif"), row=0, column=4, actions=['press_blue_block', 'push_blue_block'])
stop = Piece(name = "stop", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/stop.gif"), row=1, column=0, actions=['press_red_block', 'push_red_block'])
switch = Piece(name = "switch", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/switch.gif"), row=1, column=1, actions=['flick_switch'])
toy_monkey = Piece(name = "toy_monkey", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/toy-monkey.gif"), row=1, column=3)

eye = Piece(name = "eye", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/eye.gif"), row=0, column=2)
hand = Piece(name = "hand", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/hand.gif"), row=0, column=3)
marker = Piece(name = "marker", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/target.gif"), row=1, column=2)

agent_pieces = [eye, hand, marker]
non_agent_pieces = [ball, bell, play, stop, switch, toy_monkey]

for piece in non_agent_pieces:
    board.addpiece(piece)
for piece in agent_pieces:
    board.addpiece(piece)

state = []

update_state()

all_possible_actions = {
    'kick_ball':kick_ball,
    'move_eye_to_hand':move_eye_to_hand,
    'move_eye_to_marker':move_eye_to_marker,
    'move_eye_one_step_north':move_eye_one_step_north,
    'move_eye_one_step_south':move_eye_one_step_south,
    'move_eye_one_step_east':move_eye_one_step_east,
    'move_eye_one_step_west':move_eye_one_step_west,
    'move_eye_to_random_object':move_eye_to_random_object,
    'move_hand_to_eye':move_hand_to_eye,
    'press_blue_block':press_blue_block,
    'press_red_block':press_red_block,
    'push_red_block':push_red_block,
    'push_blue_block':push_blue_block,
    'flick_switch':flick_switch,
    'move_marker_to_eye':move_marker_to_eye,
}

action_buttons = []

available_actions = []

update_environment_labels()

create_action_buttons()

random_actions_button = tk.Button(root, text='random_actions', command=random_actions)
random_actions_button.pack(side=tk.TOP)

root.bind_all('<Key>', key)
root.mainloop()
