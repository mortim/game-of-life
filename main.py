import pygame
import rle

class GOL:
    def __init__(self):
        self.cell_size = 15
        self.window_size = (80,60)
        self.grid = {}
        self.tab_birth = []
        self.tab_death = []
        self.filepath = ""
        self.load_option = False
        # ----
        self.screen = None
        pygame.display.set_caption("game of life")
        self.clock = pygame.time.Clock()
        
    def generate(self):
        self.screen.fill((255,255,255))
        for x in range(int(self.window_size[0])):
            for y in range(int(self.window_size[1])):
                self.grid[(x,y)] = False
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(x*self.cell_size,y*self.cell_size,self.cell_size,self.cell_size),1)
    
    def set_state(self,coord,state):
        surf = pygame.Surface((self.cell_size-2,self.cell_size-2))
        if state:
            surf.fill((0,0,0))
            self.grid[coord] = True
        else:
            surf.fill((255,255,255))
            self.grid[coord] = False
        self.screen.blit(surf, (coord[0]*self.cell_size+1, coord[1]*self.cell_size+1))

    def neighbours(self,coord):
        x,y=coord
        coords=[(x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y), (x+1,y), (x-1,y+1), (x,y+1), (x+1,y+1)]
        alive=0
        for c in coords:
            # Check if the neighbour cell is in the grid
            if not((c[0] < 0 or c[1] < 0) or (c[0] > self.window_size[0]-1 or c[1] > self.window_size[1]-1)):
                if self.grid[c]: alive += 1
        return alive

    def convert_mouse_coords_on_grid(self,mouse_coords):
        x,y = mouse_coords
        return (x//self.cell_size,y//self.cell_size)
    
    def menu(self):
        print("1) Load a RLE file\n2) Continue without load a file\n3) Quit the program\n")
        while True:
            choice = input("> ")
            if choice == "1":
                self.filepath = input("filepath: ")
                self.load_option = True
                return
            if choice == "2":
                return
            if choice == "3":
                exit()
            print("The command is unknown")

    def simulate(self):
        loop=True
        while loop:
            for event in pygame.event.get():
                # -------------------------------
                if event.type == pygame.QUIT: loop = False
                # -------------------------------
                elif pygame.mouse.get_pressed()[0]:
                    cell_coords = self.convert_mouse_coords_on_grid(pygame.mouse.get_pos())
                    self.set_state(cell_coords, not self.grid[cell_coords])
                # -------------------------------
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    loop_=True
                    while loop_:
                        if all(map(lambda x: not x, self.grid.values())):
                            loop_ = False

                        for event in pygame.event.get():
                            # Exit the program during the simulation
                            if event.type == pygame.QUIT:
                                loop_ = False
                                loop = False
                            # Pause the simulation
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                l=True
                                while l:
                                    for event in pygame.event.get():
                                        # Exit the program when the simulation is paused
                                        if event.type == pygame.QUIT:
                                            l = False
                                            loop_ = False
                                            loop = False

                                        elif pygame.mouse.get_pressed()[0]:
                                            cell_coords = self.convert_mouse_coords_on_grid(pygame.mouse.get_pos())
                                            self.set_state(cell_coords, not self.grid[cell_coords])
                                            pygame.display.flip()
                                        # Resume the simulation
                                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                            l = False
        
                        for (coord,_) in self.grid.items():
                            if self.grid[coord]:
                                # A cell survive only if he has 2 or 3 alive neighbours cells
                                if not(self.neighbours(coord) == 3 or self.neighbours(coord) == 2):
                                    self.tab_death.append(coord)
                            else:
                                # If a dead cell has 3 alive neighbours cells, he wil become alive
                                if self.neighbours(coord) == 3:
                                    self.tab_birth.append(coord)

                        for n in self.tab_birth:
                            self.set_state(n,True)
                        self.tab_birth=[]

                        for m in self.tab_death:
                            self.set_state(m,False)
                        self.tab_death=[]

                        pygame.display.flip()
                        pygame.time.delay(100)
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        self.menu()
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size[0]*self.cell_size, self.window_size[1]*self.cell_size))
        self.generate()
        # ----
        if self.load_option:
            r = rle.RLE(self.filepath,self.window_size)
            output = r.parse()
            print(f"Loading the '{self.filepath}' file...")
            print(f"\nThe pattern '{output['name']}' is loaded by {output['author']}\n{output['description']}")
            # ---
            for (x,y) in output["cells"]:
                self.set_state((x,y), True)
            pygame.display.flip()
        # ----
        self.simulate()

game_of_life = GOL()
game_of_life.run()