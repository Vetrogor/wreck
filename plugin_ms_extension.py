from compiler import *
register_plugin()


troops = [
	["stack_storage_troop", "{!}disabled", "{!}disabled", tf_hero|tf_inactive, 0, 0, 0, [], 0, 0, 0, 0],
	["timer_storage_troop", "{!}disabled", "{!}disabled", tf_hero|tf_inactive, 0, 0, 0, [], 0, 0, 0, 0],
	["static_data_array",   "{!}disabled", "{!}disabled", tf_hero|tf_inactive, 0, 0, 0, [], 0, 0, 0, 0],
	["animation_duration",  "{!}disabled", "{!}disabled", tf_hero|tf_inactive, 0, 0, 0, [], 0, 0, 0, 0],
	["troop_flags",  "{!}disabled", "{!}disabled", tf_hero|tf_inactive, 0, 0, 0, [], 0, 0, 0, 0],
	["party_flags",  "{!}disabled", "{!}disabled", tf_hero|tf_inactive, 0, 0, 0, [], 0, 0, 0, 0],
	["party_template_flags",  "{!}disabled", "{!}disabled", tf_hero|tf_inactive, 0, 0, 0, [], 0, 0, 0, 0],

	# Universal mission scripts handler.
	# [       0          |      1    |         2        |   3    |                4            ]
	# [ number_of_tuples | time_msec | time_out_in_msec | script | scripts_handler_params slot ]
	["mission_scripts_handler","{!}MSH","{!}MSH",tf_hero,0,0,fac.commoners,[],0,0,0,0],
	["mission_scripts_handler_superseding","{!}MSH","{!}MSH",tf_hero,0,0,fac.commoners,[],0,0,0,0],

	# [      0       |        1      |    2    |    3    |    4    |      5        |    6    |    7    |    8     | end_of_slots ]
	# [ end_of_slots | num_of_params | param_1 | param_2 | param_N | num_of_params | param_1 | param_2 | param_N  |      0       ]
	["scripts_handler_params","{!}SHP","{!}SHP",tf_hero,0,0,fac.commoners,[],0,0,0,0],
	["scripts_handler_params_superseding","{!}SHP","{!}SHP",tf_hero,0,0,fac.commoners,[],0,0,0,0],

	["skin_scales","{!}skin_scales","{!}skin_scales",tf_hero,0,0,fac.commoners,[],0,0,0,0],
]
stack_storage = trp.stack_storage_troop
timer_storage = trp.timer_storage_troop

quests = [
	("wreck_compiler_constants", "{!}Wreck_Compiler_Constants", 0, "{!}None"),
]
# wreck compiler constants begin
slot_quest_item_id_repr = 0
# wreck compiler constants end

_imod_offset_damage      = 0
_imod_offset_armor       = 1
_imod_offset_hp          = 2
_imod_offset_speed       = 3
_imod_offset_difficulty  = 4
_imod_offset_h_charge    = 5
_imod_offset_h_speed     = 6
_imod_offset_h_maneuver  = 7
_imod_offset_value       = 8
_imod_offset_rarity      = 9


