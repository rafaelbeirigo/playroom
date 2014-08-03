#!/usr/bin/python
# coding=UTF-8

import sys
import pickle
from Board import *
from Piece import *
from random import randint
from random import choice
from time import sleep
from itertools import product
import numpy
import scipy
import scipy.sparse
import time

###############
# NumPy stuff #
###############
board_matrix = scipy.zeros((5, 5, 10), dtype=bool)


def allzerobutpos(r, c, s):
    row =  numpy.array([r])
    col =  numpy.array([c])
    data = numpy.array([1.0], dtype=scipy.float32)
    return scipy.sparse.csr_matrix((data, (row,col)), shape=s)


def allzerobutrow(m, r, reposition=None):
    if reposition == None:
        z = allzerobutpos(r, r, m.shape)
    else:
        z = allzerobutpos(reposition, r, m.shape)
    n = z * m
    del z
    return n


def allrowbutzero(m, r):
    n = allzerobutrow(m, r)
    o = m - n
    del n
    return o


def bool2int(x):
    y = 0
    for i,j in enumerate(x):
        if j: y += 1<<i
    return y


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
    update_blocks_bits()

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
            if ( row >= 0 and row < board_rows ):

                # only legal columns
                if ( column >= 0 and column < board_columns ):

                    # not the piece square
                    if ( row_inc != 0 or col_inc != 0 ):
                        adj_squares.append( (row, column ) )
    return adj_squares


def move_piece_to_square(piece, square):
    # each square is a tuple (row, column)
    move_piece_to_cell(piece, square[0], square[1])


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
    actions = [
        'move_eye_to_hand',
        'move_eye_to_marker',
        'move_eye_to_random_object',
        'move_hand_to_eye',
        'move_marker_to_eye',
    ]
    if not args.no_cardinal:
        actions += [
            'move_eye_one_step_north',
            'move_eye_one_step_south',
            'move_eye_one_step_east',
            'move_eye_one_step_west',
        ]
    return actions

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
                same_cell += ('gray_' + piece.name,)
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


def log_step(s2, current_option, a2, r_i2):
    """Logs data every step."""

    global step_filename

    if step_filename == None:    # Tests if it is the first time the file will be opened
        step_filename = get_log_filename(prefix='step-')

    f = open(step_filename, 'a')
    f.write(str(s2) + '\t' + \
            str(current_option) + '\t' + \
            str(a2) + '\t' + \
            str(r_i2) + '\t' + \
            which_salient_event() + '\n'
    )
    f.close()


def log_option_stack():
    """Logs the option stack."""

    global option_stack_filename

    if option_stack_filename == None:    # Tests if it is the first time the file will be opened
        option_stack_filename = get_log_filename(prefix='option_stack-')

    f = open(option_stack_filename, 'a')
    f.write(str(option_stack) + '\n')
    f.close()


def log_time(totaltime):
    """Logs the execution time."""

    time_filename = "logs/time-" + r_i_filename.replace("logs/", "")

    f = open(time_filename, 'a')
    f.write(str(totaltime) + '\n')
    f.close()


def update_state():
    global state

    be = board_matrix[eye.row][eye.column]
    bh = board_matrix[hand.row][hand.column]
    bm = board_matrix[marker.row][marker.column]

    undereye = scipy.concatenate((be[:1], be[2:5]))
    underhand = scipy.concatenate((bh[:1], bh[2:5]))
    undermarker = bm[1:2]

    status = []
    for ev in environment_variables:
        status.append(is_on(ev))

    statea  = scipy.concatenate((undereye, underhand, undermarker, status))
    state = bool2int(statea)

    return state


