SIMULATION_START_YEAR = 1450
SIMULATION_END_YEAR = 1470
REAL_TIME_DURATION = 600
SECONDS_PER_YEAR = REAL_TIME_DURATION / (SIMULATION_END_YEAR - SIMULATION_START_YEAR)
SECONDS_PER_MONTH = SECONDS_PER_YEAR / 12
MONTHS_PER_YEAR = 12

RESOURCES = ['wood', 'iron', 'livestock', 'grain', 'gold']

CITIES = [
    {'name': 'Goblin Stadium', 'produces': 'wood', 'pos': (300, 600)},
    {'name': 'Bone Pit', 'produces': 'iron', 'pos': (500, 700)},
    {'name': 'Barbarian Bowl', 'produces': 'livestock', 'pos': (700, 650)},
    {'name': 'P.E.K.K.A\'s Playhouse', 'produces': 'grain', 'pos': (900, 600)},
    {'name': 'Spell Valley', 'produces': 'wood', 'pos': (400, 400)},
    {'name': 'Builder\'s Workshop', 'produces': 'iron', 'pos': (600, 450)},
    {'name': 'Royal Arena', 'produces': 'livestock', 'pos': (800, 400)},
    {'name': 'Frozen Peak', 'produces': 'grain', 'pos': (1000, 450)},
    {'name': 'Jungle Arena', 'produces': 'wood', 'pos': (500, 250)},
    {'name': 'Hog Mountain', 'produces': 'iron', 'pos': (700, 200)},
    {'name': 'Windsor', 'produces': None, 'pos': (650, 500), 'is_capital': True},
]

INITIAL_POPULATION = 1000
INITIAL_RESOURCES = 150
CAPITAL_INITIAL_POPULATION = 5000
CAPITAL_INITIAL_RESOURCES = 750

BASE_PRODUCTION = 250
PRODUCTION_PER_CAPITA = 0.30
GOLD_BASE_PRODUCTION = 100
GOLD_PER_CAPITA = 0.06

CONSUMPTION_PER_CAPITA = 0.010

CAPITAL_TAX_RATE = 0.02

MINIMUM_SURVIVAL_BASE = 8
MINIMUM_SURVIVAL_PER_CAPITA = 0.004

GROWTH_THRESHOLD_BASE = 50
GROWTH_THRESHOLD_PER_CAPITA = 0.020

MAX_GROWTH_RATE = 0.02
MAX_DECLINE_RATE = -0.03

TRADE_CART_SPEED = 200
TRADE_EFFICIENCY = 0.98

EVENT_BASE_CHANCE = 0.20

EVENT_TYPES = {
    'drought': {
        'name': 'Drought',
        'duration': 3,
        'effect': 'No livestock or grain production',
        'icon': '☀️',
        'color': (255, 200, 0)
    },
    'pirates': {
        'name': 'Pirate Raid',
        'duration': 1,
        'effect': 'Steals 50% of resources',
        'icon': '🏴‍☠️',
        'color': (100, 0, 0)
    },
    'lightning': {
        'name': 'Lightning Storm',
        'duration': 2,
        'effect': 'Blocks trade routes',
        'icon': '⚡',
        'color': (200, 200, 255)
    },
    'plague': {
        'name': 'Plague',
        'duration': 4,
        'effect': 'Cuts trade, kills 10% population/month',
        'icon': '🦠',
        'color': (100, 255, 100)
    },
    'strike': {
        'name': 'Labor Strike',
        'duration': 3,
        'effect': 'No wood or iron production',
        'icon': '🔨',
        'color': (150, 150, 150)
    }
}

BUILDINGS = {
    'wall': {
        'name': 'City Wall',
        'cost': {'iron': 150, 'wood': 80, 'gold': 300},
        'effect': 'Reduces plague effects by 30%',
        'icon': '🏰',
        'color': (128, 128, 128)
    },
    'camp': {
        'name': 'Refugee Camp',
        'cost': {'wood': 100, 'livestock': 75, 'grain': 75, 'gold': 200},
        'effect': 'Increases production by 5%',
        'icon': '⛺',
        'color': (139, 69, 19)
    },
    'monument': {
        'name': 'King\'s Monument',
        'cost': {'gold': 500, 'iron': 100},
        'effect': 'Does nothing (prestige)',
        'icon': '🗿',
        'color': (180, 180, 180)
    },
    'granary': {
        'name': 'Granary Complex',
        'cost': {'gold': 300, 'wood': 150, 'grain': 100},
        'effect': '50% grain production during drought',
        'icon': '🌾',
        'color': (218, 165, 32)
    },
    'hotel': {
        'name': 'Royal Hotel',
        'cost': {'gold': 400, 'iron': 80},
        'effect': 'Increases gold production by 5%',
        'icon': '🏨',
        'color': (255, 215, 0)
    }
}

SUSTAINABILITY_WEIGHTS = {
    'resource_balance': 300,
    'population_stability': 250,
    'trade_efficiency': 200,
    'disaster_recovery': 150,
    'building_diversity': 100
}

COLOR_BG = (240, 230, 210)
COLOR_TEXT = (40, 30, 20)
COLOR_CITY = (100, 100, 200)
COLOR_CAPITAL = (200, 100, 100)
COLOR_ROUTE = (150, 150, 150)
COLOR_CART = (200, 150, 50)

RESOURCE_COLORS = {
    'wood': (139, 90, 43),
    'iron': (128, 128, 128),
    'livestock': (205, 133, 63),
    'grain': (218, 165, 32),
    'gold': (255, 215, 0)
}