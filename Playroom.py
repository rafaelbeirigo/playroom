#!/usr/bin/python
# coding=UTF-8

import Tkinter as tk
import pickle
from Board import *
from Piece import *
from random import randint
from random import random
from PIL.ImageTk import PhotoImage
from random import choice
from time import sleep
from itertools import product
from datetime import datetime

def saveobject(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def loadobject(filename):
    with open(filename, 'rb') as input:
       return pickle.load(input)

def update_light_state():
    pass

def update_music_state():
    pass

def update_bell_sound_state():
    # Only turns the bell_sound off; it is turned on using kick_ball
    # function
    if is_on(bell_sound):
        if step > bell_sound['step'] + 1:
            turn_off(bell_sound)

def update_toy_monkey_sound_state():
    if is_on(toy_monkey_sound):
        if is_on(light) or is_off(music):
            turn_off(toy_monkey_sound)
    else:
        if is_off(light) and \
           is_on(music) and \
           is_on(bell_sound):
            turn_on(toy_monkey_sound)

# Environment variables
light                 = {'state':'OFF', 'step':-1, 'update_function':update_light_state}
music                 = {'state':'OFF', 'step':-1, 'update_function':update_music_state}
bell_sound            = {'state':'OFF', 'step':-1, 'update_function':update_bell_sound_state}
toy_monkey_sound      = {'state':'OFF', 'step':-1, 'update_function':update_toy_monkey_sound_state}
environment_variables = [light, bell_sound, music, toy_monkey_sound]

step = 0

def is_on(status_var):
    return status_var['state'] == 'ON'

def is_off(status_var):
    return status_var['state'] == 'OFF'

def turn(status_var, new_status):
    status_var['state'] = new_status
    status_var['step'] = step

def turn_on(status_var):
    if is_off(status_var):
        turn(status_var, 'ON')

def turn_off(status_var):
    if is_on(status_var):
        turn(status_var, 'OFF')

def flick_switch():
    if is_on(light):
        turn_off(light)
    else:
        turn_on(light)

def flick_switch_option():
    a = select_best_action(Q_flick_switch, map_state(state))
    execute_action(a)

def square_is_occuppied(square):
    for piece in non_agent_pieces:
        if piece.row    == square[0] and \
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
                        adj_squares.append( (row, column ) )
    return adj_squares

def move_piece_to_square(piece, square):
    # each square is a tuple (row, column)
    piece.row = square[0]
    piece.column = square[1]
    board.placepiece(piece)

def move_piece_rand_adj(piece):
    adj_squares = get_adj_squares(piece)
    if len(adj_squares) > 0:
        move_piece_to_square(piece, choice(adj_squares))

def push_blue_block():
    move_piece_rand_adj(blue_block)

def push_red_block():
    move_piece_rand_adj(red_block)

def press_blue_block():
    turn_on(music)

def press_red_block():
    turn_off(music)

def kick_ball():
    move_piece_to_piece(ball, marker)
    if on_same_cell(ball, bell):
        turn_on(bell_sound)
        move_piece_rand_adj(bell)

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
        'move_marker_to_eye',
        'flick_switch_option'
        ]

def is_block(piece):
    return piece in [blue_block]

def get_actions_from_pieces():
    actions = []
    if on_same_cell(eye, hand):
        for piece in non_agent_pieces:
            if on_same_cell(piece, eye):
                if not ( is_block(piece) and is_off(light) ):
                    actions += piece.get_actions()
    return actions

def same_cell_to_tuple(ag_piece):
    same_cell = ()
    for piece in non_agent_pieces:
        if on_same_cell(piece, ag_piece):
            if ( is_block(piece) and is_off(light) ):
                same_cell += ('gray_block',)
            else:
                same_cell += (piece.name,)
    return same_cell

def is_salient_event():
    for variable in environment_variables:
        # If the variable step is equal to the current step, it means
        # the variable state was changed
        if variable['step'] == step:
            return True

    return False

