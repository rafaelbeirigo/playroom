#!/usr/bin/python
# coding=UTF-8

import sys
import pickle
from Board import *
from Piece import *
from random import randint
from random import random
from random import choice
from time import sleep
from itertools import product


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
light = {'state': 'OFF', 'step': -1, 'update_function': update_light_state, 'name': 'light'}
music = {'state': 'OFF', 'step': -1, 'update_function': update_music_state, 'name': 'music'}
bell_sound = {'state': 'OFF', 'step': -1, 'update_function': update_bell_sound_state, 'name': 'bell_sound'}
toy_monkey_sound = {'state': 'OFF', 'step': -1, 'update_function': \
                    update_toy_monkey_sound_state, 'name': 'toy_monkey_sound'}
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


def turn_bell_off():
    if is_on(bell_sound):
        bell_sound['state'] = 'OFF'


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
    move_piece_to_cell(piece, square[0], square[1])
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
        'move_eye_to_random_object',
        'move_hand_to_eye',
        'move_marker_to_eye',
        ]


def is_block(piece):
    return piece in [blue_block, red_block]


def get_actions_from_pieces():
    actions = []
    if on_same_cell(eye, hand):
        for piece in get_pieces_on_cell(eye.row, eye.column):
            if not ( is_block(piece) and is_off(light) ):
                actions += piece.get_actions()
    return actions


def same_cell_to_tuple(ag_piece):
    same_cell = ()
    for piece in get_pieces_on_cell(ag_piece.row, ag_piece.column):
        if not ( piece in agent_pieces ):
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


def which_salient_event():
    """Returns which salient event ocurred at the current step."""

    s_e = ''
    for variable in environment_variables:
        if variable['step'] == step:
            s_e += variable['name'] + '_' + variable['state'] + ';'

    return s_e


def log_r_i(r_i, s, s2, o, a):
    """Logs the r_i received at the current step."""

    global r_i_filename

    if r_i_filename == None:    # Tests if it is the first time the file will be opened
        r_i_filename = get_log_filename(prefix='r_i-')

    f = open(r_i_filename, 'a')
    f.write(str(step) + '\t' + \
            str(r_i) + '\t' + \
            which_salient_event() + '\t' + \
            str(s) + '\t' + \
            str(s2) + '\t' + \
            str(o) + '\t' + \
            str(a) + '\n'
    )
    f.close()


def update_state():
    global state

    under_eye = same_cell_to_tuple(eye)
    under_hand = same_cell_to_tuple(hand)
    under_marker = same_cell_to_tuple(marker)

    light_status = light['state']
    music_status = music['state']
    bell_sound_status = bell_sound['state']
    toy_monkey_sound_status = toy_monkey_sound['state']

    state = (under_eye, under_hand, under_marker,
             light_status, music_status, bell_sound_status, toy_monkey_sound_status)

    return state


def move_piece_to_piece(piece_to_move, destination_piece):
    move_piece_to_cell(piece_to_move, destination_piece.row, destination_piece.column)
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
    new_row = piece.row
    new_col = piece.column
    if direction == 'north':
        new_row -= 1
    elif direction == 'south':
        new_row += 1
    elif direction == 'east':
        new_col += 1
    elif direction == 'west':
        new_col -= 1

    if new_row < 0:
        new_row = 0
    if new_row > board.rows - 1:
        new_row = board.rows - 1
    if new_col < 0:
        new_col = 0
    if new_col > board.columns - 1:
        new_col = board.columns - 1

    move_piece_to_cell(piece, new_row, new_col)
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
    if event.keysym == '0':
        print 'pieces_on_cell {eye}:'
        for my_piece in pieces_on_cell[eye.row][eye.column]:
            print my_piece.name

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

        red_block.set_image(tk.PhotoImage(file="img/red_block.gif"))
        board.updatepieceimage(red_block)
    elif is_off(light):
        blue_block.set_image(tk.PhotoImage(file="img/gray_block.gif"))
        board.updatepieceimage(blue_block)

        red_block.set_image(tk.PhotoImage(file="img/gray_block.gif"))
        board.updatepieceimage(red_block)
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


