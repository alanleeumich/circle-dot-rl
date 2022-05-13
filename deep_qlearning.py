#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 19:09:32 2020

@author: alanlee
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
from numpy import argmax
from board import Board
import random
import copy
import threading

save = False

def save_input():
    loop = True
    while loop:
        if input() == "save":
            save = True
        
'''
model = keras.Sequential([
    keras.layers.Dense(81,activation="relu"),
    keras.layers.Dense(200,activation="relu"),
    keras.layers.Dense(200,activation="relu"),
    keras.layers.Dense(81,activation="relu"),
    ])

fitted_model = copy.deepcopy(model)

model.compile(optimizer = "adam", loss = "mean_squared_error")
fitted_model.compile(optimizer = "adam", loss = "mean_squared_error")
'''

fitted_model = keras.models.load_model("deep_q_model1")
model = keras.Sequential([
    keras.layers.Dense(81,activation="relu"),
    keras.layers.Dense(200,activation="relu"),
    keras.layers.Dense(200,activation="relu"),
    keras.layers.Dense(81,activation="relu"),
    ])
model.build((None,81))
model.compile(optimizer = "adam", loss = "mean_squared_error")
model.set_weights(fitted_model.get_weights())


board = Board()

fitness = 0
best_fitness = 0
average_fitness = {"total":0,"num":0}
record_fitness = 0

x_train = []
y_train = []

thread = threading.Thread(target = save_input)
thread.start()

old_board = None
epsilon = 0.95

for j in range(100000):
    
    gamestate = []
    output_to_node = {}
    i = 0
    for col_index in range(len(board.board)):       
        for row_index in range(len(board.board[col_index])):
            if board.board[col_index][row_index].blocked:
                gamestate.append(-1)
            elif board.dot == board.board[col_index][row_index]:
                gamestate.append(1)
            else:
                gamestate.append(0) 
            output_to_node[i] = board.board[col_index][row_index]
            i += 1
     
    old_state_q = model.predict([gamestate])[0]
    '''
    epsilon = 0.95
    if fitness > record_fitness/2:
        epsilon = 0.6
    '''
    if random.uniform(0,1) < epsilon:
        action = argmax(old_state_q)
    else:
        action = random.randint(0,80)
    
    reward = 0
    
    if output_to_node[action].blocked or board.dot == output_to_node[action]:
        reward = -1
    
    second_old_board = copy.deepcopy(old_board)
    old_board = copy.deepcopy(board)
    update = board.update(output_to_node[action])
    
    
    if update == "game_over":
        reward = -1
    elif update == "game_won":
        reward = 1000
        fitness += 1000
    elif reward == 0:
        reward = 1
        fitness += 1
    
    new_gamestate = []
    for col_index in range(len(board.board)):       
        for row_index in range(len(board.board[col_index])):
            if board.board[col_index][row_index].blocked:
                new_gamestate.append(-1)
            elif board.dot == board.board[col_index][row_index]:
                new_gamestate.append(1)
            else:
                new_gamestate.append(0)
    
    new_state_q = model.predict([new_gamestate])[0]
    
    
    
    old_state_q[action] = reward + 0.9*max(new_state_q)
   

    if j%30 == 0 and j > 0:
        fitted_model.fit(np.array(x_train),np.array(y_train))
        x_train = []
        y_train = []
        print("best fitness:",best_fitness)
        try:
            print("average_fitness:",average_fitness["total"]/average_fitness["num"])
        except:
            pass
        average_fitness = {"total":0,"num":0}
        best_fitness = 0
        print("record fitness:",record_fitness)
        
        if save:
            fitted_model.save("deep_q_model")
            save = False
    if j%100 == 0 and j>0:
        model = keras.Sequential([
            keras.layers.Dense(81,activation="relu"),
            keras.layers.Dense(200,activation="relu"),
            keras.layers.Dense(200,activation="relu"),
            keras.layers.Dense(81,activation="relu"),
            ])
        model.build((None,81))
        model.compile(optimizer = "adam", loss = "mean_squared_error")
        model.set_weights(fitted_model.get_weights())
            
    else:
        x_train.append(gamestate)
        y_train.append(old_state_q)
    
    if reward == -1:
        if random.uniform(0,1) > 0.5:
            board = Board()
            epsilon = 0.95
        else:
            board = second_old_board
            epsilon = 0.5
            
        if fitness > best_fitness:
            best_fitness = fitness
        if best_fitness > record_fitness:
            record_fitness = best_fitness
        average_fitness["total"] += fitness
        average_fitness["num"] += 1
        fitness = 0

fitted_model.save("deep_q_model2")   
loop = False