def update_state():
    global state

    under_eye = same_cell_to_tuple(eye)
    under_hand = same_cell_to_tuple(hand)
    under_marker = same_cell_to_tuple(marker)

    light_status = light['state']
    music_status = music['state']

    state = (under_eye, under_hand, under_marker,
             light_status, music_status)

    return state

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
        global step
        step += 1
        update_screen()

    if event.keysym == 'H':
        if move_eye_to_hand_button['state'] == 'normal':
            move_eye_to_hand_click()
    if event.keysym == 'M':
        if move_eye_to_marker_button['state'] == 'normal':
            move_eye_to_marker_click()
    if event.keysym == 'O':
        if move_eye_to_random_object_button['state'] == 'normal':
            move_eye_to_random_object_click()
    if event.keysym == 'E':
        if move_hand_to_eye_button['state'] == 'normal':
            move_hand_to_eye_click()
    if event.keysym == 'w':
        if move_marker_to_eye_button['state'] == 'normal':
            move_marker_to_eye_click()
    if event.keysym == 'k':
        if kick_ball_button['state'] == 'normal':
            kick_ball_click()
    if event.keysym == 'b':
        if press_blue_block_button['state'] == 'normal':
            press_blue_block_click()
    if event.keysym == 'B':
        if push_blue_block_button['state'] == 'normal':
            push_blue_block_click()
    if event.keysym == 'r':
        if press_red_block_button['state'] == 'normal':
            press_red_block_click()
    if event.keysym == 'R':
        if push_red_block_button['state'] == 'normal':
            push_red_block_click()
    if event.keysym == 'f':
        if flick_switch_button['state'] == 'normal':
            flick_switch_click()
    if event.keysym == 'p':
        adj_squares = get_adj_squares(eye)
        print 'entrei'
        for adj_square in adj_squares:
            print adj_square
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
    if event.keysym == 't':
        update_toy_monkey_sound_state()
    if event.keysym == 'u':
        print 'State:'
        print str(update_state())

    update_screen()

def update_environment_variables():
    for variable in environment_variables:
        variable['update_function']()

def update_environment_labels():
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

    state_label_text.set('State: [eye:'    + str(state[0]) +'], ' +
                                '[hand:'   + str(state[1]) +'], ' +
                                '[marker:' + str(state[2]) +']')

def update_blocks_color():
    if is_on(light):
        blue_block.set_image(tk.PhotoImage(file="img/blue_block.gif"))
        board.updatepieceimage(blue_block)

        # red_block.set_image(tk.PhotoImage(file="img/red_block.gif"))
        # board.updatepieceimage(red_block)
    elif is_off(light):
        blue_block.set_image(tk.PhotoImage(file="img/gray_block.gif"))
        board.updatepieceimage(blue_block)

        # red_block.set_image(tk.PhotoImage(file="img/gray_block.gif"))
        # board.updatepieceimage(red_block)
    board.canvas.tag_raise('hand')
    board.canvas.tag_raise('eye')
    board.canvas.tag_raise('marker')

def update_screen():
    update_state()
    update_environment_variables()
    update_environment_labels()
    update_blocks_color()
    update_action_buttons_state()
    # root.update_idletasks()

def create_test_buttons():
    test_buttons_frame = tk.Frame(right_frame)
    test_buttons_frame.pack(side=tk.TOP)

    separator = tk.Frame(right_frame, height=5, bd=1)#, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=5, pady=5)

    global imrl_button

    imrl_button = tk.Button(test_buttons_frame, text='imrl',
                            fg="white", bg="blue", command=imrl)
    imrl_button.pack(side=tk.TOP)

    global random_actions_button
    random_actions_button = tk.Button(test_buttons_frame, text='random_actions', fg="white", bg="blue", command=random_actions)
    random_actions_button.pack(side=tk.TOP)

    global set_random_initial_state_button
    set_random_initial_state_button = tk.Button(test_buttons_frame, text='set_random_initial_state', fg="white", bg="blue", command=set_random_initial_state)
    set_random_initial_state_button.pack(side=tk.TOP)

    global q_learning_simple_button
    q_learning_simple_button = tk.Button(test_buttons_frame, text='q_learning_simple', fg="white", bg="blue", command=q_learning_simple)
    q_learning_simple_button.pack(side=tk.TOP)

    global position_pieces_like_article_button
    position_pieces_like_article_button = tk.Button(test_buttons_frame, text='position_pieces_like_article', fg="white", bg="blue", command=position_pieces_like_article)
    position_pieces_like_article_button.pack(side=tk.TOP)