def update_available_actions(s=None):
    global available_actions

    available_actions = get_available_actions(s)


def get_available_actions(s=None):
    if s == None:
        return get_actions_from_agent() + get_actions_from_pieces()
    else:
        return get_actions_from_agent() + get_actions_from_pieces() + list(get_available_options(s))


def execute_action(action, s=None):
    if isinstance(action, str):
        all_possible_actions[action]()
    else:                       # it is an option (tuple)
        if s == None:
            print 'ERROR: s was not provided, no action will be executed this step'
            print 'action: ' + str(action)
        else:
            o = action              # the provided action is an option
            a = select_best_action(s, o)
            execute_action(a, s)

    update_toy_monkey_sound_state()


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
Ax = {}

Q_flick_switch = loadobject('flick_switch_option.q')


def which_Q(o=None):
    """Returns the correct Q table depending on the variable o:
    If o is provided, return the Q-table for the option, if it
    is not provided, return the standard Q-table."""

    if o == None:
        return Q
    else:
        return O[o]['Q']


def fix_Q(s, a, o=None):
    fix_2dic(which_Q(o), s, a)


def set_Q(s, a, new_value, o=None):
    fix_Q(s, a, o)

    my_Q = which_Q(o)
    my_Q[s][a] = new_value

    # Deals with V^*(s) and A^*(s)
    q = new_value
    vx = get_Vx(s, o)
    if q > vx:
        # Sets the new best value on V^*(s)
        set_Vx(s, q, o)

        # Clears the list of best actions (a new one will be created)
        clear_Ax(s, o)

        # Adds the action to the list of best actions
        add_Ax(s, a, o)
    elif q > 0.0 and q == vx:
        # Adds the action to the list of best actions
        add_Ax(s, a, o)


def get_Q(s, a, o=None):
    fix_Q(s, a, o)

    my_Q = which_Q(o)
    return my_Q[s][a]


def which_Vx(o=None):
    """Returns the correct Vx depending on the variable o:
    If o is provided, return the Vx for the option, if it is not
    provided, return the standard Vx.
    """

    if o == None:
        return Vx
    else:
        return O[o]['Vx']


# Vx refers to V^*
def fix_Vx(s, o=None):
    fix_1dic(which_Vx(o), s)


# Vx refers to V^*
def set_Vx(s, new_max, o=None):
    my_Vx = which_Vx(o)
    my_Vx[s] = new_max


# Vx refers to V^*
def get_Vx(s, o=None):
    fix_Vx(s, o)

    my_Vx = which_Vx(o)
    return my_Vx[s]


def state_is_goal():
    return is_on(music)


def is_option(a):
    """Returns true iff a is an option.
    Primitive actions are described by strings and options by tuples."""
    return not(isinstance(a, str))


def select_random_action(s=None):
    update_available_actions(s)
    return choice(available_actions)


def select_best_actions(s, o=None):
    """Returns the best actions to the state 's' according to a 'Q'.
    If 'o' is provided, the 'Q' used is related to the option 'o'."""

    my_Ax = which_Ax(o)

    fix_Ax(s, o)

    if len(my_Ax[s]) == 0:         # there is no best action yet to the state
        return get_available_actions(s)
    else:
        return list(my_Ax[s])


def get_action_from_option(s, o):
    a = choice(select_best_actions(s, o))
    while is_option(a):
        a = select_best_action(s, a)
    return a


def select_best_action(s, o=None):
    return choice(select_best_actions(s, o))


def set_random_initial_state():
    board_squares = list(product(range(5), range(5)))
    for piece in all_pieces:
        board_square = choice(board_squares) # each board square is a tuple (row, column)

        move_piece_to_cell(piece, board_square[0], board_square[1])
        board.placepiece(piece)


def alpha_sum(x, y, alpha):
    return (1.0 - alpha) * x + alpha * y