def move_piece_to_piece(piece_to_move, destination_piece):
    move_piece_to_cell(piece_to_move, destination_piece.row, destination_piece.column)


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
    if new_row > board_rows - 1:
        new_row = board_rows - 1
    if new_col < 0:
        new_col = 0
    if new_col > board_columns - 1:
        new_col = board_columns - 1

    move_piece_to_cell(piece, new_row, new_col)


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

    under_eye = bool2int(board_matrix[eye.row][eye.column][:-3])
    under_hand = bool2int(board_matrix[hand.row][hand.column][:-3])<<7
    under_marker = bool2int(board_matrix[marker.row][marker.column][:-3])<<14

    state_label_text.set('State: ' + str(state) + ' ' +
                                 '([eye:'    + str(under_eye) +'], '
                                 '[hand:'   + str(under_hand) +'], ' +
                                 '[marker:' + str(under_marker) +'])')


def update_blocks_bits():
    """Updates the board_matrix bits related to the blocks according to
    the light state."""
    for piece in [blue_block, red_block]:
        board_matrix[piece.row][piece.column][piece.value] = is_on(light)
        board_matrix[piece.row][piece.column][6] = not(is_on(light))


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
    for piece in all_pieces:
        board.placepiece(piece)


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
sbits=13
abits = 5
Q = numpy.matrix(scipy.zeros((1<<sbits, 1<<abits), dtype=scipy.float32), dtype=scipy.float32)
Vx = numpy.matrix(scipy.zeros((1<<sbits, 1), dtype=scipy.float32), dtype=scipy.float32)
Ax = {}

Q_default_value = 0.0

Q_flick_switch = loadobject('flick_switch_option.q')


def which_Q(o=None):
    """Returns the correct Q table depending on the variable o:
    If o is provided, return the Q-table for the option, if it
    is not provided, return the standard Q-table."""

    if o == None:
        return Q
    else:
        return O[o]['Q']


def fix_P(o, s):
    P = O[o]['P']
    try:
        dummy = P[s]
    except KeyError:
        P[s] = numpy.matrix(scipy.zeros((1, 1<<sbits),
                                        dtype=scipy.float32),
                            dtype=scipy.float32)


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
    my_Q = which_Q(o)
    try:
        return my_Q[s][a]
    except KeyError:
        return 0.0


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
def set_Vx(s, new_max, o=None):
    my_Vx = which_Vx(o)
    my_Vx[s] = new_max


# Vx refers to V^*
def get_Vx(s, o=None):
    if o == None:
        my_Vx = Vx
    else:
        my_Vx = O[o]['Vx']

    try:
        return my_Vx[s]
    except KeyError:
        return 0.0


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
    epsilon = 0.3

    if scipy.random.random() < epsilon:
        # random
        a = select_random_action(s)
    else:
        # greedy
        a = choice(select_best_actions(s, o))

    while is_option(a):
        option_stack.append(a)
        a = get_action_from_option(s, a)

    return a


def select_best_action(s, o=None):
    return choice(select_best_actions(s, o))


def set_random_initial_state():
    board_squares = list(product(range(5), range(5)))
    for piece in all_pieces:
        board_square = choice(board_squares) # each board square is a tuple (row, column)

        move_piece_to_cell(piece, board_square[0], board_square[1])


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
    if is_on(toy_monkey_sound) and toy_monkey_sound['step'] == step:
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
                if random.random() < epsilon:    # random() gives a number in the interval [0, 1).
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
global args
step_filename = None
option_stack_filename = None
ED_filename = None


def fix_2dic(dic, key1, key2):
    """ Fixes a two-dimension dictionary: receives the keys and, if
    the entry does not exist in the dictionary, creates it
    initializing with zero"""

    try:
        dummy = dic[key1]
        try:
            dummy = dic[key1][key2]
        except KeyError:
            dic[key1][key2] = 0.0
    except KeyError:
        dic[key1] = {}
        dic[key1][key2] = 0.0


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

    try:
        return dic[key]
    except KeyError:
        return 0.0


def get_2dic(dic, key1, key2):
    """Gets the value of a two-dimensional dictionary entry. If the
    entry does not exist, returns a default value of zero."""

    try:
        return dic[key1][key2]
    except KeyError:
        return 0.0


