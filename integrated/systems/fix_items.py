from compiler import *
register_plugin()

#Can fix multiplayer crash when you look at dropped item. 

def preprocess_entities(glob):
  # generate dummy props to avoid item spawn issues on dedicated servers
  if len(glob['scene_props']) < len(glob['items']): #more items than props
    for i in range(len(glob['scene_props']), len(glob['items'])):
        glob['scene_props'].append(("zyx_dummy_prop_"+str(i), 0, 0, 0, []))
