from sys import argv as sys_arguments
from compiler import *
register_plugin()

compiler_store_overlay_data =  True if 'prsnt_helper' in sys_arguments else False

ui_position = pos127

troops = [
###################################################################################################
##       0       |       1     |      2     |       3     | ....  |       N      | last_free_slot |
#----------------+-------------+------------+-------------+-------+--------------+----------------+
# last_free_slot | length_data | overlay_ID | data_slot_1 | ....  | length_data  |    empty       |
###################################################################################################
["overlay_storage", "{!}disabled", "{!}disabled", tf_hero|tf_inactive, 0, 0, 0, [], 0, 0, 0, 0],



#+-----------------------------------------------ui_create_combobox_scripted-------------------------------------------------+
#| Data_size | Overlay_ID | description_string | Num_items | script_create_str_registers | Value | container_X | container_Y |
#+---------------------------------------------------------------------------------------------------------------------------+
["scripted_overlay_storage", "{!}disabled", "{!}disabled", tf_hero|tf_inactive, 0, 0, 0, [], 0, 0, 0, 0],
]

strings = [
	("ui_create_label", 		"{!}label"),
	("ui_create_mesh", 			"{!}mesh"),
	("ui_create_button", 		"{!}button"),
	("ui_create_game_button", 	"{!}game`button"),
	("ui_create_in_game_button","{!}in`game`button"),
	("ui_create_image_button", 	"{!}image`button"),
	("ui_create_image_button_with_tableau_material", "{!}image`button`with`tableau`material"),
	("ui_create_checkbox", 		"{!}checkbox"),
	("ui_create_container", 	"{!}container"),
	("ui_create_numberbox", 	"{!}numberbox"),
	("ui_create_textbox", 		"{!}textbox"),
	("ui_create_combo_label", 	"{!}combo_label"),
	("ui_create_combobox", 		"{!}combobox"),
	("ui_create_combobox_scripted", "{!}combobox`scripted"),
	("ui_create_listbox", 		"{!}listbox"),
	("ui_create_item", 			"{!}item"),
	("ui_create_horslider", 	"{!}horslider"),
	("ui_create_mesh_with_tableau_material", "{!}mesh`with`tableau`material"),
	("unknown", "{!}unknown"),
]

# Uncomment whatever meshes you actually need in your mod.