def position_pieces_like_article():
    move_piece_to_cell(ball, 1, 0)

    move_piece_to_cell(bell, 1, 4)

    move_piece_to_cell(blue_block, 4, 0)

    move_piece_to_cell(red_block, 4, 4)

    move_piece_to_cell(switch, 2, 2)

    move_piece_to_cell(toy_monkey, 1, 2)

    move_piece_to_cell(hand, 0, 3)

    move_piece_to_cell(eye, 1, 3)

    move_piece_to_cell(marker, 2, 4)


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
        return 1.0
    else:
        return 0.0


def get_r_e():
    """Returns the extrinsic reward."""
    if is_on(toy_monkey_sound):
        return 10.0
    else:
        return 0.0


def print_Q(Q):
    for x in Q:
        print (x)
        for y in Q[x]:
            print (y,':',Q[x][y])
        print


def get_log_filename(prefix='', suffix=''):
    from datetime import datetime
    from socket import gethostname

    hostname = gethostname()
    now_str = str(datetime.now())
    filename = 'logs/' + prefix + now_str.replace(':', '-')[:19].replace(' ', '_') + suffix + '-' + hostname + '.log'

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
            if r > 0.0:
                Vx_s2 = 0.0
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
                if r > 0.0:
                    Q_s2_o = 0.0
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
S = set()
pieces_on_cell = {}
available_options = {}
r_i_filename = None

def fix_1dic(dic, key):
    """ Fixes a one-dimension dictionary: receives a key and, if the
    entry does not exist in the dictionary, creates it initializing
    with zero"""

    try:
        dummy = dic[key]
    except KeyError:
        dic[key] = 0.0


def fix_2dic(dic, key1, key2):
    """ Fixes a two-dimension dictionary: receives the keys and, if
    the entry does not exist in the dictionary, creates it
    initializing with zero"""

    try:
        dummy = dic[key1]
    except KeyError:
        dic[key1] = {}

    fix_1dic(dic[key1], key2)


def set_1dic(dic, key, new_value):
    """Sets the value of a one-dimensional dictionary entry"""

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


def fix_O(o):
    try:
        dummy = O[o]
    except KeyError:
        # Creates an entry to the option
        O[o] = {}

        # Creates an entry to the option's Q-table
        O[o]['Q'] = {}

        # Creates an entry to the option's initiation set
        O[o]['I'] = set()

        # Creates an entry to the option's V^*
        O[o]['Vx'] = {}

        # Creates an entry to the option's A^*
        O[o]['Ax'] = {}

        # Creates an entry to the option's Beta function
        O[o]['BETA'] = {}

        # Creates an entry to the option's Reward function
        O[o]['R'] = {}

        # Creates an entry to the option's transition probability
        # model
        O[o]['P'] = {}

        # Creates an entry to the option's terminal value and
        # initialize it.
        O[o]['TV'] = 1.0


def get_I(o):
    return O[o]['I']


def add_I(o, s):
    get_I(o).add(s)

    # Add o to the list of available options in s
    add_available_options(s, o)


def which_Ax(o=None):
    """Returns A^*.  If the option key is provided, the A^* refers to an
    option."""

    if o == None:
        return Ax
    else:
        return O[o]['Ax']


def fix_Ax(s, o=None):
    my_Ax = which_Ax(o)
    try:
        dummy = my_Ax[s]
    except:
        my_Ax[s] = set()


def get_Ax(s, o=None):
    fix_Ax(s, o)
    return which_Ax(o)[s]


def add_Ax(s, a, o=None):
    fix_Ax(s, o)
    which_Ax(o)[s].add(a)


def clear_Ax(s, o=None):
    fix_Ax(s, o)
    which_Ax(o)[s].clear()


def set_BETA(o, s, new_value):
    set_1dic(O[o]['BETA'], s, new_value)


def get_BETA(o, s):
    return get_1dic(O[o]['BETA'], s)


def set_R(o, s, new_value):
    set_1dic(O[o]['R'], s, new_value)


def get_R(o, s):
    return get_1dic(O[o]['R'], s)


def set_P(o, s2, s, new_value):
    set_2dic(O[o]['P'], s2, s, new_value)


def get_P(o, s2, s):
    try:
        return O[o]['P'][s2][s]
    except KeyError:
        return 0


