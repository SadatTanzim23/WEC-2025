import pygame
import sys
import time
import random
import math
from collections import deque

pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Medieval Kingdom Resource Management System - WEC 2025")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 200)
GOLD = (255, 215, 0)
GRAY = (150, 150, 150)
DARK_GREEN = (0, 100, 0)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
PURPLE = (147, 112, 219)
LAND_COLORS = [(200, 230, 200), (200, 200, 230), (230, 200, 200), (230, 230, 200), (200, 230, 230)]


font_large = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 22)
font_tiny = pygame.font.Font(None, 18)




SEASONS = ['Spring', 'Summer', 'Fall', 'Winter']
SEASON_EFFECTS = {
    'Spring': {'crops': 1.2, 'grain': 1.2, 'population_growth': 1.1},
    'Summer': {'crops': 1.5, 'fish': 1.3, 'population_growth': 1.2},
    'Fall': {'grain': 1.3, 'crops': 1.1, 'wood': 1.2},
    'Winter': {'crops': 0.5, 'fish': 0.7, 'population_growth': 0.8, 'wood': 1.3}
}


BUILDINGS = {
    'granary': {'cost': {'wood': 20, 'stone': 15}, 'effect': 'storage', 'bonus': 1.2},
    'market': {'cost': {'wood': 25, 'gold': 10}, 'effect': 'trade', 'bonus': 1.3},
    'mine': {'cost': {'wood': 30, 'stone': 20}, 'effect': 'production', 'bonus': 1.4},
    'farm': {'cost': {'wood': 15, 'stone': 10}, 'effect': 'food', 'bonus': 1.3},
    'barracks': {'cost': {'wood': 40, 'stone': 30, 'iron': 15}, 'effect': 'defense', 'bonus': 1.5}
}


ACHIEVEMENTS = [
    {'id': 'pop_1000', 'name': 'Growing Kingdom', 'desc': 'Reach 1000 total population', 'unlocked': False},
    {'id': 'sustain_90', 'name': 'Eco Warrior', 'desc': 'All villages above 90% sustainability', 'unlocked': False},
    {'id': 'prosper_500', 'name': 'Prosperous Realm', 'desc': 'Reach 500 prosperity score', 'unlocked': False},
    {'id': 'trade_100', 'name': 'Master Trader', 'desc': 'Complete 100 trades', 'unlocked': False},
    {'id': 'survive_50', 'name': 'Survivor', 'desc': 'Survive 50 ticks', 'unlocked': False}
]


SPECIALIZATIONS = {
    'Arena 1': {'wood': 1.5, 'stone': 1.2},
    'Arena 2': {'fish': 1.5, 'water': 1.3},
    'Arena 3': {'crops': 1.5, 'livestock': 1.3},
    'Arena 4': {'grain': 1.5, 'iron': 1.2},
    'Arena 5': {'gold': 1.5, 'stone': 1.2}
}


