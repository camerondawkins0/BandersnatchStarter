import random as rd

def parse_damage(damage: str) -> tuple:
    """
    Parses a damage string and calculates the damage roll for a game.

    Args:
        damage (str): The damage string to parse. It should be in the format of 'XdY' or 'XdY+Z',
                      where X is the number of rolls, Y is the number of sides on the die,
                      and Z is the additional damage.

    Returns:
        tuple: A tuple containing the low damage, high damage, and the calculated damage roll.

    Example:
        >>> parse_damage('2d6')
        (2, 12, 7)
        >>> parse_damage('3d8+5')
        (3, 29, 21)
    """
    plus_in_damage = '+' in damage

    if plus_in_damage:
        start_plus = damage.find("+")
        start_d = damage.find("d")
        added_damage = int(damage[start_plus + 1:])
        num_rolls = int(damage[:start_d])
        die_sides = int(damage[start_d + 1:start_plus])
    else:
        start = damage.find("d")
        num_rolls = int(damage[:start])
        die_sides = int(damage[start + 1:])

    roll = sum([rd.randint(1, die_sides) for _ in range(num_rolls)])

    if plus_in_damage:
        low = num_rolls + added_damage
        high = (num_rolls * die_sides) + added_damage
        roll += added_damage
        return (low, high, roll)
    else:
        low = num_rolls
        high = low * die_sides
        return (low, high, roll)