def create_action_buttons():
    action_buttons_frame = tk.Frame(right_frame)
    action_buttons_frame.pack(side=tk.TOP)

    # Agent
    global move_eye_one_step_north_button
    move_eye_one_step_north_button = tk.Button(action_buttons_frame, text='move_eye_one_step_north (Up)', command=move_eye_one_step_north_click)
    move_eye_one_step_north_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_one_step_north_button)

    global move_eye_one_step_south_button
    move_eye_one_step_south_button = tk.Button(action_buttons_frame, text='move_eye_one_step_south (Down)', command=move_eye_one_step_south_click)
    move_eye_one_step_south_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_one_step_south_button)

    global move_eye_one_step_east_button
    move_eye_one_step_east_button = tk.Button(action_buttons_frame, text='move_eye_one_step_east (Right)', command=move_eye_one_step_east_click)
    move_eye_one_step_east_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_one_step_east_button)

    global move_eye_one_step_west_button
    move_eye_one_step_west_button = tk.Button(action_buttons_frame, text='move_eye_one_step_west (Left)', command=move_eye_one_step_west_click)
    move_eye_one_step_west_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_one_step_west_button)

    global move_eye_to_marker_button
    move_eye_to_marker_button = tk.Button(action_buttons_frame, text='move_eye_to_marker (M)', command=move_eye_to_marker_click)
    move_eye_to_marker_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_to_marker_button)

    global move_eye_to_hand_button
    move_eye_to_hand_button = tk.Button(action_buttons_frame, text='move_eye_to_hand (H)', command=move_eye_to_hand_click)
    move_eye_to_hand_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_to_hand_button)

    global move_eye_to_random_object_button
    move_eye_to_random_object_button = tk.Button(action_buttons_frame, text='move_eye_to_random_object (O)', command=move_eye_to_random_object_click)
    move_eye_to_random_object_button.pack(side=tk.TOP)
    action_buttons.append(move_eye_to_random_object_button)

    global move_hand_to_eye_button
    move_hand_to_eye_button = tk.Button(action_buttons_frame, text='move_hand_to_eye (E)', command=move_hand_to_eye_click)
    move_hand_to_eye_button.pack(side=tk.TOP)
    action_buttons.append(move_hand_to_eye_button)

    global move_marker_to_eye_button
    move_marker_to_eye_button = tk.Button(action_buttons_frame, text='move_marker_to_eye (w)', command=move_marker_to_eye_click)
    move_marker_to_eye_button.pack(side=tk.TOP)
    action_buttons.append(move_marker_to_eye_button)

    global kick_ball_button
    kick_ball_button = tk.Button(action_buttons_frame, text='kick_ball (k)', command=kick_ball_click)
    kick_ball_button.pack(side=tk.TOP)
    action_buttons.append(kick_ball_button)

    global press_blue_block_button
    press_blue_block_button = tk.Button(action_buttons_frame, text='press_blue_block (b)', command=press_blue_block_click)
    press_blue_block_button.pack(side=tk.TOP)
    action_buttons.append(press_blue_block_button)

    global push_blue_block_button
    push_blue_block_button = tk.Button(action_buttons_frame, text='push_blue_block (B)', command=push_blue_block_click)
    push_blue_block_button.pack(side=tk.TOP)
    action_buttons.append(push_blue_block_button)

    global press_red_block_button
    press_red_block_button = tk.Button(action_buttons_frame, text='press_red_block (r)', command=press_red_block_click)
    press_red_block_button.pack(side=tk.TOP)
    action_buttons.append(press_red_block_button)

    global push_red_block_button
    push_red_block_button = tk.Button(action_buttons_frame, text='push_red_block (R)', command=push_red_block_click)
    push_red_block_button.pack(side=tk.TOP)
    action_buttons.append(push_red_block_button)

    global flick_switch_button
    flick_switch_button = tk.Button(action_buttons_frame, text='flick_switch (f)', command=flick_switch_click)
    flick_switch_button.pack(side=tk.TOP)
    action_buttons.append(flick_switch_button)

    global flick_switch_option_button
    flick_switch_option_button = tk.Button(action_buttons_frame, text='flick_switch_option ', command=flick_switch_option_click)
    flick_switch_option_button.pack(side=tk.TOP)
    action_buttons.append(flick_switch_option_button)

def update_available_actions():
    global available_actions

    available_actions = get_available_actions()

def get_available_actions():
    return get_actions_from_agent() + get_actions_from_pieces()

def execute_action(action):
    all_possible_actions[action]()

def update_action_buttons_state():
    update_available_actions()
    for button in action_buttons:
        # Remove keyboard shortcut hint before searching
        function_name = button['text'][:button['text'].find(' ')]
        if function_name in available_actions:
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

def move_eye_one_step_north_click():
    global step

    move_eye_one_step_north()
    step += 1
    update_screen()

def move_eye_one_step_south_click():
    global step

    move_eye_one_step_south()
    step += 1
    update_screen()

def move_eye_one_step_east_click():
    global step

    move_eye_one_step_east()
    step += 1
    update_screen()

def move_eye_one_step_west_click():
    global step

    move_eye_one_step_west()
    step += 1
    update_screen()

def move_eye_to_hand_click():
    global step

    move_eye_to_hand()
    step += 1
    update_screen()

def move_eye_to_marker_click():
    global step

    move_eye_to_marker()
    step += 1
    update_screen()

def move_eye_to_random_object_click():
    global step

    move_eye_to_random_object()
    step += 1
    update_screen()

