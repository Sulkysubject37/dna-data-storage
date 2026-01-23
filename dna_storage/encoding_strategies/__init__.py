from .baseline import BaselineStrategy
from .rotating import RotatingStrategy

STRATEGIES = {
    'baseline': BaselineStrategy,
    'rotating': RotatingStrategy
}

def get_strategy(name):
    return STRATEGIES.get(name, BaselineStrategy)()
