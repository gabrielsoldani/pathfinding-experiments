from collections import deque

# Size of a tile, in pixels
TILE_SIZE = 32

# Screen dimensions, in tiles
SCREEN_WIDTH = 20
SCREEN_HEIGHT = 15

# If set to True, each draw call will do one step of the algorithm.
# If set to False, the algorithm will be solved in one draw call.
SHOW_STEPS = True

GROUND = 0
WALL = 1

world = [x[:] for x in [[GROUND] * SCREEN_WIDTH] * SCREEN_HEIGHT]

player = (-1, -1)
target = (-1, -1)

STATE_SELECTING_PLAYER = 0
STATE_SELECTING_TARGET = 1
STATE_CALCULATING = 2
STATE_READY = 3

state = STATE_SELECTING_PLAYER

def in_bounds(p):
    """Returns true if the tile p is within the screen bounds"""
    x, y = p
    return x >= 0 and x < SCREEN_WIDTH and y >= 0 and y < SCREEN_HEIGHT

def can_walk(p):
    """Returns true if the player can walk over the tile at p."""
    x, y = p
    return world[y][x] == GROUND

def sum_tiles(a, b):
    """Returns the sum of two tiles a and b."""
    return a[0] + b[0], a[1] + b[1]

def adjacents(p):
    """Returns the tiles the player in tile p can reach in one step"""
    result = []
    for adj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        q = sum_tiles(p, adj)
        if in_bounds(q) and can_walk(q):
            result.append(q)
    return result

def tiles_to_pixels(tiles):
    """Converts tiles to pixels"""
    return tiles * TILE_SIZE

def pixels_to_tiles(pixels):
    """Converts pixels to tiles"""
    return pixels / TILE_SIZE

def toggle_tile(p):
    x, y = p

    if world[y][x] == GROUND:
        world[y][x] = WALL
    else:
        world[y][x] = GROUND

def setup():
    size(SCREEN_WIDTH * TILE_SIZE + 1, SCREEN_HEIGHT * TILE_SIZE + 1)

lastMousePressed = False

def update():
    """Updates the state of the world"""
    global lastMousePressed

    mouse = (pmouseX, pmouseY)
    clicked = lastMousePressed == True and mousePressed == False
    button = mouseButton

    lastMousePressed = mousePressed

    if state == STATE_SELECTING_PLAYER:
        func = update_selecting_player
    elif state == STATE_SELECTING_TARGET:
        func = update_selecting_target
    elif state == STATE_CALCULATING:
        func = update_calculating
    else:
        func = update_ready

    func(mouse, clicked, button)

def update_selecting_player(mouse, clicked, button):
    global state, player

    if not clicked:
        return

    mouse_tile = tuple(pixels_to_tiles(x) for x in mouse)

    if not in_bounds(mouse_tile):
        return

    if mouseButton == RIGHT:
        toggle_tile(mouse_tile)
        return

    if not can_walk(mouse_tile):
        return

    player = mouse_tile
    state = STATE_SELECTING_TARGET

def update_selecting_target(mouse, clicked, button):
    global state, target

    if not clicked:
        return

    mouse_tile = tuple(pixels_to_tiles(x) for x in mouse)

    if not in_bounds(mouse_tile):
        return

    if mouseButton == RIGHT:
        toggle_tile(mouse_tile)
        return

    if not can_walk(mouse_tile):
        return

    target = mouse_tile
    state = STATE_CALCULATING

    init_algorithm()

def update_calculating(mouse, clicked, button):
    global state

    if SHOW_STEPS:
        if not loop_algorithm():
            return
    else:
        while not loop_algorithm():
            pass

    path_algorithm()
    state = STATE_READY

def update_ready(mouse, clicked, button):
    pass

def draw():
    """Draws the state of the world"""
    update()
    background(255)
    stroke(0)
    fill(255)
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            p = (x, y)
            if len(frontier) > 0 and p == frontier[0]:
                fill(0xAA, 0x66, 0xCC)
            elif p == player:
                fill(0x33, 0xB5, 0xE5)
            elif p == target:
                fill(0xFF, 0x44, 0x00)
            elif p in path:
                fill(0xFF)
            elif p in frontier:
                fill(0x80)
            elif p in discovered:
                fill(0x55)
            elif can_walk(p):
                fill(0x33)
            else:
                fill(0xFF, 0xBB, 0x33)

            rect(tiles_to_pixels(x), tiles_to_pixels(y), tiles_to_pixels(1), tiles_to_pixels(1))

frontier = deque()
discovered = set()
source = {}
path = deque()

def path_algorithm():
    p = target
    path.appendleft(p)
    while p in source and source[p] != player:
        p = source[p]
        path.appendleft(p)

def init_algorithm():
    global frontier, discovered, source, path

    frontier = deque()
    discovered = set()
    source = {}
    path = deque()

    frontier.append(player)
    discovered.add(player)

def loop_algorithm():
    if len(frontier) == 0:
        return True

    p = frontier.popleft()

    if p == target:
        return True

    for q in adjacents(p):
        if q not in discovered:
            frontier.append(q)
            discovered.add(q)

            source[q] = p

    return False