scripts = [

	("plugin_ms_extension_init", [
		(try_begin),
			(troop_slot_eq, trp.static_data_array, 1 * 10 + _imod_offset_damage, 0),
			(troop_set_slot, trp.static_data_array,  1 * 10 + _imod_offset_damage, -5),
			(troop_set_slot, trp.static_data_array,  1 * 10 + _imod_offset_armor, -4),
			(troop_set_slot, trp.static_data_array,  1 * 10 + _imod_offset_hp, -46),
			(troop_set_slot, trp.static_data_array,  2 * 10 + _imod_offset_damage, -3),
			(troop_set_slot, trp.static_data_array,  2 * 10 + _imod_offset_armor, -3),
			(troop_set_slot, trp.static_data_array,  3 * 10 + _imod_offset_damage, -3),
			(troop_set_slot, trp.static_data_array,  3 * 10 + _imod_offset_speed, -3),
			(troop_set_slot, trp.static_data_array,  4 * 10 + _imod_offset_damage, -1),
			(troop_set_slot, trp.static_data_array,  5 * 10 + _imod_offset_armor, -2),
			(troop_set_slot, trp.static_data_array,  5 * 10 + _imod_offset_hp, -26),
			(troop_set_slot, trp.static_data_array,  7 * 10 + _imod_offset_damage, -2),
			(troop_set_slot, trp.static_data_array,  7 * 10 + _imod_offset_armor, -1),
			(troop_set_slot, trp.static_data_array, 10 * 10 + _imod_offset_damage, 1),
			(troop_set_slot, trp.static_data_array, 13 * 10 + _imod_offset_damage, 3),
			(troop_set_slot, trp.static_data_array, 13 * 10 + _imod_offset_speed, 3),
			(troop_set_slot, trp.static_data_array, 14 * 10 + _imod_offset_damage, 4),
			(troop_set_slot, trp.static_data_array, 17 * 10 + _imod_offset_damage, 5),
			(troop_set_slot, trp.static_data_array, 17 * 10 + _imod_offset_speed, 1),
			(troop_set_slot, trp.static_data_array, 17 * 10 + _imod_offset_difficulty, 4),
			(troop_set_slot, trp.static_data_array, 18 * 10 + _imod_offset_damage, 2),
			(troop_set_slot, trp.static_data_array, 18 * 10 + _imod_offset_armor, 3),
			(troop_set_slot, trp.static_data_array, 18 * 10 + _imod_offset_hp, 10),
			(troop_set_slot, trp.static_data_array, 18 * 10 + _imod_offset_speed, -2),
			(troop_set_slot, trp.static_data_array, 18 * 10 + _imod_offset_difficulty, 1),
			(troop_set_slot, trp.static_data_array, 18 * 10 + _imod_offset_h_charge, 4),
			(troop_set_slot, trp.static_data_array, 19 * 10 + _imod_offset_damage, 3),
			(troop_set_slot, trp.static_data_array, 19 * 10 + _imod_offset_speed, -3),
			(troop_set_slot, trp.static_data_array, 19 * 10 + _imod_offset_difficulty, 2),
			(troop_set_slot, trp.static_data_array, 21 * 10 + _imod_offset_armor, -3),
			(troop_set_slot, trp.static_data_array, 22 * 10 + _imod_offset_armor, -2),
			(troop_set_slot, trp.static_data_array, 24 * 10 + _imod_offset_armor, 1),
			(troop_set_slot, trp.static_data_array, 25 * 10 + _imod_offset_armor, 2),
			(troop_set_slot, trp.static_data_array, 25 * 10 + _imod_offset_hp, 47),
			(troop_set_slot, trp.static_data_array, 26 * 10 + _imod_offset_armor, 3),
			(troop_set_slot, trp.static_data_array, 27 * 10 + _imod_offset_armor, 4),
			(troop_set_slot, trp.static_data_array, 27 * 10 + _imod_offset_hp, 83),
			(troop_set_slot, trp.static_data_array, 29 * 10 + _imod_offset_armor, 6),
			(troop_set_slot, trp.static_data_array, 29 * 10 + _imod_offset_hp, 155),
			(troop_set_slot, trp.static_data_array, 30 * 10 + _imod_offset_h_speed, -10),
			(troop_set_slot, trp.static_data_array, 30 * 10 + _imod_offset_h_maneuver, -5),
			(troop_set_slot, trp.static_data_array, 31 * 10 + _imod_offset_h_speed, -4),
			(troop_set_slot, trp.static_data_array, 31 * 10 + _imod_offset_h_maneuver, -2),
			(troop_set_slot, trp.static_data_array, 32 * 10 + _imod_offset_hp, 5),
			(troop_set_slot, trp.static_data_array, 32 * 10 + _imod_offset_difficulty, 1),
			(troop_set_slot, trp.static_data_array, 33 * 10 + _imod_offset_difficulty, -1),
			(troop_set_slot, trp.static_data_array, 35 * 10 + _imod_offset_h_charge, 1),
			(troop_set_slot, trp.static_data_array, 35 * 10 + _imod_offset_h_speed, 2),
			(troop_set_slot, trp.static_data_array, 35 * 10 + _imod_offset_h_maneuver, 1),
			(troop_set_slot, trp.static_data_array, 36 * 10 + _imod_offset_h_charge, 2),
			(troop_set_slot, trp.static_data_array, 36 * 10 + _imod_offset_h_speed, 4),
			(troop_set_slot, trp.static_data_array, 36 * 10 + _imod_offset_h_maneuver, 2),
			(troop_set_slot, trp.static_data_array, 36 * 10 + _imod_offset_difficulty, 2),
		(try_end),
	]),

	#place holders
	("animation_duration_init", []),
	("init_troop_flags", []),
	("init_party_flags", []),
	("init_party_template_flags", []),
	("init_wreck_compiler_constants", []),

	# script_array_remove_item
	("array_remove_item", [
		(store_script_param, ":troop", 1),
		(store_script_param, ":shift_start", 2),
		(store_script_param, ":item_size", 3),
		(troop_get_slot, ":num_slots", ":troop", 0),
		(store_add, ":shift_size", ":item_size", 1),
		(store_sub, ":shift_end", ":num_slots", ":shift_size"),
		(try_for_range, ":slot_destination", ":shift_start", ":shift_end"),
			(store_add, ":slot_source", ":slot_destination", ":shift_size"),
			(troop_get_slot, ":value", ":troop", ":slot_source"),
			(troop_set_slot, ":troop", ":slot_destination", ":value"),
		(try_end),
		(val_sub, ":num_slots", ":shift_size"),
		(troop_set_slot, ":troop", 0, ":num_slots"),
	]),

	# script_debug_universal_mission_scripts_handler
	("debug_universal_mission_scripts_handler", [
		(try_begin),
			(troop_slot_ge, "trp_mission_scripts_handler", 0, 1),
			(assign, ":scripts_array", "trp_mission_scripts_handler"),
			(assign, ":params_array", "trp_scripts_handler_params"),
		(else_try),
			(assign, ":scripts_array", "trp_mission_scripts_handler_superseding"),
			(assign, ":params_array", "trp_scripts_handler_params_superseding"),
		(try_end),
		(troop_get_slot, ":num_tuples", ":scripts_array", 0),
		(assign, ":end", ":num_tuples"),
		(display_message, "@Debugging scripts array:"),
		(try_for_range, ":i", 0, ":end"),
			(store_mul, ":slot", ":i", 4),
			(val_add, ":slot", 1),
			(troop_get_slot, ":time", ":scripts_array", ":slot"),
			(val_add, ":slot", 1),
			(troop_get_slot, ":time_out", ":scripts_array", ":slot"),
			(val_add, ":slot", 1),
			(troop_get_slot, ":script", ":scripts_array", ":slot"),
			(val_add, ":slot", 1),
			(troop_get_slot, ":params_slot", ":scripts_array", ":slot"),
			(assign, reg0, ":i"),
			(assign, reg1, ":time"),
			(assign, reg2, ":time_out"),
			(assign, reg3, ":script"),
			(assign, reg4, ":params_slot"),
			(display_message, "@No#{reg0} Time#{reg1} TimeOut#{reg2} ScriptID#{reg3} ParamsSlot#{reg4}"),
		(try_end),
		
		(display_message, "@Debugging params array:"),
		(troop_get_slot, ":end", ":params_array", 0),
		(assign, reg0, ":end"),
		(str_store_string, s1, "@{reg0}"),
		(try_for_range, ":i", 1, ":end"),
		   (troop_get_slot, reg0, ":params_array", ":i"),
		   (str_store_string, s1, "@{s1}, {reg0}"),
		(try_end),
		(display_message, "@{s1}"),
	]),

	# script_cf_universal_mission_scripts_handler
	("cf_universal_mission_scripts_handler", [
		(this_or_next|troop_slot_ge, "trp_mission_scripts_handler", 0, 1),
		(troop_slot_ge, "trp_mission_scripts_handler_superseding", 0, 1),
		(store_mission_timer_a_msec, ":cur_time"),
		(try_begin),
			(troop_slot_ge, "trp_mission_scripts_handler", 0, 1),
			(assign, ":scripts_array", "trp_mission_scripts_handler"),
			(assign, ":scripts_array_next", "trp_mission_scripts_handler_superseding"),
			(assign, ":params_array", "trp_scripts_handler_params"),
			(assign, ":params_array_next", "trp_scripts_handler_params_superseding"),
		(else_try),
			(assign, ":scripts_array", "trp_mission_scripts_handler_superseding"),
			(assign, ":scripts_array_next", "trp_mission_scripts_handler"),
			(assign, ":params_array", "trp_scripts_handler_params_superseding"),
			(assign, ":params_array_next", "trp_scripts_handler_params"),
		(try_end),
		(troop_get_slot, ":num_tuples", ":scripts_array", 0),
		(assign, ":end", ":num_tuples"),
		(try_for_range, ":i", 0, ":end"),
			(store_mul, ":slot", ":i", 4),
			(val_add, ":slot", 1),
			(troop_get_slot, ":time", ":scripts_array", ":slot"),
			(val_add, ":slot", 1),
			(troop_get_slot, ":time_out", ":scripts_array", ":slot"),
			(store_add, ":time_trigger", ":time", ":time_out"),	
			(val_add, ":slot", 1),
			(troop_get_slot, ":script", ":scripts_array", ":slot"),
			(val_add, ":slot", 1),
			(troop_get_slot, ":params_slot", ":scripts_array", ":slot"),
			(troop_get_slot, ":size", ":params_array", ":params_slot"),
			(try_begin),
				(ge, ":cur_time", ":time_trigger"),
				(call_script, ":script", ":params_slot"), # if script fail - we don't remove it
			(else_try),
				(troop_get_slot, ":num_scripts", ":scripts_array_next", 0),
				(val_add, ":num_scripts", 1), # we need to shift default -1 to 0
				(store_mul, ":slot", ":num_scripts", -4), # negative before activation
				(val_add, ":slot", 1),
				(troop_set_slot, ":scripts_array_next", ":slot", ":time"),
				(val_add, ":slot", 1),
				(troop_set_slot, ":scripts_array_next", ":slot", ":time_out"), # time_out_msec
				(val_add, ":slot", 1),
				(troop_set_slot, ":scripts_array_next", ":slot", ":script"), # script_callback
				(val_add, ":slot", 1),
				(troop_get_slot, ":last_slot", ":params_array_next", 0),
				(troop_set_slot, ":scripts_array_next", ":slot", ":last_slot"),
				(troop_set_slot, ":params_array_next", ":last_slot", ":size"),
				(val_add, ":last_slot", 1),
				(store_add, ":get_slot_no", ":params_slot", 1),
				(try_for_range, ":param_no", 0, ":size"),
					(troop_get_slot, ":value", ":params_array", ":get_slot_no"),
					(troop_set_slot, ":params_array_next", ":last_slot", ":value"),
					(val_add, ":get_slot_no", 1),
					(val_add, ":last_slot", 1),
				(try_end),
				(troop_set_slot, ":params_array_next", 0, ":last_slot"),
				(val_sub, ":num_scripts", 2), # on script was added and  minus one for deactivation
				(troop_set_slot, ":scripts_array_next", 0, ":num_scripts"),
			(try_end),
			(troop_get_slot, ":end", ":scripts_array", 0), # if we added scripts recursively they will trigger in the same frame
		(try_end),
		#(call_script, "script_debug_universal_mission_scripts_handler"),
		(troop_get_slot, ":num_new_scripts", ":scripts_array_next", 0),
		(val_add, ":num_new_scripts", 1), # we need to shift default -1 to 0
		(val_mul, ":num_new_scripts", -1),
		(troop_set_slot, ":scripts_array_next", 0, ":num_new_scripts"),
		(troop_set_slot, ":scripts_array", 0, -1),
		(troop_set_slot, ":params_array", 0, 1),
	]),
]


