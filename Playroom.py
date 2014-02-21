#!/usr/bin/python
# coding=UTF-8

import Tkinter as tk
from Board import *
from Piece import *
from random import randint
from random import random
from PIL.ImageTk import PhotoImage
from random import choice
from time import sleep
from itertools import product
from datetime import datetime

def update_light_state():
    pass

def update_music_state():
    pass

def update_bell_sound_state():
    # only turns of, it is turned on using
    # kick_ball function
    global bell_sound
    global step

    if bell_sound['state'] == 'ON':
        if step > bell_sound['step'] + 1:
            turn_bell('OFF')

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
light = {'state':'OFF', 'step':0, 'update_function':update_light_state}
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
                        adj_squares.append( (row, column ) )
    return adj_squares

def move_piece_to_square(piece, square):
    piece.row = square[0]
    piece.column = square[1]
    board.placepiece(piece)

def move_piece_rand_adj(block):
    adj_squares = get_adj_squares(block)
    if len(adj_squares) > 0:
        random_index = randint(0, len(adj_squares) - 1)
        move_piece_to_square(block, adj_squares[random_index])

def push_blue_block():
    move_piece_rand_adj(blue_block)

def push_red_block():
    move_piece_rand_adj(red_block)

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
        'move_marker_to_eye'
        ]

def get_actions_from_pieces():
    actions = []
    if on_same_cell(eye, hand):
        for piece in non_agent_pieces:
            if on_same_cell(piece, eye):
                if not (piece in [blue_block, red_block] and \
                        light['state'] == 'OFF'):
                    actions += piece.get_actions()
    return actions

def turn_bell(new_state):
    global bell
    global step
    bell_sound['state'] = new_state
    bell_sound['step'] = step

def turn_toy_monkey(new_state):
    global toy_monkey_sound
    toy_monkey_sound['state'] = new_state
    toy_monkey_sound['step'] = step

def same_cell_to_tuple(ag_piece):
    global light
    same_cell = ()
    for piece in non_agent_pieces:
        if on_same_cell(piece, ag_piece):
            if light['state'] == 'OFF' and \
              piece in [blue_block, red_block]:
                same_cell += ('gray_block',)
            else:
                same_cell += (piece.name,)
    return same_cell

def update_state():
    global state
    under_eye = same_cell_to_tuple(eye)
    under_hand = same_cell_to_tuple(hand)
    under_marker = same_cell_to_tuple(marker)
    state = (under_eye, under_hand, under_marker)
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
        execute_action
    if event.keysym == 't':
        update_toy_monkey_sound_state()
    if event.keysym == 'u':
        print 'State:'
        print str(update_state())

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

    state_label_text.set('State: [eye:'    + str(state[0]) +'], ' +
                                '[hand:'   + str(state[1]) +'], ' +
                                '[marker:' + str(state[2]) +']')