class Village:
    def __init__(self, name, pos, population, resources, production):
        self.name = name
        self.pos = pos
        self.population = population
        self.resources = resources
        self.production = production
        self.trade_queue = []
        self.labor_limit = population // 10
        self.event_history = []
        self.tax_rate = 0.1
        self.sustainability_score = 100
        self.happiness = 100
        self.buildings = []
        self.specialization = SPECIALIZATIONS.get(name, {})
    
    def produce(self, season_effects):
        labor_efficiency = min(1.0, self.labor_limit / 50)
        happiness_modifier = self.happiness / 100
        
        
        building_bonus = 1.0
        if 'mine' in self.buildings:
            building_bonus *= 1.4
        if 'farm' in self.buildings:
            building_bonus *= 1.3
        
        for res, amount in self.production.items():
            
            produced = amount * labor_efficiency * happiness_modifier * building_bonus
            
    
            if res in self.specialization:
                produced *= self.specialization[res]
            
        
            if res in season_effects:
                produced *= season_effects[res]
            
            self.resources[res] = self.resources.get(res, 0) + produced
    
    def grow_population(self, season_modifier):
       
        food = self.resources.get('grain', 0) + self.resources.get('crops', 0) + self.resources.get('fish', 0)
        happiness_factor = self.happiness / 100
        
        if food > self.population * 0.1:
            growth = int(self.population * 0.02 * happiness_factor * season_modifier)
            self.population += growth
            self.labor_limit = self.population // 10
        elif food < self.population * 0.05:
            decline = int(self.population * 0.01)
            self.population = max(0, self.population - decline)
            self.labor_limit = self.population // 10
            self.happiness = max(0, self.happiness - 5)
    
    def calculate_happiness(self):
        
        self.happiness = 100
        
       
        for res, amt in self.resources.items():
            if amt < 10:
                self.happiness -= 5
        
        
        if self.population > 1000:
            self.happiness -= 10
        
    
        recent_bad = sum(1 for e in self.event_history[-5:] if e in ['Plague', 'Drought', 'Famine', 'Bandits'])
        self.happiness -= recent_bad * 5
        
        self.happiness = max(0, min(100, self.happiness))
    
    def collect_taxes(self):
        gold = self.resources.get('gold', 0)
        happiness_factor = self.happiness / 100
        tax_collected = gold * self.tax_rate * happiness_factor
        self.resources['gold'] = gold - tax_collected
        return tax_collected
    
    def calculate_sustainability(self):
        
        score = 100
        for res, amount in self.resources.items():
            if amount < 10:
                score -= 10
            elif amount > 200:
                score -= 5
        if self.population < 100:
            score -= 20
        self.sustainability_score = max(0, min(100, score))
        return self.sustainability_score
    
    def process_trades(self):
        
        new_queue = []
        for trade in self.trade_queue:
            resource, amount, destination, ticks = trade
            if ticks <= 1:
                destination.resources[resource] = destination.resources.get(resource, 0) + amount
            else:
                new_queue.append((resource, amount, destination, ticks - 1))
        self.trade_queue = new_queue
    
    def build_structure(self, building_type):
        if building_type in BUILDINGS:
            costs = BUILDINGS[building_type]['cost']
            can_build = all(self.resources.get(res, 0) >= amt for res, amt in costs.items())
            
            if can_build and building_type not in self.buildings:
                for res, amt in costs.items():
                    self.resources[res] -= amt
                self.buildings.append(building_type)
                
                return True
        return False


class Notification:
    def __init__(self, message, type='info'):
        self.message = message
        self.type = type  
        self.lifetime = 180 
        self.alpha = 255
    
    def update(self):
        self.lifetime -= 1
        if self.lifetime < 60:
            self.alpha = int((self.lifetime / 60) * 255)
    
    def is_alive(self):
        return self.lifetime > 0
    
    def draw(self, screen, y_pos):
        colors = {
            'info': BLUE,
            'good': GREEN,
            'bad': RED,
            'achievement': GOLD
        }
        color = colors.get(self.type, GRAY)
        
      
        box_width = 400
        box_height = 60
        box_x = WIDTH - box_width - 20
        
        
        surface = pygame.Surface((box_width, box_height))
        surface.set_alpha(self.alpha)
        surface.fill(color)
        screen.blit(surface, (box_x, y_pos))
        
        pygame.draw.rect(screen, BLACK, (box_x, y_pos, box_width, box_height), 3)
        
        
        icon_x = box_x + 10
        icon_y = y_pos + 15
        if self.type == 'good':
            pygame.draw.circle(screen, WHITE, (icon_x + 15, icon_y + 15), 12)
            pygame.draw.line(screen, color, (icon_x + 8, icon_y + 15), (icon_x + 13, icon_y + 22), 3)
            pygame.draw.line(screen, color, (icon_x + 13, icon_y + 22), (icon_x + 22, icon_y + 8), 3)
        elif self.type == 'bad':
            pygame.draw.circle(screen, WHITE, (icon_x + 15, icon_y + 15), 12)
            pygame.draw.line(screen, color, (icon_x + 8, icon_y + 8), (icon_x + 22, icon_y + 22), 3)
            pygame.draw.line(screen, color, (icon_x + 22, icon_y + 8), (icon_x + 8, icon_y + 22), 3)
        elif self.type == 'achievement':
            pygame.draw.polygon(screen, WHITE, [
                (icon_x + 15, icon_y + 5),
                (icon_x + 18, icon_y + 12),
                (icon_x + 26, icon_y + 12),
                (icon_x + 20, icon_y + 17),
                (icon_x + 23, icon_y + 25),
                (icon_x + 15, icon_y + 20),
                (icon_x + 7, icon_y + 25),
                (icon_x + 10, icon_y + 17),
                (icon_x + 4, icon_y + 12),
                (icon_x + 12, icon_y + 12)
            ])
        
        
        text = font_small.render(self.message, True, WHITE)
        text_surface = pygame.Surface((text.get_width(), text.get_height()))
        text_surface.set_alpha(self.alpha)
        text_surface.blit(text, (0, 0))
        screen.blit(text, (box_x + 50, y_pos + 20))


