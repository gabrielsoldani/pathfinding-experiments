from collections import deque

# Size of a tile, in pixels
TILE_SIZE = 20

# Screen dimensions, in tiles
SCREEN_WIDTH = 20
SCREEN_HEIGHT = 15

GROUND = 0
WALL = 1

world = [
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND,   WALL, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND,   WALL, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND,   WALL, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND,   WALL, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND],
        [GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND, GROUND]
        ]
      
player_x = -1
player_y = -1

target_x = -1
target_y = -1

STATE_SELECTING_PLAYER = 0
STATE_SELECTING_TARGET = 1
STATE_CALCULATING = 2
STATE_READY = 3

state = STATE_SELECTING_PLAYER

def in_bounds(x, y):
    """Returns true if the tile at (x, y) is within the screen bounds"""
    return x >= 0 and x < SCREEN_WIDTH and y >= 0 and y < SCREEN_HEIGHT
    
def can_walk(x, y):
    """Returns true if the player can walk over the tile at (x, y)"""
    return world[y][x] == GROUND
    
def adjacent(x, y):
    """Returns the tiles the player in (x, y) can reach in one step"""
    result = []
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        pos_x, pos_y = x + dx, y + dy
        if in_bounds(pos_x, pos_y) and can_walk(pos_x, pos_y):
            result.append((pos_x, pos_y))
    return result

def tiles_to_pixels(tiles):
    """Converts tiles to pixels"""
    return tiles * TILE_SIZE
      
def pixels_to_tiles(pixels):
    """Converts pixels to tiles"""
    return pixels / TILE_SIZE
      
def setup():
    size(SCREEN_WIDTH * TILE_SIZE + 1, SCREEN_HEIGHT * TILE_SIZE + 1)
    
lastMousePressed = False

def update():
    """Updates the state of the world"""
    global state
    global lastMousePressed
    global player_x
    global player_y
    global target_x
    global target_y
    
    clicked = lastMousePressed == True and mousePressed == False    
    lastMousePressed = mousePressed
    
    if state == STATE_SELECTING_PLAYER:
        if clicked:
            mouse_x = pixels_to_tiles(pmouseX)
            mouse_y = pixels_to_tiles(pmouseY)
            
            if in_bounds(mouse_x, mouse_y) and can_walk(mouse_x, mouse_y):
                player_x, player_y = mouse_x, mouse_y
                state = STATE_SELECTING_TARGET
            
    elif state == STATE_SELECTING_TARGET:
        if clicked:
            mouse_x = pixels_to_tiles(pmouseX)
            mouse_y = pixels_to_tiles(pmouseY)
            
            if in_bounds(mouse_x, mouse_y) and can_walk(mouse_x, mouse_y):
                target_x, target_y = mouse_x, mouse_y
                state = STATE_CALCULATING
                bfs_init()
        
    elif state == STATE_CALCULATING:
        if bfs_loop():
            state = STATE_READY
            x, y = target_x, target_y
            path.appendleft((x, y))
            while source[y][x] != (player_x, player_y):
                x, y = source[y][x]
                path.appendleft((x, y))
    
def draw():
    """Draws the state of the world"""
    update()
    background(255)
    stroke(0)
    fill(255)
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            if len(frontier) > 0 and (x, y) == frontier[0]:
                fill(0, 0, 255)
            elif (x, y) == (player_x, player_y):
                fill(0, 255, 255)
            elif (x, y) == (target_x, target_y):
                fill(255, 0, 0)
            elif (x, y) in path:
                fill(255)
            elif (x, y) in frontier:
                fill(128)
            elif discovered[y][x]:
                fill(64)
            elif can_walk(x, y):
                fill(0)
            else:
                fill(0, 255, 0)
            
            rect(tiles_to_pixels(x), tiles_to_pixels(y), tiles_to_pixels(1), tiles_to_pixels(1))

frontier = deque()
discovered = [x[:] for x in [[False] * SCREEN_WIDTH] * SCREEN_HEIGHT]
source = [x[:] for x in [[(-1, -1)] * SCREEN_WIDTH] * SCREEN_HEIGHT]
print source
path = deque()
    
def bfs_loop():
    global discovered
    global source
       

    x, y = frontier.popleft()
    discovered[y][x] = True
   
   
    if (x, y) == (target_x, target_y):
        return True
        
    for el in adjacent(x, y):
        if not discovered[el[1]][el[0]] and (x, y) not in frontier:
            source[el[1]][el[0]] = (x, y)
            frontier.append(el)
           
    return False
            
def bfs_init():
    frontier.append((player_x, player_y))