strings = [

	# Character Attribute abbreviated and full names (defaults, will be overridden with values retrieved from module_ui_strings if it's present)
	("attribute_0", "STR"),
	("attribute_1", "AGI"),
	("attribute_2", "INT"),
	("attribute_3", "CHA"),

	("attribute_0_full", "Strength"),
	("attribute_1_full", "Agility"),
	("attribute_2_full", "Intelligence"),
	("attribute_3_full", "Charisma"),

	# Weapon Proficiency names (same)
	("proficiency_0", "One-Handed Weapons"),
	("proficiency_1", "Two-Handed Weapons"),
	("proficiency_2", "Polearms"),
	("proficiency_3", "Archery"),
	("proficiency_4", "Crossbows"),
	("proficiency_5", "Thrown Weapons"),
	("proficiency_6", "Firearms"),

	# Skill names (placeholders, will be overridden with values retrieved from module_skills)
	("skill_00", "Trade"),
	("skill_01", "Leadership"),
	("skill_02", "Prisoner Management"),
	("skill_03", "Reserved Skill 1"),
	("skill_04", "Reserved Skill 2"),
	("skill_05", "Reserved Skill 3"),
	("skill_06", "Reserved Skill 4"),
	("skill_07", "Persuasion"),
	("skill_08", "Engineer"),
	("skill_09", "First Aid"),
	("skill_10", "Surgery"),
	("skill_11", "Wound Treatment"),
	("skill_12", "Inventory Management"),
	("skill_13", "Spotting"),
	("skill_14", "Path-finding"),
	("skill_15", "Tactics"),
	("skill_16", "Tracking"),
	("skill_17", "Trainer"),
	("skill_18", "Reserved Skill 5"),
	("skill_19", "Reserved Skill 6"),
	("skill_20", "Reserved Skill 7"),
	("skill_21", "Reserved Skill 8"),
	("skill_22", "Looting"),
	("skill_23", "Horse Archery"),
	("skill_24", "Riding"),
	("skill_25", "Athletics"),
	("skill_26", "Shield"),
	("skill_27", "Weapon Master"),
	("skill_28", "Reserved Skill 9"),
	("skill_29", "Reserved Skill 10"),
	("skill_30", "Reserved Skill 11"),
	("skill_31", "Reserved Skill 12"),
	("skill_32", "Reserved Skill 13"),
	("skill_33", "Power Draw"),
	("skill_34", "Power Throw"),
	("skill_35", "Power Strike"),
	("skill_36", "Ironflesh"),
	("skill_37", "Reserved Skill 14"),
	("skill_38", "Reserved Skill 15"),
	("skill_39", "Reserved Skill 16"),
	("skill_40", "Reserved Skill 17"),
	("skill_41", "Reserved Skill 18"),

	# Item modifier names (placeholders, will be overridden by actual values retrieved from module_item_modifiers if present, or compiler's default module_item_modifiers if not)
	("item_modifier_00", "Plain {s99}"),
	("item_modifier_01", "Cracked {s99}"),
	("item_modifier_02", "Rusty {s99}"),
	("item_modifier_03", "Bent {s99}"),
	("item_modifier_04", "Chipped {s99}"),
	("item_modifier_05", "Battered {s99}"),
	("item_modifier_06", "Poor {s99}"),
	("item_modifier_07", "Crude {s99}"),
	("item_modifier_08", "Old {s99}"),
	("item_modifier_09", "Cheap {s99}"),
	("item_modifier_10", "Fine {s99}"),
	("item_modifier_11", "Well Made {s99}"),
	("item_modifier_12", "Sharp {s99}"),
	("item_modifier_13", "Balanced {s99}"),
	("item_modifier_14", "Tempered {s99}"),
	("item_modifier_15", "Deadly {s99}"),
	("item_modifier_16", "Exquisite {s99}"),
	("item_modifier_17", "Masterwork {s99}"),
	("item_modifier_18", "Heavy {s99}"),
	("item_modifier_19", "Strong {s99}"),
	("item_modifier_20", "Powerful {s99}"),
	("item_modifier_21", "Tattered {s99}"),
	("item_modifier_22", "Ragged {s99}"),
	("item_modifier_23", "Rough {s99}"),
	("item_modifier_24", "Sturdy {s99}"),
	("item_modifier_25", "Thick {s99}"),
	("item_modifier_26", "Hardened {s99}"),
	("item_modifier_27", "Reinforced {s99}"),
	("item_modifier_28", "Superb {s99}"),
	("item_modifier_29", "Lordly {s99}"),
	("item_modifier_30", "Lame {s99}"),
	("item_modifier_31", "Swaybacked {s99}"),
	("item_modifier_32", "Stubborn {s99}"),
	("item_modifier_33", "Timid {s99}"),
	("item_modifier_34", "Meek {s99}"),
	("item_modifier_35", "Spirited {s99}"),
	("item_modifier_36", "Champion {s99}"),
	("item_modifier_37", "Fresh {s99}"),
	("item_modifier_38", "Day-old {s99}"),
	("item_modifier_39", "Two Days-old {s99}"),
	("item_modifier_40", "Smelling {s99}"),
	("item_modifier_41", "Rotten {s99}"),
	("item_modifier_42", "Large Bag of {s99}"),

	("damage_type_0", "cut"),
	("damage_type_1", "pierce"),
	("damage_type_2", "blunt"),

	("damage_type_0_adj", "cutting"),
	("damage_type_1_adj", "piercing"),
	("damage_type_2_adj", "blunt"),

	# Human bones
	("hb_none",       "None"      ),
	("hb_abdomen",    "abdomen"   ),
	("hb_thigh_l",    "thigh-l"   ),
	("hb_calf_l",     "calf-l"    ),
	("hb_foot_l",     "foot-l"    ),
	("hb_thigh_r",    "thigh-r"   ),
	("hb_calf_r",     "calf-r"    ),
	("hb_foot_r",     "foot-r"    ),
	("hb_spine",      "spine"     ),
	("hb_thorax",     "thorax"    ),
	("hb_head",       "head"      ),
	("hb_shoulder_l", "shoulder-l"),
	("hb_upperarm_l", "upperarm-l"),
	("hb_forearm_l",  "forearm-l" ),
	("hb_hand_l",     "hand-l"    ),
	("hb_item_l",     "item-l"    ),
	("hb_shoulder_r", "shoulder-r"),
	("hb_upperarm_r", "upperarm-r"),
	("hb_forearm_r",  "forearm-r" ),
	("hb_hand_r",     "hand-r"    ),
	("hb_item_r",     "item-r"    ),
	# Horse bones (from wse)
	("hrsb_none",         "None"        ),
	("hrsb_pelvis",       "pelvis"      ),
	("hrsb_spine_1",      "spine-1"     ),
	("hrsb_spine_2",      "spine-2"     ),
	("hrsb_spine_3",      "spine-3"     ),
	("hrsb_neck_1",       "neck-1"      ),
	("hrsb_neck_2",       "neck-2"      ),
	("hrsb_neck_3",       "neck-3"      ),
	("hrsb_head",         "head"        ),
	("hrsb_l_clavicle",   "l-clavicle"  ),
	("hrsb_l_upper_arm",  "l-upper_arm" ),
	("hrsb_l_forearm",    "l-forearm"   ),
	("hrsb_l_hand",       "l-hand"      ),
	("hrsb_l_front_hoof", "l-front_hoof"),
	("hrsb_r_clavicle",   "r-clavicle"  ),
	("hrsb_r_upper_arm",  "r-upper-arm" ),
	("hrsb_r_forearm",    "r-forearm"   ),
	("hrsb_r_hand",       "r-hand"      ),
	("hrsb_r_front_hoof", "r-front-hoof"),
	("hrsb_l_thigh",      "l-thigh"     ),
	("hrsb_l_calf",       "l-calf"      ),
	("hrsb_l_foot",       "l-foot"      ),
	("hrsb_l_back_hoof",  "l-back-hoof" ),
	("hrsb_r_thigh",      "r-thigh"     ),
	("hrsb_r_calf",       "r-calf"      ),
	("hrsb_r_foot",       "r-foot"      ),
	("hrsb_r_back_hoof",  "r-back-hoof" ),
	("hrsb_tail_1",       "tail-1"      ),
	("hrsb_tail_2",       "tail-2"      ),
]

