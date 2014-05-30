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

world = [x[:] for x in [[GROUND] * SCREEN_HEIGHT] * SCREEN_WIDTH]

player = (-1, -1)
target = (-1, -1)

STATE_SELECTING_PLAYER = 0
STATE_SELECTING_TARGET = 1
STATE_CALCULATING = 2
STATE_READY = 3

state = STATE_SELECTING_PLAYER

def tiles():
    for x in xrange(SCREEN_WIDTH):
        for y in xrange(SCREEN_HEIGHT):
            yield (x, y)

def in_bounds(p):
    """Returns true if the tile p is within the screen bounds"""
    x, y = p
    return x >= 0 and x < SCREEN_WIDTH and y >= 0 and y < SCREEN_HEIGHT

def can_walk(p):
    """Returns true if the player can walk over the tile at p."""
    x, y = p
    return world[x][y] == GROUND

def sum_points(a, b):
    """Returns the sum of two points a and b."""
    return a[0] + b[0], a[1] + b[1]

def adjacents(p):
    """Returns the tiles the player in tile p can reach in one step"""
    result = []
    for adj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        q = sum_points(p, adj)
        if in_bounds(q) and can_walk(q):
            result.append(q)
    return result

def tiles_to_pixels(p):
    """Converts a point or rectangle in tiles to pixels"""
    return tuple(x * TILE_SIZE for x in p)

def pixels_to_tiles(p):
    """Converts a point or rectangle in pixels to tiles"""
    return tuple(x / TILE_SIZE for x in p)

def toggle_tile(p):
    x, y = p

    if world[x][y] == GROUND:
        world[x][y] = WALL
    else:
        world[x][y] = GROUND

def setup():
    w, h = sum_points(tiles_to_pixels((SCREEN_WIDTH, SCREEN_HEIGHT)), (1, 1))
    size(w, h)

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

    mouse_tile = pixels_to_tiles(mouse)

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

    mouse_tile = pixels_to_tiles(mouse)

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

def get_color(p):
    if len(frontier) > 0 and p == frontier[0]:
        return 0xAA, 0x66, 0xCC
    elif p == player:
        return 0x33, 0xB5, 0xE5
    elif p == target:
        return 0xFF, 0x44, 0x00
    elif p in path:
        return 0xFF, 0xFF, 0xFF
    elif p in frontier:
        return 0x80, 0x80, 0x80
    elif p in discovered:
        return 0x55, 0x55, 0x55
    elif can_walk(p):
        return 0x33, 0x33, 0x33
    else:
        return 0xFF, 0xBB, 0x33

def draw():
    """Draws the state of the world"""
    update()
    stroke(0x00, 0x00, 0x00)

    for p in tiles():
        c = get_color(p)

        fill(c[0], c[1], c[2])

        r = tiles_to_pixels(p + (1, 1))

        rect(r[0], r[1], r[2], r[3])

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