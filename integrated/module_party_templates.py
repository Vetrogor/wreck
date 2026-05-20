from compiler import * # should be after all imports

####################################################################################################################
#  Each party template record contains the following fields:
#  1) Party-template id: used for referencing party-templates in other files.
#     The prefix pt_ is automatically added before each party-template id.
#  2) Party-template name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Faction
#  6) Personality. See header_parties.py for an explanation of personality flags.
#  7) List of stacks. Each stack record is a tuple that contains the following fields:
#    7.1) Troop-id. 
#    7.2) Minimum number of troops in the stack. 
#    7.3) Maximum number of troops in the stack. 
#    7.4) Member flags(optional). Use pmf_is_prisoner to note that this member is a prisoner.
#     Note: There can be at most 6 stacks.
####################################################################################################################


party_templates = [
  ("none","none",icon.gray_knight,0,fac.commoners,merchant_personality,[]),
  ("rescued_prisoners","Rescued Prisoners",icon.gray_knight,0,fac.commoners,merchant_personality,[]),
  ("enemy","Enemy",icon.gray_knight,0,fac.undeads,merchant_personality,[]),
  ("hero_party","Hero Party",icon.gray_knight,0,fac.commoners,merchant_personality,[]),
####################################################################################################################
# Party templates before this point are hard-wired into the game and should not be changed. 
####################################################################################################################
##  ("old_garrison","Old Garrison",icon.vaegir_knight,0,fac.neutral,merchant_personality,[]),
  ("village_defenders","Village Defenders",icon.peasant,0,fac.commoners,merchant_personality,[(trp.farmer,10,20),(trp.peasant_woman,0,4)]),

  ("cattle_herd","Cattle Herd",icon.cattle|carries_goods(10),0,fac.neutral,merchant_personality,[(trp.cattle,80,120)]),

##  ("vaegir_nobleman","Vaegir Nobleman",icon.vaegir_knight|carries_goods(10)|pf_quest_party,0,fac.commoners,merchant_personality,[(trp.nobleman,1,1),(trp.vaegir_knight,2,6),(trp.vaegir_horseman,4,12)]),
##  ("swadian_nobleman","Swadian Nobleman",icon.gray_knight|carries_goods(10)|pf_quest_party,0,fac.commoners,merchant_personality,[(trp.nobleman,1,1),(trp.swadian_knight,2,6),(trp.swadian_man_at_arms,4,12)]),
# Ryan BEGIN
  ("looters","Looters",icon.axeman|carries_goods(8),0,fac.outlaws,bandit_personality,[(trp.looter,3,45)]),
# Ryan END
  ("manhunters","Manhunters",icon.gray_knight,0,fac.manhunters,soldier_personality,[(trp.manhunter,9,40)]),
##  ("peasant","Peasant",icon.peasant,0,fac.commoners,merchant_personality,[(trp.farmer,1,6),(trp.peasant_woman,0,7)]),

#  ("black_khergit_raiders","Black Khergit Raiders",icon.khergit_horseman_b|carries_goods(2),0,fac.black_khergits,bandit_personality,[(trp.black_khergit_guard,1,10),(trp.black_khergit_horseman,5,5)]),
  ("steppe_bandits","Steppe Bandits",icon.khergit|carries_goods(2),0,fac.outlaws,bandit_personality,[(trp.steppe_bandit,4,58)]),
  ("taiga_bandits","Tundra Bandits",icon.axeman|carries_goods(2),0,fac.outlaws,bandit_personality,[(trp.taiga_bandit,4,58)]),
  ("desert_bandits","Desert Bandits",icon.vaegir_knight|carries_goods(2),0,fac.outlaws,bandit_personality,[(trp.desert_bandit,4,58)]),
  ("forest_bandits","Forest Bandits",icon.axeman|carries_goods(2),0,fac.forest_bandits,bandit_personality,[(trp.forest_bandit,4,52)]),
  ("mountain_bandits","Mountain Bandits",icon.axeman|carries_goods(2),0,fac.mountain_bandits,bandit_personality,[(trp.mountain_bandit,4,60)]),
  ("sea_raiders","Sea Raiders",icon.axeman|carries_goods(2),0,fac.outlaws,bandit_personality,[(trp.sea_raider,5,50)]),

  ("deserters","Deserters",icon.vaegir_knight|carries_goods(3),0,fac.deserters,bandit_personality,[]),
    
  ("merchant_caravan","Merchant Caravan",icon.gray_knight|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac.commoners,escorted_merchant_personality,[(trp.caravan_master,1,1),(trp.caravan_guard,5,25)]),
  ("troublesome_bandits","Troublesome Bandits",icon.axeman|carries_goods(9)|pf_quest_party,0,fac.outlaws,bandit_personality,[(trp.bandit,14,55)]),
  ("bandits_awaiting_ransom","Bandits Awaiting Ransom",icon.axeman|carries_goods(9)|pf_auto_remove_in_town|pf_quest_party,0,fac.neutral,bandit_personality,[(trp.bandit,24,58),(trp.kidnapped_girl,1,1,pmf_is_prisoner)]),
  ("kidnapped_girl","Kidnapped Girl",icon.woman|pf_quest_party,0,fac.neutral,merchant_personality,[(trp.kidnapped_girl,1,1)]),

  ("village_farmers","Village Farmers",icon.peasant|pf_civilian,0,fac.innocents,merchant_personality,[(trp.farmer,5,10),(trp.peasant_woman,3,8)]),

  ("spy_partners", "Unremarkable Travellers", icon.gray_knight|carries_goods(10)|pf_default_behavior|pf_quest_party,0,fac.neutral,merchant_personality,[(trp.spy_partner,1,1),(trp.caravan_guard,5,11)]),
  ("runaway_serfs","Runaway Serfs",icon.peasant|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac.neutral,merchant_personality,[(trp.farmer,6,7), (trp.peasant_woman,3,3)]),
  ("spy", "Ordinary Townsman", icon.gray_knight|carries_goods(4)|pf_default_behavior|pf_quest_party,0,fac.neutral,merchant_personality,[(trp.spy,1,1)]),
  ("sacrificed_messenger", "Sacrificed Messenger", icon.gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac.neutral,merchant_personality,[]),
##  ("conspirator", "Conspirators", icon.gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac.neutral,merchant_personality,[(trp.conspirator,3,4)]),
##  ("conspirator_leader", "Conspirator Leader", icon.gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac.neutral,merchant_personality,[(trp.conspirator_leader,1,1)]),
##  ("peasant_rebels", "Peasant Rebels", icon.peasant,0,fac.peasant_rebels,bandit_personality,[(trp.peasant_rebel,33,97)]),
##  ("noble_refugees", "Noble Refugees", icon.gray_knight|carries_goods(12)|pf_quest_party,0,fac.noble_refugees,merchant_personality,[(trp.noble_refugee,3,5),(trp.noble_refugee_woman,5,7)]),

  ("forager_party","Foraging Party",icon.gray_knight|carries_goods(5)|pf_show_faction,0,fac.commoners,merchant_personality,[]),
  ("scout_party","Scouts",icon.gray_knight|carries_goods(1)|pf_show_faction,0,fac.commoners,bandit_personality,[]),
  ("patrol_party","Patrol",icon.gray_knight|carries_goods(2)|pf_show_faction,0,fac.commoners,soldier_personality,[]),
#  ("war_party", "War Party",icon.gray_knight|carries_goods(3),0,fac.commoners,soldier_personality,[]),
  ("messenger_party","Messenger",icon.gray_knight|pf_show_faction,0,fac.commoners,merchant_personality,[]),
  ("raider_party","Raiders",icon.gray_knight|carries_goods(16)|pf_quest_party,0,fac.commoners,bandit_personality,[]),
  ("raider_captives","Raider Captives",0,0,fac.commoners,0,[(trp.peasant_woman,6,30,pmf_is_prisoner)]),
  ("kingdom_caravan_party","Caravan",icon.mule|carries_goods(25)|pf_show_faction,0,fac.commoners,merchant_personality,[(trp.caravan_master,1,1),(trp.caravan_guard,12,40)]),
  ("prisoner_train_party","Prisoner Train",icon.gray_knight|carries_goods(5)|pf_show_faction,0,fac.commoners,merchant_personality,[]),
  ("default_prisoners","Default Prisoners",0,0,fac.commoners,0,[(trp.bandit,5,10,pmf_is_prisoner)]),

  ("routed_warriors","Routed Enemies",icon.vaegir_knight,0,fac.commoners,soldier_personality,[]),


# Caravans
  ("center_reinforcements","Reinforcements",icon.axeman|carries_goods(16),0,fac.commoners,soldier_personality,[(trp.townsman,5,30),(trp.watchman,4,20)]),  

  ("kingdom_hero_party","War Party",icon.flagbearer_a|pf_show_faction|pf_default_behavior,0,fac.commoners,soldier_personality,[]),
  
# Reinforcements
  # each faction includes three party templates. One is less-modernised, one is med-modernised and one is high-modernised
  # less-modernised templates are generally includes 7-14 troops in total, 
  # med-modernised templates are generally includes 5-10 troops in total, 
  # high-modernised templates are generally includes 3-5 troops in total

  ("kingdom_1_reinforcements_a", "{!}kingdom_1_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.swadian_recruit,5,10),(trp.swadian_militia,2,4)]),
  ("kingdom_1_reinforcements_b", "{!}kingdom_1_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.swadian_footman,3,6),(trp.swadian_skirmisher,2,4)]),
  ("kingdom_1_reinforcements_c", "{!}kingdom_1_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.swadian_man_at_arms,2,4),(trp.swadian_crossbowman,1,2)]), #Swadians are a bit less-powered thats why they have a bit more troops in their modernised party template (3-6, others 3-5)

  ("kingdom_2_reinforcements_a", "{!}kingdom_2_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.vaegir_recruit,5,10),(trp.vaegir_footman,2,4)]),
  ("kingdom_2_reinforcements_b", "{!}kingdom_2_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.vaegir_veteran,2,4),(trp.vaegir_skirmisher,2,4),(trp.vaegir_footman,1,2)]),
  ("kingdom_2_reinforcements_c", "{!}kingdom_2_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.vaegir_horseman,2,3),(trp.vaegir_infantry,1,2)]),

  ("kingdom_3_reinforcements_a", "{!}kingdom_3_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.khergit_tribesman,3,5),(trp.khergit_skirmisher,4,9)]), #Khergits are a bit less-powered thats why they have a bit more 2nd upgraded(trp.khergit_skirmisher) than non-upgraded one(trp.khergit_tribesman).
  ("kingdom_3_reinforcements_b", "{!}kingdom_3_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.khergit_horseman,2,4),(trp.khergit_horse_archer,2,4),(trp.khergit_skirmisher,1,2)]),
  ("kingdom_3_reinforcements_c", "{!}kingdom_3_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.khergit_horseman,2,4),(trp.khergit_veteran_horse_archer,2,3)]), #Khergits are a bit less-powered thats why they have a bit more troops in their modernised party template (4-7, others 3-5)

  ("kingdom_4_reinforcements_a", "{!}kingdom_4_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.nord_footman,5,10),(trp.nord_recruit,2,4)]),
  ("kingdom_4_reinforcements_b", "{!}kingdom_4_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.nord_huntsman,2,5),(trp.nord_archer,2,3),(trp.nord_footman,1,2)]),
  ("kingdom_4_reinforcements_c", "{!}kingdom_4_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.nord_warrior,3,5)]),

  ("kingdom_5_reinforcements_a", "{!}kingdom_5_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.rhodok_tribesman,5,10),(trp.rhodok_spearman,2,4)]),
  ("kingdom_5_reinforcements_b", "{!}kingdom_5_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.rhodok_crossbowman,3,6),(trp.rhodok_trained_crossbowman,2,4)]),
  ("kingdom_5_reinforcements_c", "{!}kingdom_5_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.rhodok_veteran_spearman,2,3),(trp.rhodok_veteran_crossbowman,1,2)]), 

  ("kingdom_6_reinforcements_a", "{!}kingdom_6_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.sarranid_recruit,5,10),(trp.sarranid_footman,2,4)]),
  ("kingdom_6_reinforcements_b", "{!}kingdom_6_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.sarranid_skirmisher,2,4),(trp.sarranid_veteran_footman,2,3),(trp.sarranid_footman,1,3)]),
  ("kingdom_6_reinforcements_c", "{!}kingdom_6_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.sarranid_horseman,3,5)]),

##  ("kingdom_1_reinforcements_a", "kingdom_1_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.swadian_footman,3,7),(trp.swadian_skirmisher,5,10),(trp.swadian_militia,11,26)]),
##  ("kingdom_1_reinforcements_b", "kingdom_1_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.swadian_man_at_arms,5,10),(trp.swadian_infantry,5,10),(trp.swadian_crossbowman,3,8)]),
##  ("kingdom_1_reinforcements_c", "kingdom_1_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.swadian_knight,2,6),(trp.swadian_sergeant,2,5),(trp.swadian_sharpshooter,2,5)]),
##
##  ("kingdom_2_reinforcements_a", "kingdom_2_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.vaegir_veteran,3,7),(trp.vaegir_skirmisher,5,10),(trp.vaegir_footman,11,26)]),
##  ("kingdom_2_reinforcements_b", "kingdom_2_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.vaegir_horseman,4,9),(trp.vaegir_infantry,5,10),(trp.vaegir_archer,3,8)]),
##  ("kingdom_2_reinforcements_c", "kingdom_2_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.vaegir_knight,3,7),(trp.vaegir_guard,2,5),(trp.vaegir_marksman,2,5)]),
##
##  ("kingdom_3_reinforcements_a", "kingdom_3_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.khergit_horseman,3,7),(trp.khergit_skirmisher,5,10),(trp.khergit_tribesman,11,26)]),
##  ("kingdom_3_reinforcements_b", "kingdom_3_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.khergit_veteran_horse_archer,4,9),(trp.khergit_horse_archer,5,10),(trp.khergit_horseman,3,8)]),
##  ("kingdom_3_reinforcements_c", "kingdom_3_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.khergit_lancer,3,7),(trp.khergit_veteran_horse_archer,2,5),(trp.khergit_horse_archer,2,5)]),
##
##  ("kingdom_4_reinforcements_a", "kingdom_4_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.nord_trained_footman,3,7),(trp.nord_footman,5,10),(trp.nord_recruit,11,26)]),
##  ("kingdom_4_reinforcements_b", "kingdom_4_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.nord_veteran,4,9),(trp.nord_warrior,5,10),(trp.nord_footman,3,8)]),
##  ("kingdom_4_reinforcements_c", "kingdom_4_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.nord_champion,1,3),(trp.nord_veteran,2,5),(trp.nord_warrior,2,5)]),
##
##  ("kingdom_5_reinforcements_a", "kingdom_5_reinforcements_a", 0, 0, fac.commoners, 0, [(trp.rhodok_spearman,3,7),(trp.rhodok_crossbowman,5,10),(trp.rhodok_tribesman,11,26)]),
##  ("kingdom_5_reinforcements_b", "kingdom_5_reinforcements_b", 0, 0, fac.commoners, 0, [(trp.rhodok_trained_spearman,4,9),(trp.rhodok_spearman,5,10),(trp.rhodok_crossbowman,3,8)]),
##  ("kingdom_5_reinforcements_c", "kingdom_5_reinforcements_c", 0, 0, fac.commoners, 0, [(trp.rhodok_sergeant,3,7),(trp.rhodok_veteran_spearman,2,5),(trp.rhodok_veteran_crossbowman,2,5)]),



  ("steppe_bandit_lair" ,"Steppe Bandit Lair",icon.bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac.neutral,bandit_personality,[(trp.steppe_bandit,15,58)]),
  ("taiga_bandit_lair","Tundra Bandit Lair",icon.bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac.neutral,bandit_personality,[(trp.taiga_bandit,15,58)]),
  ("desert_bandit_lair" ,"Desert Bandit Lair",icon.bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac.neutral,bandit_personality,[(trp.desert_bandit,15,58)]),
  ("forest_bandit_lair" ,"Forest Bandit Camp",icon.bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac.neutral,bandit_personality,[(trp.forest_bandit,15,58)]),
  ("mountain_bandit_lair" ,"Mountain Bandit Hideout",icon.bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac.neutral,bandit_personality,[(trp.mountain_bandit,15,58)]),
  ("sea_raider_lair","Sea Raider Landing",icon.bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac.neutral,bandit_personality,[(trp.sea_raider,15,50)]),
  ("looter_lair","Kidnappers' Hideout",icon.bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac.neutral,bandit_personality,[(trp.looter,15,25)]),
  
  ("bandit_lair_templates_end","{!}bandit_lair_templates_end",icon.axeman|carries_goods(2)|pf_is_static,0,fac.outlaws,bandit_personality,[(trp.sea_raider,15,50)]),

  ("leaded_looters","Band of robbers",icon.axeman|carries_goods(8)|pf_quest_party,0,fac.neutral,bandit_personality,[(trp.looter_leader,1,1),(trp.looter,3,3)]),
]