triggers = [
	# Universal mission scripts handler +
	(ti_before_mission_start, 0, 0, [],[
		(troop_set_slot, "trp_mission_scripts_handler", 0, 0),
		(troop_set_slot, "trp_mission_scripts_handler_superseding", 0, -1),
		(troop_set_slot, "trp_scripts_handler_params", 0, 1),
		(troop_set_slot, "trp_scripts_handler_params_superseding", 0, 1),
	]),
	# Universal mission scripts handler -
]

#strings.extend([('animation_00%d' if i < 100 else 'animation_0%d' if i < 10 else 'animation_%d') % i, ('animation_00%d' if i<100 else 'animation_0%d' if i<10 else 'animation_%d') % i] for i in range(670))
strings.append(("animation_none", "none")) # id = -1
for cur_id in range(0, 670 + 200):
	strings.append( ("animation_{:0>3}".format(cur_id), "animation_{:0>3}".format(cur_id)), )

## item_id placeholders
#strings.append(("item_id_repr_none", "none")) # id = -1
#for cur_id in range(len(get_globals()['items'])):
#	strings.append( ("item_id_repr_{0}".format(cur_id), "item_id_repr_{0}".format(cur_id)), )

#init_animation_strings()

def preprocess_entities(glob):
	# Retrieve item modifier names
	for index in range(len(glob['item_modifiers'])):
		str_id = ('item_modifier_0%d' if index < 10 else 'item_modifier_%d') % index
		imod_real_name = glob['item_modifiers'][index][1]
		str_offset = int(getattr(WRECK.s, str_id)) & 0xFFFFFFFF # Strip opmask
		glob['strings'][str_offset][1] = imod_real_name % '{s99}'
	# Set item modifiers rarity and price
	for script_no in glob['scripts']:
		if script_no[0] == "plugin_ms_extension_init":
			export_script = script_no
			break
	export_code = []
	for index in range(len(glob['item_modifiers'])):
		modifier_no = glob['item_modifiers'][index]
		slot_value = index * 10 + _imod_offset_value
		slot_rarity = index * 10 + _imod_offset_rarity
		value = modifier_no[2] * 1000000
		rarity = modifier_no[3] * 1000000
		export_code.extend([
			(troop_set_slot, trp.static_data_array, slot_value, value),
			(troop_set_slot, trp.static_data_array, slot_rarity, rarity),
		])
	export_script[1].extend(export_code)

	# support for str_store_item_id_repr
	glob['strings'].append(('item_id_repr_none', 'none'))
	id = len(glob['strings'])
	for cur_script in glob['scripts']:
		if cur_script[0] == 'init_wreck_compiler_constants':
			cur_script[1].append((quest_set_slot, "qst_wreck_compiler_constants", slot_quest_item_id_repr, id))
			break
	for index in range(len(glob['items'])):
		str_id = 'item_id_repr_' + str(index)
		item_id_repr = glob['items'][index][0]
		s = ''
		for i in range(len(item_id_repr)):
			c = item_id_repr[i]
			if c == "_":
				#c = u"\u25AC"
				c = "`"
			s = s + c
		item_id_repr = 'itm`' + s
		export = (str_id, item_id_repr)
		glob['strings'].append(export)
	
	# Retrieve skill names
	for index in range(len(glob['skills'])):
		str_id = ('skill_0%d' if index < 10 else 'skill_%d') % index
		skill_real_name = glob['skills'][index][1]
		str_offset = int(getattr(WRECK.s, str_id)) & 0xFFFFFFFF # Strip opmask
		glob['strings'][str_offset][1] = skill_real_name
	# Retrieve animation names
	for index in range(len(glob['animations'])):
		str_id = ('animation_00%d' if index < 10 else 'animation_0%d' if index < 100 else 'animation_%d') % index
		animation_real_name = glob['animations'][index][0]
		s = ""
		for i in range(len(animation_real_name)):
			c = animation_real_name[i]
			if c == "_":
				#c = u"\u25AC"
				c = "`"
			s = s + c
		animation_real_name = s
		str_offset = int(getattr(WRECK.s, str_id)) & 0xFFFFFFF # Strip opmask
		glob['strings'][str_offset][1] = animation_real_name
	#Retrieve animation duration
	slot = 0
	for cur_script in glob['scripts']:
		if cur_script[0] == 'animation_duration_init':
			export = cur_script[1]
			break
	for animation in glob['animations']:
		duration = 1000
		command = ()
		for sequence in animation[3]:
			cur_duration = sequence[0]
			if cur_duration < duration: duration = cur_duration
		duration *= 1000
		command += (troop_set_slot, trp.animation_duration, slot, duration)
		export.append(command)
		slot += 1

	for cur_script in glob['scripts']:
		if cur_script[0] == 'init_troop_flags':
			export = cur_script[1]
			break
	index = 0
	for troop in glob['troops']:
		export.append((troop_set_slot, trp.troop_flags, index, troop[3]))
		index += 1

	for cur_script in glob['scripts']:
		if cur_script[0] == 'init_party_flags':
			export = cur_script[1]
			break
	index = 0
	for party in glob['parties']:
		flags = (party[2] & 0xFFFFFF00)
		export.append((troop_set_slot, trp.party_flags, index, flags))
		index += 1

	for cur_script in glob['scripts']:
		if cur_script[0] == 'init_party_template_flags':
			export = cur_script[1]
			break
	index = 0
	for party_template in glob['party_templates']:
		flags = (party_template[2] & 0xFFFFFF00)
		export.append((troop_set_slot, trp.party_template_flags, index, flags))
		index += 1

	index = 0
	for skin in glob['skins']:
		export.append((troop_set_slot, trp.skin_scales, index, round(skin[14]*100)))
		index += 1
	
	for cur_script in glob['scripts']:
		if cur_script[0] == 'game_start':
			cur_script[1].append((call_script, "script_animation_duration_init"))
			cur_script[1].append((call_script, "script_plugin_ms_extension_init"))
			cur_script[1].append((call_script, "script_init_troop_flags"))
			cur_script[1].append((call_script, "script_init_party_flags"))
			cur_script[1].append((call_script, "script_init_party_template_flags"))
			cur_script[1].append((call_script, "script_init_wreck_compiler_constants"))
			break
	# If module_ui_strings is active, retrieve attribute and weapon proficiency names
	if WRECK.generate_ui_strings:
		data = {
			'str': 'attribute_0',
			'agi': 'attribute_1',
			'int': 'attribute_2',
			'cha': 'attribute_3',
			'strength': 'attribute_0_full',
			'agility': 'attribute_1_full',
			'intelligence': 'attribute_2_full',
			'charisma': 'attribute_3_full',
			'one_handed_weapons': 'proficiency_0',
			'two_handed_weapons': 'proficiency_1',
			'polearms': 'proficiency_2',
			'archery': 'proficiency_3',
			'crossbows': 'proficiency_4',
			'throwing': 'proficiency_5',
			'firearms': 'proficiency_6',
		}
		for ui_str in glob['ui_strings']:
			try:
				str_id = data[ui_str[0]]
				ui_text = ui_str[1]
				str_offset = int(getattr(WRECK.s, str_id)) & 0xFFFFFFFF # Strip opmask
				glob['strings'][str_offset][1] = ui_text
			except:
				pass

	for cur_mission in glob['mission_templates']:
		cur_mission[5].extend(triggers)
		cur_mission[5].append((ti_before_mission_start, 0, 0, [], [(assign, "$mission_template_id", "mt_" + cur_mission[0])]))