def get_TV(o):
    return O[o]['TV']


def delta(a, b):
    if a == b:
        return 1.0
    else:
        return 0.0


def get_sum_pvx(s, o):
    """Returns the sum used in
    //— SMDP-planning update of behavior action-value function"""

    sum_pvx = 0.0
    for x in S:
        p_x_s = get_P(o, x, s)

        vx = get_Vx(x, o)

        sum_pvx += p_x_s * vx

    return sum_pvx


def get_sum_pvxo(s, o2, o):
    """Returns the sum used in
    //— Update option action-value functions
    Here o2 == o-prime from the article."""

    tv = get_TV(o)
    sum_pvxo = 0.0
    for x in S:
        p_x_s = get_P(o2, x, s)

        bx = get_BETA(o, x)

        vx = get_Vx(x, o)

        sum_pvxo += p_x_s * (bx * tv + (1 - bx) * vx)

    return sum_pvxo


def fix_pieces_on_cell(row, col):
    """Fixes the entry for pieces_on_cell[row][col]: if it does not exist
    yet, creates it with an empty set"""

    fix_2dic(pieces_on_cell, row, col)
    if pieces_on_cell[row][col] == 0.0:
        pieces_on_cell[row][col] = set() # corrects the initialization to put a set on the entry

def add_pieces_on_cell(row, col, piece):
    """Adds the piece to the set correspondig to [row][col]."""

    fix_pieces_on_cell(row, col)
    pieces_on_cell[row][col].add(piece)


def del_pieces_on_cell(row, col, piece):
    """Removes a piece from the set corresponding to [row][col]."""

    fix_pieces_on_cell(row, col)
    pieces_on_cell[row][col].discard(piece)


def get_pieces_on_cell(row, col):
    """Gets a set of the pieces present on [row][col] on the board"""
    fix_pieces_on_cell(row, col)
    return pieces_on_cell[row][col]


def move_piece_to_cell(piece, row, col):
    """Moves a piece to [row][col] on the board and updates pieces_on_cell
    accordingly."""

    del_pieces_on_cell(piece.row, piece.column, piece)
    add_pieces_on_cell(row, col, piece)

    piece.row = row
    piece.column = col


def fix_available_options(s):
    """If the entry does not exist, creates it."""
    try:
        dummy = available_options[s]
    except KeyError:
        available_options[s] = set()


def add_available_options(s, o):
    """Add an option to the set of available options in 's'."""
    fix_available_options(s)
    available_options[s].add(o)


def get_available_options(s):
    """Gets the available options on the state 's'."""
    fix_available_options(s)
    return available_options[s]

def o_exists(o):
    """Tests if there is an entry in O for the option o."""
    try:
        dummy = O[o]
        return True
    except KeyError:
        return False