def fix_O(o):
    try:
        dummy = O[o]
    except KeyError:
        # Creates an entry to the option
        O[o] = {}

        # Creates an entry to the option's Q-table
        O[o]['Q'] = numpy.matrix(scipy.zeros((1<<sbits, 1<<abits),
                                             dtype=scipy.float32), dtype=scipy.float32)

        # Creates an entry to the option's initiation set
        O[o]['I'] = set()

        # Creates an entry to the option's V^*
        O[o]['Vx'] = numpy.matrix(scipy.zeros((1<<sbits, 1),
                                              dtype=scipy.float32), dtype=scipy.float32)

        # Creates an entry to the option's A^*
        O[o]['Ax'] = {}

        # Creates an entry to the option's Beta function
        O[o]['BETA'] = numpy.matrix(scipy.zeros((1<<sbits, 1),
                                                dtype=scipy.int8), dtype=scipy.int8)

        # Creates an entry to the option's Reward function
        O[o]['R'] = numpy.matrix(scipy.zeros((1<<sbits, 1),
                                              dtype=scipy.float32), dtype=scipy.float32)

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
    try:
        return which_Ax(o)[s]
    except KeyError:
        return set()


def add_Ax(s, a, o=None):
    fix_Ax(s, o)
    which_Ax(o)[s].add(a)


def clear_Ax(s, o=None):
    fix_Ax(s, o)
    which_Ax(o)[s].clear()


def set_BETA(o, s, new_value):
    set_1dic(O[o]['BETA'], s, new_value)


def get_BETA(o, s):
    try:
        return O[o]['BETA'][s]
    except KeyError:
        return 0.0


def set_R(o, s, new_value):
    set_1dic(O[o]['R'], s, new_value)


def get_R(o, s):
    try:
        return O[o]['R'][s]
    except KeyError:
        return 0.0


def set_P(o, s2, s, new_value):
    O[o]['P'][s2, s] = new_value


def get_P(o, s2, s):
    return O[o]['P'][s, s2]


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


def add_pieces_on_cell(row, col, piece):
    """Adds the piece to the set correspondig to [row][col]."""

    board_matrix[row][col][piece.value] = True


def del_pieces_on_cell(row, col, piece):
    """Removes a piece from the set corresponding to [row][col]."""

    board_matrix[row][col][piece.value] = False


def get_pieces_on_cell(row, col):
    """Gets a set of the pieces present on [row][col] on the board"""
    i = 0
    pieces_on_cell = []
    for bit in board_matrix[row][col][:-4]:
        if bit: pieces_on_cell.append(non_agent_pieces[i])
        i += 1
    return pieces_on_cell

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
    try:
        return available_options[s]
    except KeyError:
        return set()


def o_exists(o):
    """Tests if there is an entry in O for the option o."""
    try:
        dummy = O[o]
        return True
    except KeyError:
        return False


def get_top_stack(stack):
    """Returns the item on top of the stack if it exists or None if the
    stack is empty"""
    try:
        return stack[-1:][0] # Top of the stack
    except IndexError:       # Stack is empty
        return 0


option_stack = []
def get_current_option(s2):
    """Resolves the option stack and eventually returns an option.

    The strategy to abandon an option is "bottom-up" in relation to
    salient events:

    The function goes through the option stack from the oldest one to
    the newest one (from the bottom to the top).  If the current state
    is a salient event to an option, this option is removed from the
    stack, along with all the other options (if any) that are newer
    than this one.

    """

    # 'current' is the status combination of the current state
    current = bool2int(numpy.array([is_on(light), is_on(music),
                                    is_on(bell_sound),
                                    is_on(toy_monkey_sound)])) + \
                                    len(all_possible_actions) + 1

    # 'target' is the status combination that the option 'wants'
    for i in range(len(option_stack)-1, -1, -1):
        target = option_stack[i]
        if current == target:
            del option_stack[i:]

    return get_top_stack(option_stack)