# New string operations.

def str_store_attribute_name(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.attribute_0, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_attribute_name_full(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.attribute_0_full, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_proficiency_name(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.proficiency_0, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_skill_name(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.skill_00, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_item_modifier_name(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.item_modifier_00, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_damage_type_name(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.damage_type_0, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_damage_type_adjective(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.damage_type_0_adj, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_anim_name(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.animation_000, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_human_bone_name(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.hb_abdomen, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_horse_bone_name(string_reg, value, *argl):
	return [
		(store_add, l._cached_, s.hrsb_pelvis, value),
		(str_store_string, string_reg, l._cached_),
	]
def str_store_item_id_repr(string_reg, value, *argl):
	return [
		(quest_get_slot, l._cached_, "qst_wreck_compiler_constants", slot_quest_item_id_repr),
		(val_add, l._cached_, value),
		(str_store_string, string_reg, l._cached_),
	]

# Global stack operations

def push_value(value, *argl):
	return [
		(troop_get_slot, l._cached_, stack_storage, 0),
		(val_add, l._cached_, 1),
		(troop_set_slot, stack_storage, 0, l._cached_),
		(troop_set_slot, stack_storage, l._cached_, value),
	]
def pop_value(destination, *argl):
	return [
		(troop_get_slot, l._cached_, stack_storage, 0),
		(troop_get_slot, l.destination, stack_storage, l._cached_),
		(val_sub, l._cached_, 1),
		(troop_set_slot, stack_storage, 0, l._cached_),
	]
def peek_value(destination, *argl):
	return [
		(troop_get_slot, l._cached_, stack_storage, 0),
		(troop_get_slot, l.destination, stack_storage, l._cached_),
	]
def is_stack_empty(*argl):
	return [
		(troop_slot_eq, stack_storage, 0, 0),
	]

# Unlimited mission timers

def start_mission_timer(timer_index, *argl):
	return [
		(store_mission_timer_c_msec, l._cached_),
		(troop_set_slot, timer_storage, timer_index, l._cached_),
	]
def store_mission_timer(destination, timer_index, *argl):
	return [
		(store_mission_timer_c_msec, destination),
		(troop_get_slot, l._cached_, timer_storage, timer_index),
		(val_sub, destination, l._cached_),
	]

# Generic operations

def store_script_params(*argl):
	return [(store_script_param, argl[index], index + 1) for index in range(len(argl))]

def get_params(*argl):
	result = [(store_script_param, l._slot_, 1)]
	result.extend([
		(try_begin),
			(troop_slot_ge, "trp_mission_scripts_handler", 0, 0),
			(assign, l._params_array_, "trp_scripts_handler_params"),
		(else_try),
			(assign, l._params_array_, "trp_scripts_handler_params_superseding"),
		(try_end),
	])
	for index in range(len(argl)):
		result.append((val_add, l._slot_, 1))
		result.append((troop_get_slot, argl[index], l._params_array_, l._slot_))
	return result

def push_script_with_params(*argl):
	size = len(argl) - 2
	result = [
		(try_begin),
			(troop_slot_ge, "trp_mission_scripts_handler", 0, 0),
			(assign, l._scripts_array_, "trp_mission_scripts_handler"),
			(assign, l._params_array_, "trp_scripts_handler_params"),
		(else_try),
			(assign, l._scripts_array_, "trp_mission_scripts_handler_superseding"),
			(assign, l._params_array_, "trp_scripts_handler_params_superseding"),
		(try_end),
		(troop_get_slot, l._num_scripts_, l._scripts_array_, 0),
		(store_mul, l._slot_, l._num_scripts_, 4),
		(val_add, l._slot_, 1),
		(store_mission_timer_a_msec, l._time_),
		(troop_set_slot, l._scripts_array_, l._slot_, l._time_),
		(val_add, l._slot_, 1),
		(troop_set_slot, l._scripts_array_, l._slot_, argl[0]), # time_out_msec
		(val_add, l._slot_, 1),
		(troop_set_slot, l._scripts_array_, l._slot_, argl[1]), # script_callback
		(val_add, l._slot_, 1),
		(troop_get_slot, l._last_slot_, l._params_array_, 0),
		(troop_set_slot, l._scripts_array_, l._slot_, l._last_slot_),
		(troop_set_slot, l._params_array_, l._last_slot_, size),
	]
	for index in range(2, len(argl)):
		result.append((val_add, l._last_slot_, 1))
		result.append((troop_set_slot, l._params_array_, l._last_slot_, argl[index]))
	result.extend([
		(val_add, l._last_slot_, 1),
		(troop_set_slot, l._params_array_, 0, l._last_slot_),
		(val_add, l._num_scripts_, 1),
		(troop_set_slot, l._scripts_array_, 0, l._num_scripts_),
	])
	return result

# Mathematical operations

def get_fixed_point_multiplier(destination, *argl):
	return [
		(assign, destination, 1),
		(convert_to_fixed_point, destination),
	]

# Position operations

def position_set_coordinates(position, x, y, z, *argl):
	return [
		(position_set_x, position, x),
		(position_set_y, position, y),
		(position_set_z, position, z),
	]

def position_aim_at_position(position, target, *argl):
	return [
		(call_script, script.point_y_toward_position, position, target), # in formations code
	]

def get_distance_between_positions_fixed_point(destination, position1, position2, *argl):
	return [
		(position_get_x, l._cached_1_, position1),
		(position_get_x, l._cached_2_, position2),
		(val_sub, l._cached_1_, l._cached_2_),
		(val_mul, l._cached_1_, l._cached_1_),
		(assign, destination, l._cached_1_),
		(position_get_y, l._cached_1_, position1),
		(position_get_y, l._cached_2_, position2),
		(val_sub, l._cached_1_, l._cached_2_),
		(val_mul, l._cached_1_, l._cached_1_),
		(val_add, destination, l._cached_1_),
		(position_get_z, l._cached_1_, position1),
		(position_get_z, l._cached_2_, position2),
		(val_sub, l._cached_1_, l._cached_2_),
		(val_mul, l._cached_1_, l._cached_1_),
		(val_add, destination, l._cached_1_),
		(convert_from_fixed_point, destination),
		(store_sqrt, destination, destination),
	]

def position_move_y_fp(position, y_fp, *argl):
	return [
		(init_position, position_move_xyz_fp_pos),
		(position_set_y, position_move_xyz_fp_pos, y_fp),
		(position_transform_position_to_parent, position, position, position_move_xyz_fp_pos),
	]

def position_move_xyz_fp(position, x_fp, y_fp, z_fp, *argl):
	return [
		(init_position, position_move_xyz_fp_pos),
		(position_set_x, position_move_xyz_fp_pos, x_fp),
		(position_set_y, position_move_xyz_fp_pos, y_fp),
		(position_set_z, position_move_xyz_fp_pos, z_fp),
		(position_transform_position_to_parent, position, position, position_move_xyz_fp_pos),
	]


# Troop operations

def troop_set_attribute(troop, attribute, value, *argl):
	return [
		(store_attribute_level, l._cached_, troop, attribute),
		(store_sub, l._cached_, value, l._cached_),
		(troop_raise_attribute, troop, attribute, l._cached_),
	]

def troop_set_skill(troop, skill, value, *argl):
	return [
		(store_skill_level, l._cached_, skill, troop),
		(store_sub, l._cached_, value, l._cached_),
		(troop_raise_skill, troop, skill, l._cached_),
	]

def troop_is_not_capturable_alive(troop, *argl):
	return [
		(troop_get_slot, l._flags_, trp.troop_flags, troop),
		(store_and, l._not_capturable_, l._flags_, tf_no_capture_alive),
		(gt, l._not_capturable_, 0),
	]

def troop_is_allways_fall_dead(troop, *argl):
	return [
		(troop_get_slot, l._flags_, trp.troop_flags, troop),
		(store_and, l._allways_fall_dead_, l._flags_, tf_allways_fall_dead),
		(gt, l._allways_fall_dead_, 0),
	]

def troop_is_unkillable(troop, *argl):
	return [
		(troop_get_slot, l._flags_, trp.troop_flags, troop),
		(store_and, l._unkillable_, l._flags_, tf_unkillable),
		(gt, l._unkillable_, 0),
	]

def troop_is_unmoveable(troop, *argl):
	return [
		(troop_get_slot, l._flags_, trp.troop_flags, troop),
		(store_and, l._unkillable_, l._flags_, tf_unmoveable_in_party_window),
		(gt, l._unkillable_, 0),
	]

def skin_get_scale(destination, type, *argl):
	return [
		(troop_get_slot, destination, "trp_skin_scales", type),
	]

# Item operations

def item_get_real_difficulty(destination, item, modifier = None, *argl):
	if modifier is None: return [(item_get_difficulty, destination, item),]
	return [
		(item_get_difficulty, destination, item),
		(try_begin),
			(lt, destination, 1),
		(else_try),
			(is_between, modifier, 17, 20), # We're using numeric references here because imod_* modifiers may be renamed.
			(item_get_type, l._cached_, item),
			(eq, l._cached_, itp_type_horse),
		(else_try),
			(this_or_next|eq, modifier, 18), # imod_heavy
			(this_or_next|eq, modifier, 32), # imod_stubborn
			(eq, modifier, imod.restless),
			(val_add, destination, 1),
		(else_try),
			(this_or_next|eq, modifier, 19), # imod_powerful
			(eq, modifier, 36), # imod_champion
			(val_add, destination, 2),
		(else_try),
			(eq, modifier, 17), # imod_masterwork
			(val_add, destination, 4),
		(else_try),
			(eq, modifier, 33), # imod_timid
			(val_sub, destination, 1),
		(try_end),
	]

# Item modifier operations

def item_modifier_get_damage(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_damage),
		(troop_get_slot, destination, trp.static_data_array, destination),
	]
def item_modifier_get_armor(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_armor),
		(troop_get_slot, destination, trp.static_data_array, destination),
	]
def item_modifier_get_hp(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_hp),
		(troop_get_slot, destination, trp.static_data_array, destination),
	]
def item_modifier_get_weapon_speed(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_speed),
		(troop_get_slot, destination, trp.static_data_array, destination),
	]
def item_modifier_get_difficulty(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_difficulty),
		(troop_get_slot, destination, trp.static_data_array, destination),
	]
def item_modifier_get_horse_charge(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_h_charge),
		(troop_get_slot, destination, trp.static_data_array, destination),
	]
def item_modifier_get_horse_speed(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_h_speed),
		(troop_get_slot, destination, trp.static_data_array, destination),
	]
def item_modifier_get_horse_maneuver(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_h_maneuver),
		(troop_get_slot, destination, trp.static_data_array, destination),
	]
def item_modifier_get_value_multiplier(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_value),
		(troop_get_slot, destination, trp.static_data_array, destination), # value multiplied by 1000000
		(assign, l._cached_, 1),
		(convert_to_fixed_point, l._cached_),
		(val_mul, destination, l._cached_),
		(val_div, destination, 1000000), # convert to current fixed point
	]