def imrl():
    global step
    global r_i_filename

    # Saves resources
    board.update_screen = False

    # Learning parameters
    alpha            = 0.1
    gamma            = 0.9
    epsilon          = 0.25
    tau              = 0.9

    steps = int(2.5e5)

    # Log stuff
    r_i_filename = get_log_filename(prefix='r_i-')
    print 'Logging to: ' + r_i_filename

    # Git: commit (if that is the case) and tag (always succeed),
    # using the experiment's log filename. This way it is possible to
    # track the version that generated each result
    git_commit_and_tag(r_i_filename[5:])

    # Variables initialization
    s = update_state()
    S.add(s)
    a = select_random_action()
    r_e = 0.0
    r_i = 0.0
    step = 1
    current_option = None
    for current_step in range(steps):
        # Obtain next state s_{t+1}
        execute_action(a, s)
        s2 = update_state()
        S.add(s2)

        # Deal with special case if next state is salient
        if is_salient_event():        # If s_{t+1} is a salient event e
            o = s2                    # The option is described by the salient state

            # If option for e, o_e , does not exist in O (skill-KB)
            if not (o_exists(o)):
                # Create option o_e in skill-KB;
                fix_O(o)

                # Add s_t to I^{o_e} // initialize initiation set
                add_I(o, s)

                # Set β^{o_e}(s_{t+1}) = 1 // set termination probability
                set_BETA(o, s2, 1.0)

            # //— set intrinsic reward value
            r_i2 = tau * ( 1.0 - get_P(o, s2, s) )

            log_r_i(r_i2, s, s2, current_option, a)
        else:
            r_i2 = 0.0

        # //- Update all option models
        for o in O.keys(): # For each option o = o_e in skill-KB (O)
            # If s_{t+1} ∈ I^o , then add s_t to I^o // grow
            # initiation set
            if s2 in get_I(o):
                add_I(o, s)

            # If a_t is greedy action for o in state s_t
            my_Ax = get_Ax(s, o)
            if len(my_Ax) == 0 or a in my_Ax:
                # //— update option transition probability model
                # for each state reachable by the option
                for x in S:
                    # arg1
                    arg1 = get_P(o, x, s)

                    # arg2
                    beta_s2 = get_BETA(o, s2)
                    p_x_s2 = get_P(o, x, s2)
                    arg2 = gamma * ( 1.0 - beta_s2 ) * p_x_s2 + \
                           gamma * beta_s2 * delta(s2, x)

                    # calculates the new value
                    new_p = alpha_sum(arg1, arg2, alpha)

                    # sets the new value
                    set_P(o, x, s, new_p)

                # //— update option reward model
                # arg1
                arg1 = get_R(o, s)

                # arg2
                beta_s2 = get_BETA(o, s2)
                R_s2 = get_R(o, s2)
                arg2 = r_e + gamma * ((1.0 - beta_s2) * R_s2)

                # calculates the new value
                new_R = alpha_sum(arg1, arg2, alpha)

                # sets the new value
                set_R(o, s, new_R)

        # //— Q-learning update of behavior action-value function
        # arg1
        arg1 = get_Q(s, a)

        # arg2
        arg2 = r_e + r_i + gamma * get_Vx(s2)

        # calculates the new value
        new_Q = alpha_sum(arg1, arg2, alpha)

        # sets the new value
        set_Q(s, a, new_Q)

        # //— SMDP-planning update of behavior action-value function
        for o in O.keys(): # For each option o = o_e in skill-KB (O)
            # calculates arg1
            arg1 = get_Q(s, o)

            # calculates arg2
            arg2 = get_R(o, s) + get_sum_pvx(s, o)

            # calculates the new value
            new_Q = alpha_sum(arg1, arg2, alpha)

            # sets the new value
            set_Q(s, o, new_Q)

        # //— Update option action-value functions
        for o in O.keys(): # For each option o ∈ O such that s_t ∈ I^o
            if s in get_I(o):
                # calculates arg1
                arg1 = get_Q(s, a, o)

                # calculates arg2
                arg2 = r_e + gamma * get_BETA(o, s2) * get_TV(o) \
                           + gamma * (1.0 - get_BETA(o, s2)) * get_Vx(s2, o)

                # calculates the new value
                new_Q = alpha_sum(arg1, arg2, alpha)

                # sets the new value
                set_Q(s, a, new_Q, o)

            for o2 in O.keys(): # For each option o2 ∈ O such that s_t ∈ I^o2 and o != o2
                if (o != o2) and (s in get_I(o2)):
                    # calculates arg1
                    arg1 = get_Q(s, o2, o)

                    # calculates arg2
                    arg2 = get_R(o2, s) + get_sum_pvxo(s, o2, o)

                    # calculates the new value
                    new_Q = alpha_sum(arg1, arg2, alpha)

                    # sets the new value
                    set_Q(s, o2, new_Q, o)

        # Choose a_{t+1} using epsilon-greedy policy w.r.to Q_B // — Choose next action
        # If the option took the agent to a state that isn't in I yet,
        # abandon the option
        if current_option != None:
            if not (s2 in get_I(current_option)):
                current_option = None

        if current_option == None:
            if random() < epsilon:    # random() gives a number in the interval [0, 1).
                # random
                next_action = select_random_action(s2)
            else:
                # greedy
                next_action = select_best_action(s2)
        elif get_BETA(current_option, s2) == 1.0:
            current_option = None # The option will stop being followed
            if random() < epsilon:    # random() gives a number in the interval [0, 1).
                # random
                next_action = select_random_action(s2)
            else:
                # greedy
                next_action = select_best_action(s2)
        else:
            next_action = current_option # continues to follow the option

        if is_option(next_action):
            current_option = next_action
            a2 = get_action_from_option(s2, next_action)
        else:
            current_option = None
            a2 = next_action

        # //— Determine next extrinsic reward
        # Set r^e_{t+1} to the extrinsic reward for transition s_t, a_t → s_{t+1}
        r_e2 = get_r_e()

        # Set st ← st+1 ; at ← at+1 ; r^e_t ← r^e_{t+1} ; r^i_t ← r^i_{t+1}
        s = s2
        a = a2
        r_i = r_i2
        r_e = r_e2
        step += 1

        # Sets bell_sound status
        turn_bell_off()

    saveobject(O, get_log_filename(prefix='O-')) # persists O

    # Returns to original configuration
    board.update_screen = True

    sys.exit()


