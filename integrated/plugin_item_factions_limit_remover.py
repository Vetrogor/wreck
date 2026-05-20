from compiler import *
register_plugin()

# The engine limitation is 16 factions for each item.
# It crushes if there are more.
# This plugin stores information to slots instead.
# Following operators replaced automatically:
# 		item_has_faction
# 		troop_add_merchandise_with_faction
# 		reset_item_probabilities
# 		set_item_probability_in_merchandise
# 		set_merchandise_modifier_quality

# Credits to K700 who helped with source code of engine operators.

# Installation:
# Import this plugin after the "plugin_ms_extension.py"
# i.e.
#		import plugin_ms_extension
#		import plugin_item_factions_limit_remover
#		import plugin_presentations

# You can use custom "module_item_modifiers.py"(rename "DISABLED_module_item_modifiers.py"). Deafault is Native rarity and price_factor.
# Only works with WRECK v1.1.2 and above. There was missed code in plugin_ms_extension.

# Usage: just use default operators and add more than 16 factions to items.



troops = [
	["item_pointers","{!}item_pointers","{!}item_pointers",tf_hero,0,0,fac.commoners,[],0,0,0,0], # store slot of the next array
	["item_factions","{!}item_factions","{!}item_factions",tf_hero,0,0,fac.commoners,[],0,0,0,0],
	# slot offsets <0> - num_factions
	#              <1> - cur_faction_1
	#              . .
	#              <n> - cur_faction_n
	["item_kindnos","{!}item_kindnos","{!}item_kindnos",tf_hero,0,0,fac.commoners,[],0,0,0,0],
	["item_thresholds","{!}item_thresholds","{!}item_thresholds",tf_hero,0,0,fac.commoners,[],0,0,0,0],
	["item_probabilities","{!}item_probabilities","{!}item_probabilities",tf_hero,0,0,fac.commoners,[],0,0,0,0],
]

scripts = [
	("init_item_factions", []), # placeholder
	("cf_item_has_faction",[
		(store_script_param, ":item_id", 1),
		(store_script_param, ":faction_id", 2),
		(troop_get_slot, ":item_pointer", "trp_item_pointers", ":item_id"),
		(troop_get_slot, ":num_factions", "trp_item_factions", ":item_pointer"),
		(try_begin),
			(eq, ":num_factions", 0),
			(assign, ":has_faction", 1),
		(else_try),
			(assign, ":has_faction", 0),
			(store_add, ":first_faction", ":item_pointer", 1),
			(try_for_range, ":offset", 0, ":num_factions"),
				(store_add, ":slot", ":first_faction", ":offset"),
				(troop_get_slot, ":cur_faction", "trp_item_factions", ":slot"),
				(eq, ":cur_faction", ":faction_id"),
				(assign, ":has_faction", 1),
			(try_end),
		(try_end),
		(eq, ":has_faction", 1),
	]),
	("troop_add_merchandise_with_faction", [
		(store_script_param, ":troop_id", 1),
		(store_script_param, ":faction_id", 2),
		(store_script_param, ":item_type", 3),
		(store_script_param, ":value", 4),

		(assign, ":totalthreshold", 0),
		(assign, ":num_item_kindnos", 0),
		(try_for_range, ":item_no", 0, "itm_items_end"),
			(item_get_type, ":type", ":item_no"),
			(eq, ":type", ":item_type"),
			(negate|item_has_property, ":item_no", itp_unique),
			(item_has_property, ":item_no", itp_merchandise),
			(call_script, "script_cf_item_has_faction", ":item_no", ":faction_id"),

			(item_get_abundance, ":abundance", ":item_no"),
			(troop_get_slot, ":probability", "trp_item_probabilities", ":item_no"),
			(store_mul, ":cur_threshold", ":abundance", ":probability"),
			(val_div, ":cur_threshold", 100),
			(troop_set_slot, "trp_item_kindnos", ":num_item_kindnos", ":item_no"),
			(troop_set_slot, "trp_item_thresholds", ":num_item_kindnos", ":totalthreshold"),
			(val_add, ":totalthreshold", ":cur_threshold"),
			(val_add, ":num_item_kindnos", 1),
		(try_end),
		(try_begin),
			(gt, ":num_item_kindnos", 0),
			(try_for_range, ":unused", 0, ":value"),
				(store_random_in_range, ":random_threshold", 0, ":totalthreshold"),
				(assign, ":end", 1),
				(try_for_range, ":index", 0, ":end"),
					(gt, ":end", 10000),
				(else_try),
					(ge, ":index", ":num_item_kindnos"),
				(else_try),
					(troop_get_slot, ":cur_threshold", "trp_item_thresholds", ":index"),
					(ge, ":cur_threshold", ":random_threshold"),
				(else_try),
					(val_add, ":end", 1),
				(try_end),
				(troop_get_slot, ":cur_item", "trp_item_kindnos", ":index"),
				(call_script, "script_get_modifier", ":cur_item", "$merchandise_modifier_quality"),
				(assign, ":modifier", reg0),
				(troop_add_item, ":troop_id", ":cur_item", ":modifier"),
			(try_end),
			(troop_sort_inventory, ":troop_id"),
		(try_end),
	]),
	("reset_item_probabilities",[
		(store_script_param, ":probability", 1),
		(1492, ":probability"), # Original operator for compatibility with <troop_loot_troop>
		(try_for_range, ":item_no", 0, "itm_items_end"),
			(troop_set_slot, "trp_item_probabilities", ":item_no", ":probability"),
		(try_end),
	]),
	("set_item_probability_in_merchandise", [
		(store_script_param, ":item_id", 1),
		(store_script_param, ":probability", 2),
		(1493, ":item_id", ":probability"), # Original operator for compatibility with <troop_loot_troop>
		(troop_set_slot, "trp_item_probabilities", ":item_id", ":probability"),
	]),
	("set_merchandise_modifier_quality", [
		(store_script_param, ":value", 1),
		(1490, ":value"), # Original operator for compatibility with <troop_loot_troop>
		(val_clamp, ":value", 0, 1000*100),
		(assign, "$merchandise_modifier_quality", ":value"),
	]),
	("get_modifier_probability",[
		(store_script_param, ":rarity", 1),
		(store_script_param, ":price_factor", 2),
		(store_script_param, ":quality", 3),
		(store_sub, ":v7", ":quality", ":price_factor"),
		(val_abs, ":v7"),
		
		(assign, ":decrease", 0),
		(try_begin),
			(gt, ":quality", 100),
			(le, ":price_factor", 100),
			(assign, ":decrease", 1),
		(try_end),
		(try_begin),
			(lt, ":quality", 100),
			(ge, ":price_factor", 100),
			(assign, ":decrease", 1),
		(try_end),
		(try_begin),
		   (eq, ":decrease", 1),
		   (val_mul, ":v7", 5),
		   (val_add, ":v7", 300),
		(try_end),
		(val_add, ":v7", 100),
		(val_mul, ":rarity", 100),
		(store_div, ":probability", ":rarity", ":v7"),
		(assign, reg0, ":probability"),
	]),
	("get_modifier",[
		(store_script_param, ":item_id", 1),
		(store_script_param, ":quality", 2),
		(assign, ":modifier", 0),
		(try_begin),
		   (store_random_in_range, ":random", 0, 100),
		   (lt, ":random", 10),
		(else_try),
			(call_script, "script_get_modifier_probability", 100, 100, ":quality"),
			(assign, ":minimum_probability", reg0),
			(assign, ":total_probability", ":minimum_probability"),
			(try_for_range, ":modifier_no", 0, 43),
				(item_has_modifier, ":item_id", ":modifier_no"),
				(set_fixed_point_multiplier, 100),
				(item_modifier_get_rarity_multiplier, ":rarity", ":modifier_no"),
				(item_modifier_get_value_multiplier, ":price_factor", ":modifier_no"),
				(call_script, "script_get_modifier_probability", ":rarity", ":price_factor", ":quality"),
				(assign, ":probability", reg0),
				(val_add, ":total_probability", ":probability"),
			(try_end),
			(store_random_in_range, ":threshold", 0, ":total_probability"),
			(try_begin),
				(lt, ":minimum_probability", ":threshold"),
				(assign, ":probability", ":minimum_probability"),
				(assign, ":modifier", -1),
				(assign, ":end", 43),
				(try_for_range, ":modifier_no", 0, ":end"),
					(negate|eq, ":modifier", -1),
					(assign, ":end", 0),
				(else_try),
					(item_has_modifier, ":item_id", ":modifier_no"),
					(set_fixed_point_multiplier, 100),
					(item_modifier_get_rarity_multiplier, ":rarity", ":modifier_no"),
					(item_modifier_get_value_multiplier, ":price_factor", ":modifier_no"),
					(call_script, "script_get_modifier_probability", ":rarity", ":price_factor", ":quality"),
					(assign, ":cur_probability", reg0),
					(val_add, ":probability", ":cur_probability"),
					(gt, ":probability", ":threshold"),
					(assign, ":modifier", ":modifier_no"),
				(try_end),
				(try_begin),
					(ge, ":modifier", 0),
				(else_try),
					(assign, ":modifier", 0),
				(try_end),
			(try_end),
		(try_end),
		(assign, reg0, ":modifier"),
	]),
]

