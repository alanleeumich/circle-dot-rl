#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 13:34:03 2020

@author: alanlee
"""

import tensorflow as tf
from tensorflow import keras
import pygame
from pygame import gfxdraw
import numpy as np
import time

from board import Board

model = keras.models.load_model("deep_q_model2")

def max_index(a):
    max_val = a[0]
    max_i = 0
    for i in range(len(a)):
        if a[i] > max_val:
            max_val = a[i]
            max_i = i
    return max_i

pygame.init()
win = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
fitness = 0



board = Board()
node_cords = {}
for col_index in range(len(board.board)):       
    for row_index in range(len(board.board[col_index])):
         node_cords[(row_index*34+50+(col_index%2)*17,col_index*30+50)] = board.board[col_index][row_index]   


run = True

def redraw():
    win.fill((255,255,255))
    for cord in node_cords.keys():
        if node_cords[cord].blocked:
            color = (255, 171, 46)
        elif node_cords[cord] == board.dot:
            color = (122, 198, 255)
        else:
            color = (230, 227, 220)
        gfxdraw.filled_circle(win, cord[0], cord[1], 15, color)
                
    pygame.display.update()


time.sleep(5)

while run:

    redraw()
    clock.tick(1)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        pass
    
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
    output = model.predict([gamestate])[0]
    repeat = False
    output = output.tolist()
    while output_to_node[max_index(output)].blocked or board.dot == output_to_node[max_index(output)]:
        output[max_index(output)] = -10000
        repeat = True
        print("stuck")
    if repeat:
        fitness -= 0
        print("stuck")
        
    output_node = output_to_node[max_index(output)]
    update = board.update(output_node)
    if update == "game_over":
        print(update)
        fitness -= 1
        print(fitness)
        run = False
    elif update == "game_won":
        print("U WIN")
        fitness += 20
        print(fitness)
        run = False
    else:
        fitness += 1
        
    

pygame.quit()