def item_modifier_get_rarity_multiplier(destination, modifier, *argl):
	return [
		(store_mul, destination, modifier, 10),
		(val_add, destination, _imod_offset_rarity),
		(troop_get_slot, destination, trp.static_data_array, destination), # value multiplied by 1000000
		(assign, l._cached_, 1),
		(convert_to_fixed_point, l._cached_),
		(val_mul, destination, l._cached_),
		(val_div, destination, 1000000), # convert to current fixed point
	]
def try_for_party_group(destination, source_party, *argl):
	return [
		(party_get_num_attached_parties, l._cached_, source_party),
		(store_add, l._end_, l._cached_, 1),
		(try_for_range, l._rank_, 0, l._end_),
			(try_begin),
				(eq, l._rank_, 0),
				(assign, destination, source_party),
			(else_try),
				(val_sub, l._rank_, 1),
				(party_get_attached_party_with_rank, destination, source_party, l._rank_),
			(try_end),
	]

def party_has_flag(party, flag, *argl):
	return [
		(assign, l._check_, 0),
		(try_begin),
			(lt, party, p.parties_end),
			(troop_get_slot, l._mask_, trp.party_flags, party),
			(val_or, l._check_, l._mask_),
		(try_end),
		(party_get_template_id, l._template_, party),
		(troop_get_slot, l._mask_, trp.party_template_flags, l._template_),
		(val_or, l._check_, l._mask_),
		(val_and, l._check_, flag),
		(gt, l._check_, 0),
	]