class Kingdom:
    def __init__(self, villages):
        self.villages = villages
        self.time = 0
        self.prosperity_score = 0
        self.total_taxes = 0
        self.event_log = deque(maxlen=10)
        self.paused = False
        self.season_index = 0
        self.current_season = SEASONS[0]
        self.notifications = []
        self.total_trades = 0
        self.achievements_unlocked = 0
    
    def update(self):
        
        if self.paused:
            return
        
        self.time += 1
        
        
        if self.time % 20 == 0:
            self.season_index = (self.season_index + 1) % 4
            self.current_season = SEASONS[self.season_index]
            self.add_notification(f"Season changed to {self.current_season}", 'info')
        
        season_effects = SEASON_EFFECTS[self.current_season]
        pop_modifier = season_effects.get('population_growth', 1.0)
        
        
        for village in self.villages:
            village.produce(season_effects)
            village.grow_population(pop_modifier)
            village.calculate_happiness()
            self.total_taxes += village.collect_taxes()
            village.process_trades()
            village.calculate_sustainability()
        
     
        for village in self.villages:
            if random.random() < 0.08:  
                self.trigger_event(village)
        
        
        self.auto_trade()
        
        
        self.calculate_prosperity()
        
        
        self.check_achievements()
        
        
        self.notifications = [n for n in self.notifications if n.is_alive()]
        for n in self.notifications:
            n.update()
    
    def add_notification(self, message, type='info'):
        
        self.notifications.append(Notification(message, type))
        
    
    def trigger_event(self, village):
        
        events = [
            {
                'name': 'Drought',
                'type': 'bad',
                'effect': lambda v: self._drain_resources(v, ['grain', 'crops'], 15)
            },
            {
                'name': 'Plague',
                'type': 'bad',
                'effect': lambda v: setattr(v, 'population', max(0, v.population - 30))
            },
            {
                'name': 'Population Boom',
                'type': 'good',
                'effect': lambda v: setattr(v, 'population', v.population + 25)
            },
            {
                'name': 'Bandits',
                'type': 'bad',
                'effect': lambda v: self._drain_resources(v, list(v.resources.keys()), 8)
            },
            {
                'name': 'Rich Harvest',
                'type': 'good',
                'effect': lambda v: self._boost_resources(v, ['grain', 'crops'], 20)
            },
            {
                'name': 'Trade Caravan',
                'type': 'good',
                'effect': lambda v: v.resources.update({'gold': v.resources.get('gold', 0) + 15})
            },
            {
                'name': 'Famine',
                'type': 'bad',
                'effect': lambda v: (
                    self._drain_resources(v, ['grain', 'crops', 'fish'], 25),
                    setattr(v, 'population', max(0, v.population - 20))
                )
            },
            {
                'name': 'Festival',
                'type': 'good',
                'effect': lambda v: setattr(v, 'happiness', min(100, v.happiness + 15))
            },
            {
                'name': 'Winter Storm',
                'type': 'bad',
                'effect': lambda v: (
                    self._drain_resources(v, ['wood'], 10),
                    setattr(v, 'happiness', max(0, v.happiness - 10))
                )
            }
        ]
        
        event = random.choice(events)
        event['effect'](village)
        self.event_log.append(f"{village.name}: {event['name']}")
        village.event_history.append(event['name'])
        self.add_notification(f"{village.name}: {event['name']}!", event['type'])
    
    def _drain_resources(self, village, resources, amount):
        for res in resources:
            if res in village.resources:
                village.resources[res] = max(0, village.resources[res] - amount)
    
    def _boost_resources(self, village, resources, amount):
        for res in resources:
            village.resources[res] = village.resources.get(res, 0) + amount
    
    def auto_trade(self):
        
        resource_types = set()
        for v in self.villages:
            resource_types.update(v.resources.keys())
        
        for resource in resource_types:
            surplus = [(v, v.resources.get(resource, 0)) for v in self.villages if v.resources.get(resource, 0) > 60]
            shortage = [(v, v.resources.get(resource, 0)) for v in self.villages if v.resources.get(resource, 0) < 20]
            
            for v_surplus, amt_surplus in surplus:
                for v_shortage, amt_shortage in shortage:
                    if v_surplus != v_shortage:
                        
                        dx = v_surplus.pos[0] - v_shortage.pos[0]
                        dy = v_surplus.pos[1] - v_shortage.pos[1]
                        distance = math.sqrt(dx**2 + dy**2)
                        delay = max(2, int(distance / 200))
                        
                        trade_amount = min(10, amt_surplus - 60)
                        trade_cost = trade_amount * 0.1  
                        
                        if trade_amount > 0 and v_surplus.resources.get('gold', 0) >= trade_cost:
                            v_surplus.resources[resource] -= trade_amount
                            v_surplus.resources['gold'] = v_surplus.resources.get('gold', 0) - trade_cost
                            v_surplus.trade_queue.append((resource, trade_amount, v_shortage, delay))
                            self.total_trades += 1
    
    def calculate_prosperity(self):
        """Calculate overall kingdom prosperity"""
        total_population = sum(v.population for v in self.villages)
        total_resources = sum(sum(v.resources.values()) for v in self.villages)
        avg_sustainability = sum(v.sustainability_score for v in self.villages) / len(self.villages)
        avg_happiness = sum(v.happiness for v in self.villages) / len(self.villages)
        
        self.prosperity_score = int((total_population * 0.2 + total_resources * 0.05 + 
                                     avg_sustainability * 3 + avg_happiness * 2) / 10)
    
    def check_achievements(self):
        
        total_pop = sum(v.population for v in self.villages)
        all_sustain = all(v.sustainability_score >= 90 for v in self.villages)
        
        for achievement in ACHIEVEMENTS:
            if not achievement['unlocked']:
                unlocked = False
                
                if achievement['id'] == 'pop_1000' and total_pop >= 1000:
                    unlocked = True
                elif achievement['id'] == 'sustain_90' and all_sustain:
                    unlocked = True
                elif achievement['id'] == 'prosper_500' and self.prosperity_score >= 500:
                    unlocked = True
                elif achievement['id'] == 'trade_100' and self.total_trades >= 100:
                    unlocked = True
                elif achievement['id'] == 'survive_50' and self.time >= 50:
                    unlocked = True
                
                if unlocked:
                    achievement['unlocked'] = True
                    self.achievements_unlocked += 1
                    self.add_notification(f"Achievement: {achievement['name']}", 'achievement')