def move_hand_to_eye_click():
    global step

    move_hand_to_eye()
    step += 1
    update_screen()

def move_marker_to_eye_click():
    global step

    move_marker_to_eye()
    step += 1
    update_screen()

def kick_ball_click():
    global step

    kick_ball()
    step += 1
    update_screen()

def press_blue_block_click():
    global step

    press_blue_block()
    step += 1
    update_screen()

def push_blue_block_click():
    global step

    push_blue_block()
    step += 1
    update_screen()

def press_red_block_click():
    global step

    press_red_block()
    step += 1
    update_screen()

def push_red_block_click():
    global step

    push_red_block()
    step += 1
    update_screen()

def flick_switch_click():
    global step

    flick_switch()
    step += 1
    update_screen()

def flick_switch_option_click():
    global step

    flick_switch_option()
    step += 1
    update_screen()

##############
# Q-Learning #
##############
Q = {}
Q_default_value = 0.0
Vx = {}

Q_flick_switch = loadobject('flick_switch_option.q')

def fix_Q(my_Q, state_key, action_key):
    if not (state_key in my_Q.keys()):
        my_Q[state_key] = {}

    if not (action_key in my_Q[state_key].keys()):
        my_Q[state_key][action_key] = Q_default_value

def set_Q(my_Q, state_key, action_key, new_value):
    fix_Q(my_Q, state_key, action_key)

    my_Q[state_key][action_key] = new_value

def get_Q(my_Q, state_key, action_key):
    fix_Q(my_Q, state_key, action_key)

    return my_Q[state_key][action_key]

# Vx refers to V^*
def fix_Vx(state_key):
    if not (state_key in Vx.keys()):
        Vx[state_key] = Q_default_value

# Vx refers to V^*
def set_Vx(state_key, new_max):
    fix_Vx(state_key)

    Vx[state_key] = new_max

# Vx refers to V^*
def get_Vx(state_key):
    fix_Vx(state_key)

    return Vx[state_key]

def state_is_goal():
    return is_on(music)

def select_random_action():
    update_available_actions()

    return choice(available_actions)

def select_best_actions(my_Q, my_state):
    update_available_actions()

    best_value = 0
    best_actions = []
    for action in available_actions:
        Q_value = get_Q(my_Q, my_state, action)
        if Q_value >= best_value:
            if Q_value > best_value:
                best_value = Q_value
                del best_actions[:]; best_actions = []

            best_actions.append(action)

    return best_actions

def select_best_action(my_Q, my_state):
    return choice(select_best_actions(my_Q, my_state))

def set_random_initial_state():
    board_squares = list(product(range(5), range(5)))
    for piece in all_pieces:
        board_square = choice(board_squares) # each board square is a tuple (row, column)

        piece.row = board_square[0] # the first position of the tuple
        piece.column = board_square[1]

        board.placepiece(piece)

def alpha_sum(x, y, alpha):
    return (1 - alpha) * x + alpha * y

def position_pieces_like_article():
    # ball.row = 1
    # ball.column = 0

    # bell.row = 1
    # bell.column = 4

    blue_block.row = 4
    blue_block.column = 0

    # red_block.row = 4
    # red_block.column = 4

    switch.row = 2
    switch.column = 2

    # toy_monkey.row = 1
    # toy_monkey.column = 2

    hand.row = 0
    hand.column = 3

    eye.row = 1
    eye.column = 3

    marker.row = 2
    marker.column = 4

    for piece in all_pieces:
        board.placepiece(piece)

def setup_new_episode():
    light['state'] = 'OFF'
    light['step'] = -1

    music['state'] = 'OFF'
    music['step'] = -1

    bell_sound['state'] = 'OFF'
    bell_sound['step'] = -1

    toy_monkey_sound['state'] = 'OFF'
    toy_monkey_sound['step'] = -1

    position_pieces_like_article()

    step = 0

def get_reward():
    if state_is_goal():
        return 1
    else:
        return 0

def print_Q(Q):
    for x in Q:
        print (x)
        for y in Q[x]:
            print (y,':',Q[x][y])
        print

def get_log_filename():
    now_str = str(datetime.now())
    filename = 'logs/' + now_str.replace(':', '-')[:19].replace(' ', '_') + '.log'
    return filename

def git_commit_and_tag(text):
    from subprocess import call

    call(['git', 'commit', '-a', '-m', text])
    call(['git', 'tag', text])

def map_state(old_state):
    # Remove 'gray_block' from state description
    # Get only the first 3 positions (eye, hand, marker)
    new_state = ()
    for under_thing in old_state[:3]:
        new_under_thing = ()
        for thing in under_thing:
            if not ( thing in ['gray_block', 'blue_block'] ):
                new_under_thing += (thing,)
        new_state += (new_under_thing,)
    return new_state