def update_blocks_color():
    global light
    if light['state'] == 'ON':
        blue_block.set_image(tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/blue_block.gif"))
        board.updatepieceimage(blue_block)

        red_block.set_image(tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/red_block.gif"))
        board.updatepieceimage(red_block)
    elif light['state'] == 'OFF':
        blue_block.set_image(tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/gray_block.gif"))
        board.updatepieceimage(blue_block)

        red_block.set_image(tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/gray_block.gif"))
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
    root.update_idletasks()

def create_action_buttons():
    action_buttons_frame = tk.Frame(central_frame)
    action_buttons_frame.pack(side=tk.RIGHT)

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

##############
# Q-Learning #
##############
Q = {}
Q_default_value = 0.0
Q_max = {}

def fix_Q_value(state_key, action_key):
    global Q
    global Q_default_value

    if not (state_key in Q.keys()):
        Q[state_key] = {}

    if not (action_key in Q[state_key].keys()):
        Q[state_key][action_key] = Q_default_value

def set_Q_value(state_key, action_key, new_value):
    global Q

    fix_Q_value(state_key, action_key)

    Q[state_key][action_key] = new_value

def get_Q_value(state_key, action_key):
    global Q

    fix_Q_value(state_key, action_key)

    return Q[state_key][action_key]

def fix_Q_max(state_key):
    global Q_max
    global Q_default_value

    if not (state_key in Q_max.keys()):
        Q_max[state_key] = Q_default_value

def set_Q_max(state_key, new_max):
    global Q_max

    fix_Q_max(state_key)

    Q_max[state_key] = new_max

def get_Q_max(state_key):
    global Q_max

    fix_Q_max(state_key)

    return Q_max[state_key]

def state_is_goal():
    return light['state'] == 'ON'

def select_random_action():
    global available_actions

    update_available_actions()

    return choice(available_actions)

def select_best_action():
    global available_actions
    global state
    
    update_available_actions()

    best_value = 0
    best_actions = []
    for action in available_actions:
        Q_value = get_Q_value(state, action)
        if Q_value >= best_value:
            if Q_value > best_value:
                best_value = Q_value
                del best_actions[:]; best_actions = []
                
            best_actions.append(action)

    return choice(best_actions)

def set_random_initial_state():
    global all_pieces
    global board

    board_squares = list(product(range(5), range(5)))

    for piece in all_pieces:
        board_square = choice(board_squares)

        piece.row = board_square[0]
        piece.column = board_square[1]

        board.placepiece(piece)

def position_pieces_like_article():
    global ball
    global bell
    global blue_block
    global red_block
    global switch
    global toy_monkey
    global hand
    global eye
    global marker
    global board
    global all_pieces

    ball.row = 1
    ball.column = 0

    bell.row = 1
    bell.column = 4

    blue_block.row = 4
    blue_block.column = 0

    red_block.row = 4
    red_block.column = 4

    switch.row = 2
    switch.column = 2

    toy_monkey.row = 1
    toy_monkey.column = 2

    hand.row = 0
    hand.column = 3

    eye.row = 1
    eye.column = 3

    marker.row = 2
    marker.column = 4

    for piece in all_pieces:
        board.placepiece(piece)

def setup_new_episode():
    global step

    step = 0
    turn_light('OFF')
    position_pieces_like_article()

def get_reward():
    if state_is_goal():
        print 'reward!!!'
        return 1
    else:
        return 0

def q_learning_simple():
    global Q
    global step
    global state

    alpha            = 0.9
    gamma            = 0.9
    epsilon          = 0.1
    epsilonIncrement = 0.0

    episodes = 100000
    steps = 1000

    now_str = str(datetime.now())
    filename = '/home/rafaelbeirigo/' + now_str.replace(':', '-')[:19] + '.log'
    print 'Logging to: ' + filename

    global_step_count = 0
    for episode in range(episodes):
        setup_new_episode()
        start_step = global_step_count
        for current_step in range(steps):
            update_state()
            update_environment_variables()
            update_screen()

            # if a goal state is reached the episode ends
            if state_is_goal():
                break

            # Following epsilon-greedy strategy, Select an action a
            # and execute it. Receive immediate reward r. Observe the
            # new state s2
            randomNumber = random()
            if randomNumber < epsilon:
                # random
                a = select_random_action()
            else:
                # greedy
                a = select_best_action()

            s = state
            execute_action(a)
            s2 = state
            r = get_reward()

            Q_s_a_old = get_Q_value(s, a)
            Q_max_s2 = get_Q_max(s2)
            
            # Update the table entry for Q(s, a)
            Q_s_a_new = (1.0 - alpha) * Q_s_a_old + \
                               alpha  * (r + gamma * Q_max_s2)
            set_Q_value(s, a, Q_s_a_new)

            if Q_s_a_new > get_Q_max(s):
                set_Q_max(s, Q_s_a_new)

            step += 1
            global_step_count += 1
                        
            root.update_idletasks()
            # sleep(.01)

        # Here an episode just ended
        episode_number = episode
        end_step = global_step_count
        duration = end_step - start_step

        last_start_step = end_step
                
        f = open(filename, 'w')
        f.write('Hello File!\n')
        f.close()


        # epsilon = epsilon + epsilonIncrement

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

state_frame = tk.Frame(root)
state_frame.pack(side=tk.TOP)
state_label_text = tk.StringVar()
state_label = tk.Label( state_frame, textvariable=state_label_text, relief=tk.RAISED, borderwidth=4 )
state_label.pack(side=tk.TOP)

central_frame = tk.Frame(root)
central_frame.pack(side=tk.TOP)

board = Board(central_frame)
board.pack(side="left", fill="both", expand="true", padx=4, pady=4)

ball = Piece(name = "ball", image=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/ball.gif"), actions=['kick_ball'])
bell = Piece(name = "bell", image=tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/bell.gif"), row=0, column=1)
blue_block = Piece(name = "blue_block", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/blue_block.gif"), row=0, column=4, actions=['press_blue_block', 'push_blue_block'])
red_block = Piece(name = "red_block", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/red_block.gif"), row=1, column=0, actions=['press_red_block', 'push_red_block'])
switch = Piece(name = "switch", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/switch.gif"), row=1, column=1, actions=['flick_switch'])
toy_monkey = Piece(name = "toy_monkey", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/toy-monkey.gif"), row=1, column=3)

hand = Piece(name = "hand", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/hand.gif"), row=0, column=3)
eye = Piece(name = "eye", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/eye.gif"), row=0, column=2)
marker = Piece(name = "marker", image = tk.PhotoImage(file="/home/rafaelbeirigo/ciencia/playroom/img/target.gif"), row=1, column=2)

agent_pieces = [hand, eye, marker]
non_agent_pieces = [ball, bell, blue_block, red_block, switch, toy_monkey]
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
}

action_buttons = []

available_actions = []

update_environment_labels()

create_action_buttons()

random_actions_button = tk.Button(root, text='random_actions', command=random_actions)
random_actions_button.pack(side=tk.TOP)

set_random_initial_state_button = tk.Button(root, text='set_random_initial_state', command=set_random_initial_state)
set_random_initial_state_button.pack(side=tk.TOP)

q_learning_simple_button = tk.Button(root, text='q_learning_simple', command=q_learning_simple)
q_learning_simple_button.pack(side=tk.TOP)

position_pieces_like_article_button = tk.Button(root, text='position_pieces_like_article', command=position_pieces_like_article)
position_pieces_like_article_button.pack(side=tk.TOP)

root.bind_all('<Key>', key)

update_screen()

root.mainloop()
