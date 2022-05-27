import pygame
import rle

print("1) Load a RLE file\n2) Continue without load a file\n3) Quit the program\n")
loop = True
load_file_option = False
filepath = ""
while loop:
    choice = input("> ")
    if choice == "1":
        filepath = input("filepath: ")
        load_file_option = True
        loop = False
    elif choice == "2":
        loop = False
    elif choice == "3":
        exit()
    else:
        print("The command is unknown")

pygame.init()

# Initial configuration
CELL_SIZE=15
WINDOW_SIZE=(80,60)
TAB_BIRTH=[]
TAB_DEATH=[]
# ---
screen = pygame.display.set_mode((WINDOW_SIZE[0]*CELL_SIZE, WINDOW_SIZE[1]*CELL_SIZE))
pygame.display.set_caption("Conway_gol")
clock = pygame.time.Clock()

# Generate the cell grid
def generate(w,h,size):
    screen.fill((255,255,255))
    res={}
    for x in range(w):
        for y in range(h):
            res[(x,y)] = False
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x*size,y*size,size,size),1)
    return res

GRID = generate(*WINDOW_SIZE,CELL_SIZE)

# Set a cell alive or dead 
def setState(coord,state):
    surf = pygame.Surface((CELL_SIZE-2,CELL_SIZE-2))
    if state:
        surf.fill((0,0,0))
        GRID[coord] = True
    else:
        surf.fill((255,255,255))
        GRID[coord] = False
    screen.blit(surf, (coord[0]*CELL_SIZE+1, coord[1]*CELL_SIZE+1))

# Get the number of the alive neighbours cells
def neighbours(coord):
    x,y=coord
    coords=[(x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y), (x+1,y), (x-1,y+1), (x,y+1), (x+1,y+1)]
    alive=0
    for c in coords:
        # Check if the neighbour cell is in the grid
        if not((c[0] < 0 or c[1] < 0) or (c[0] > WINDOW_SIZE[0]-1 or c[1] > WINDOW_SIZE[1]-1)):
            if GRID[c]: alive += 1
    return alive

def changeCellState(coords):
    (x,y) = coords
    cell_coords=(x//CELL_SIZE,y//CELL_SIZE)
    if GRID[cell_coords]:
        setState(cell_coords, False)
    else:
        setState(cell_coords, True)

if load_file_option:
    r = rle.RLE(filepath,(10,10))
    output = r.parse()
    print(f"Loading the '{filepath}' file...")
    print(f"""
The pattern '{output["name"]}' is loaded by {output["author"]}
{output["description"]}
    """)
    for (x,y) in output["cells"]:
        setState((x,y), True)
    pygame.display.flip()

loop=True
while loop:
    for event in pygame.event.get():
        # -------------------------------
        if event.type == pygame.QUIT: loop = False
        # -------------------------------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            changeCellState(pygame.mouse.get_pos())
        # -------------------------------
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            while loop:
                for event in pygame.event.get():
                    # Exit the program during the simulation
                    if event.type == pygame.QUIT: loop = False
                    # Pause the simulation
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        l=True
                        while l:
                            for event in pygame.event.get():
                                # Exit the program when the similation is paused
                                if event.type == pygame.QUIT:
                                    l=False
                                    loop = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    changeCellState(pygame.mouse.get_pos())
                                    pygame.display.flip()
                                # Resume the simulation
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                    l = False

                for (coord,_) in GRID.items():
                    if GRID[coord]:
                        # A cell survive only if he has 2 or 3 alive neighbours cells
                        if not(neighbours(coord) == 3 or neighbours(coord) == 2):
                            TAB_DEATH.append(coord)
                    else:
                        # If a dead cell has 3 alive neighbours cells, he wil become alive
                        if neighbours(coord) == 3:
                            TAB_BIRTH.append(coord)

                for n in TAB_BIRTH:
                    setState(n,True)
                TAB_BIRTH=[]

                for m in TAB_DEATH:
                    setState(m,False)
                TAB_DEATH=[]

                pygame.display.flip()
                pygame.time.delay(100)
    pygame.display.flip()
    clock.tick(60)