def q_learning_simple():
    global step

    # Saves resources
    board.update_screen = False

    # Learning parameters
    alpha            = 0.9
    gamma            = 0.9
    epsilon          = 0.1
    epsilonIncrement = 0.0

    episodes = 10000
    steps = 100

    # Log stuff
    filename = get_log_filename()
    print 'Logging to: ' + filename

    # Git: commit (if that is the case) and tag (always succeed),
    # using the experiment's log filename. This way it is possible to
    # track the version that generated each result
    git_commit_and_tag(filename[5:])

    # "global_step_count" is used to keep track of the total number of
    # steps. The global variable "step" is reset at the beginning of
    # each episode
    global_step_count = 0
    for episode in range(episodes):
        setup_new_episode()
        update_state()
        start_step = global_step_count
        current_option = None
        reached_goal = 'n'
        for current_step in range(steps):
            update_environment_variables()

            # if a goal state is reached the episode ends
            if state_is_goal():
                break

            # The option is followed in a full greedy manner, although
            # there is a probability of stopping the use of the option
            if current_option == 'flick_switch_option':
                # option stops its execution with fixed probability
                if is_off(light):
                    a = select_best_action(Q_flick_switch,
                                           map_state(state))
                else:
                    current_option = None

            # This test has to be made as the option may have just be
            # abandoned on the previous "if"
            if current_option == None:
                # Following epsilon-greedy strategy, Select an action a
                # and execute it. Receive immediate reward r. Observe the
                # new state s2
                if random() < epsilon:    # random() gives a number in the interval [0, 1).
                    # random
                    a = select_random_action()
                else:
                    # greedy
                    a = select_best_action(Q, state)

                # Tests if the selected action is an option
                if a == 'flick_switch_option':
                    current_option = a

            s = state                     # the current state

            execute_action(a)
            update_state()

            s2 = state                    # the new state, after the execution of the action
            r = get_reward()

            Q_s_a_old = get_Q(Q, s, a)   # current (will be the "old" one when updating Q) value of Q(s,a)

            # Makes sure that the goal is an absorbing state: if the
            # reward received is greater than zero the agent must have
            # reached the goal state (rewards are only awarded when
            # the agent reaches the goal)
            if r > 0:
                Vx_s2 = 0
            else:
                Vx_s2 = get_Vx(s2)

            # Update the table entry for Q(s,a)
            Q_s_a_new = (1.0 - alpha) * Q_s_a_old + \
                               alpha  * (r + gamma * Vx_s2)
            set_Q(Q, s, a, Q_s_a_new)

            if Q_s_a_new > get_Vx(s):
                set_Vx(s, Q_s_a_new)

            ##########
            # OPTION #
            ##########
            if current_option == 'flick_switch_option':
                # Update the table entry for Q(s, flick_switch_option)
                Q_s_o_old = get_Q(Q, s, current_option)

                # Goal is an absorbing state
                if r > 0:
                    Q_s2_o = 0
                else:
                    Q_s2_o = get_Q(Q, s2, current_option)

                Q_s_o_new = (1.0 - alpha) * Q_s_o_old + \
                                   alpha  * (r + gamma * Q_s2_o)

                set_Q(Q, s, current_option, Q_s_o_new)

            step += 1
            global_step_count += 1

        if state_is_goal():
            reached_goal = 'y'

        # Here an episode just ended
        episode_number = episode
        end_step = global_step_count - 1
        duration = end_step - start_step + 1

        f = open(filename, 'a')
        f.write(str(episode_number) + '\t' + \
                str(start_step) + '\t' + \
                str(end_step) + '\t' + \
                str(duration) + '\t' + \
                reached_goal + '\n')
        f.close()

        epsilon = epsilon + epsilonIncrement
    print_Q(Q)

    # Returns to original configuration
    board.update_screen = True

############
# Playroom #
############
O = {}

def fix_1dic(dic, key):
    """ Fixes a one-dimension dictionary: receives a key and, if the
    entry does not exist in the dictionary, creates it initializing
    with zero"""

    if not (key in dic.keys()):
        dic[key] = 0

def fix_2dic(dic, key1, key2):
    """ Fixes a two-dimension dictionary: receives the keys and, if
    the entry does not exist in the dictionary, creates it
    initializing with zero"""

    if not (key1 in dic.keys()):
        dic[key1] = {}

    fix_1dic(dic[key1], key2)

def set_1dic(dic, key, new_value):
    """Sets the value of a one-dimensional dictionary entry"""

    fix_1dic(dic, key)

    dic[key] = new_value