meshes = [

	# Backgrounds for entire presentations

	# core_ui_meshes.brf
	#("ui_bg_quests", 0, "quests_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Two vertical parts, left is a big black rectangle
	#("ui_bg_inventory_old", 0, "inventory_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Left and right panels plus equipment area
	#("ui_bg_dialog", 0, "conversation_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Smaller transparent area top-left, text area top-right, dialog options area bottom
	#("ui_bg_message", 0, "message_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # One big area, decorated left/right, lighter
	#("ui_bg_debrief", 0, "debrief_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # One big area, decorated left/right, darker
	#("ui_bg_meeting", 0, "meeting_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # One big area, lighter
	#("ui_bg_options_old", 0, "options_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # One big area, darker
	#("ui_bg_2a", 0, "bg2a", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Very dark reddish bg, large area top, narrow black bottom
	# user_interface_b.brf
	#("ui_bg_character", 0, "character_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Background for character window, with areas for portrait, attributes, skills, proficiencies etc
	#("ui_bg_facegen", 0, "face_gen_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Background for facegen, with transparent area for portrait
	#("ui_bg_inventory", 0, "inventory_window_b", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Background for inventory and equipment window
	("ui_bg_party", 0, "party_window_b", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Background for party window, with central area for interface elements
	#("ui_bg_notes", 0, "note_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Parchment sheet on wooden boards, parchment split into two areas: wider left and narrower right
	#("ui_bg_game_logs", 0, "game_log_window", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Parchment sheet on wooden boards, single big area
	#("ui_bg_mp_host", 0, "mp_ui_host_main", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Parchment sheet, one big area, some area on top is left transparent
	#("ui_bg_mp_profile", 0, "mp_ui_profile", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Screen split into two areas, each has a header placeholder, nice borders
	#("ui_bg_mp_bg", 0, "mp_ui_bg", 0, 0, 0, 0, 0, 0, 1, 1, 1), # One big area, nice borders
	# user_interface_c.brf
	#("ui_bg_parchdoor", 0, "cb_ui_main", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Parchment w/o borders, weird door with staircase in bottom-center
	#("ui_bg_options", 0, "ui_options_bg", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Three areas, small top-right, small transparent bottom-right and big remaining, plain borders

	# Large panels

	# core_ui_meshes.brf
	#("ui_panel_facegen", 0, "facegen_board", 0, 0, 0, 0, 0, 0, 1, 1, 1), # Half-screen area (0.5 * 0.7).
	# user_interface_b.brf
	#("ui_panel_mp_menu", 0, "mp_ingame_menu", 0, 0, 0, 0, 0, 0, 1, 1, 1), # semi-transparent, (0,0.5),(0,0.59),(0,0)
	#("ui_panel_mp_score_b", 0, "mp_score_b", 0, 0, 0, 0, 0, 0, 1, 1, 1), # semi-transparent, (0,0.786684),(0,0.59),(0,0)
	#("ui_panel_mp_score_a", 0, "mp_score_a", 0, 0, 0, 0, 0, 0, 1, 1, 1), # semi-transparent, (0,0.393342),(0,0.59),(0,0)
	#("ui_panel_mp_inv_left", 0, "mp_inventory_left",  0, 0, 0, 0, 0, 0, 1, 1, 1), # transparent with 5 slots, (0,0.133),(0,0.90396),(0,0)
	#("ui_panel_mp_inv_right", 0, "mp_inventory_right", 0, 0, 0, 0, 0, 0, 1, 1, 1), # transparent with 4 slots, (0,0.133),(0,0.77696),(0,0)
	#("ui_panel_mp_welcome", 0, "mp_ui_welcome_panel", 0, 0, 0, 0, 0, 0, 1, 1, 1), # semi-transparent, (0,0.599999),(0,0.2),(0,0)
	#("ui_panel_mp_order", 0, "mp_ui_order_button", 0, 0, 0, 0, 0, 0, 1, 1, 1), # semi-transparent, (0,0.399982),(0,0.04),(0,0)
	# user_interface_c.brf
	#("ui_panel_quickbattle", 0, "ui_quick_battle_a", 0, 0, 0, 0, 0, 0, 1, 1, 1), # reddish, (0,0.35),(0,0.75),(0,0)
	#("ui_panel_title", 0, "cb_ui_title_panel", 0, 0, 0, 0, 0, 0, 1, 1, 1), # white, (0,0.6),(0,0.1),(0,0)

	# Buttons

	# core_ui_meshes.brf
	#("ui_btn_dialog_u", 0, "dlg_button",      0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.009827,0.962631),(-0.007161,0.043302),(0,0)
	#("ui_btn_dialog_d", 0, "dlg_button_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_medium_u", 0, "medium_button",      0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.015689,0.285534),(-0.018568,0.079553),(0,0)
	#("ui_btn_medium_d", 0, "medium_button_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	("ui_btn_short_u", 0, "short_button",      0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.014919,0.239568),(-0.019886,0.083876),(0,0)
	#("ui_btn_short_d", 0, "short_button_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	("ui_btn_long_u", 0, "longer_button",      0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.011017,0.722294),(-0.015044,0.080305),(0,0)
	("ui_btn_long_d", 0, "longer_button_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_party_u", 0, "party_button",      0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.009763,0.57704),(-0.009225,0.067976),(0,0)
	#("ui_btn_party_d", 0, "party_button_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_1_u", 0, "button1_up",   0, 0, 0, 0, 0, 0, 1, 1, 1), # (2e-06,0.074053),(1e-06,0.073358),(0,0)
	#("ui_btn_1_d", 0, "button1_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_1_h", 0, "button1_hl",   0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_2_u", 0, "button2_up",   0, 0, 0, 0, 0, 0, 1, 1, 1), # (2e-06,0.133476),(1e-06,0.073358),(0,0)
	#("ui_btn_2_d", 0, "button2_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_2_h", 0, "button2_hl",   0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_3_u", 0, "button3_up",   0, 0, 0, 0, 0, 0, 1, 1, 1), # (2e-06,0.193311),(1e-06,0.073358),(0,0)
	#("ui_btn_3_d", 0, "button3_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_3_h", 0, "button3_hl",   0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_4_u", 0, "button4_up",   0, 0, 0, 0, 0, 0, 1, 1, 1), # (2e-06,0.253934),(1e-06,0.073358),(0,0)
	#("ui_btn_4_d", 0, "button4_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_4_h", 0, "button4_hl",   0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_5_u", 0, "button5_up",   0, 0, 0, 0, 0, 0, 1, 1, 1), # (2e-06,0.310907),(1e-06,0.073358),(0,0)
	#("ui_btn_5_d", 0, "button5_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_5_h", 0, "button5_hl",   0, 0, 0, 0, 0, 0, 1, 1, 1),
	# user_interface_b.brf
	("ui_btn_member_u", 0, "party_member_button",      0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.067433,0.533963),(-0.010751,0.058116),(0.000942,0.000942)
	("ui_btn_member_d", 0, "party_member_button_pressed", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_loadgame_u", 0, "restore_game_panel",      0, 0, 0, 0, 0, 0, 1, 1, 1), # semi-transparent, (0,0.601396),(0,0.386578),(0.000942,0.000942)
	#("ui_btn_loadgame_d", 0, "restore_game_panel_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	("ui_btn_drop_u", 0, "button_drop",         0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.017586,0.236414),(0,0.073),(0,0)
	("ui_btn_drop_d", 0, "button_drop_clicked", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	("ui_btn_drop_h", 0, "button_drop_hl",      0, 0, 0, 0, 0, 0, 1, 1, 1),
	("ui_btn_dropchild_u", 0, "button_drop_child",         0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.004735,0.221721),(0,0.058312),(0,0)
	("ui_btn_dropchild_d", 0, "button_drop_child_clicked", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	("ui_btn_dropchild_h", 0, "button_drop_child_hl",      0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_uparrow_u", 0, "small_arrow_up",         0, 0, 0, 0, 0, 0, 1, 1, 1), # (0,0.088293),(0,0.094),(0,0)
	#("ui_btn_uparrow_d", 0, "small_arrow_up_clicked", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_uparrow_h", 0, "small_arrow_up_hl",      0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_downarrow_u", 0, "small_arrow_down",         0, 0, 0, 0, 0, 0, 1, 1, 1), # (0,0.088293),(0,0.094),(0,0)
	#("ui_btn_downarrow_d", 0, "small_arrow_down_clicked", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_btn_downarrow_h", 0, "small_arrow_down_hl",      0, 0, 0, 0, 0, 0, 1, 1, 1),

	# Other interface elements and components of them

	# core_ui_meshes.brf
	#("ui_slider_panel",  0, "slider_hor", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.009398,0.260111),(0.002459,0.024835),(0,0)
	#("ui_slider_handle", 0, "handle_hor", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.010753,0.013258),(-0.007538,0.037135),(0,0)
	#("ui_scrollbar_panel",  0, "scrollbar",        0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.002323,0.025361),(-0.013153,0.651827),(0,0)
	#("ui_scrollbar_handle", 0, "scrollbar_handle", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (0.004206,0.01845),(-0.004966,0.312926),(0,0)
	#("ui_progressbar_panel",  0, "progressbar",        0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.013153,0.651827),(-0.000956,0.026729),(0,0)
	#("ui_progressbar_handle", 0, "progressbar_handle", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.006251,0.6433),(0.005296,0.01954),(0,0)
	#("ui_relationbar_panel",  0, "talk_relation_bar", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (9.3e-05,0.190265),(3.3e-05,0.019447),(0,0)
	#("ui_relationbar_handle", 0, "talk_reln_pointer", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.011035,0.012976),(-0.007538,0.037135),(0,0)
	# user_interface_b.brf
	#("ui_status_player_panel", 0, "status_background_player", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (0,0.176193),(0,0.051532),(0.0002,0.0002)
	#("ui_status_horse_panel", 0, "status_background_horse", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (0,0.173771),(0,0.051532),(0.0002,0.0002)
	#("ui_status_healthbar", 0, "status_health_bar", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (0,0.103666),(0,0.004613),(0,0)
	#("ui_shield_100", 0, "status_shield_100", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (-0.018475,0.02292),(-0.025124,0.026726),(0.000236,0.000236)
	#("ui_shield_80",  0, "status_shield_80",  0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_shield_60",  0, "status_shield_60",  0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_shield_40",  0, "status_shield_40",  0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_shield_20",  0, "status_shield_20",  0, 0, 0, 0, 0, 0, 1, 1, 1),
	#("ui_checkbox_off", 0, "checkbox_off", 0, 0, 0, 0, 0, 0, 1, 1, 1), # (0,0.022162),(0,0.023176),(0,0)
	#("ui_checkbox_on",  0, "checkbox_on",  0, 0, 0, 0, 0, 0, 1, 1, 1),
	# other
	#("ui_gold_icon", 0, "mp_ico_gold", 0, 0, 0, 0, 0, 0, 1, 1, 1),

]


def ui_create_label(destination, text, x, y, alignment = 0, scale = None, color = None, rotation = None, *argl):
	result = [(create_text_overlay, destination, text, alignment),]
	
	if not scale: scale = -1
	else: result.extend([
		(position_set_x, ui_position, scale),
		(position_set_y, ui_position, scale),
		(overlay_set_size, destination, ui_position),
	])

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	if color is None: color = -1
	else: result.append((overlay_set_color, destination, color))

	if rotation is None: rotation = 0
	else: result.extend([
		(position_rotate_z, ui_position, rotation),
		(overlay_set_mesh_rotation, destination, ui_position),
	])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_label, x, y, scale, scale, 0, 0, color, alignment, rotation, 0, 0)])
	
	return result

def ui_create_mesh(destination, mesh, x, y, scale_x = None, scale_y = None, color = None, *argl):
	result = [(create_mesh_overlay, destination, mesh),]

	if scale_x is None: scale_x = scale_y = -1
	else: 
		if scale_y is None: scale_y = scale_x		
		result.append((position_set_x, ui_position, scale_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))

	if color is not None:
		result.append((overlay_set_color, destination, color))
	else: color = 0

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_mesh, x, y, scale_x, scale_y, 0, 0, color, 0, 0,0,0)])

	return result

