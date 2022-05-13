#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 22:20:38 2020

@author: alanlee
"""


import pygame
from pygame import gfxdraw
from board import Board
from math import sqrt

SCREEN_W = 500
SCREEN_H = 500

pygame.init()
win = pygame.display.set_mode((SCREEN_W,SCREEN_H))
clock = pygame.time.Clock()

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



while run:
    clock.tick(180)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        pass
    
    if pygame.mouse.get_pressed()[0]:
        mouse_cords = pygame.mouse.get_pos()
        for cord in node_cords.keys():
            if sqrt((mouse_cords[0]-cord[0])**2+(mouse_cords[1]-cord[1])**2) < 15:
                update = board.update(node_cords[cord])
                if update == "game_over":
                    print(update)
                    run = False
                elif update == "game_won":
                    print("U WIN")
                    run = False
                    
        
    redraw()

pygame.quit()
