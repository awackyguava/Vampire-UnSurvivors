import pygame
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 32
SPEED = {'enemy': 150, 'projectile': 1000}
## TODO make stat list
STATS = {
    'damage' : 10,
    'health' : 100,
    'speed' : 220,
} 
COLOURS = {
    'white' : '#E4BDBD',
    'black' : '#1B1818',
    'lightred' : '#BF3939',
    'hoverred' : '#EF4747',
    'gray' : '#C5B5B5',
}