def ui_create_button(destination, caption, x, y, alignment = 0, size_x = None, size_y = None, color = None, hilight_color = None, *argl):
	result = [(create_button_overlay, destination, caption, alignment),]
	
	if size_x is None: size_x = size_y = -1
	else:
		if size_y is None: size_y = size_x		
		result.append((position_set_x, ui_position, size_x))
		result.append((position_set_y, ui_position, size_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	if color is not None: result.append((overlay_set_color, destination, color))
	else: color = -1
	if hilight_color is not None: result.append((overlay_set_hilight_color, destination, hilight_color))

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_button, x, y, size_x, size_y, 0, 0, color, alignment, 0, 0, 0)])
	
	return result

def ui_create_game_button(destination, caption, x, y, size_x = None, size_y = None, *argl):
	result = [(create_game_button_overlay, destination, caption),]
	
	if size_x is None: size_x = size_y = -1
	else:
		if size_y is None: size_y = size_x		
		result.append((position_set_x, ui_position, size_x))
		result.append((position_set_y, ui_position, size_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_game_button, x, y, size_x, size_y, 0, 0, 0, 0, 0, 0, 0)])
	
	return result

def ui_create_in_game_button(destination, caption, x, y, size_x = None, size_y = None, *argl):
	result = [(create_in_game_button_overlay, destination, caption),]
	
	if size_x is None: size_x = size_y = -1
	else:
		if size_y is None: size_y = size_x		
		result.append((position_set_x, ui_position, size_x))
		result.append((position_set_y, ui_position, size_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_in_game_button, x, y, size_x, size_y, 0, 0, 0, 0, 0, 0, 0)])
	
	return result

def ui_create_image_button(destination, mesh, mesh_pressed, x, y, scale_x = None, scale_y = None, color = None, *argl):
	result = [(create_image_button_overlay, destination, mesh, mesh_pressed),]

	if scale_x is None: scale_x = scale_y = -1
	else:
		if scale_y is None: scale_y = scale_x
		result.append((position_set_x, ui_position, scale_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	if color is None: color = -1
	else: result.append((overlay_set_color, destination, color))

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_image_button, x, y, scale_x, scale_y, 0, 0, color, 0, 0, 0, 0)])
	
	return result

def ui_create_image_button_with_tableau_material(destination, mesh, tableau_material, value, x, y, scale_x = None, scale_y = None, *argl):
	result = [(create_image_button_overlay_with_tableau_material, destination, mesh, tableau_material, value),]

	if scale_x is None: scale_x = scale_y = -1
	else:
		if scale_y is None: scale_y = scale_x		
		result.append((position_set_x, ui_position, scale_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_image_button_with_tableau_material, x, y, scale_x, scale_y, 0, 0, 0, 0, 0, 0, 0)])	
	
	return result

def ui_create_checkbox(destination, mesh_off, mesh_on, x, y, value = 0, scale = None, *argl):
	result = [(create_check_box_overlay, destination, mesh_off, mesh_on),]

	if scale is None: scale = -1
	else: result.extend([
		(position_set_x, ui_position, scale),
		(position_set_y, ui_position, scale),
		(overlay_set_size, destination, ui_position),
	])

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
		(overlay_set_val, destination, value),
	])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_checkbox, x, y, scale, scale, 0, 0, 0, 0, 0, 0, 0)])	

	return result

def ui_create_container(destination, x, y, width = 0, height = 0, *argl):
	result = [
		(create_text_overlay, destination, "str_empty_string", tf_scrollable),
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
		(position_set_x, ui_position, width),
		(position_set_y, ui_position, height),
		(overlay_set_area_size, destination, ui_position),
	]

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_container, x, y, 0, 0, width, height, 0, tf_scrollable, 0, 0, 0)])	

	return result

def ui_create_numberbox(destination, x, y, min_value, max_value, *argl):
	result = [
		(create_number_box_overlay, destination, min_value, max_value),
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	]

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_numberbox, x, y, 0, 0, 0, 0, 0, 0, 0,0,0)])

	return result

def ui_create_textbox(destination, x, y, size_x = None, scale_y = None, *argl):
	result = [(create_simple_text_box_overlay, destination),]

	if size_x is None: size_x = scale_y = -1
	else:
		if scale_y is None: scale_y = 1000
		result.append((position_set_x, ui_position, size_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_textbox, x, y, size_x, scale_y, 0, 0, 0, 0, 0,0,0)])

	return result

def ui_create_combo_label(destination, x, y, scale_x = None, scale_y = None, *argl):
	result = [(create_combo_label_overlay, destination),]

	if scale_x is None: scale_x = scale_y = -1
	else:
		if scale_y is None: scale_y = scale_x
		result.append((position_set_x, ui_position, scale_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([	
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	result.extend([(overlay_add_item, destination, item) for item in argl])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_combo_label, x, y, scale_x, scale_y, 0, 0, 0, 0, 0,0,0)])

	return result

def ui_create_combobox(destination, x, y, scale_x = None, scale_y = None, *argl):
	result = [(create_combo_button_overlay, destination),]

	if scale_x is None: scale_x = scale_y = -1
	else:
		if scale_y is None: scale_y = scale_x		
		result.append((position_set_x, ui_position, scale_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([	
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	result.extend([(overlay_add_item, destination, item) for item in argl])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_combobox, x, y, scale_x, scale_y, 0, 0, 0, 0, 0,0,0)])

	return result

def ui_create_combobox_scripted(destination, x, y, item_names_script, num_items, cur_item = 0, scale_x = None, scale_y = None, *argl):
	if (scale_x is None) or (scale_x == 0): scale_x = scale_y = 1000
	elif (scale_y is None) or (scale_y == 0): scale_y = scale_x
	result = [
		(call_script, "script_create_combobox", x, y, scale_x, scale_y, item_names_script, num_items, cur_item),
		(assign, destination, reg1)
	]
	return result

def overlay_scripted_set_display(overlay, display, *argl): return [(call_script, "script_overlay_scripted_set_display", overlay, display)]
def overlay_scripted_set_val(overlay, value, *argl): return [(call_script, "script_overlay_scripted_set_val", overlay, value)]
def overlay_scripted_get_val(destination, overlay, *argl): return [(call_script, "script_overlay_scripted_get_val", overlay), (assign, destination, reg0)]
def overlay_scripted_item_set_text(overlay, item, text, *argl): return [(call_script, "script_overlay_scripted_item_set_text", overlay, item, text)]

def ui_create_listbox(destination, x, y, scale_x = None, scale_y = None, alpha = 0x60, value = 0, *argl):
	result = [(create_listbox_overlay, destination, "str_space", 0),]

	result.extend([(overlay_add_item, destination, item) for item in argl])

	if scale_x is None: scale_x = scale_y = -1
	else:
		if scale_y is None: scale_y = scale_x		
		result.append((position_set_x, ui_position, scale_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	result.append((overlay_set_alpha, destination, alpha))
	if value != 0: result.append((overlay_set_val, destination, value))

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_listbox, x, y, scale_x, scale_y, 0, 0, 0, 0, 0,0,0)])

	return result

def ui_create_item(destination, item, x, y, scale_x = None, scale_y = None, *argl):
	result = [(create_mesh_overlay_with_item_id, destination, item),]

	if scale_x is None: scale_x = scale_y = -1
	else:
		if scale_y is None: scale_y = scale_x		
		result.append((position_set_x, ui_position, scale_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))

	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])

	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_item, x, y, scale_x, scale_y, 0, 0, 0, 0, 0,0,0)])
	
	return result

