import pygame
import json
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 32
SPEED = {'projectile': 1000}
COLOURS = {
    'white' : '#E4BDBD',
    'black' : '#1B1818',
    'lightred' : '#BF3939',
    'hoverred' : '#EF4747',
    'gray' : '#C5B5B5',
    'gold' : '#CAA314',
    'transparent' : (197, 181, 181, 128)
}