def update_vxax(myQ, myVx, myAx, s, a, o=None):
    if o is None:
        ai = all_possible_actions_int[a]
    else:
        a = o
        ai = o
    if myQ[s, ai] > 0.0:
        if myQ[s, ai] > myVx[s, 0]:
            myVx[s, 0] = myQ[s, ai]

            try:
                myAx[s].clear()
            except KeyError:
                myAx[s] = set()
            myAx[s].add(a)
        elif myQ[s, ai] == myVx[s, 0]:
            myAx[s].add(a)


def imrl():
    global step
    global r_i_filename
    global step_filename
    global option_stack_filename
    global ED_filename
    global args

    starttime = time.time()

    # Sees if should open previous saved data from another experiment
    if args.load:
        global S
        global option_stack
        global Q
        global O
        global Vx
        global Ax

        [args, alpha, gamma, epsilon, tau, r_i_filename,
         step_filename, option_stack_filename, ED_filename, s, s2, S,
         a, a2, r_e, r_e2, r_i, r_i2, current_option, option_stack,
         current_step, steps, Q, O, Vx, Ax] = loadobject(args.load[0])

        initial_step = current_step + 1
        step = initial_step
    else:
        # Learning parameters
        alpha            = 0.1
        gamma            = 0.99
        epsilon          = 0.1
        tau              = 0.5

        steps = int(5e5)

        # Variables initialization
        s = update_state()
        S.add(s)
        a = select_random_action()
        r_e = 0.0
        r_i = 0.0
        step = 1
        initial_step = 0
        current_option = 0

        # Log stuff
        r_i_filename = get_log_filename(prefix='r_i-')

    print 'Logging to: ' + r_i_filename

    # Git: commit (if that is the case) and tag (always succeed),
    # using the experiment's log filename. This way it is possible to
    # track the version that generated each result
    git_commit_and_tag(r_i_filename[5:])

    for current_step in xrange(initial_step, steps):
        # Obtain next state s_{t+1}
        execute_action(a, s)
        s2 = update_state()
        S.add(s2)

        if current_option != 0:
            add_I(current_option, s2)

        # Deal with special case if next state is salient
        o_e = None
        if is_salient_event():        # If s_{t+1} is a salient event e
            o = bool2int(numpy.array([is_on(light), is_on(music),
                                      is_on(bell_sound), is_on(toy_monkey_sound)]))
            o += len(all_possible_actions) + 1

            # If option for e, o_e, does not exist in O (skill-KB)
            if not (o_exists(o)):
                # Create option o_e in skill-KB;
                fix_O(o)

                o_e = o                   # Used in "Update all option models", below

            # Add s_t to I^{o_e} // initialize initiation set
            add_I(o, s)

            # Set β^{o_e}(s_{t+1}) = 1 // set termination probability
            set_BETA(o, s2, 1.0)

            # //— set intrinsic reward value
            P = O[o]['P']

            fix_P(o, s)

            r_i2 = tau * (1.0 - P[s][0, s2])
            log_r_i(r_i2, s, s2, current_option, a)
        else:
            r_i2 = 0.0

        # //— Determine next extrinsic reward
        # Set r^e_{t+1} to the extrinsic reward for transition s_t, a_t → s_{t+1}
        r_e2 = get_r_e()


        ################################
        # //- Update all option models #
        ################################
        O_keys = [o for o in O.keys() if o != o_e]
        for o in O_keys: # For each option o != o_e in skill-KB (O)
            # If s_{t+1} ∈ I^o , then add s_t to I^o // grow initiation set
            if s2 in get_I(o):
                if get_BETA(o, s) != 1.0:
                    add_I(o, s)

            # If a_t is greedy action for o in state s_t
            try: As = O[o]['Ax'][s]
            except KeyError: As = set()
            if a in As:
                ##################################################
                # //— update option transition probability model #
                ##################################################
                P = O[o]['P']

                fix_P(o, s)
                fix_P(o, s2)

                if get_BETA(o, s2) == 0.0:
                    pr = (1.0 - alpha) * P[s] + alpha * gamma * P[s2]
                else:
                    pdelta = numpy.matrix(scipy.zeros((1, 1<<sbits),
                                                      dtype=scipy.float32),
                                          dtype=scipy.float32)
                    pdelta[0, s2] = 1.0

                    pr = (1.0 - alpha) * P[s] + alpha * gamma * pdelta

                    del pdelta

                del P[s]
                P[s] = pr.copy()
                del pr

                ##################################
                # //— update option reward model #
                ##################################
                # Gets some nice abbreviations
                R = O[o]['R']
                Bs2 = float(O[o]['BETA'][s2, 0])

                # Calculates and sets the new value
                x = R[s, 0]
                y = r_e2 + gamma * (1.0 - Bs2) * R[s2, 0]
                R[s, 0] = alpha_sum(x, y, alpha)


        ###########################################################
        # //— Q-learning update of behavior action-value function #
        ###########################################################
        # Calculates the new value of Q(s, a)
        ai = all_possible_actions_int[a]
        Q[s, ai] = (1.0 - alpha) * Q[s, ai] + \
                   (alpha) * (r_e + r_i + gamma * Vx[s2, 0])
        update_vxax(Q, Vx, Ax, s, a)


        ##############################################################
        # //— SMDP-planning update of behavior action-value function #
        ##############################################################
        for o in O.keys(): # For each option o = o_e in skill-KB (O)
            if s in get_I(o):
                # Gets some nice abbreviations
                R = O[o]['R']
                P = O[o]['P']

                fix_P(o, s)

                # Calculates and sets the new value
                x = Q[s, o]
                y = R[s, 0] + P[s].dot(Vx)
                Q[s, o] = alpha_sum(x, y, alpha)
                update_vxax(Q, Vx, Ax, s, a, o)


        ############################################
        # //— Update option action-value functions #
        ############################################
        for o in O.keys(): # For each option o ∈ O such that s_t ∈ I^o
            if s in get_I(o):
                # Gets some nice abbreviations
                Qo = O[o]['Q']
                Vo = O[o]['Vx']
                Ao = O[o]['Ax']
                TV = O[o]['TV']
                Beta_o = O[o]['BETA']
                Beta_s2 = float(Beta_o[s2, 0])
                V2 = numpy.where(Beta_o, TV, Vo)
                ai = all_possible_actions_int[a]

                # Calculates and sets the new value
                x = Qo[s, ai]
                if Beta_s2 == 1.0:
                    y = r_e2 + gamma * TV
                else:
                    y = r_e2 + gamma * Vo[s2, 0]
                Qo[s, ai] = alpha_sum(x, y, alpha)
                update_vxax(Qo, Vo, Ao, s, a)

                for o2 in O.keys(): # For each option o2 ∈ O such that s_t ∈ I^o2 and o != o2
                    if (o != o2) and (s in get_I(o2)):
                        # Gets some nice abbreviations
                        Po2 = O[o2]['P']
                        Ro2 = O[o2]['R']

                        fix_P(o2, s)

                        # Calculates and sets the new value
                        x = Qo[s, o2]
                        y = Ro2[s, 0] + Po2[s].dot(V2)
                        Qo[s, o2] = alpha_sum(x, y, alpha)
                        update_vxax(Qo, Vo, Ao, s, a, o2)

        #################################################################################
        # Choose a_{t+1} using epsilon-greedy policy w.r.to Q_B // — Choose next action #
        #################################################################################
        current_option = get_current_option(s2)

        if current_option == 0:
            if scipy.random.random() < epsilon:    # random() gives a number in the interval [0, 1).
                # random
                next_action = select_random_action(s2)
            else:
                # greedy
                next_action = select_best_action(s2)

            if is_option(next_action):
                option_stack.append(next_action)
                current_option = next_action
        else:
            next_action = current_option

        if is_option(next_action):
            a2 = get_action_from_option(s2, next_action)
        else:
            a2 = next_action

        # Set st ← st+1 ; at ← at+1 ; r^e_t ← r^e_{t+1} ; r^i_t ← r^i_{t+1}
        s = s2
        a = a2
        r_i = r_i2
        r_e = r_e2
        step += 1

        # Sets bell_sound status
        turn_bell_off()

        # Log
        if args.log_step: log_step(s2, current_option, a2, r_i2)
        if args.log_option_stack: log_option_stack()

        # # Persist data related to this experiment
        # if random.random() < 1e-4:
        #     if ED_filename == None:
        #         if r_i_filename == None:
        #             r_i_filename = get_log_filename(prefix='r_i-')
        #         ED_filename = r_i_filename + '.dat'
        #     saveobject([args, alpha, gamma, epsilon, tau, r_i_filename, step_filename, option_stack_filename, ED_filename, s, s2, S, a, a2, r_e, r_e2, r_i, r_i2, current_option, option_stack, current_step, steps, Q, O, Vx, Ax], ED_filename)

    # saveobject(O, get_log_filename(prefix='O-')) # persists O

    totaltime = time.time() - starttime
    log_time(totaltime)

    sys.exit()