def val_divup(destination, value, *argl):
	return [
		(val_add, destination, value),
		(val_sub, destination, 1),
		(val_div, destination, value),
	]

def store_divup(destination, value1, value2, *argl):
	return [
		(store_add, l._cached_, value1, value2),
		(val_sub, l._cached_, 1),
		(store_div, destination, l._cached_, value2),
	]

def val_div_round(destination, value, *argl):
	return [
		(store_div, l._cached_, value, 2),
		(val_add, destination, l._cached_),
		(val_div, destination, value),
	]

def store_div_round(destination, value1, value2, *argl):
	return [
		(store_div, l._cached_, value2, 2),
		(val_add, l._cached_, value1),
		(store_div, destination, l._cached_, value2),
	]

def val_not(destination, *argl):
	return [
		(val_add, destination, 1),
		(val_mul, destination, -1),
	]

def store_not(destination, value, *argl):
	return [
		(store_add, destination, value, 1),
		(val_mul, destination, -1),
	]

def val_xor(destination, value, *argl):
	return [
		(store_and, l._cached_, destination, value),
		(val_add, l._cached_, 1), # not l._cached_
		(val_mul, l._cached_, -1),
		(val_or, destination, value),
		(val_and, destination, l._cached_),
	]

def store_xor(destination, value1, value2, *argl):
	return [
		(store_and, l._cached_, value1, value2),
		(val_add, l._cached_, 1), # not l._cached_
		(val_mul, l._cached_, -1),
		(store_or, destination, value1, value2),
		(val_and, destination, l._cached_),
	]

def get_animation_duration(destination, animation_id, *argl):
	return [
		(troop_get_slot, destination, trp.animation_duration, animation_id)
	]


extend_syntax(str_store_attribute_name)        # (str_store_attribute_name, <string_reg_no>, <attribute_id>),
															  # Stores specified attribute name (3 capitalized letters by default) to string register, as specified in module_ui_strings.
extend_syntax(str_store_attribute_name_full)   # (str_store_attribute_name_full, <string_reg_no>, <attribute_id>),
															  # Stores specified attribute full name to string register, as specified in module_ui_strings.
extend_syntax(str_store_proficiency_name)      # (str_store_proficiency_name, <string_reg_no>, <proficiency_id>),
															  # Stores specified proficiency name to string register.
extend_syntax(str_store_skill_name)            # (str_store_skill_name, <string_reg_no>, <skill_id>),
															  # Stores specified skill name (as specified in module_skills) to string register
extend_syntax(str_store_item_modifier_name)    # (str_store_item_modifier_name, <string_reg_no>, <imod_value>),
															  # Stores specified item modifier name (as specified in module_item_modifiers) to string register.
extend_syntax(str_store_damage_type_name)      # (str_store_damage_type_name, <string_reg_no>, <damage_type>),
															  # Stores specified damage type name to string register.
extend_syntax(str_store_damage_type_adjective) # (str_store_damage_type_adjective, <string_reg_no>, <damage_type>),
															  # Stores specified damage type adjective to string register.
extend_syntax(str_store_anim_name)             # (str_store_anim_name, <string_reg_no>, <animation_id>),
															  # Stores specified animation name to string register, as specified in module_animations.py.