villages = [
    Village("Leamington", (150, 150), 500,
            {"wood": 50, "stone": 30, "grain": 40}, 
            {"wood": 3, "stone": 2, "grain": 1}),
    Village("Lasalle", (1150, 150), 300,
            {"water": 40, "fish": 20, "stone": 15}, 
            {"water": 2, "fish": 3, "stone": 1}),
    Village("Lakeshore", (650, 300), 450,
            {"crops": 60, "livestock": 30, "wood": 25}, 
            {"crops": 3, "livestock": 2, "wood": 1}),
    Village("Amherstburg", (300, 700), 350,
            {"grain": 40, "iron": 20, "stone": 20}, 
            {"grain": 3, "iron": 2, "stone": 1}),
    Village("Windsor", (1050, 650), 400,
            {"stone": 30, "gold": 10, "iron": 15}, 
            {"stone": 2, "gold": 2, "iron": 1})
]


lands = [
    {"points": [(0,0),(400,0),(350,350),(0,300)], "color": LAND_COLORS[0]},
    {"points": [(950,0),(1400,0),(1400,350),(1050,300)], "color": LAND_COLORS[1]},
    {"points": [(350,350),(1050,300),(1100,550),(400,600)], "color": LAND_COLORS[2]},
    {"points": [(0,300),(400,400),(350,900),(0,900)], "color": LAND_COLORS[3]},
    {"points": [(1050,300),(1400,350),(1400,900),(1100,600)], "color": LAND_COLORS[4]},
]


kingdom = Kingdom(villages)


zoomed = False
zoom_target = None
selected_tab = "resources"
show_achievements = False

def draw_resource_icon(screen, x, y, resource_type):
    
    icons = {
        'wood': ('', (139, 69, 19)),
        'stone': ('', GRAY),
        'grain': ('', (218, 165, 32)),
        'gold': ('', GOLD),
        'iron': ('️', (105, 105, 105)),
        'fish': ('', BLUE),
        'crops': ('', (34, 139, 34)),
        'water': ('', LIGHT_BLUE),
        'livestock': ('', (160, 82, 45))
    }
    
    if resource_type in icons:
        symbol, color = icons[resource_type]
        pygame.draw.circle(screen, color, (x, y), 10)
        pygame.draw.circle(screen, BLACK, (x, y), 10, 2)

