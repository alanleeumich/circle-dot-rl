#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 22:30:20 2020

@author: alanlee
"""

import random

class Board():
    ROWS = 9
    COLS = 9
    def __init__(self):
        self.board = [[Node() for _ in range(self.ROWS)] for _ in range(self.COLS)]
        self.dot = self.board[4][4]
        self.connect_nodes()
        self.target_nodes = []
        for col_index in range(len(self.board)):       
            for row_index in range(len(self.board[col_index])):
                if col_index == 0 or col_index == len(self.board)-1 or row_index == 0 or row_index == len(self.board[col_index])-1:
                    self.target_nodes.append(self.board[col_index][row_index])
        i = 0
        while i < 7:
            col = random.randint(0,8)
            row = random.randint(0,8)
            if not (self.board[col][row] == self.dot or self.board[col][row].blocked):
                self.board[col][row].blocked = True
                i += 1
            
    def connect_nodes(self):
        for col_index in range(len(self.board)):       
            for row_index in range(len(self.board[col_index])):
                blocked_up = col_index == 0
                blocked_down = col_index == len(self.board)-1
                blocked_left = row_index == 0
                blocked_right = row_index == len(self.board[col_index])-1
                
                if not blocked_up:
                    self.board[col_index][row_index].connect(self.board[col_index-1][row_index])
                if not blocked_down:
                    self.board[col_index][row_index].connect(self.board[col_index+1][row_index])
                if not blocked_left:
                    self.board[col_index][row_index].connect(self.board[col_index][row_index-1])
                if not blocked_right:
                    self.board[col_index][row_index].connect(self.board[col_index][row_index+1])

                if col_index%2 == 0:
                    if not blocked_left:
                        if not blocked_up:
                            self.board[col_index][row_index].connect(self.board[col_index-1][row_index-1])
                        if not blocked_down:
                            self.board[col_index][row_index].connect(self.board[col_index+1][row_index-1])
                else:
                    if not blocked_right:
                        if not blocked_up:
                            self.board[col_index][row_index].connect(self.board[col_index-1][row_index+1])
                        if not blocked_down:
                            self.board[col_index][row_index].connect(self.board[col_index+1][row_index+1])
    
    def pathfind(self,start_node,finish_nodes):
        start_node.distance = 0
        edge_nodes = [start_node]
        reach_finish = False
        
        while not reach_finish:
            temp_edge = edge_nodes.copy()
            edge_nodes = []
            for node in temp_edge: 
                for connected_node in node.connected:
                    if not connected_node in edge_nodes:
                        if not connected_node.blocked:
                            edge_nodes.append(connected_node)
            new_node = False
            for node in edge_nodes:
                if node in finish_nodes:
                    reach_finish = True
                    current_node = node
                for connected_node in node.connected:
                    if not connected_node.blocked:
                        if not connected_node.distance == "-":
                            if node.distance == "-":
                                node.distance = connected_node.distance + 1
                                new_node = True
                            else:
                                if connected_node.distance + 1 < node.distance:
                                    node.distance = connected_node.distance + 1
            if not new_node:
                return "stuck"    
                   
        #backtracking from finish
        while not current_node == start_node:     
            current_node.path = True
            next_node = current_node
            for node in current_node.connected:
                if not (node.blocked or node.distance == "-"):
                    if node.distance < next_node.distance:
                        next_node = node
            current_node = next_node
        #finding first move
        for node in start_node.connected:
            if node.path:
                self.reset_nodes()
                return node
            
    
    def reset_nodes(self):
         for col_index in range(len(self.board)):       
            for row_index in range(len(self.board[col_index])):
                self.board[col_index][row_index].reset()
    
    def update(self,node):
        if not (node.blocked or node == self.dot):
            node.blocked = True
            if self.dot in self.target_nodes:
                return "game_over"
            pathfind = self.pathfind(self.dot,self.target_nodes)
            if pathfind == "stuck":
                return "game_won"
            self.dot = pathfind
            
class Node():
    def __init__(self):
        self.connected = []
        self.distance = "-"
        self.blocked = False
        self.target = False
        self.path = False
        
        
    def __repr__(self):
        if self.blocked:
            return "X"
        elif self.path:
            return "O"
        else:
            return "-"
    
    def connect(self,node):
        if not node in self.connected:
            self.connected.append(node)
        if not self in node.connected:
            node.connected.append(self)
            
    def reset(self):
        self.distance = "-"
        self.target = False
        self.path = False