def ui_create_horslider(destination, x, y, min_value, max_value, scale_x = None, scale_y = None, *argl):
	result = [(create_slider_overlay, destination, min_value, max_value),]

	if scale_x is None: scale_x = scale_y = -1
	else:
		if scale_y is None: scale_y = scale_x
		result.append((position_set_x, ui_position, scale_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))
	
	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])
	
	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_horslider, x, y, scale_x, scale_y, 0, 0, 0, 0, 0,0,0)])
	
	return result

def ui_create_mesh_with_tableau_material(destination, mesh, tableau_material, value, x, y, scale_x = None, scale_y = None, *argl):
	result = [(create_mesh_overlay_with_tableau_material, destination, mesh, tableau_material, value),]

	if scale_x is None: scale_x = scale_y = -1
	else:
		if scale_y is None: scale_y = scale_x
		result.append((position_set_x, ui_position, scale_x))
		result.append((position_set_y, ui_position, scale_y))
		result.append((overlay_set_size, destination, ui_position))
	
	result.extend([
		(position_set_x, ui_position, x),
		(position_set_y, ui_position, y),
		(overlay_set_position, destination, ui_position),
	])
	
	if compiler_store_overlay_data: result.extend([(call_script, "script_store_overlay_data", destination, s.ui_create_mesh_with_tableau_material, x, y, scale_x, scale_y, 0, 0, 0, 0, 0,0,0)])
	
	return result

#Optional parameters should be used as 'None' if not used but needed for syntax.
extend_syntax(ui_create_label)        # (ui_create_label, <destination>, <string>, <x>, <y>, [<alignment>], [<scale>], [<color>], [<rotation>]),
                                      # See header_presentations.py file for text alignment constants.
extend_syntax(ui_create_mesh)         # (ui_create_mesh, <destination>, <mesh>, <x>, <y>, [<scale_x>], [<scale_y>], [<color>]),
                                      # If only <scale_x> is provided, it will be used for both dimensions.
extend_syntax(ui_create_button)  	  # (ui_create_button, <destination>, <string>, <x>, <y>, <alignment>, [<scale_x>], [<scale_y>], [<color>], [<hilight_color>]),
                                      # If only <scale_x> is provided, it will be used for both dimensions.
extend_syntax(ui_create_game_button)  # (ui_create_game_button, <destination>, <string>, <x>, <y>, [<scale_x>], [<scale_y>]),
                                      # If only <scale_x> is provided, it will be used for both dimensions.
extend_syntax(ui_create_in_game_button) # (ui_create_in_game_button, <destination>, <string>, <x>, <y>, [<scale_x>], [<scale_y>]),
                                      # If only <scale_x> is provided, it will be used for both dimensions.
extend_syntax(ui_create_image_button) # (ui_create_image_button, <destination>, <mesh_base>, <mesh_clicked>, <x>, <y>, [<scale_x>], [<scale_y>], [color]),
                                      # If only <scale_x> is provided, it will be used for both dimensions.
extend_syntax(ui_create_image_button_with_tableau_material) # (ui_create_image_button_with_tableau_material, <destination>, <mesh>, <tableau_material>, <value> x, y, [<scale_x], [<scale_y]),
                                      # If only <scale_x> is provided, it will be used for both dimensions.
extend_syntax(ui_create_checkbox)     # (ui_create_checkbox, <destination>, <mesh_off_state>, <mesh_on_state>, <x>, <y>, [<start_value>], [<scale>]),
                                      # Typically "mesh_checkbox_off", "mesh_checkbox_on" are used as checkbox meshes. Checkbox is not checked by default.
extend_syntax(ui_create_container)    # (ui_create_container, <destination>, <x>, <y>, <width>, <height>),
                                      # Creates a scrollable area with specified dimensions.
extend_syntax(ui_create_numberbox)	  # (ui_create_numberbox, <destination>, <x>, <y>, <min_value>, <max_value>, [<scale_x>], [<scale_y>]),
                                      # Normal empty numberbox.
extend_syntax(ui_create_textbox)      # (ui_create_textbox, <destination>, <x>, <y>, [<scale_x>], [<scale_y>]),
                                      # Normal empty textbox.
extend_syntax(ui_create_combo_label)  # (ui_create_combo_label, <destination>, <x>, <y>, [<scale_x], [scale_y], [<list_item>,...]),
									  # You can add any number of combobox items in this operation instead of using (overlay_add_item).
extend_syntax(ui_create_combobox)     # (ui_create_combobox, <destination>, <x>, <y>, [<scale_x>], [<scale_y>], [<list_item>,...]),
                                      # You can add any number of combobox items in this operation instead of using (overlay_add_item).
extend_syntax(ui_create_combobox_scripted) # (ui_create_combobox_scripted, <destination>, <x>, <y>, <item_names_script>, <num_items>, <value>, [<scale_x], [<scale_y>])
                                      # Create scripted combobox where <item_names_script> stores strings to string registers started from s4.
                                      # <value> - selected item started from bottom
extend_syntax(overlay_scripted_set_display) # (overlay_scripted_set_display, <overlay>, <display>),
extend_syntax(overlay_scripted_set_val) # (overlay_scripted_set_val, <overlay>, <value>),
extend_syntax(overlay_scripted_get_val) # (overlay_scripted_get_val, <destination>, <overlay>),
extend_syntax(overlay_scripted_item_set_text) # (overlay_scripted_item_set_text, <overlay>, <item>, <text>), items are indexed from 0.
extend_syntax(ui_create_listbox)      # (ui_create_listbox, <destination>, <x>, <y>, [<scale_x>], [<scale_y>], [<list_item>,...]),
                                      # You can add any number of combobox items in this operation instead of using (overlay_add_item).                                      
extend_syntax(ui_create_item)         # (ui_create_item, <destination>, <item>, <x>, <y>, [<scale_x>], [<scale_y>]),
                                      # If only <scale_x> is provided, it will be used for both dimensions.
