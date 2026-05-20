####################################################################################################################
#  Each item modifier record contains the following fields:
#  1) Modifier id: used for referencing modifiers in other files.
#  2) Modifier name: how this modifier will change item name, with %s being substituted by item's base name.
#  3) Price modifier: coefficient for item price when modifier is in effect.
#  4) Rarity modifier: how common are items with this modifier.
####################################################################################################################

item_modifiers = [

    ("plain",       "Plain %s",         1.000000, 1.000000), # Default. No effects. Item name is not modified.
    ("cracked",     "Cracked %s",       0.500000, 1.000000), # -5 damage, -4 armor, -46 hp
    ("rusty",       "Rusty %s",         0.550000, 1.000000), # -3 damage, -3 armor
    ("bent",        "Bent %s",          0.650000, 1.000000), # -3 damage,                   -3 speed
    ("chipped",     "Chipped %s",       0.720000, 1.000000), # -1 damage
    ("battered",    "Battered %s",      0.750000, 1.000000), #            -2 armor, -26 hp
    ("poor",        "Poor %s",          0.800000, 1.000000), # No effects.
    ("crude",       "Crude %s",         0.830000, 1.000000), # -2 damage, -1 armor
    ("old",         "Old %s",           0.860000, 1.000000), # No effects.
    ("cheap",       "Cheap %s",         0.900000, 1.000000), # No effects.
    ("fine",        "Fine %s",          1.900000, 0.600000), # +1 damage
    ("well_made",   "Well_Made %s",     2.500000, 0.500000), # No effects.
    ("sharp",       "Sharp %s",         1.600000, 0.600000), # No effects.
    ("balanced",    "Balanced %s",      3.500000, 0.500000), # +3 damage,                   +3 speed
    ("tempered",    "Tempered %s",      6.700000, 0.400000), # +4 damage
    ("deadly",      "Deadly %s",        8.500000, 0.300000), # No effects.
    ("exquisite",   "Exquisite %s",    14.500000, 0.300000), # No effects.
    ("masterwork",  "Masterwork %s",   17.500000, 0.300000), # +5 damage,                   +1 speed, +4 prerequisite
    ("heavy",       "Heavy %s",         1.900000, 0.700000), # +2 damage, +3 armor, +10 hp, -2 speed, +1 prerequisite, +4 horse charge
    ("strong",      "Strong %s",        4.900000, 0.400000), # +3 damage,                   -3 speed, +2 preresuisite
    ("powerful",    "Powerful %s",      3.200000, 0.400000), # No effects.
    ("tattered",    "Tattered %s",      0.500000, 1.000000), #            -3 armor
    ("ragged",      "Ragged %s",        0.700000, 1.000000), #            -2 armor
    ("rough",       "Rough %s",         0.600000, 1.000000), # No effects.
    ("sturdy",      "Sturdy %s",        1.700000, 0.500000), #            +1 armor
    ("thick",       "Thick %s",         2.600000, 0.350000), #            +2 armor, +47 hp
    ("hardened",    "Hardened %s",      3.900000, 0.300000), #            +3 armor
    ("reinforced",  "Reinforced %s",    6.500000, 0.250000), #            +4 armor, +83 hp
    ("superb",      "Superb %s",        2.500000, 0.250000), # No effects.
    ("lordly",      "Lordly %s",       11.500000, 0.250000), #            +6 armor, +155 hp
    ("lame",        "Lame %s",          0.400000, 1.000000), # -5 horse maneuver, -10 horse speed
    ("swaybacked",  "Swaybacked %s",    0.600000, 1.000000), # -2 horse maneuver, -4 horse speed
    ("stubborn",    "Stubborn %s",      0.900000, 1.000000), #                       +5 hp,           +1 prerequisite
    ("timid",       "Timid %s",         1.800000, 1.000000), #                                        -1 prerequisite
    ("meek",        "Meek %s",          1.800000, 1.000000), # No effects.
    ("spirited",    "Spirited %s",      6.500000, 0.600000), # +1 horse maneuver, +2 horse speed, +1 horse charge, +1 prerequisite
    ("champion",    "Champion %s",     14.500000, 0.200000), # +2 horse maneuver, +4 horse speed, +2 horse charge, +2 prerequisite
    ("fresh",       "Fresh %s",         1.000000, 1.000000), # No effects. Commonly used to track perishable foods.
    ("day_old",     "Day-old %s",       1.000000, 1.000000), # No effects. Commonly used to track perishable foods.
    ("two_day_old", "Two Days-old %s",  0.900000, 1.000000), # No effects. Commonly used to track perishable foods.
    ("smelling",    "Smelling %s",      0.400000, 1.000000), # No effects. Commonly used to track perishable foods.
    ("rotten",      "Rotten %s",        0.050000, 1.000000), # No effects. Commonly used to track perishable foods.
    ("large_bag",   "Large Bag of %s",  1.900000, 0.300000), # Increased item amount, repeated shot for crossbows.

]