def main():
    global args
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--nox", help="Does not use the X (graphical) part (runs imrl)",
                        action="store_true")
    parser.add_argument("--log_step", help="Logs lots of information at each step",
                        action="store_true")
    parser.add_argument("--log_option_stack", help="Logs the option stack",
                        action="store_true")
    parser.add_argument("--no_cardinal", help="The eye does not use the cardinal actions",
                        action="store_true")
    parser.add_argument("--load", nargs='*', help="Loads saved data from previous experiment.")

    args = parser.parse_args()

    global board_rows
    board_rows = 5
    global board_columns
    board_columns = 5

    ####################
    # Non-agent Pieces #
    ####################
    global ball
    ball = Piece(name = "ball", actions=['kick_ball'], value=0)
    global bell
    bell = Piece(name = "bell", row=0, column=1, value=1)
    global blue_block
    blue_block = Piece(name = "blue_block", row=0, column=4, actions=['press_blue_block', 'push_blue_block'], value=2)
    global red_block
    red_block = Piece(name = "red_block", row=1, column=0, actions=['press_red_block', 'push_red_block'], value=3)
    global switch
    switch = Piece(name = "switch", row=1, column=1, actions=['flick_switch'], value=4)
    global toy_monkey
    toy_monkey = Piece(name = "toy_monkey", row=1, column=3, value=5)

    ################
    # Agent Pieces #
    ################
    global eye
    eye = Piece(name = "eye", row=0, column=2, value=7)
    global hand
    hand = Piece(name = "hand", row=0, column=3, value=8)
    global marker
    marker = Piece(name = "marker", row=1, column=2, value=9)

    ################
    # Pieces Lists #
    ################
    global agent_pieces
    agent_pieces = [eye, hand, marker]
    global non_agent_pieces
    non_agent_pieces = [ball, bell, blue_block, red_block, switch, toy_monkey]

    global all_pieces
    all_pieces = agent_pieces + non_agent_pieces

    global state
    state = 0

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

    global all_possible_actions_int
    all_possible_actions_int = {
        'move_eye_to_hand':0,
        'move_eye_to_marker':1,
        'move_eye_one_step_north':2,
        'move_eye_one_step_south':3,
        'move_eye_one_step_east':4,
        'move_eye_one_step_west':5,
        'move_eye_to_random_object':6,
        'move_hand_to_eye':7,
        'move_marker_to_eye':8,
        'kick_ball':9,
        'press_blue_block':10,
        'push_red_block':11,
        'press_red_block':12,
        'push_blue_block':13,
        'flick_switch':14,
    }

    # Filled in update_available_actions
    global available_actions
    available_actions = []

    position_pieces_like_article()
    update_blocks_bits()

    if args.nox:
        print "Will not run the graphical part. Running imrl..."
        imrl()
    else:
        create_x()


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
    board = Board(central_frame, rows=board_rows, columns=board_columns)
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

    update_environment_labels()

    #################
    # Key shortcuts #
    #################
    root.bind_all('<Key>', key)

    update_screen()

    root.mainloop()


if __name__ == '__main__':
    main()
