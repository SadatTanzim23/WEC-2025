'''KINGDOM OF WINDSOR 1450'''
import pygame
from random import*

pygame.init()
pygame.font.init()
pygame.mixer.init()

width, height = 1250, 700 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("KINGDOM OF WINDSOR")

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (40, 40, 40)
DARK_BLUE = (20, 20, 50)
LIGHT_GREY = (180, 180, 180)
GOLD = (220, 180, 60)

#default faunts to use
mainF = pygame.font.SysFont("Arial", 24)
bigF = pygame.font.SysFont("Arial", 40)

#music-----------------------------------------------------------------------------
#loading the music
ost=["music/ost1.ogg"]
posx = 0
pygame.mixer.music.load(ost[posx])
pygame.mixer.music.play(-1) 


#arrays of pictures
msPicList=["images/bg.png","images/name.png", "images/menu.png", "images/map.png", "images/logo.png"]
arena=["images/BP.png", "images/SV.png", "images/JA.png", "images/FP.png", "images/PP.png"]
PicPos=[(0,0),(280,20),(1150,20), (185, 180), (25, 30)]

msPicList1=[]
for img in msPicList:
    mage=pygame.image.load(img).convert_alpha()
    msPicList1.append(mage)

arenaList=[]
for img1 in arena:
    mage=pygame.image.load(img1).convert_alpha()
    arenaList.append(mage)

#defining the rects for the rects
menuRect=pygame.Rect(1150,20,70,67)
vil1=pygame.Rect(120, 200, 200, 200)
vil2=pygame.Rect(340, 200, 200, 200)
vil3=pygame.Rect(560, 200, 200, 200)
vil4=pygame.Rect(780, 200, 200, 200)
vil5=pygame.Rect(1000, 200, 200, 200)

#Load Image -------------------------------------------------------------------------
def loadImage(path, fallback_color=(100, 100, 100), size=None):#image loader function to make it easier to implement the iamges
    """Load an image but don't crash if it's missing."""
    try:
        img = pygame.image.load(path).convert_alpha()
        if size is not None:
            img = pygame.transform.smoothscale(img, size)
        return img
    except Exception as e:
        print("Could not load image:", path, "->", e)
        # fallback: colored rectangle surface
        surf = pygame.Surface(size if size else (200, 200))
        surf.fill(fallback_color)
        return surf