extend_syntax(ui_create_horslider)    # (ui_create_numberbox, <destination>, <x>, <y>, <min_value>, <max_value>, [<scale_x>], [<scale_y>]),
                                      # Creates horisontal slider.
extend_syntax(ui_create_mesh_with_tableau_material) # (ui_create_mesh_with_tableau_material, <destination>, <mesh>, <tableau_material>, <value>, <x>, <y>, [<scale_x>], [<scale_y>]),
                                      # Creates tableu mesh with troop. <value> = <troop_id> * 2.


scripts = [
# Output: reg1 - overlay ID
("create_combobox_parent", [
(store_script_param, ":x", 1),
(store_script_param, ":y", 2),
(store_script_param, ":scale_x", 3),
(store_script_param, ":scale_y", 4),
(val_div, ":scale_y", 2),
(ui_create_mesh, ":mesh_combobox_down", "mesh_ui_btn_drop_d", l.x, l.y, l.scale_x, l.scale_y), # Macro operator
(ui_create_image_button, ":button_combobox", "mesh_ui_btn_drop_h", "mesh_ui_btn_drop_d", l.x, l.y, l.scale_x, l.scale_y), # Macro operator
(ui_create_mesh, ":mesh_combobox_up", "mesh_ui_btn_drop_u", l.x, l.y, l.scale_x, l.scale_y), # Macro operator
(assign, reg1, ":button_combobox"),
]),

# Output: reg1 - overlay ID
("create_combobox_child", [
(store_script_param, ":x", 1),
(store_script_param, ":y", 2),
(store_script_param, ":scale_x", 3),
(store_script_param, ":scale_y", 4),
(val_div, ":scale_y", 2),
(ui_create_image_button, ":button_child_combobox", "mesh_ui_btn_dropchild_h", "mesh_ui_btn_dropchild_d", l.x, l.y, l.scale_x, l.scale_y), # Macro operator
(ui_create_mesh, ":mesh_combobox_up", "mesh_ui_btn_dropchild_u", l.x, l.y, l.scale_x, l.scale_y), # Macro operator
(assign, reg1, ":button_child_combobox"),
]),

# Output: reg1 - overlay ID
("create_combobox", [
(store_script_param, ":x", 1),
(store_script_param, ":y", 2),
(val_sub, ":y", 1),
(store_script_param, ":scale_x", 3),
(store_script_param, ":scale_y", 4),
(store_script_param, ":item_names_script", 5),
(store_script_param, ":num_items", 6),
(store_script_param, ":cur_item", 7),
(call_script, ":item_names_script"),
(store_mul, ":container_x", 230, ":scale_x"),
(val_div, ":container_x", 1000),
(store_div, ":x_middle", ":container_x", 2),
(val_sub, ":x", ":x_middle"),
(call_script, "script_create_combobox_parent", ":x", ":y", ":scale_x", ":scale_y"),
(assign, ":button", reg1),
(store_mul, ":item_y", 30, ":scale_y"),
(val_div, ":item_y", 1000),
(store_mul, ":container_y", ":item_y", ":num_items"),
(try_begin),
   (gt, ":container_y", ":y"),
   (store_div, ":num_items_fit", ":y", ":item_y"),
   (store_mul, ":container_y", ":num_items_fit", ":item_y"),
(try_end),
(store_div, ":label_x", ":container_x", 2),
(store_mul, ":sub_x", ":container_x", 4), #mesh displacement fix
(val_div, ":sub_x", 100),
(val_sub, ":label_x", ":sub_x"),
(val_add, ":label_x", ":x"),
(store_add, ":label_y", ":y", l.item_y / 5),
(ui_create_label, reg1, (l.num_items - 1) - l.cur_item + 4, ":label_x", ":label_y", tf_center_justify, ":scale_y"),
(store_mul, ":offset_x", 10, ":scale_x"),
(val_div, ":offset_x", 1000),
(val_sub, l.x, l.offset_x),
(val_sub, ":y", ":container_y"),
(store_div, ":child_x", ":offset_x", 2),
(assign, ":child_y", 0),
(ui_create_container, ":container", l.x, l.y, ":container_x", ":container_y"), # Macro operator
(set_container_overlay, ":container"),
(try_for_range_backwards, ":str_register_no", 0, ":num_items"),
   (call_script, "script_create_combobox_child", ":child_x", ":child_y", ":scale_x", ":scale_y"),
   (store_add, ":label_x", ":child_x", l.container_x / 2),
   (val_sub, ":label_x", ":sub_x"),
   (store_add, ":label_y", ":child_y", l.item_y / 7),
   (ui_create_label, reg1, l.str_register_no + 4, ":label_x", ":label_y", tf_center_justify, ":scale_y"),
   (val_add, ":child_y", ":item_y"),
(try_end),
(set_container_overlay, -1),
(overlay_get_position, pos1, ":container"),
(position_get_y, ":container_pos_y", pos1),
(val_sub, ":container_pos_y", 750),
(position_set_y, pos1, ":container_pos_y"),
(overlay_set_position, ":container", pos1),
(troop_get_slot, ":free_offset", "trp_scripted_overlay_storage", 0),
(store_add, ":slot_no", ":free_offset", 1), (troop_set_slot, "trp_scripted_overlay_storage", ":slot_no", ":button"),
(val_add, ":slot_no", 1),                   (troop_set_slot, "trp_scripted_overlay_storage", ":slot_no", "str_ui_create_combobox_scripted"),
(val_add, ":slot_no", 1),                   (troop_set_slot, "trp_scripted_overlay_storage", ":slot_no", ":num_items"),
(val_add, ":slot_no", 1),                   (troop_set_slot, "trp_scripted_overlay_storage", ":slot_no", ":item_names_script"),
(val_add, ":slot_no", 1),                   (troop_set_slot, "trp_scripted_overlay_storage", ":slot_no", ":cur_item"),
(val_add, ":slot_no", 1),                   (troop_set_slot, "trp_scripted_overlay_storage", ":slot_no", ":container_x"),
(val_add, ":slot_no", 1),                   (troop_set_slot, "trp_scripted_overlay_storage", ":slot_no", ":container_y"),
(val_add, ":slot_no", 1),
(store_sub, ":data_size", ":slot_no", ":free_offset"),
(troop_set_slot, "trp_scripted_overlay_storage", ":free_offset", ":data_size"),
(val_add, ":free_offset", ":data_size"),
(troop_set_slot, "trp_scripted_overlay_storage", 0, ":free_offset"),
(assign, reg1, ":button"),
]),

("combobox_scripted_mouse_enter_leave", [
(store_trigger_param, ":object", 1),
(store_trigger_param, ":value", 2),
(assign, ":end", 1),
(assign, ":offset", 1),
(try_for_range, ":unused", 0, ":end"),
	(gt, ":end", 1000000), #prevent softlock
(else_try),
	(troop_slot_eq, "trp_scripted_overlay_storage", ":offset", 0),
(else_try),
	(val_add, ":end", 1),
	(troop_get_slot, ":data_size", "trp_scripted_overlay_storage", ":offset"),
	(assign, ":cur_slot", ":offset"),
	(val_add, ":offset", ":data_size"), #next scripted button
	(val_add, ":cur_slot", 1), (troop_get_slot, ":button", "trp_scripted_overlay_storage", ":cur_slot"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":string", "trp_scripted_overlay_storage", ":cur_slot"),
	(eq, ":string", "str_ui_create_combobox_scripted"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":num_items", "trp_scripted_overlay_storage", ":cur_slot"),
	(store_add, ":mesh_u", ":button", 1),
	(try_begin),
		(eq, ":object", ":mesh_u"),
		(eq, ":value", 0),
		(overlay_set_display, ":mesh_u", 0),
	(else_try),
		(eq, ":object", ":button"),
		(eq, ":value", 1),
		(overlay_set_display, ":mesh_u", 1),
	(else_try),
		(try_for_range, ":item_no", 0, ":num_items"),
			(val_mul, ":item_no", 3),
			(store_add, ":cur_item_button", l.button + 4, l.item_no),
			(store_add, ":mesh_child_u", ":cur_item_button", 1),
			(store_add, ":label_child_u", ":cur_item_button", 2),
			(try_begin),
			  (eq, ":object", ":label_child_u"),
			  (eq, ":value", 0),
			  (overlay_set_display, ":mesh_child_u", 0),
			(else_try),
			  (eq, ":object", ":label_child_u"),
			  (eq, ":value", 1),
			  (overlay_set_display, ":mesh_child_u", 1),
			(try_end),
		(try_end),
	(try_end),
(try_end),
]),

#Return new object and value
("cf_combobox_event_state_change", [
(set_fixed_point_multiplier, 1000),
(store_trigger_param, ":object", 1),
(store_trigger_param, ":value", 2),
(assign, ":fail", 0),
(assign, ":end", 1),
(assign, ":offset", 1),
(try_for_range, ":unused", 0, ":end"),
	(gt, ":end", 1000000), #prevent softlock
(else_try),
	(troop_slot_eq, "trp_scripted_overlay_storage", ":offset", 0),
(else_try),
	(val_add, ":end", 1),
	(troop_get_slot, ":data_size", "trp_scripted_overlay_storage", ":offset"),
	(assign, ":cur_slot", ":offset"),
	(val_add, ":offset", ":data_size"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":button", "trp_scripted_overlay_storage", ":cur_slot"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":string", "trp_scripted_overlay_storage", ":cur_slot"),
	(eq, ":string", "str_ui_create_combobox_scripted"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":num_items", "trp_scripted_overlay_storage", ":cur_slot"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":item_names_script", "trp_scripted_overlay_storage", ":cur_slot"),
	(val_add, ":cur_slot", 1), #(troop_get_slot, ":cur_item", "trp_scripted_overlay_storage", ":cur_slot"),
	(try_begin),
		(eq, ":object", ":button"),
		(store_add, ":container", ":button", 3),
		(overlay_get_position, pos1, ":container"),
		(position_get_y, ":container_pos_y", pos1),
		(val_add, ":container_pos_y", 750),
		(position_set_y, pos1, ":container_pos_y"),
		(overlay_set_position, ":container", pos1),
		(overlay_set_display, ":button", 0),
		(assign, ":fail", 1),
	(else_try),
		(assign, ":end", ":num_items"),
		(try_for_range, ":item_no", 0, ":end"),
			(store_add, ":cur_item_button", l.button + 4, l.item_no * 3),
			(eq, ":object", ":cur_item_button"),
			(assign, ":end", 0),
			(assign, ":object", ":button"),
			(assign, ":value", ":item_no"),
			(store_sub, ":cur_slot", ":offset", ":data_size"),
			(val_add, ":cur_slot", 5),
			(troop_set_slot, "trp_scripted_overlay_storage", ":cur_slot", ":value"),
			(call_script, ":item_names_script"),
			(store_add, ":label_button", ":button", 2),
			(store_sub, ":max_item_value", ":num_items", 1),
			(store_sub, ":display_name", ":max_item_value", ":value"),
			(val_add, ":display_name", 4),
			(overlay_set_text, ":label_button", ":display_name"),
			(overlay_set_display, ":button", 1),
			(store_add, ":container", ":button", 3),
			(overlay_get_position, pos1, ":container"),
			(position_get_y, ":container_pos_y", pos1),
			(try_begin),
	  			(gt, ":container_pos_y", 0),
	  			(val_sub, ":container_pos_y", 750),
	  			(position_set_y, pos1, ":container_pos_y"),
	  			(overlay_set_position, ":container", pos1),
			(try_end),
			(store_add, ":mesh_parent_u", ":button", 1),
			(overlay_set_display, ":mesh_parent_u", 1),
		(try_end),
	(try_end),
(try_end),
(eq, ":fail", 0),
(assign, reg0, ":object"),
(assign, reg1, ":value"),
]),

("combobox_mouse_press", [
(store_trigger_param, ":value", 2),
(try_begin),
	(eq, ":value", 0), #left mouse button
	(set_fixed_point_multiplier, 1000),
	(assign, ":end", 1),
	(assign, ":offset", 1),
	(try_for_range, ":unused", 0, ":end"),
		(gt, ":end", 1000000), #prevent softlock
	(else_try),
		(troop_slot_eq, "trp_scripted_overlay_storage", ":offset", 0),
	(else_try),
		(val_add, ":end", 1),
		(troop_get_slot, ":data_size", "trp_scripted_overlay_storage", ":offset"),
		(assign, ":cur_slot", ":offset"),
		(val_add, ":offset", ":data_size"),
		(val_add, ":cur_slot", 1), (troop_get_slot, ":button", "trp_scripted_overlay_storage", ":cur_slot"),
		(val_add, ":cur_slot", 1), (troop_get_slot, ":string", "trp_scripted_overlay_storage", ":cur_slot"),
		(eq, ":string", "str_ui_create_combobox_scripted"),
		(try_begin),
			(val_add, ":cur_slot", 1), #(troop_get_slot, ":num_items", "trp_scripted_overlay_storage", ":cur_slot"),
			(val_add, ":cur_slot", 1), #(troop_get_slot, ":item_names_script", "trp_scripted_overlay_storage", ":cur_slot"),
			(val_add, ":cur_slot", 1), #(troop_get_slot, ":cur_item", "trp_scripted_overlay_storage", ":cur_slot"),
			(val_add, ":cur_slot", 1), (troop_get_slot, ":container_x", "trp_scripted_overlay_storage", ":cur_slot"),
			(val_add, ":cur_slot", 1), (troop_get_slot, ":container_y", "trp_scripted_overlay_storage", ":cur_slot"),
			(store_add, ":container", ":button", 3),
			(overlay_get_position, pos1, ":container"),
			(position_get_y, ":container_pos_y", pos1),
			(gt, ":container_pos_y", 0),
			(mouse_get_position, pos10),
			(position_get_x, ":mouse_x", pos10),
			(position_get_y, ":mouse_y", pos10),
			(position_get_x, ":container_pos_x", pos1),
			(store_add, ":upper_bound_x", ":container_pos_x", ":container_x"),
			(store_add, ":upper_bound_y", ":container_pos_y", ":container_y"),
			(this_or_next|negate|is_between, ":mouse_x", ":container_pos_x", ":upper_bound_x"),
			(negate|is_between, ":mouse_y", ":container_pos_y", ":upper_bound_y"),
			(val_sub, ":container_pos_y", 750),
			(position_set_y, pos1, ":container_pos_y"),
			(overlay_set_position, ":container", pos1),
			(store_add, ":mesh_parent_u", ":button", 1),
			(overlay_set_display, ":button", 1),
			(overlay_set_display, ":mesh_parent_u", 1),
		(try_end),
	(try_end),
(try_end),
]),

#Input: troop_storage
("clear_storage", [
(store_script_param, ":storage", 1),
(assign, ":end", 1),
(assign, ":offset", 1),
(try_for_range, ":unused", 0, ":end"),
	(gt, ":end", 10000),
(else_try),
	(troop_slot_eq, ":storage", ":offset", 0),
(else_try),
	(val_add, ":end", 1),
	(troop_get_slot, ":data_size", ":storage", ":offset"),
	(assign, ":start", ":offset"),
	(val_add, ":offset", ":data_size"),
	(try_for_range, ":slot_no", ":start", ":offset"),
		(troop_set_slot, ":storage", ":slot_no", 0),
	(try_end),
(try_end),
(troop_set_slot, ":storage", 0, 1),
]),

("overlay_scripted_set_display", [
(store_script_param, ":overlay_id", 1),
(store_script_param, ":display", 2),
(assign, ":end", 1),
(assign, ":offset", 1),
(try_for_range, ":unused", 0, ":end"),
	(gt, ":end", 10000),
(else_try),
	(troop_slot_eq, "trp_scripted_overlay_storage", ":offset", 0),
(else_try),
	(val_add, ":end", 1),
	(troop_get_slot, ":data_size", "trp_scripted_overlay_storage", ":offset"),
	(assign, ":cur_slot", ":offset"),
	(val_add, ":offset", ":data_size"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":cur_overlay", "trp_scripted_overlay_storage", ":cur_slot"),
	(eq, ":cur_overlay", ":overlay_id"),
	(try_begin),
		(val_add, ":cur_slot", 1), (troop_get_slot, ":string", "trp_scripted_overlay_storage", ":cur_slot"),
		(eq, ":string", "str_ui_create_combobox_scripted"),
		(overlay_set_display, ":overlay_id", ":display"),
		(store_sub, ":mesh_d", ":overlay_id", 1), (overlay_set_display, ":mesh_d", ":display"),
		(store_add, ":mesh_u", ":overlay_id", 1), (overlay_set_display, ":mesh_u", ":display"),
		(store_add, ":mesh_label", ":overlay_id", 2), (overlay_set_display, ":mesh_label", ":display"),
	(try_end),
(try_end),
]),

("overlay_scripted_set_val", [
(store_script_param, ":overlay_id", 1),
(store_script_param, ":value", 2),
(assign, ":end", 1),
(assign, ":offset", 1),
(try_for_range, ":unused", 0, ":end"),
	(gt, ":end", 10000),
(else_try),
	(troop_slot_eq, "trp_scripted_overlay_storage", ":offset", 0),
(else_try),
	(val_add, ":end", 1),
	(troop_get_slot, ":data_size", "trp_scripted_overlay_storage", ":offset"),
	(assign, ":cur_slot", ":offset"),
	(val_add, ":offset", ":data_size"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":cur_overlay", "trp_scripted_overlay_storage", ":cur_slot"),
	(eq, ":cur_overlay", ":overlay_id"),
	(try_begin),
		(val_add, ":cur_slot", 1), (troop_get_slot, ":string", "trp_scripted_overlay_storage", ":cur_slot"),
		(eq, ":string", "str_ui_create_combobox_scripted"),
		(val_add, ":cur_slot", 1), (troop_get_slot, ":num_items", "trp_scripted_overlay_storage", ":cur_slot"),
		(val_add, ":cur_slot", 1), (troop_get_slot, ":item_names_script", "trp_scripted_overlay_storage", ":cur_slot"),
		(val_add, ":cur_slot", 1), (troop_set_slot, "trp_scripted_overlay_storage", ":cur_slot", ":value"),
		(call_script, ":item_names_script"),
		(store_add, ":label", ":overlay_id", 2),
		(overlay_set_text, ":label", (l.num_items - 1) - l.value + 4),
	(try_end),
(try_end),
]),

#Output: reg0 - value
("overlay_scripted_get_val", [
(store_script_param, ":overlay_id", 1),
(assign, ":end", 1),
(assign, ":offset", 1),
(try_for_range, ":unused", 0, ":end"),
	(gt, ":end", 10000),
(else_try),
	(troop_slot_eq, "trp_scripted_overlay_storage", ":offset", 0),
(else_try),
	(val_add, ":end", 1),
	(troop_get_slot, ":data_size", "trp_scripted_overlay_storage", ":offset"),
	(assign, ":cur_slot", ":offset"),
	(val_add, ":offset", ":data_size"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":cur_overlay", "trp_scripted_overlay_storage", ":cur_slot"),
	(eq, ":cur_overlay", ":overlay_id"),
	(try_begin),
		(val_add, ":cur_slot", 1), (troop_get_slot, ":string", "trp_scripted_overlay_storage", ":cur_slot"),
		(eq, ":string", "str_ui_create_combobox_scripted"),
		(val_add, ":cur_slot", 1), #(troop_get_slot, ":num_items", "trp_scripted_overlay_storage", ":cur_slot"),
		(val_add, ":cur_slot", 1), #(troop_get_slot, ":item_names_script", "trp_scripted_overlay_storage", ":cur_slot"),
		(val_add, ":cur_slot", 1), (troop_get_slot, ":value", "trp_scripted_overlay_storage", ":cur_slot"),
	(try_end),
(try_end),
(assign, reg0, ":value"),
]),

# script_overlay_scripted_item_set_text
("overlay_scripted_item_set_text", [
(store_script_param, ":overlay", 1),
(store_script_param, ":item", 2),
(store_script_param, ":text", 3),
(assign, ":end", 1),
(assign, ":offset", 1),
(try_for_range, ":unused", 0, ":end"),
	(gt, ":end", 10000),
(else_try),
	(troop_slot_eq, "trp_scripted_overlay_storage", ":offset", 0),
(else_try),
	(val_add, ":end", 1),
	(troop_get_slot, ":data_size", "trp_scripted_overlay_storage", ":offset"),
	(assign, ":cur_slot", ":offset"),
	(val_add, ":offset", ":data_size"),
	(val_add, ":cur_slot", 1), (troop_get_slot, ":cur_overlay", "trp_scripted_overlay_storage", ":cur_slot"),
	(eq, ":cur_overlay", ":overlay"),
	(try_begin),
		(val_add, ":cur_slot", 1), (troop_get_slot, ":string", "trp_scripted_overlay_storage", ":cur_slot"),
		(eq, ":string", "str_ui_create_combobox_scripted"),
		(val_add, ":cur_slot", 1), #(troop_get_slot, ":num_items", "trp_scripted_overlay_storage", ":cur_slot"),
		(val_add, ":cur_slot", 1), #(troop_get_slot, ":item_names_script", "trp_scripted_overlay_storage", ":cur_slot"),
		(val_add, ":cur_slot", 1), #(troop_get_slot, ":value", "trp_scripted_overlay_storage", ":cur_slot"),
		(store_add, ":item_label", l.overlay + 4, l.item * 3 + 2),
		(overlay_set_text, ":item_label", ":text"),
		(overlay_scripted_get_val, ":value", ":overlay"),
		(try_begin),
			(eq, ":item", ":value"),
			(store_add, ":label", ":overlay", 2),
			(overlay_set_text, ":label", ":text"),
		(try_end),
	(try_end),
(try_end),
]),
## END COMBOBOX #############################################################

# script_store_overlay_data
("store_overlay_data", [
(store_script_param, ":overlay_id", 1),
(store_script_param, ":string_id", 2),
(store_script_param, ":pos_x", 3),
(store_script_param, ":pos_y", 4),
(store_script_param, ":size_x", 5),
(store_script_param, ":size_y", 6),
(store_script_param, ":area_size_x", 7),
(store_script_param, ":area_size_y", 8),
(store_script_param, ":color", 9),
(store_script_param, ":alignment", 10),
(store_script_param, ":rotation_z", 11),
(store_script_param, ":rotation_x", 12),
(store_script_param, ":rotation_y", 13),
(troop_get_slot, ":free_offset", "trp_overlay_storage", 0),
(store_add, ":slot_no", ":free_offset", 1),	(troop_set_slot, "trp_overlay_storage", ":slot_no", ":overlay_id"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":string_id"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":pos_x"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":pos_y"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":size_x"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":size_y"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":area_size_x"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":area_size_y"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":color"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":alignment"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":rotation_z"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":rotation_x"),
(val_add, ":slot_no", 1),						(troop_set_slot, "trp_overlay_storage", ":slot_no", ":rotation_y"),
(val_add, ":slot_no", 1), 
(store_sub, ":length", ":slot_no", ":free_offset"),
(troop_set_slot, "trp_overlay_storage", ":free_offset", ":length"), #data size
(troop_set_slot, "trp_overlay_storage", 0, ":slot_no"), #free offset
]),
]