extend_syntax(str_store_human_bone_name)       # (str_store_human_bone_name, <string_reg>, <bone>),
extend_syntax(str_store_horse_bone_name)       # (str_store_horse_bone_name, <string_reg>, <bone>),
extend_syntax(str_store_item_id_repr)          # (str_store_item_id_repr, <string_reg>, <item_id>),
extend_syntax(push_value)                 # (push_value, <value>),
														# Saves a single value to stack.
extend_syntax(pop_value)                  # (pop_value, <destination>),
														# Retrieves a single value from top of stack.
extend_syntax(peek_value)                 # (peek_value, <destination>),
														# Retrieves a single value from top of stack but keeps it in stack.
extend_syntax(is_stack_empty)             # (is_stack_empty),
														# Checks that the stack is empty.
extend_syntax(start_mission_timer)        # (start_mission_timer, <timer_index>),
														# Starts a new mission timer with specified index.
extend_syntax(store_mission_timer)        # (store_mission_timer, <destination>, <timer_index>),
														# Stores current value (in milliseconds) for specified mission timer.
extend_syntax(store_script_params)        # (store_script_params, <param1>, <param2>...),
														# Retrieves arbitrary number of script parameters with a single line.
extend_syntax(push_script_with_params)    # (push_script_with_params, <time_out_msec>, <script_callback>, <param1>, <param2>...),
														# Pushes timeout and script with arbitrary number of script parameters with a single line.
														# This script will be executed after timeout milliseconds. Timeout 0 executes in the same frame.
extend_syntax(get_params)                 # (get_params, <param1>, <param2>...),
														# Retrieves arbitrary number of script handler parameters with a single line.
														# Used in the script given in the previous operand.
extend_syntax(get_fixed_point_multiplier) # (get_fixed_point_multiplier, <destination>),
														# Retrieves current fixed point multiplier value.
extend_syntax(position_set_coordinates)   # (position_set_coordinates, <pos>, <x_fixed_point>, <y_fixed_point>, <z_fixed_point>),
														# Sets all 3 position coordinates with a single line.
extend_syntax(position_aim_at_position)   # (position_aim_at_position, <position_reg>, <aim_position_reg>),
														# Rotates the position so it's Y axis points at specified aim position.
extend_syntax(get_distance_between_positions_fixed_point) # (get_distance_between_positions_fixed_point, distance_fp, position1, position2),
														# Gets distance with fixed point specified before operation.
extend_syntax(position_move_y_fp)         # (position_move_y_fp, position, y_fixed_point),
														# Moves position with fixed point value.
extend_syntax(position_move_xyz_fp)       # (position_move_xyz_fp, position, x_fixed_point, y_fixed_point, z_fixed_point),
														# Moves position with fixed point values XYZ.
extend_syntax(troop_set_attribute)        # (troop_set_attribute, <troop_id>, <attribute_id>, <value>),
														# Sets troop attribute to specified value.
extend_syntax(troop_set_skill)            # (troop_set_skill, <troop_id>, <skill_id>, <value>),
														# Sets troop skill to specified value.
extend_syntax(troop_is_not_capturable_alive) # (troop_is_not_capturable_alive, <troop_id>),
														# Check if troop is not capturable alive.
extend_syntax(troop_is_allways_fall_dead) # (troop_is_allways_fall_dead, <troop_id>),
														# Check if troop is allways fall dead.
extend_syntax(troop_is_unkillable)        # (troop_is_unkillable, <troop_id>),
														# Check if troop is unkillable.
extend_syntax(troop_is_unmoveable)        # (troop_is_unmoveable, <troop_id>),
                                          # Check if troop is tf_unmoveable_in_party_window.

extend_syntax(skin_get_scale)             # (skin_get_scale, <destination>, <skin>),
                                          # Get the scale of the skin in percents. I.e. fpm = 100.
extend_syntax(item_get_real_difficulty)   # (item_get_real_difficulty, <destination>, <item_id>, [<imod_value>]),
														# Retrieves item difficulty value, taking modifier into account. If modifier is omitted, standard item difficulty is returned.

extend_syntax(item_modifier_get_damage)            # (item_modifier_get_damage, <destination>, <imod_value>),
extend_syntax(item_modifier_get_armor)             # (item_modifier_get_armor, <destination>, <imod_value>),
extend_syntax(item_modifier_get_hp)                # (item_modifier_get_hp, <destination>, <imod_value>),
extend_syntax(item_modifier_get_weapon_speed)      # (item_modifier_get_weapon_speed, <destination>, <imod_value>),
extend_syntax(item_modifier_get_difficulty)        # (item_modifier_get_difficulty, <destination>, <imod_value>),
extend_syntax(item_modifier_get_horse_charge)      # (item_modifier_get_horse_charge, <destination>, <imod_value>),
extend_syntax(item_modifier_get_horse_speed)       # (item_modifier_get_horse_speed, <destination>, <imod_value>),
extend_syntax(item_modifier_get_horse_maneuver)    # (item_modifier_get_horse_maneuver, <destination>, <imod_value>),
extend_syntax(item_modifier_get_rarity_multiplier) # (item_modifier_get_rarity_multiplier, <destination_fixed_point>, <imod_value>),
extend_syntax(item_modifier_get_value_multiplier)  # (item_modifier_get_value_multiplier, <destination_fixed_point>, <imod_value>),

extend_syntax(try_for_party_group)        # (try_for_party_group, <destination>, <source_party>),
														# Loops for all parties in the group including source party.
extend_syntax(party_has_flag)             # (party_has_flag, <party>, <flag>),
														# Checks that party or it's template has flag.
extend_syntax(val_divup)                  # (val_divup, <destination>, <value>),
														# Divide destination with round up. Only positive values.
extend_syntax(store_divup)                # (store_divup, <destination>, <value1>, <value2>),
														# Divide destination := value1/value2 with round up. Only positive values.
extend_syntax(val_div_round)              # (val_div_round, <destination>, <value>),
														# Divide with math rounding to nearest integer. Only positive values.
extend_syntax(store_div_round)            # (store_div_round, <destination>, <value1>, <value2>),
														# Divide with math rounding to nearest integer. Only positive values.
extend_syntax(val_not)                    # (val_not, <destination>),
														# Logical NOT (compl, ~). Inverts bits in destination.
extend_syntax(store_not)                  # (store_not, <destination>, <value>),
														# Logical NOT (compl, ~). Stores inverted bits of value in destination.
extend_syntax(val_xor)                    # (val_xor, <destination>, <value>),
														# Logical XOR (exclusive OR). It's like logical OR but excludes when both bits are TRUE.
extend_syntax(store_xor)                  # (store_xor, <destination>, <value1>, <value2>),
														# Logical XOR (exclusive OR). It's like logical OR but excludes when both bits are TRUE.
extend_syntax(get_animation_duration)     # (get_animation_duration, <destination>, <animation_id>),
														# Get animation duration in milliseconds. Only minimal duration of different variants is counted.