# Item modifiers are hardcoded.
# Dmg - damage weapon, missile
# Arm - armor and shield resistance
# HP - hit points of horses and shields
# Speed - weapon usage speed and horse speed
# Arm_Dif - difficulties for arms: weapons, armor.
# Horse_Dif - difficulty for horse
                      #╔════╤════╤═════╤═════╤═══════╤══════╤════════╤═════════╗
imod_plain       = 0  #║Dmg │Arm │ HP  │Speed│Arm_Dif│Charge│Maneuver│Horse_Dif║
                      #╟────┼────┼─────┼─────┼───────┼──────┼────────┼─────────╢
imod_cracked     = 1  #║ -5 │ -4 │ -56 │     │       │      │        │         ║
imod_rusty       = 2  #║ -3 │ -3 │     │     │       │      │        │         ║
imod_bent        = 3  #║ -3 │    │     │  -3 │       │      │        │         ║
imod_chipped     = 4  #║ -1 │    │     │     │       │      │        │         ║
imod_battered    = 5  #║    │ -2 │ -26 │     │       │      │        │         ║
imod_poor        = 6  #║    │    │     │     │       │      │        │         ║
imod_crude       = 7  #║ -2 │ -1 │     │     │       │      │        │         ║
imod_old         = 8  #║    │    │     │     │       │      │        │         ║
imod_cheap       = 9  #║    │    │     │     │       │      │        │         ║
imod_fine        = 10 #║ +1 │    │     │     │       │      │        │         ║
imod_well_made   = 11 #║    │    │     │     │       │      │        │         ║
imod_sharp       = 12 #║    │    │     │     │       │      │        │         ║
imod_balanced    = 13 #║ +3 │    │     │  +3 │       │      │        │         ║
imod_tempered    = 14 #║ +4 │    │     │     │       │      │        │         ║
imod_deadly      = 15 #║    │    │     │     │       │      │        │         ║
imod_exquisite   = 16 #║    │    │     │     │       │      │        │         ║
imod_masterwork  = 17 #║ +5 │    │     │  +1 │   +4  │      │        │         ║
imod_heavy       = 18 #║ +2 │ +3 │ +10 │  -2 │   +1  │  +4  │        │         ║
imod_strong      = 19 #║ +3 │    │     │  -3 │   +2  │      │        │         ║
imod_powerful    = 20 #║    │    │     │     │       │      │        │         ║
imod_tattered    = 21 #║    │ -3 │     │     │       │      │        │         ║
imod_ragged      = 22 #║    │ -2 │     │     │       │      │        │         ║
imod_rough       = 23 #║    │    │     │     │       │      │        │         ║
imod_sturdy      = 24 #║    │ +1 │     │     │       │      │        │         ║
imod_thick       = 25 #║    │ +2 │ +47 │     │       │      │        │         ║
imod_hardened    = 26 #║    │ +3 │     │     │       │      │        │         ║
imod_reinforced  = 27 #║    │ +4 │ +83 │     │       │      │        │         ║
imod_superb      = 28 #║    │    │     │     │       │      │        │         ║
imod_lordly      = 29 #║    │ +6 │     │     │       │      │        │         ║
imod_lame        = 30 #║    │    │     │ -10 │       │      │   -5   │         ║
imod_swaybacked  = 31 #║    │    │     │ -4  │       │      │   -2   │         ║
imod_stubborn    = 32 #║    │    │ +5  │     │       │      │        │    +1   ║
imod_timid       = 33 #║    │    │     │     │       │      │        │    -1   ║
imod_meek        = 34 #║    │    │     │     │       │      │        │         ║
imod_spirited    = 35 #║    │    │     │ +2  │       │  +1  │   +1   │         ║
imod_champion    = 36 #║    │    │     │ +4  │       │  +2  │   +2   │    +2   ║
                      #╚════╧════╧═════╧═════╧═══════╧══════╧════════╧═════════╝
imod_fresh       = 37 # No effects. Used in Native to track perishable foods.
imod_day_old     = 38 # No effects. Used in Native to track perishable foods.
imod_two_day_old = 39 # No effects. Used in Native to track perishable foods.
imod_smelling    = 40 # No effects. Used in Native to track perishable foods.
imod_rotten      = 41 # No effects. Used in Native to track perishable foods.
imod_large_bag   = 42 # Increased item amount +13% with math rounding, i.e. 3.4-->3, 3.5-->4. Repeated shot for crossbows?


imodbit_plain       = 0x000000000001
imodbit_cracked     = 0x000000000002
imodbit_rusty       = 0x000000000004
imodbit_bent        = 0x000000000008
imodbit_chipped     = 0x000000000010
imodbit_battered    = 0x000000000020
imodbit_poor        = 0x000000000040
imodbit_crude       = 0x000000000080
imodbit_old         = 0x000000000100
imodbit_cheap       = 0x000000000200
imodbit_fine        = 0x000000000400
imodbit_well_made   = 0x000000000800
imodbit_sharp       = 0x000000001000
imodbit_balanced    = 0x000000002000
imodbit_tempered    = 0x000000004000
imodbit_deadly      = 0x000000008000
imodbit_exquisite   = 0x000000010000
imodbit_masterwork  = 0x000000020000
imodbit_heavy       = 0x000000040000
imodbit_strong      = 0x000000080000
imodbit_powerful    = 0x000000100000
imodbit_tattered    = 0x000000200000
imodbit_ragged      = 0x000000400000
imodbit_rough       = 0x000000800000
imodbit_sturdy      = 0x000001000000
imodbit_thick       = 0x000002000000
imodbit_hardened    = 0x000004000000
imodbit_reinforced  = 0x000008000000
imodbit_superb      = 0x000010000000
imodbit_lordly      = 0x000020000000
imodbit_lame        = 0x000040000000
imodbit_swaybacked  = 0x000080000000
imodbit_stubborn    = 0x000100000000
imodbit_timid       = 0x000200000000
imodbit_meek        = 0x000400000000
imodbit_spirited    = 0x000800000000
imodbit_champion    = 0x001000000000
imodbit_fresh       = 0x002000000000
imodbit_day_old     = 0x004000000000
imodbit_two_day_old = 0x008000000000
imodbit_smelling    = 0x010000000000
imodbit_rotten      = 0x020000000000
imodbit_large_bag   = 0x040000000000
