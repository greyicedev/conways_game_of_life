import sys
import random
import pyglet

def init_grid(size):

    grid = []
    for i in range(0,size):
        grid.append([0 for i in range(0,size)])
    return grid

def random_grid():

    for i in range(0,len(grid)):
        for j in range(0, len(grid)):
            grid[j][i] = random.randint(0,1)

def populate_glider():
    
    x = int(size/2)
    y = int(size/2)
    
    grid[x + 1][y] = 1
    grid[x][y - 1] = 1
    grid[x][y + 1] = 1
    grid[x - 1][y + 1] = 1
    grid[x + 1][y + 1]  = 1
    
def calculate_neighbors(g, size, x, y):

    sum = 0
    offsets = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    for offset in offsets:
        off_x, off_y = offset
        if ((x + off_x < 0) or (x + off_x == size)) or ((y + off_y < 0) or (y + off_y == size)):
            sum += 0
        else:
            sum += g[x + off_x][y + off_y]

    return sum

def update_cells():

    new_grid = init_grid(size)

    for i in range(0,len(grid)):
        for j in range(0,len(grid)):
            if (grid[j][i] == 1) and (calculate_neighbors(grid, size, j, i) < 2):
                new_grid[j][i] = 0
            if (grid[j][i] == 1) and (calculate_neighbors(grid, size, j, i) in (2,3)):
                new_grid[j][i] = 1
            if (grid[j][i] == 1) and (calculate_neighbors(grid, size, j ,i) > 3):
                new_grid[j][i] = 0
            if (grid[j][i] == 0) and (calculate_neighbors(grid, size, j, i) == 3):
                new_grid[j][i] = 1

    return new_grid
    
def draw_grid(dt):

    global boxes
    global batch
    global grid

    boxes = []
    batch = pyglet.graphics.Batch()

    new_grid = update_cells()

    for i in range(0, len(new_grid)):
        for j in range(0, len(new_grid)):
            if new_grid[i][j] == 0:
                boxes.append(pyglet.sprite.Sprite(black,j * cell_size, i * cell_size,batch=batch))
            else:
                boxes.append(pyglet.sprite.Sprite(white,j * cell_size,i * cell_size,batch=batch))
    
    grid = new_grid
    
if __name__ == "__main__":

    size = int(sys.argv[1])
    cell_size = 4

    grid = init_grid(size)
    random_grid()

    window = pyglet.window.Window(width=size * cell_size,height=size * cell_size)

    boxes = []
    batch = pyglet.graphics.Batch()

    white = pyglet.image.load("white.png")
    black = pyglet.image.load("black.png")

    pyglet.clock.schedule_interval(draw_grid, 0.5)

    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    pyglet.app.run()

    

    
