import random as rd

def parse_damage(damage: str) -> int:
    # if there is damage to be added (e.g. 27d4+8)
    plus_in_damage = False
    
    if '+' in damage:
        start_plus = damage.find("+")
        plus_in_damage = True
        start_d = damage.find("d")
        added_damage = int(damage[start_plus + 1:])
        num_rolls = int(damage[:damage.find("d")])
        die_sides = int(damage[start_d + 1:start_plus])
    else:
        start = damage.find("d")
        num_rolls = int(damage[:start])
        die_sides = int(damage[start + 1:])
    
    roll = sum([rd.randint(1, die_sides) for _ in range(num_rolls)])
    
    if plus_in_damage:
        low = num_rolls + int(added_damage)
        high = (num_rolls * die_sides) + int(added_damage)
        roll = roll + added_damage
        return (low, high, roll)  
    else:    
        low = num_rolls
        high = low * die_sides
        return (low, high, roll)
    
    
       