def set_2dic(dic, key1, key2, new_value):
    """Sets the value of a two-dimensional dictionary entry"""

    fix_2dic(dic, key1, key2)

    dic[key1][key2] = new_value

def get_1dic(dic, key):
    """Gets the value of a one-dimensional dictionary entry. If the
    entry does not exist, creates it with a value of zero."""

    fix_1dic(dic, key)

    return dic[key]

def get_2dic(dic, key1, key2):
    """Gets the value of a two-dimensional dictionary entry. If the
    entry does not exist, creates it with a value of zero."""

    fix_2dic(dic, key1, key2)

    return dic[key1][key2]

def fix_O(my_O, salient_event):
    if not (salient_event in my_O.keys()):
        # Creates an entry to the option
        my_O[salient_event] = {}

        # Creates an entry to the option's Q-table
        my_O[salient_event]['Q'] = {}

        # Creates an entry to the option's initiation set
        my_O[salient_event]['I'] = []

        # Creates an entry to the option's Beta function
        my_O[salient_event]['BETA'] = {}

        # Creates an entry to the option's Reward function
        my_O[salient_event]['R'] = {}

        # Creates an entry to the option's transition probability
        # model
        my_O[salient_event]['P'] = {}

def get_I(my_O, salient_event):
    return my_O[salient_event]['I']

def add_I(my_O, salient_event, s):
    if not (s in get_I(my_O, salient_event)):
        my_O[salient_event]['I'].append(s)

def set_BETA(my_O, salient_event, s, new_value):
    set_1dic(my_O[salient_event]['BETA'], s, new_value)

def get_BETA(my_O, salient_event, s):
    return get_1dic(my_O[salient_event]['BETA'], s)

def set_P(my_O, salient_event, s2, s, new_value):
    set_2dic(my_O[salient_event]['P'], s2, s, new_value)

def get_P(my_O, salient_event, s2, s):
    return get_2dic(my_O[salient_event]['P'], s2, s)

def delta(a, b):
    if a == b:
        return 1
    else:
        return 0