def main():
    ####################
    # Non-agent Pieces #
    ####################
    global ball
    ball = Piece(name = "ball", actions=['kick_ball'])
    global bell
    bell = Piece(name = "bell", row=0, column=1)
    global blue_block
    blue_block = Piece(name = "blue_block", row=0, column=4, actions=['press_blue_block', 'push_blue_block'])
    global red_block
    red_block = Piece(name = "red_block", row=1, column=0, actions=['press_red_block', 'push_red_block'])
    global switch
    switch = Piece(name = "switch", row=1, column=1, actions=['flick_switch'])
    global toy_monkey
    toy_monkey = Piece(name = "toy_monkey", row=1, column=3)

    ################
    # Agent Pieces #
    ################
    global hand
    hand = Piece(name = "hand", row=0, column=3)
    global eye
    eye = Piece(name = "eye", row=0, column=2)
    global marker
    marker = Piece(name = "marker", row=1, column=2)

    ################
    # Pieces Lists #
    ################
    global agent_pieces
    agent_pieces = [hand, eye, marker]
    global non_agent_pieces
    non_agent_pieces = [switch, blue_block, red_block, ball, bell, toy_monkey]

    global all_pieces
    all_pieces = agent_pieces + non_agent_pieces

    global state
    state = ()

    update_state()

    global all_possible_actions
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
    }

    create_x()

    # Filled in update_available_actions
    global available_actions
    available_actions = []

    update_environment_labels()

    # Associate keys to buttons
    root.bind_all('<Key>', key)

    position_pieces_like_article()

    update_screen()

    root.mainloop()