def draw_map():
    
    screen.fill(WHITE)
    
    
    for land in lands:
        pygame.draw.polygon(screen, land["color"], land["points"])
    
   
    for village in villages:
        for trade in village.trade_queue:
            resource, amount, dest, ticks = trade
            start = village.pos
            end = dest.pos
            progress = 1 - (ticks / max(2, int(math.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2) / 200)))
            current_x = start[0] + (end[0] - start[0]) * progress
            current_y = start[1] + (end[1] - start[1]) * progress
            
          
            pygame.draw.line(screen, BLUE, start, end, 2)
            
       
            draw_resource_icon(screen, int(current_x), int(current_y), resource)
    

    for village in villages:
        x, y = village.pos
        
        
        if village.happiness > 70 and village.sustainability_score > 70:
            color = GREEN
        elif village.happiness > 40 and village.sustainability_score > 40:
            color = ORANGE
        else:
            color = RED
        
        pygame.draw.circle(screen, color, (x, y), 30)
        pygame.draw.circle(screen, BLACK, (x, y), 30, 3)
        
        if village.buildings:
            for i, building in enumerate(village.buildings[:3]):
                icon_x = x - 20 + i * 15
                icon_y = y - 45
                pygame.draw.rect(screen, PURPLE, (icon_x, icon_y, 10, 10))
        
        text = font_small.render(village.name, True, BLACK)
        screen.blit(text, (x-70, y-60))
        
        
        pop_text = font_tiny.render(f"Pop: {village.population}", True, BLACK)
        screen.blit(pop_text, (x-40, y+35))
        
        happiness_text = font_tiny.render(f"😊 {int(village.happiness)}%", True, BLACK)
        screen.blit(happiness_text, (x-40, y+50))
    
    draw_dashboard()
    
    y_offset = 20
    for notification in kingdom.notifications:
        notification.draw(screen, y_offset)
        y_offset += 70

def draw_dashboard():
    """Draw enhanced kingdom dashboard"""
    panel_x = 20
    panel_y = 20
    panel_w = 350
    panel_h = 280
    
    
    panel = pygame.Surface((panel_w, panel_h))
    panel.set_alpha(240)
    panel.fill((245, 245, 245))
    screen.blit(panel, (panel_x, panel_y))
    pygame.draw.rect(screen, BLACK, (panel_x, panel_y, panel_w, panel_h), 3)
    
   
    title = font_medium.render("Kingdom Dashboard", True, BLACK)
    screen.blit(title, (panel_x + 10, panel_y + 10))
    
    
    season_text = font_small.render(f"Season: {kingdom.current_season}", True, BLUE)
    screen.blit(season_text, (panel_x + 10, panel_y + 45))
    
    
    y_offset = panel_y + 75
    stats = [
        f"Time: {kingdom.time} ticks",
        f"Prosperity: {kingdom.prosperity_score}",
        f"Total Population: {sum(v.population for v in villages)}",
        f"Treasury: {int(kingdom.total_taxes)} gold",
        f"Avg Happiness: {int(sum(v.happiness for v in villages) / len(villages))}%",
        f"Total Trades: {kingdom.total_trades}",
        f"Achievements: {kingdom.achievements_unlocked}/{len(ACHIEVEMENTS)}"
    ]
    
    for stat in stats:
        text = font_small.render(stat, True, BLACK)
        screen.blit(text, (panel_x + 10, y_offset))
        y_offset += 25
    
    
    ach_button = pygame.Rect(panel_x + 10, panel_y + panel_h - 40, 150, 30)
    pygame.draw.rect(screen, GOLD, ach_button)
    pygame.draw.rect(screen, BLACK, ach_button, 2)
    ach_text = font_small.render("Achievements", True, BLACK)
    screen.blit(ach_text, (panel_x + 25, panel_y + panel_h - 35))
    
   
    log_y = HEIGHT - 220
    log_panel = pygame.Surface((450, 200))
    log_panel.set_alpha(240)
    log_panel.fill((245, 245, 245))
    screen.blit(log_panel, (20, log_y))
    pygame.draw.rect(screen, BLACK, (20, log_y, 450, 200), 3)
    
    log_title = font_medium.render("Recent Events", True, BLACK)
    screen.blit(log_title, (30, log_y + 10))
    
    y_offset = log_y + 45
    for event in list(kingdom.event_log)[-7:]:
        text = font_tiny.render(event, True, BLACK)
        screen.blit(text, (30, y_offset))
        y_offset += 22