def preprocess_entities(glob):

	num_scripts_initialised = 0
	for index in range(len(glob['scripts'])):
		if glob['scripts'][index][0] == "game_start":
			glob['scripts'][index][1].append((call_script, "script_init_item_factions"))
			num_scripts_initialised += 1
		if glob['scripts'][index][0] == "init_item_factions":
			init_script = glob['scripts'][index]
			num_scripts_initialised += 1
		if num_scripts_initialised == 2: break

	init_code = []
	cur_slot = 0
	for index in range(len(glob['items'])):
		item_no = glob['items'][index]
		num_factions = len(item_no[9])
		init_code.extend([
			(troop_set_slot, "trp_item_factions", cur_slot, num_factions),
			(troop_set_slot, "trp_item_pointers", index, cur_slot),
		])
		cur_slot += 1
		for cur_faction in item_no[9]:
			init_code.append((troop_set_slot, "trp_item_factions", cur_slot, cur_faction))
			cur_slot += 1
		item_no[9].clear()
	init_script[1] = init_code

def item_has_faction(item_kind_no, faction_no, *argl):
	return[(call_script, "script_cf_item_has_faction", item_kind_no, faction_no)]
def troop_add_merchandise_with_faction(troop_id, faction_id, item_type_id, value, *argl):
	return[(call_script, "script_troop_add_merchandise_with_faction", troop_id, faction_id, item_type_id, value)]
def reset_item_probabilities(value, *argl):
	return[(call_script, "script_reset_item_probabilities", value)]
def set_item_probability_in_merchandise(item_id, probability, *argl):
	return[(call_script, "script_set_item_probability_in_merchandise", item_id, probability)]
def set_merchandise_modifier_quality(value, *argl):
	return[(call_script, "script_set_merchandise_modifier_quality", value)]

extend_syntax(item_has_faction)
extend_syntax(troop_add_merchandise_with_faction)
extend_syntax(reset_item_probabilities)
extend_syntax(set_item_probability_in_merchandise)
extend_syntax(set_merchandise_modifier_quality)