def imrl():
    global step

    # Saves resources
    board.update_screen = False

    # Learning parameters
    alpha            = 0.9
    gamma            = 0.9
    epsilon          = 0.1
    epsilonIncrement = 0.0

    # imrl parameters
    tau = 0.9

    episodes = 10000
    steps = 100

    # Log stuff
    filename = get_log_filename()
    print 'Logging to: ' + filename

    # Git: commit (if that is the case) and tag (always succeed),
    # using the experiment's log filename. This way it is possible to
    # track the version that generated each result
    git_commit_and_tag(filename[5:])

    # "global_step_count" is used to keep track of the total number of
    # steps. The global variable "step" is reset at the beginning of
    # each episode
    global_step_count = 0
    for episode in range(episodes):
        setup_new_episode()
        update_state()
        start_step = global_step_count
        current_option = None
        reached_goal = 'n'
        for current_step in range(steps):
            update_environment_variables()

            # if a goal state is reached the episode ends
            if state_is_goal():
                break

            # The option is followed in a full greedy manner, although
            # there is a probability of stopping the use of the option
            if current_option == 'flick_switch_option':
                # option stops its execution with fixed probability
                if is_off(light):
                    a = select_best_action(Q_flick_switch,
                                           map_state(state))
                else:
                    current_option = None

            # This test has to be made as the option may have just be
            # abandoned on the previous "if"
            if current_option == None:
                # Following epsilon-greedy strategy, Select an action a
                # and execute it. Receive immediate reward r. Observe the
                # new state s2
                if random() < epsilon:    # random() gives a number in the interval [0, 1).
                    # random
                    a = select_random_action()
                else:
                    # greedy
                    a = select_best_action(Q, state)

                # Tests if the selected action is an option
                if a == 'flick_switch_option':
                    current_option = a

            s = state                     # the current state

            execute_action(a)
            update_state()

            s2 = state                    # the new state, after the execution of the action
            r = get_reward()

            # Deal with special case if next state is salient
            if is_salient_event():        # If s_{t+1} is a salient event e
                salient_event = state[3:]

                # print '=============================================='
                # print 'a: ' + a
                # print 'old state: ' + str(s)
                # print 'new state: ' + str(s2)
                # print 'salient_event: ' + str(salient_event)
                # print '=============================================='

                # If option for e, o_e , does not exist in O (skill-KB)
                if not (salient_event in O.keys()): 
                    # Create option o_e in skill-KB;
                    fix_O(O, salient_event)

                    # Add s_t to I^{o_e} // initialize initiation set
                    add_I(O, salient_event, s)

                    # Set β^{o_e}(s_{t+1}) = 1 // set termination probability
                    set_BETA(O, salient_event, s2, 1)

                # //— set intrinsic reward value
                r_i2 = tau * ( 1 - get_P(O, salient_event, s2, s) )
            else:
                r_i2 = 0

            # //- Update all option models
            for salient_event in O.keys(): # For each option o = o_e in skill-KB (O)
                # Here the salient event being there means the option
                # has been already created

                if s2 in get_I(O, salient_event):
                    # If s_{t+1} ∈ I^o , then add s_t to I^o // grow
                    # initiation set
                    add_I(O, salient_event, s)

                # If a_t is greedy action for o in state s_t
                if a in select_best_actions(O[salient_event]['Q'], s):
                    # //— update option transition probability model
                    # for each state reachable by the option
                    for x in get_I(O, salient_event):
                        # arg1
                        arg1 = get_P(O, salient_event, s2, s)

                        # arg2
                        beta_s2 = get_BETA(O, salient_event, s2)
                        p_x_s2 = get_P(O, salient_event, x, s2)
                        arg2 = gamma * ( 1 - beta_s2 ) * p_x_s2 + \
                               gamma * beta_s2 * delta(s2, x)

                        # gets the alpha sum (as described in the
                        # article)
                        new_p = alpha_sum(arg1, arg2, alpha)

                        # sets the new value
                        set_P(O, salient_event, x, s, new_p)
                    
            Q_s_a_old = get_Q(Q, s, a)   # current (will be the "old" one when updating Q) value of Q(s,a)

            # Makes sure that the goal is an absorbing state: if the
            # reward received is greater than zero the agent must have
            # reached the goal state (rewards are only awarded when
            # the agent reaches the goal)
            if r > 0:
                Vx_s2 = 0
            else:
                Vx_s2 = get_Vx(s2)

            # Update the table entry for Q(s,a)
            Q_s_a_new = (1.0 - alpha) * Q_s_a_old + \
                               alpha  * (r + gamma * Vx_s2)
            set_Q(Q, s, a, Q_s_a_new)

            if Q_s_a_new > get_Vx(s):
                set_Vx(s, Q_s_a_new)

            ##########
            # OPTION #
            ##########
            if current_option == 'flick_switch_option':
                # Update the table entry for Q(s, flick_switch_option)
                Q_s_o_old = get_Q(Q, s, current_option)

                # Goal is an absorbing state
                if r > 0:
                    Q_s2_o = 0
                else:
                    Q_s2_o = get_Q(Q, s2, current_option)

                Q_s_o_new = (1.0 - alpha) * Q_s_o_old + \
                                   alpha  * (r + gamma * Q_s2_o)

                set_Q(Q, s, current_option, Q_s_o_new)

            step += 1
            global_step_count += 1

        if state_is_goal():
            reached_goal = 'y'

        # Here an episode just ended
        episode_number = episode
        end_step = global_step_count - 1
        duration = end_step - start_step + 1

        f = open(filename, 'a')
        f.write(str(episode_number) + '\t' + \
                str(start_step) + '\t' + \
                str(end_step) + '\t' + \
                str(duration) + '\t' + \
                reached_goal + '\n')
        f.close()

        epsilon = epsilon + epsilonIncrement
    print_Q(Q)

    # Returns to original configuration
    board.update_screen = True

root = tk.Tk()

########################################################
# Status Frame and Lables (Enviroment characteristics) #
########################################################
env_charact_frame = tk.Frame(root)
env_charact_frame.pack(side = tk.TOP)

light_label_text = tk.StringVar()
light_label_image_on = tk.PhotoImage(file='img/labels/light_on.gif')
light_label_image_off = tk.PhotoImage(file='img/labels/light_off.gif')
light_label_images = {'ON':light_label_image_on, 'OFF':light_label_image_off}
light_label = tk.Label( env_charact_frame, textvariable=light_label_text, relief=tk.RAISED, borderwidth=4, image = light_label_image_on )
light_label.pack(side = tk.LEFT)

bell_sound_label_text = tk.StringVar()
bell_sound_label_image_on = tk.PhotoImage(file='img/labels/bell_on.gif')
bell_sound_label_image_off = tk.PhotoImage(file='img/labels/bell_off.gif')
bell_sound_label_images = {'ON':bell_sound_label_image_on, 'OFF':bell_sound_label_image_off}
bell_sound_label = tk.Label( env_charact_frame, textvariable=bell_sound_label_text, relief=tk.RAISED, borderwidth=4 )
bell_sound_label.pack(side = tk.LEFT)