def draw_achievements_panel():
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    panel_w = 700
    panel_h = 500
    panel_x = (WIDTH - panel_w) // 2
    panel_y = (HEIGHT - panel_h) // 2
    
    pygame.draw.rect(screen, WHITE, (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(screen, GOLD, (panel_x, panel_y, panel_w, panel_h), 5)
    
    title = font_large.render("Achievements", True, GOLD)
    screen.blit(title, (panel_x + 200, panel_y + 20))
    
    y_offset = panel_y + 80
    for achievement in ACHIEVEMENTS:
        color = GOLD if achievement['unlocked'] else GRAY
        
     
        box_rect = pygame.Rect(panel_x + 30, y_offset, panel_w - 60, 70)
        pygame.draw.rect(screen, color, box_rect)
        pygame.draw.rect(screen, BLACK, box_rect, 2)
        
        
        icon_x = panel_x + 50
        icon_y = y_offset + 25
        if achievement['unlocked']:
            pygame.draw.polygon(screen, WHITE, [
                (icon_x, icon_y - 10),
                (icon_x + 3, icon_y - 3),
                (icon_x + 10, icon_y - 3),
                (icon_x + 5, icon_y + 2),
                (icon_x + 8, icon_y + 10),
                (icon_x, icon_y + 5),
                (icon_x - 8, icon_y + 10),
                (icon_x - 5, icon_y + 2),
                (icon_x - 10, icon_y - 3),
                (icon_x - 3, icon_y - 3)
            ])
        else:
            pygame.draw.circle(screen, WHITE, (icon_x, icon_y), 12)
            pygame.draw.line(screen, color, (icon_x - 5, icon_y), (icon_x + 5, icon_y), 3)
        
        
        name_text = font_medium.render(achievement['name'], True, WHITE if achievement['unlocked'] else BLACK)
        screen.blit(name_text, (panel_x + 90, y_offset + 10))
        
        desc_text = font_small.render(achievement['desc'], True, WHITE if achievement['unlocked'] else BLACK)
        screen.blit(desc_text, (panel_x + 90, y_offset + 40))
        
        y_offset += 85
    
   
    close_text = font_medium.render("Press ESC or Click to Close", True, BLACK)
    screen.blit(close_text, (panel_x + 200, panel_y + panel_h - 50))

def draw_zoomed(village):
    
    screen.fill((245, 245, 245))
    
    
    header = pygame.Surface((WIDTH, 100))
    header.fill((50, 50, 50))
    screen.blit(header, (0, 0))
    
    title = font_large.render(f"Village of {village.name}", True, WHITE)
    screen.blit(title, (50, 20))
    
    
    if village.specialization:
        spec_text = font_small.render(f"Specialization: {', '.join(village.specialization.keys())}", True, GOLD)
        screen.blit(spec_text, (50, 60))
    
    
    back_text = font_medium.render("← Back to Map", True, WHITE)
    screen.blit(back_text, (WIDTH - 220, 35))
    
   
    tab_y = 110
    tabs = [("Resources", "resou"), ("Statistics", "stati"), ("Events", "event"), ("Buildings", "build")]
    tab_width = 180
    
    for i, (tab_name, tab_id) in enumerate(tabs):
        tab_x = 50 + i * (tab_width + 10)
        color = BLUE if selected_tab == tab_id else GRAY
        
        pygame.draw.rect(screen, color, (tab_x, tab_y, tab_width, 45))
        pygame.draw.rect(screen, BLACK, (tab_x, tab_y, tab_width, 45), 2)
        
        tab_text = font_small.render(tab_name, True, WHITE)
        screen.blit(tab_text, (tab_x + 40, tab_y + 12))
    
    
    content_y = 175
    
    if selected_tab == "resou":
        draw_resources_tab(village, content_y)
    elif selected_tab == "stati":
        draw_statistics_tab(village, content_y)
    elif selected_tab == "event":
        draw_events_tab(village, content_y)
    elif selected_tab == "build":
        draw_buildings_tab(village, content_y)

def draw_resources_tab(village, y):
    
    x = 100
    y_offset = y
    
    resources_list = list(village.resources.items())
    col = 0
    
    for i, (res, amt) in enumerate(resources_list):
        if i > 0 and i % 6 == 0:
            col += 1
            y_offset = y
        
        current_x = x + col * 600
        
    
        draw_resource_icon(screen, current_x, y_offset + 15, res)
        
     
        text = font_medium.render(f"{res.capitalize()}:", True, BLACK)
        screen.blit(text, (current_x + 20, y_offset))
        
        
        bar_x = current_x + 150
        bar_width = 350
        bar_height = 30
        fill_width = min(bar_width, int((amt / 100) * bar_width))
        
        pygame.draw.rect(screen, GRAY, (bar_x, y_offset, bar_width, bar_height))
        
        
        if amt > 60:
            bar_color = GREEN
        elif amt > 30:
            bar_color = ORANGE
        else:
            bar_color = RED
        
        pygame.draw.rect(screen, bar_color, (bar_x, y_offset, fill_width, bar_height))
        pygame.draw.rect(screen, BLACK, (bar_x, y_offset, bar_width, bar_height), 2)
        
        amt_text = font_small.render(f"{int(amt)}", True, BLACK)
        screen.blit(amt_text, (bar_x + bar_width + 20, y_offset + 5))
        
        y_offset += 55

def draw_statistics_tab(village, y):
    """Draw village statistics with visual elements"""
    x = 100
    y_offset = y
    
    
    stats = [
        ("Population", village.population, None),
        ("Labor Force", village.labor_limit, None),
        ("Happiness", f"{int(village.happiness)}%", village.happiness),
        ("Sustainability", f"{int(village.sustainability_score)}%", village.sustainability_score),
        ("Tax Rate", f"{int(village.tax_rate * 100)}%", None),
        ("Active Trades", len(village.trade_queue), None),
        ("Total Resources", int(sum(village.resources.values())), None),
        ("Buildings", len(village.buildings), None)
    ]
    
    for stat_name, value, bar_value in stats:
        text = font_medium.render(f"{stat_name}:", True, BLACK)
        screen.blit(text, (x, y_offset))
        
        if bar_value is not None:
            
            bar_x = x + 250
            bar_width = 300
            bar_height = 25
            fill = int((bar_value / 100) * bar_width)
            
            pygame.draw.rect(screen, GRAY, (bar_x, y_offset, bar_width, bar_height))
            
            if bar_value > 70:
                color = GREEN
            elif bar_value > 40:
                color = ORANGE
            else:
                color = RED
            
            pygame.draw.rect(screen, color, (bar_x, y_offset, fill, bar_height))
            pygame.draw.rect(screen, BLACK, (bar_x, y_offset, bar_width, bar_height), 2)
            
            value_text = font_small.render(str(value), True, BLACK)
            screen.blit(value_text, (bar_x + bar_width + 20, y_offset + 2))
        else:
            value_text = font_medium.render(str(value), True, BLUE)
            screen.blit(value_text, (x + 250, y_offset))
        
        y_offset += 50
    
    y_offset += 30
    prod_title = font_medium.render("Production Rates (per tick):", True, BLACK)
    screen.blit(prod_title, (x, y_offset))
    y_offset += 40
    
    for res, rate in village.production.items():
        bonus = ""
        if res in village.specialization:
            bonus = f" (×{village.specialization[res]} specialization)"
        
        text = font_small.render(f"  • {res.capitalize()}: +{rate}{bonus}", True, DARK_GREEN)
        screen.blit(text, (x + 20, y_offset))
        y_offset += 30

def draw_events_tab(village, y):
    
    x = 100
    y_offset = y
    
    title = font_medium.render("Recent Events:", True, BLACK)
    screen.blit(title, (x, y_offset))
    y_offset += 50
    
    if not village.event_history:
        text = font_small.render("No events yet - the village is peaceful", True, GRAY)
        screen.blit(text, (x, y_offset))
    else:
        event_types = {
            'Plague': ('bad', ''),
            'Drought': ('bad', '️'),
            'Famine': ('bad', ''),
            'Bandits': ('bad', ''),
            'Winter Storm': ('bad', ''),
            'Population Boom': ('good', ''),
            'Rich Harvest': ('good', ''),
            'Trade Caravan': ('good', ''),
            'Festival': ('good', '')
        }
        
        for i, event in enumerate(village.event_history[-20:]):
            event_type, icon = event_types.get(event, ('info', ''))
            color = RED if event_type == 'bad' else GREEN if event_type == 'good' else BLUE
            
            pygame.draw.circle(screen, color, (x + 20, y_offset + 10), 8)
            
            text = font_small.render(f"{icon} {event}", True, BLACK)
            screen.blit(text, (x + 40, y_offset))
            y_offset += 35

def draw_buildings_tab(village, y):
    
    x = 100
    y_offset = y
    
    title = font_medium.render("Village Buildings:", True, BLACK)
    screen.blit(title, (x, y_offset))
    y_offset += 50
    
   
    if village.buildings:
        built_title = font_small.render("Built Structures:", True, DARK_GREEN)
        screen.blit(built_title, (x, y_offset))
        y_offset += 30
        
        for building in village.buildings:
            text = font_small.render(f"  • {building.capitalize()} - {BUILDINGS[building]['effect']}", True, BLACK)
            screen.blit(text, (x + 20, y_offset))
            y_offset += 30
        y_offset += 20
    
    
    avail_title = font_small.render("Available to Build:", True, BLUE)
    screen.blit(avail_title, (x, y_offset))
    y_offset += 40
    
    for building_type, details in BUILDINGS.items():
        if building_type not in village.buildings:
       
            box_rect = pygame.Rect(x, y_offset, 600, 100)
            
           
            can_afford = all(village.resources.get(res, 0) >= amt for res, amt in details['cost'].items())
            box_color = GREEN if can_afford else GRAY
            
            pygame.draw.rect(screen, box_color, box_rect)
            pygame.draw.rect(screen, BLACK, box_rect, 2)
            
            name_text = font_medium.render(building_type.capitalize(), True, WHITE if can_afford else BLACK)
            screen.blit(name_text, (x + 20, y_offset + 10))
            
         
            effect_text = font_small.render(f"Effect: {details['effect']} (×{details['bonus']})", True, WHITE if can_afford else BLACK)
            screen.blit(effect_text, (x + 20, y_offset + 40))
            
           
            cost_str = ", ".join([f"{amt} {res}" for res, amt in details['cost'].items()])
            cost_text = font_small.render(f"Cost: {cost_str}", True, WHITE if can_afford else BLACK)
            screen.blit(cost_text, (x + 20, y_offset + 65))
            
            
            if can_afford:
                button_text = font_small.render("Click to Build", True, BLACK)
                button_rect = pygame.Rect(x + 450, y_offset + 30, 130, 40)
                pygame.draw.rect(screen, GOLD, button_rect)
                pygame.draw.rect(screen, BLACK, button_rect, 2)
                screen.blit(button_text, (x + 460, y_offset + 40))
            
            y_offset += 120

def draw_controls():
    """Draw play/pause and reset buttons"""
    button_y = HEIGHT - 70
    
    
    pause_color = RED if not kingdom.paused else GREEN
    pause_rect = pygame.Rect(WIDTH - 260, button_y, 120, 50)
    pygame.draw.rect(screen, pause_color, pause_rect)
    pygame.draw.rect(screen, BLACK, pause_rect, 3)
    pause_text = font_medium.render("⏸ Pause" if not kingdom.paused else "▶ Play", True, WHITE)
    screen.blit(pause_text, (WIDTH - 245, button_y + 12))
    
    
    reset_rect = pygame.Rect(WIDTH - 130, button_y, 120, 50)
    pygame.draw.rect(screen, GRAY, reset_rect)
    pygame.draw.rect(screen, BLACK, reset_rect, 3)
    reset_text = font_medium.render("Reset", True, WHITE)
    screen.blit(reset_text, (WIDTH - 115, button_y + 12))

last_update = time.time()
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if show_achievements:
                    show_achievements = False
                elif zoomed:
                    zoomed = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            
            if show_achievements:
                show_achievements = False
                continue
            
            if not zoomed:
               
                for village in villages:
                    vx, vy = village.pos
                    if (mx - vx)**2 + (my - vy)**2 <= 30**2:
                        zoomed = True
                        zoom_target = village
                        selected_tab = "resou"
                        
                        break
                
                
                if 30 <= mx <= 180 and 260 <= my <= 290:
                    show_achievements = True
                    
                
                
                if WIDTH - 260 <= mx <= WIDTH - 140 and HEIGHT - 70 <= my <= HEIGHT - 20:
                    kingdom.paused = not kingdom.paused
                    
                elif WIDTH - 130 <= mx <= WIDTH - 10 and HEIGHT - 70 <= my <= HEIGHT - 20:
                    
                    kingdom = Kingdom(villages)
                    for v in villages:
                        v.event_history = []
                        v.buildings = []
                    
            else:
               
                if WIDTH - 220 <= mx <= WIDTH - 50 and 20 <= my <= 80:
                    zoomed = False
                    
                if 110 <= my <= 155:
                    if 50 <= mx <= 230:
                        selected_tab = "resou"
                    elif 240 <= mx <= 420:
                        selected_tab = "stati"
                    elif 430 <= mx <= 610:
                        selected_tab = "event"
                    elif 620 <= mx <= 800:
                        selected_tab = "build"
                
                
                if selected_tab == "build" and zoom_target:
                    y_check = 265
                    for building_type, details in BUILDINGS.items():
                        if building_type not in zoom_target.buildings:
                            if 550 <= mx <= 680 and y_check + 30 <= my <= y_check + 70:
                                can_afford = all(zoom_target.resources.get(res, 0) >= amt 
                                               for res, amt in details['cost'].items())
                                if can_afford:
                                    zoom_target.build_structure(building_type)
                                    kingdom.add_notification(f"{zoom_target.name} built a {building_type}!", 'good')
                                    
                            y_check += 120
    
    
    if time.time() - last_update > 0.5:
        kingdom.update()
        last_update = time.time()
    
    
    if show_achievements:
        draw_map()
        draw_controls()
        draw_achievements_panel()
    elif zoomed and zoom_target:
        draw_zoomed(zoom_target)
    else:
        draw_map()
        draw_controls()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