# menuScreen -------------------------------------------------------------------------
class menuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.font = mainF
        self.title_font = bigF
        self.buttons = []
        start_x = 200
        start_y = 200
        w = 400
        h = 60
        gap = 15

        #create the 5 village buttons
        self.villages = [
            ("Bone Pit", Village1Screen),
            ("Spell Valley",    Village2Screen),
            ("Hog Mountain",    Village3Screen),
            ("Frozen Peak", Village4Screen),
            ("Barbarian Bowl",    Village5Screen),
        ]

        for i, (name, cls) in enumerate(self.villages):# keeps looping thorugh the list
            rect = pygame.Rect(start_x, start_y + i*(h+gap), w, h)
            self.buttons.append((name, cls, rect))

        # back to main screen
        self.back_rect = pygame.Rect(20, 620, 150, 40)#the rect for the back button

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos

                    # click on village
                    for name, cls, rect in self.buttons:
                        if rect.collidepoint(mx, my):
                            village_screen = cls(self.screen)
                            village_screen.run()

                    # back
                    if self.back_rect.collidepoint(mx, my):
                        self.running = False

            self.draw()
            pygame.display.flip()

    def draw(self):
        self.screen.fill((10, 10, 30))

        title = self.title_font.render("Village Selection", True, GOLD)
        self.screen.blit(title, (width//2 - title.get_width()//2, 80))

        for name, cls, rect in self.buttons:
            pygame.draw.rect(self.screen, (80, 80, 120), rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            txt = self.font.render(name, True, WHITE)
            self.screen.blit(txt, (rect.x + 10, rect.y + 18))

        pygame.draw.rect(self.screen, (120, 0, 0), self.back_rect)
        pygame.draw.rect(self.screen, BLACK, self.back_rect, 1)
        back_text = self.font.render("BACK", True, WHITE)
        self.screen.blit(back_text, (self.back_rect.x + 10, self.back_rect.y + 10))



# Villages Main Screen -----------------------------------------------------------------
class BaseVillageScreen:
    def __init__(self, screen, name, map_path, resources, stats, events):#initialzing them vairables
        self.screen = screen
        self.name = name
        self.running = True
        self.font = mainF
        self.title_font = bigF
        self.mapRect = pygame.Rect(20, 50, 700, 600)          # left side
        self.panelRect = pygame.Rect(750, 50, 480, 600)       # right side

        # tabs
        self.tabNames = ["Resources", "Stats", "Events"]
        self.tabs = []
        tab_w = self.panelRect.width // 3
        for i, tname in enumerate(self.tabNames):
            self.tabs.append(
                (tname, pygame.Rect(self.panelRect.x + i * tab_w,
                                    self.panelRect.y,
                                    tab_w,
                                    40))
            )
        self.current_tab = "Resources"
        #initializing
        self.resources = resources
        self.stats = stats
        self.events = events[:]

        self.mapImage = loadImage(map_path, size=(self.mapRect.width, self.mapRect.height))

        # back button
        self.backRect = pygame.Rect(self.panelRect.x, self.panelRect.bottom - 50, 150, 40)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos

                    # tabs
                    for tname, rect in self.tabs:
                        if rect.collidepoint(mx, my):
                            self.current_tab = tname

                    # back button
                    if self.backRect.collidepoint(mx, my):
                        self.running = False

            self.draw()
            pygame.display.flip()

    def draw(self):
        self.screen.fill(DARK_BLUE)

        # title
        title = self.title_font.render(self.name, True, GOLD)
        self.screen.blit(title, (20, 5))

        pygame.draw.rect(self.screen, BLACK, self.mapRect, 2)#the mapp on the lfet of the screen
        screen.blit(arenaList[0], (300, 200))
        self.screen.blit(self.mapImage, self.mapRect.topleft)

        pygame.draw.rect(self.screen, GREY, self.panelRect)#right panel ofo teh screen

        pygame.draw.rect(self.screen, BLACK, self.panelRect, 2)

        # tabs
        for tname, rect in self.tabs:
            color = LIGHT_GREY if tname == self.current_tab else (100, 100, 100)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)
            label = self.font.render(tname, True, BLACK)
            self.screen.blit(label, (rect.x + 10, rect.y + 10))

        # content area under tabs
        contentRect = pygame.Rect(self.panelRect.x + 10,
                                   self.panelRect.y + 50,
                                   self.panelRect.width - 20,
                                   self.panelRect.height - 110)
        pygame.draw.rect(self.screen, (30, 30, 30), contentRect)
        pygame.draw.rect(self.screen, BLACK, contentRect, 1)

        # draw content based on current tab
        if self.current_tab == "Resources":
            self.draw_resources(contentRect)
        elif self.current_tab == "Stats":
            self.draw_stats(contentRect)
        elif self.current_tab == "Events":
            self.draw_events(contentRect)

        # back button
        pygame.draw.rect(self.screen, (120, 0, 0), self.backRect)
        pygame.draw.rect(self.screen, BLACK, self.backRect, 1)
        backText = self.font.render("Back to Menu", True, WHITE)
        self.screen.blit(backText, (self.backRect.x + 5, self.backRect.y + 10))

    def draw_resources(self, rect):
        x = rect.x + 10
        y = rect.y + 10
        line_h = 28
        title = self.font.render("Resources & Production / Year", True, GOLD)
        self.screen.blit(title, (x, y))
        y += line_h * 2

        for rname, (amount, prod) in self.resources.items():
            line = f"{rname}: {amount} ( +{prod} / year )"
            txt = self.font.render(line, True, WHITE)
            self.screen.blit(txt, (x, y))
            y += line_h

    def draw_stats(self, rect):
        x = rect.x + 10
        y = rect.y + 10
        line_h = 28
        title = self.font.render("Village Statistics", True, GOLD)
        self.screen.blit(title, (x, y))
        y += line_h * 2

        for key, val in self.stats.items():
            if key == "tax_rate":
                line = f"Tax rate: {val}%"
            elif key == "sustainability":
                line = f"Sustainability: {val}/100"
            else:
                line = f"{key.replace('_', ' ').title()}: {val}"
            txt = self.font.render(line, True, WHITE)
            self.screen.blit(txt, (x, y))
            y += line_h

    def draw_events(self, rect):
        x = rect.x + 10
        y = rect.y + 10
        line_h = 28
        title = self.font.render("Recent Events", True, GOLD)
        self.screen.blit(title, (x, y))
        y += line_h * 2

        if not self.events:
            txt = self.font.render("No major events recorded.", True, WHITE)
            self.screen.blit(txt, (x, y))
        else:
            for e in self.events[-8:]:  # last 8 events max
                txt = self.font.render(f"- {e}", True, WHITE)
                self.screen.blit(txt, (x, y))
                y += line_h


# Village1 ----------------------------------------------------------------------------
class Village1Screen(BaseVillageScreen):
    def __init__(self, screen):
        resources = {
            "Wood": (500, 120),
            "Iron": (200, 40),
            "Grain": (800, 200),
            "Stone": (350, 60),
            "Gold": (150, 15),
        }
        stats = {
            "population": 1200,
            "tax_rate": 12,
            "sustainability": 78,
            "total_resources": sum(v[0] for v in resources.values())
        }
        events = [
            "Spring harvest was abundant.",
            "Mild winter increased grain reserves.",
            "New sawmill built near the forest.",
        ]
        super().__init__(screen, "Bone Pit",
                         "images/village1.png",
                         resources, stats, events)
        

# Village2 ----------------------------------------------------------------------------
class Village2Screen(BaseVillageScreen):
    def __init__(self, screen):
        resources = {
            "Wood": (300, 60),
            "Iron": (600, 150),
            "Grain": (400, 80),
            "Stone": (500, 90),
            "Gold": (220, 20),
        }
        stats = {
            "population": 900,
            "tax_rate": 15,
            "sustainability": 70,
            "total_resources": sum(v[0] for v in resources.values())
        }
        events = [
            "New iron vein discovered in the mines.",
            "Minor cave-in slowed production.",
        ]
        super().__init__(screen, "Spell Valley",
                         "images/village2.png",
                         resources, stats, events)
        
# Village3 ----------------------------------------------------------------------------
class Village3Screen(BaseVillageScreen):
    def __init__(self, screen):
        resources = {
            "Wood": (250, 50),
            "Iron": (180, 35),
            "Grain": (900, 220),
            "Stone": (260, 40),
            "Gold": (300, 30),
        }
        stats = {
            "population": 1500,
            "tax_rate": 10,
            "sustainability": 82,
            "total_resources": sum(v[0] for v in resources.values())
        }
        events = [
            "Grand market festival increased trade.",
            "Light flooding near the river docks.",
        ]
        super().__init__(screen, "Hog Mountain",
                         "images/village3.png",
                         resources, stats, events)
        
    # Village4 ----------------------------------------------------------------------------
class Village4Screen(BaseVillageScreen):
    def __init__(self, screen):
        resources = {
            "Wood": (700, 170),
            "Iron": (280, 45),
            "Grain": (450, 100),
            "Stone": (650, 120),
            "Gold": (180, 18),
        }
        stats = {
            "population": 1100,
            "tax_rate": 13,
            "sustainability": 75,
            "total_resources": sum(v[0] for v in resources.values())
        }
        events = [
            "Strong winds damaged a few rooftops.",
            "Guild of masons repaired the main tower.",
        ]
        super().__init__(screen, "Frozen Peak",
                         "images/village4.png",
                         resources, stats, events)
        
# Village4 ----------------------------------------------------------------------------
class Village5Screen(BaseVillageScreen):
    def __init__(self, screen):
        resources = {
            "Wood": (400, 90),
            "Iron": (260, 55),
            "Grain": (500, 130),
            "Stone": (300, 50),
            "Gold": (500, 60),
        }
        stats = {
            "population": 1000,
            "tax_rate": 18,
            "sustainability": 68,
            "total_resources": sum(v[0] for v in resources.values())
        }
        events = [
            "Caravan from distant lands brought exotic goods.",
            "Bandits were sighted near the trade road.",
        ]
        super().__init__(screen, "Barbarian Bowl",
                         "images/village5.png",
                         resources, stats, events)



# Main loop ----------------------------------------------------------------------------
running = True
clock = pygame.time.Clock()  #to limit FPS

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:#left click
                if menuRect.collidepoint(event.pos):
                    menu=menuScreen(screen)
                    menu.run()

        
                if menuRect.collidepoint(event.pos):
                    menu=menuScreen(screen)
                    menu.run()
    # fill background (blank canvas)
    screen.fill(WHITE)


    # draw the selected image
    for i in range(len(msPicList1)):
        screen.blit(msPicList1[i], PicPos[i])

    # later you can draw your tools, UI, shapes, etc. here
    #pygame.draw.rect(screen, (255, 0, 0), menuRect, 2)

    mx, my = pygame.mouse.get_pos()
    print(mx, my)  # shows in the console (terminal)

    #screen.fill((255, 255, 255))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()   