def create_x():
    """Deals with the graphical part."""
    import Tkinter as tk
    global root
    root = tk.Tk()

    ########################################################
    # Status Frame and Lables (Enviroment characteristics) #
    ########################################################
    global env_charact_frame
    env_charact_frame = tk.Frame(root)
    env_charact_frame.pack(side = tk.TOP)

    global light_label_text
    light_label_text = tk.StringVar()
    global light_label_image_on
    light_label_image_on = tk.PhotoImage(file='img/labels/light_on.gif')
    global light_label_image_off
    light_label_image_off = tk.PhotoImage(file='img/labels/light_off.gif')
    global light_label_images
    light_label_images = {'ON':light_label_image_on, 'OFF':light_label_image_off}
    global light_label
    light_label = tk.Label( env_charact_frame, textvariable=light_label_text, relief=tk.RAISED, borderwidth=4, image = light_label_image_on )
    light_label.pack(side = tk.LEFT)

    global bell_sound_label_text
    bell_sound_label_text = tk.StringVar()
    global bell_sound_label_image_on
    bell_sound_label_image_on = tk.PhotoImage(file='img/labels/bell_on.gif')
    global bell_sound_label_image_off
    bell_sound_label_image_off = tk.PhotoImage(file='img/labels/bell_off.gif')
    global bell_sound_label_images
    bell_sound_label_images = {'ON':bell_sound_label_image_on, 'OFF':bell_sound_label_image_off}
    global bell_sound_label
    bell_sound_label = tk.Label( env_charact_frame, textvariable=bell_sound_label_text, relief=tk.RAISED, borderwidth=4 )
    bell_sound_label.pack(side = tk.LEFT)

    global music_label_text
    music_label_text = tk.StringVar()
    global music_label_image_on
    music_label_image_on = tk.PhotoImage(file='img/labels/music_on.gif')
    global music_label_image_off
    music_label_image_off = tk.PhotoImage(file='img/labels/music_off.gif')
    global music_label_images
    music_label_images = {'ON':music_label_image_on, 'OFF':music_label_image_off}
    global music_label
    music_label = tk.Label( env_charact_frame, textvariable=music_label_text, relief=tk.RAISED, borderwidth=4 )
    music_label.pack(side = tk.LEFT)

    global toy_monkey_sound_label_text
    toy_monkey_sound_label_text = tk.StringVar()
    global toy_monkey_sound_label_image_on
    toy_monkey_sound_label_image_on = tk.PhotoImage(file='img/labels/toy-monkey_on.gif')
    global toy_monkey_sound_label_image_off
    toy_monkey_sound_label_image_off = tk.PhotoImage(file='img/labels/toy-monkey_off.gif')
    global toy_monkey_sound_label_images
    toy_monkey_sound_label_images = {'ON':toy_monkey_sound_label_image_on, 'OFF':toy_monkey_sound_label_image_off}
    global toy_monkey_sound_label
    toy_monkey_sound_label = tk.Label( env_charact_frame, textvariable=toy_monkey_sound_label_text, relief=tk.RAISED, borderwidth=4 )
    toy_monkey_sound_label.pack(side = tk.LEFT)

    global step_count_label_text
    step_count_label_text = tk.StringVar()
    global step_count_label
    step_count_label = tk.Label( env_charact_frame, textvariable=step_count_label_text, relief=tk.RAISED, borderwidth=4 )
    step_count_label.pack(side = tk.LEFT)

    #########################
    # State Frame and Lable #
    #########################
    global state_frame
    state_frame = tk.Frame(root)
    state_frame.pack(side=tk.TOP)
    global state_label_text
    state_label_text = tk.StringVar()
    global state_label
    state_label = tk.Label( state_frame, textvariable=state_label_text, relief=tk.RAISED, borderwidth=4 )
    state_label.pack(side=tk.TOP)

    ##########################
    # Board Frame and itself #
    ##########################
    global central_frame
    central_frame = tk.Frame(root)
    central_frame.pack(side=tk.LEFT)
    global board
    board = Board(central_frame)
    board.pack(side="left", fill="both", expand="true", padx=4, pady=4)

    ###############
    # Right Frame #
    ###############
    global right_frame
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT)

    ####################
    # Non-agent Pieces #
    ####################
    ball.image=tk.PhotoImage(file="img/ball.gif")
    bell.image=tk.PhotoImage(file="img/bell.gif")
    blue_block.image = tk.PhotoImage(file="img/blue_block.gif")
    red_block.image = tk.PhotoImage(file="img/red_block.gif")
    switch.image = tk.PhotoImage(file="img/switch.gif")
    toy_monkey.image = tk.PhotoImage(file="img/toy-monkey.gif")

    ################
    # Agent Pieces #
    ################
    hand.image = tk.PhotoImage(file="img/hand.gif")
    eye.image = tk.PhotoImage(file="img/eye.gif")
    marker.image = tk.PhotoImage(file="img/target.gif")

    ###########################
    # Add pieces to the board #
    ###########################
    for piece in non_agent_pieces:
        board.addpiece(piece)
    for piece in agent_pieces:
        board.addpiece(piece)

    ###########
    # Buttons #
    ###########
    create_test_buttons()

    # Each possible primitive action has a button associated to it and
    # they are all present in action_buttons, filled in
    # create_action_buttons
    global action_buttons
    action_buttons = []
    create_action_buttons()



if __name__ == '__main__':
    main()