def find_custom_operation(script_name, custom_operation_name, glob, array, empty_array):
	for script in glob['scripts']:
		if script[0] == script_name:
			for operator in script[1]:
				if not(type(operator) == tuple): continue
				elif (isinstance(operator[0], CUSTOM_OPERATION)) and (operator[0].name == custom_operation_name):
					array.add(script[0])
					return True
				elif (operator[0] == call_script) and (operator[1] in array):
					array.add(script[0])
					return True
				elif (operator[0] == call_script) and (operator[1] != script_name) and not(operator[1] in empty_array) and find_custom_operation(operator[1], custom_operation_name, glob, array, empty_array):
					array.add(script[0])
					return True
			else: empty_array.add(script[0])
			break
	return False

def preprocess_entities(glob):
	# Integrate scripted overlays to all presentations
	ui_create_combobox_scripted_set = set()
	empty_scripts_set = set()
	for script in glob['scripts']:
		if find_custom_operation(script[0], "ui_create_combobox_scripted", glob, ui_create_combobox_scripted_set, empty_scripts_set): ui_create_combobox_scripted_set.add(script[0])
		else: empty_scripts_set.add(script[0])

	for presentation_no in glob['presentations']:
		add_scripted_code_for_combobox = False
		for cur_trigger in presentation_no[3]:
			for operator in cur_trigger[1]:
				if not(type(operator) == tuple): continue 
				elif (isinstance(operator[0], CUSTOM_OPERATION)) and (operator[0].name == "ui_create_combobox_scripted"):
					add_scripted_code_for_combobox = True
					break
				elif (operator[0] == call_script):
					if operator[1][7:] in ui_create_combobox_scripted_set:
						add_scripted_code_for_combobox = True
						break
			if add_scripted_code_for_combobox == True: break
		if add_scripted_code_for_combobox == True:
			for cur_trigger in presentation_no[3]:
				if cur_trigger[0] == ti_on_presentation_load: break
			else: presentation_no[3].append((ti_on_presentation_load,[]))
			for cur_trigger in presentation_no[3]:
				if cur_trigger[0] == ti_on_presentation_mouse_enter_leave: break
			else: presentation_no[3].append((ti_on_presentation_mouse_enter_leave,[]))
			for cur_trigger in presentation_no[3]:
				if cur_trigger[0] == ti_on_presentation_event_state_change: break
			else: presentation_no[3].append((ti_on_presentation_event_state_change,[]))
			for cur_trigger in presentation_no[3]:
				if cur_trigger[0] == ti_on_presentation_mouse_press: break
			else: presentation_no[3].append((ti_on_presentation_mouse_press,[]))
			for cur_trigger in presentation_no[3]:
				if cur_trigger[0] == ti_on_presentation_load: cur_trigger[1].insert(0, (call_script, "script_clear_storage", "trp_scripted_overlay_storage"))
				if cur_trigger[0] == ti_on_presentation_mouse_enter_leave:
					if add_scripted_code_for_combobox == True: cur_trigger[1].append((call_script, "script_combobox_scripted_mouse_enter_leave"))
				if cur_trigger[0] == ti_on_presentation_event_state_change:
					if add_scripted_code_for_combobox == True:
						object_string = ":unused_object"
						value_string = ":unused_value"
						for operator in reversed(cur_trigger[1]):
							if type(operator) == tuple:
								if (operator[0] == store_trigger_param_1) or ((operator[0] == store_trigger_param) and (operator[2] == 1)):
									object_string = operator[1]
									cur_trigger[1].remove(operator)
								elif (operator[0] == store_trigger_param_2) or ((operator[0] == store_trigger_param) and (operator[2] == 2)):
									value_string = operator[1]
									cur_trigger[1].remove(operator)
						cur_trigger[1].insert(0, (call_script, "script_cf_combobox_event_state_change"))
						cur_trigger[1].insert(1, (assign, object_string, reg0))
						cur_trigger[1].insert(2, (assign, value_string, reg1))
				if cur_trigger[0] == ti_on_presentation_mouse_press:
					if add_scripted_code_for_combobox == True: cur_trigger[1].append((call_script, "script_combobox_mouse_press"))

	#glob['strings'][4:4] = [("register_s%d" % i, "{!}{s%d}" % i) for i in range(4, 128)]
	#calculate_identifiers(strings, s)