music_label_text = tk.StringVar()
music_label_image_on = tk.PhotoImage(file='img/labels/music_on.gif')
music_label_image_off = tk.PhotoImage(file='img/labels/music_off.gif')
music_label_images = {'ON':music_label_image_on, 'OFF':music_label_image_off}
music_label = tk.Label( env_charact_frame, textvariable=music_label_text, relief=tk.RAISED, borderwidth=4 )
music_label.pack(side = tk.LEFT)

toy_monkey_sound_label_text = tk.StringVar()
toy_monkey_sound_label_image_on = tk.PhotoImage(file='img/labels/toy-monkey_on.gif')
toy_monkey_sound_label_image_off = tk.PhotoImage(file='img/labels/toy-monkey_off.gif')
toy_monkey_sound_label_images = {'ON':toy_monkey_sound_label_image_on, 'OFF':toy_monkey_sound_label_image_off}
toy_monkey_sound_label = tk.Label( env_charact_frame, textvariable=toy_monkey_sound_label_text, relief=tk.RAISED, borderwidth=4 )
toy_monkey_sound_label.pack(side = tk.LEFT)

step_count_label_text = tk.StringVar()
step_count_label = tk.Label( env_charact_frame, textvariable=step_count_label_text, relief=tk.RAISED, borderwidth=4 )
step_count_label.pack(side = tk.LEFT)

#########################
# State Frame and Lable #
#########################
state_frame = tk.Frame(root)
state_frame.pack(side=tk.TOP)
state_label_text = tk.StringVar()
state_label = tk.Label( state_frame, textvariable=state_label_text, relief=tk.RAISED, borderwidth=4 )
state_label.pack(side=tk.TOP)

##########################
# Board Frame and itself #
##########################
central_frame = tk.Frame(root)
central_frame.pack(side=tk.LEFT)
board = Board(central_frame)
board.pack(side="left", fill="both", expand="true", padx=4, pady=4)

###############
# Right Frame #
###############
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT)

####################
# Non-agent Pieces #
####################
# ball = Piece(name = "ball", image=tk.PhotoImage(file="img/ball.gif"), actions=['kick_ball'])
# bell = Piece(name = "bell", image=tk.PhotoImage(file="img/bell.gif"), row=0, column=1)
blue_block = Piece(name = "blue_block", image = tk.PhotoImage(file="img/blue_block.gif"), row=0, column=4, actions=['press_blue_block', 'push_blue_block'])
# red_block = Piece(name = "red_block", image = tk.PhotoImage(file="img/red_block.gif"), row=1, column=0, actions=['press_red_block', 'push_red_block'])
switch = Piece(name = "switch", image = tk.PhotoImage(file="img/switch.gif"), row=1, column=1, actions=['flick_switch'])
# toy_monkey = Piece(name = "toy_monkey", image = tk.PhotoImage(file="img/toy-monkey.gif"), row=1, column=3)

################
# Agent Pieces #
################
hand = Piece(name = "hand", image = tk.PhotoImage(file="img/hand.gif"), row=0, column=3)
eye = Piece(name = "eye", image = tk.PhotoImage(file="img/eye.gif"), row=0, column=2)
marker = Piece(name = "marker", image = tk.PhotoImage(file="img/target.gif"), row=1, column=2)

################
# Pieces Lists #
################
agent_pieces = [hand, eye, marker]
non_agent_pieces = [switch, blue_block]

all_pieces = agent_pieces + non_agent_pieces

for piece in non_agent_pieces:
    board.addpiece(piece)
for piece in agent_pieces:
    board.addpiece(piece)

state = ()

update_state()

all_possible_actions = {
    'move_eye_to_hand':move_eye_to_hand,
    'move_eye_to_marker':move_eye_to_marker,
    'move_eye_one_step_north':move_eye_one_step_north,
    'move_eye_one_step_south':move_eye_one_step_south,
    'move_eye_one_step_east':move_eye_one_step_east,
    'move_eye_one_step_west':move_eye_one_step_west,
    'move_eye_to_random_object':move_eye_to_random_object,
    'move_hand_to_eye':move_hand_to_eye,
    'move_marker_to_eye':move_marker_to_eye,
    'kick_ball':kick_ball,
    'press_blue_block':press_blue_block,
    'push_red_block':push_red_block,
    'press_red_block':press_red_block,
    'push_blue_block':push_blue_block,
    'flick_switch':flick_switch,
    'flick_switch_option':flick_switch_option,
}

# Buttons mostly used for test purposes
create_test_buttons()

# Each possible primitive action has a button associated to it and
# they are all present in action_buttons, filled in
# create_action_buttons
action_buttons = []
create_action_buttons()

# Filled in update_available_actions
available_actions = []

update_environment_labels()

# Associate keys to buttons
root.bind_all('<Key>', key)

update_screen()

root.mainloop()
