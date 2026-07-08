import sys
sys.dont_write_bytecode = True

from traceback import format_exc as formatted_exception, extract_stack
from inspect import currentframe as inspect_currentframe, getmembers as inspect_getmembers
from os.path import split as path_split, exists as path_exists
from copy import deepcopy, copy

# Color support
if 'bw' in sys.argv:
	COLORAMA = ('', '', '', '', '', '', '', '')
else:
	try:
		import colorama

		colorama.init()
#                     0-white    1-errors    2-green    3-yellow    4-blue      5-magenta   6-notices   7-white    8-lighter		
		COLORAMA = ('\x1b[0m', '\x1b[31m', '\x1b[32m', '\x1b[33m', '\x1b[34m', '\x1b[35m', '\x1b[36m', '\x1b[37m', '\x1b[1m')
	except:
		COLORAMA = ('', '', '', '', '', '', '', '')

get_globals = globals
get_locals = locals

check_nested_loops =  False if 'nested_loops' in sys.argv else True

try:
	from header_common import *
except:
	print(('\nError importing header_common.py file:\n\n%s' % formatted_exception()))
	if 'wait' in sys.argv: input('Press Enter to finish>')
	exit()

def parse_int(value):
	if isinstance(value, list) or isinstance(value, tuple): return list(map(parse_int, value))
	#if isinstance(value, VARIABLE) and value.is_static and (value.module is not None) and (value.module[5]): return int(value) & 0xffffffff
	try:
		if value.is_static and value.module[5]: return value.__int__() & 0xffffffff
	except: pass
	return int(value)

# Standard W.R.E.C.K. exception class. Used to differentiate Python-generated exceptions from internal exceptions,
# and to aggregate error information on different levels.
class MSException(Exception):

	def formatted(self):
		output = []
		for index in range(len(self.args)):
			prefix = '  ' * (index + 1)
			messages = self.args[index].strip().split('\n')
			for message in messages:
				output.append(prefix)
				output.append(message.strip())
				output.append('\n')
		return ''.join(output)



# Generic class which is used to quietly replace some pipe-joined lists in the game (particularly, item property list and troop attribute/skill/proficiency lists)
class AGGREGATE(dict):
	def __or__(self, other):
		if not other: return self
		result = AGGREGATE(self)
		for key, value in other.items():
			if type(value) == float: result[key] = max(result.get(key, 0.0), value)
			else: result[key] = result.get(key, 0) | value
		#result.update(other)
		return result
	__ror__ = __radd__ = __add__ = __or__

# Standard operations to unparse certain vanilla bitmasks if they've been fed into the compiler
def unparse_item_aggregate(value):
	if isinstance(value, AGGREGATE): return value
	return AGGREGATE({
		'weight': get_weight(value),
		'head': get_head_armor(value),
		'body': get_body_armor(value),
		'leg': get_leg_armor(value),
		'diff': get_difficulty(value),
		'hp': get_hit_points(value) & 0x3ff, # patch for Native compiler glitch
		'speed': get_speed_rating(value),
		'msspd': get_missile_speed(value),
		'size': get_weapon_length(value),
		'qty': get_max_ammo(value),
		'swing': get_swing_damage(value),
		'thrust': get_thrust_damage(value),
		'abundance': get_abundance(value),
	})
def unparse_attr_aggregate(value):
	if isinstance(value, AGGREGATE): return value
	return AGGREGATE({
		'str': value & 0xFF,
		'agi': (value >> 8) & 0xFF,
		'int': (value >> 16) & 0xFF,
		'cha': (value >> 24) & 0xFF,
		'level': (value >> level_bits) & level_mask
	})
def unparse_wp_aggregate(value):
	if isinstance(value, AGGREGATE): return value
	return AGGREGATE([(i, (value >> (10*i)) & 0x3FF) for i in range(num_weapon_proficiencies)])
def unparse_terrain_aggregate(value):
	value = str(value).lower()
	if value[0:2] == '0x':
		value = value[2:]
		return AGGREGATE({
			'terrain_seed': int('0x0%s' % value[-4:], 16),
			'river_seed': int('0x0%s' % value[-12:-8], 16),
			'flora_seed': int('0x0%s' % value[-20:-16], 16),
			'size_x': int('0x0%s' % value[-29:-24], 16) & 0x3ff,
			'size_y': (int('0x0%s' % value[-29:-24], 16) >> 10) & 0x3ff,
			'valley': (int('0x0%s' % value[-39:-32], 16) >> 0) & 0x7f,
			'hill_height': (int('0x0%s' % value[-39:-32], 16) >> 7) & 0x7f,
			'ruggedness': (int('0x0%s' % value[-39:-32], 16) >> 14) & 0x7f,
			'vegetation': (int('0x0%s' % value[-39:-32], 16) >> 21) & 0x7f,
			'terrain': int('0x0%s' % value[-40:-39], 16),
			'polygon_size': (int('0x0%s' % value[-41:-40], 16) & 0x3) + 2,
			'disable_grass': (int('0x0%s' % value[-41:-40], 16) >> 2) & 0x1,
			'shade_occlude': (int('0x0%s' % value[-32:-31], 16) >> 2) & 0x1,
			'place_river': (int('0x0%s' % value[-32:-31], 16) >> 3) & 0x1,
			'deep_water': (int('0x0%s' % value[-16:-15], 16) >> 3) & 0x1,
		})
	else:
		value = int(value)
		return AGGREGATE({
			'terrain_seed': value & 0xffffffff,
			'river_seed': (value >> 32) & 0x7fffffff,
			'flora_seed': (value >> 64) & 0xffffffff,
			'deep_water': (value >> 63) & 0x1,
		})


# Basic W.R.E.C.K. class. Represents any valid game reference or object, including entity references, local & global variables, registers of all types, and mathematical expressions including all of the aforementioned data.
class VARIABLE(object):

	operations = set(['+', '-', '*', '/', '%', '**', '<<', '>>', '&', '|', '^', 'neg', 'abs', 'val'])

	references = None

	is_expression = False
	is_static = True

	module = None
	name = None
	value = None

	operation = None
	operands = None

	def __init__(self, module = None, name = None, value = None, operation = None, operands = None, static = True):
		self.module = module
		self.name = name
		self.references = set()
		if operation:
			self.operation = operation
			self.operands = operands
			self.is_expression = True
			if static:
				for operand in operands:
					if isinstance(operand, VARIABLE) and not operand.is_static: static = False
			if operation not in VARIABLE.operations: raise SyntaxError('Illegal MSC expression: %r' % self)
		else:
			self.value = value
		self.is_static = static

	def __add__(self, other):    return VARIABLE(operands = [self, other], operation = '+')
	def __sub__(self, other):    return VARIABLE(operands = [self, other], operation = '-')
	def __mul__(self, other):    return VARIABLE(operands = [self, other], operation = '*')
	def __truediv__(self, other):    return VARIABLE(operands = [self, other], operation = '/')
	def __mod__(self, other):    return VARIABLE(operands = [self, other], operation = '%')
	def __pow__(self, other):    return VARIABLE(operands = [self, other], operation = '**')
	def __lshift__(self, other): return VARIABLE(operands = [self, other], operation = '<<')
	def __rshift__(self, other): return VARIABLE(operands = [self, other], operation = '>>')
	def __and__(self, other):    return VARIABLE(operands = [self, other], operation = '&')
	def __or__(self, other):     return VARIABLE(operands = [self, other], operation = '|')

	def __radd__(self, other):    return VARIABLE(operands = [other, self], operation = '+')
	def __rsub__(self, other):    return VARIABLE(operands = [other, self], operation = '-')
	def __rmul__(self, other):    return VARIABLE(operands = [other, self], operation = '*')
	def __rdiv__(self, other):    return VARIABLE(operands = [other, self], operation = '/')
	def __rmod__(self, other):    return VARIABLE(operands = [other, self], operation = '%')
	def __rpow__(self, other):    return VARIABLE(operands = [other, self], operation = '**')
	def __rlshift__(self, other): return VARIABLE(operands = [other, self], operation = '<<')
	def __rrshift__(self, other): return VARIABLE(operands = [other, self], operation = '>>')
	def __rand__(self, other):    return VARIABLE(operands = [other, self], operation = '&')
	def __ror__(self, other):     return VARIABLE(operands = [other, self], operation = '|')

	def __neg__(self): return VARIABLE(operands = [self], operation = 'neg')
	def __pos__(self): return self
	def __abs__(self): return VARIABLE(operands = [self], operation = 'abs')

	def formatted_name(self):
		if self.is_expression: return '<expr>'
		if self.module is None: return '?.%s' % self.name
		if self.module[2] == 's':  return 'str_%s' % self.name
		return '%s.%s' % (self.module[2], self.name)

	def __str__(self):
		return str(self.__int__())

	def __repr__(self):
		if self.is_expression:
			if len(self.operands) == 1:
				result = '%s(%r)' % (self.operation, self.operands[0])
			else:
				operands = [(('(%r)' if (isinstance(op, VARIABLE) and op.is_expression and (len(op.operands) > 1)) else '%r') % op) for op in self.operands]
				result = (' %s ' % self.operation).join(operands)
		else:
			if self.is_static:
				value = '?' if self.value is None else str(self.value)
				result = '%s[#%s]' % (self.formatted_name(), value)
			else:
				value = '?' if self.value is None else str(self.value)
				result = '%s[@%s]' % (self.formatted_name(), value)
		return '<%s>' % result

	def __int__(self):
		try:
			if self.is_expression:
				if not self.is_static: raise MSException('expression %r is not static and cannot be calculated at compile-time' % self)
				if self.operation == 'neg': return -parse_int(self.operands[0])
				elif self.operation == 'abs': return abs(parse_int(self.operands[0]))
				elif self.operation == 'val': return parse_int(self.operands[0])
				elif self.operation == '+': return parse_int(self.operands[0]) + parse_int(self.operands[1])
				elif self.operation == '-': return parse_int(self.operands[0]) - parse_int(self.operands[1])
				elif self.operation == '*': return parse_int(self.operands[0]) * parse_int(self.operands[1])
				elif self.operation == '/': return parse_int(self.operands[0]) // parse_int(self.operands[1])
				elif self.operation == '%': return parse_int(self.operands[0]) % parse_int(self.operands[1])
				elif self.operation == '**': return parse_int(self.operands[0]) ** parse_int(self.operands[1])
				elif self.operation == '<<': return parse_int(self.operands[0]) << parse_int(self.operands[1])
				elif self.operation == '>>': return parse_int(self.operands[0]) >> parse_int(self.operands[1])
				elif self.operation == '&': return parse_int(self.operands[0]) & parse_int(self.operands[1])
				elif self.operation == '|': return parse_int(self.operands[0]) | parse_int(self.operands[1])
				else: raise MSException('expression %r contains illegal operation %s' % (self, self.operation))
			else:
				if self.value is not None: return self.value
				if self.is_static: raise MSException('identifier {0}{9}{1}{8} value is not defined.'.format(*COLORAMA, self))
				else: raise MSException('variable %r is not allocated' % self)
		except MSException as e:
			raise MSException('failed to calculate expression %r' % self, *e.args)
		except Exception as e:
			raise MSException('failed to calculate expression %r' % self, str(e))

	def __float__(self): return float(self.__int__())

	def __call__(self, script_name, destination, local_depth):
		try:
			total_commands = 1 # Usually an expression will generate one command
			operations = []
			tmp_used_loc = set()
			# Pre-calculate operands
			for index in range(len(self.operands)):
				operand = self.operands[index]
				if isinstance(operand, VARIABLE):
					if operand.is_expression and not(operand.is_static):
						operand = self.operands[index] = operand.newcopy() #Fix for mission_template triggers usage more than once
						local_tmp_id = 0
						while not local_tmp_id:
							local_tmp_id = WRECK.get_local_tmp_id(script_name, local_depth)
							if not local_tmp_id:
								local_depth += 1
						tmp_local = opmask_local_variable | local_tmp_id
						new_commands, new_operations, new_used_loc = operand(script_name, tmp_local, local_depth)
						operations.extend(new_operations)
						total_commands += new_commands
						tmp_used_loc.update(new_used_loc)
						self.operands[index] = tmp_local
						local_depth += 1
						#print('Operand %r depth %d' % (operand, local_depth))
					else:
						self.operands[index] = int(operand)
						if operand.module == WRECK.l: tmp_used_loc.add(operand.name)
			if self.operation   == 'neg': operations.extend([store_sub, 3, destination, 0, self.operands[0]])
			elif self.operation == 'abs':
				operations.extend([assign, 2, destination, self.operands[0], val_abs, 1, destination])
				total_commands += 1 # We generate two commands instead of one with this expression
			elif self.operation == 'val': operations.extend([assign, 2, destination, self.operands[0]])
			elif self.operation == '+'  : operations.extend([store_add, 3, destination, self.operands[0], self.operands[1]])
			elif self.operation == '-'  : operations.extend([store_sub, 3, destination, self.operands[0], self.operands[1]])
			elif self.operation == '*'  : operations.extend([store_mul, 3, destination, self.operands[0], self.operands[1]])
			elif self.operation == '/'  : operations.extend([store_div, 3, destination, self.operands[0], self.operands[1]])
			elif self.operation == '%'  : operations.extend([store_mod, 3, destination, self.operands[0], self.operands[1]])
			elif self.operation == '**' : operations.extend([store_pow, 3, destination, self.operands[0], self.operands[1]])
			elif self.operation == '<<' :
				operations.extend([assign, 2, destination, self.operands[0], val_lshift, 2, destination, self.operands[1]])
				total_commands += 1 # We generate two commands instead of one with this expression
			elif self.operation == '>>' :
				operations.extend([assign, 2, destination, self.operands[0], val_rshift, 2, destination, self.operands[1]])
				total_commands += 1 # We generate two commands instead of one with this expression
			elif self.operation == '&'  : operations.extend([store_and, 3, destination, self.operands[0], self.operands[1]])
			elif self.operation == '|'  : operations.extend([store_or, 2, destination, self.operands[0], self.operands[1]])
			else: raise MSException('expression %r contains illegal operation %s' % (self, self.operation))
			return total_commands, operations, tmp_used_loc
		except MSException as e:
			raise MSException('failed to generate dynamic code for expression %r' % self, *e.args)
		except Exception as e:
			raise MSException('failed to generate dynamic code for expression %r' % self, str(e))
	def newcopy(self):
		cls = self.__class__
		result = cls.__new__(cls)
		for k, v in list(self.__dict__.items()):
			if type(k) == VARIABLE and VARIABLE.is_expression == True:
				setattr(result, k, self.newcopy(v))
			else:
				setattr(result, k, copy(v))
		return result

# A specific sub-variant of VARIABLE, representing some entity's property. Used to gain access to entity properties at compile time using syntax like: itm.long_spear.weapon_length. And since it's an attribute as well, it can be freely used in the code and mathematical expressions.
class VAR_PROPERTY(VARIABLE):

	entity = None
	retrieval = None

	def __init__(self, module, entity, prop_name, *retrieval, **argd):
		self.module = module
		self.name = prop_name
		self.references = set()
		self.is_expression = True
		self.operands = []
		self.entity = entity
		self.retrieval = retrieval
		if not entity.is_static: raise MSException('property %r cannot be evaluated for non-static reference %s' % (prop_name, entity.formatted_name()))
		self.normalizer = argd.get('normalizer', None)
		self.is_static = True

	def formatted_name(self):
		return '%s.%s' % (self.entity.formatted_name(), self.name)

	def __repr__(self):
		return '<%s>' % self.formatted_name()

	def __val__(self):
		try: result = self.module[7][parse_int(self.entity)]
		except MSException as e: raise MSException('failed to calculate property %s' % repr(self), *e.args)
		except Exception as e: raise MSException('failed to calculate property %s' % repr(self), str(e))
		for key, convertor, default in self.retrieval:
			try:
				result = result[key]
				if convertor: result = convertor(result)
			except: result = default
		if self.normalizer: result = self.normalizer(result)
		return result

	def __int__(self): return int(self.__val__())
	def __float__(self): return float(self.__val__())

# VARIABLE sub-class for game items, providing direct compile-time access to item attributes.
class VAR_ITEM(VARIABLE):

	@property
	def flags(self):              return VAR_PROPERTY(WRECK.itm, self, 'flags',              (4, None, 0))
	@property
	def capabilities(self):       return VAR_PROPERTY(WRECK.itm, self, 'capabilities',       (5, None, 0))
	@property
	def price(self):              return VAR_PROPERTY(WRECK.itm, self, 'price',              (6, None, 0))
	@property
	def weight(self):             return VAR_PROPERTY(WRECK.itm, self, 'weight',             (7, unparse_item_aggregate, {}), ('weight', None, 0.0))
	@property
	def head_armor(self):         return VAR_PROPERTY(WRECK.itm, self, 'head_armor',         (7, unparse_item_aggregate, {}), ('head', None, 0))
	@property
	def body_armor(self):         return VAR_PROPERTY(WRECK.itm, self, 'body_armor',         (7, unparse_item_aggregate, {}), ('body', None, 0))
	@property
	def leg_armor(self):          return VAR_PROPERTY(WRECK.itm, self, 'leg_armor',          (7, unparse_item_aggregate, {}), ('leg', None, 0))
	@property
	def difficulty(self):         return VAR_PROPERTY(WRECK.itm, self, 'difficulty',         (7, unparse_item_aggregate, {}), ('diff', None, 0))
	@property
	def hp(self):                 return VAR_PROPERTY(WRECK.itm, self, 'hp',                 (7, unparse_item_aggregate, {}), ('hp', None, 0))
	@property
	def speed(self):              return VAR_PROPERTY(WRECK.itm, self, 'speed',              (7, unparse_item_aggregate, {}), ('speed', None, 0))
	@property
	def missile_speed(self):      return VAR_PROPERTY(WRECK.itm, self, 'missile_speed',      (7, unparse_item_aggregate, {}), ('msspd', None, 0))
	@property
	def size(self):               return VAR_PROPERTY(WRECK.itm, self, 'size',               (7, unparse_item_aggregate, {}), ('size', None, 0))
	@property
	def max_amount(self):         return VAR_PROPERTY(WRECK.itm, self, 'max_amount',         (7, unparse_item_aggregate, {}), ('qty', None, 0))
	@property
	def swing(self):              return VAR_PROPERTY(WRECK.itm, self, 'swing',              (7, unparse_item_aggregate, {}), ('swing', None, 0))
	@property
	def swing_damage(self):       return VAR_PROPERTY(WRECK.itm, self, 'swing_damage',       (7, unparse_item_aggregate, {}), ('swing', lambda x: x&ibf_armor_mask, 0))
	@property
	def swing_damage_type(self):  return VAR_PROPERTY(WRECK.itm, self, 'swing_damage_type',  (7, unparse_item_aggregate, {}), ('swing', lambda x: x>>iwf_damage_type_bits, 0))
	@property
	def thrust(self):             return VAR_PROPERTY(WRECK.itm, self, 'thrust',             (7, unparse_item_aggregate, {}), ('thrust', None, 0))
	@property
	def thrust_damage(self):      return VAR_PROPERTY(WRECK.itm, self, 'thrust_damage',      (7, unparse_item_aggregate, {}), ('thrust', lambda x: x&ibf_armor_mask, 0))
	@property
	def thrust_damage_type(self): return VAR_PROPERTY(WRECK.itm, self, 'thrust_damage_type', (7, unparse_item_aggregate, {}), ('thrust', lambda x: x>>iwf_damage_type_bits, 0))
	@property
	def abundance(self):          return VAR_PROPERTY(WRECK.itm, self, 'abundance',          (7, unparse_item_aggregate, {}), ('abundance', None, 0))
	@property
	def modifiers(self):          return VAR_PROPERTY(WRECK.itm, self, 'modifiers',          (8, None, 0))

	food_quality = head_armor
	accuracy = leg_armor
	horse_maneuver = speed
	horse_speed = shield_height = missile_speed
	weapon_length = horse_scale = size
	horse_charge = thrust_damage

# VARIABLE sub-class for game scenes , providing direct compile-time access to scene attributes.
class VAR_SCENE(VARIABLE):

	@property
	def flags(self): return VAR_PROPERTY(WRECK.scn, self, 'flags', (1, None, 0))
	@property
	def min_x(self): return VAR_PROPERTY(WRECK.scn, self, 'min_x', (4, None, 0), (0, int, 0))
	@property
	def min_y(self): return VAR_PROPERTY(WRECK.scn, self, 'min_y', (4, None, 0), (1, int, 0))
	@property
	def max_x(self): return VAR_PROPERTY(WRECK.scn, self, 'max_x', (5, None, 0), (0, int, 0))
	@property
	def max_y(self): return VAR_PROPERTY(WRECK.scn, self, 'max_y', (5, None, 0), (1, int, 0))
	@property
	def water_level(self): return VAR_PROPERTY(WRECK.scn, self, 'water_level', (6, lambda x: int(x+0.5), 0))
	@property
	def water_level_cm(self): return VAR_PROPERTY(WRECK.scn, self, 'water_level_cm', (6, lambda x: int(x*100+0.5), 0))
	@property
	def terrain_seed(self): return VAR_PROPERTY(WRECK.scn, self, 'terrain_seed', (7, unparse_terrain_aggregate, None), ('terrain_seed', None, 0))
	@property
	def river_seed(self): return VAR_PROPERTY(WRECK.scn, self, 'river_seed', (7, unparse_terrain_aggregate, None), ('river_seed', None, 0))
	@property
	def flora_seed(self): return VAR_PROPERTY(WRECK.scn, self, 'flora_seed', (7, unparse_terrain_aggregate, None), ('flora_seed', None, 0))
	@property
	def size_x(self): return VAR_PROPERTY(WRECK.scn, self, 'size_x', (7, unparse_terrain_aggregate, None), ('size_x', None, 0))
	@property
	def size_y(self): return VAR_PROPERTY(WRECK.scn, self, 'size_y', (7, unparse_terrain_aggregate, None), ('size_y', None, 0))
	@property
	def valley(self): return VAR_PROPERTY(WRECK.scn, self, 'valley', (7, unparse_terrain_aggregate, None), ('valley', None, 0))
	@property
	def hill_height(self): return VAR_PROPERTY(WRECK.scn, self, 'hill_height', (7, unparse_terrain_aggregate, None), ('hill_height', None, 0))
	@property
	def ruggedness(self): return VAR_PROPERTY(WRECK.scn, self, 'ruggedness', (7, unparse_terrain_aggregate, None), ('ruggedness', None, 0))
	@property
	def vegetation(self): return VAR_PROPERTY(WRECK.scn, self, 'vegetation', (7, unparse_terrain_aggregate, None), ('vegetation', None, 0))
	@property
	def terrain(self): return VAR_PROPERTY(WRECK.scn, self, 'terrain', (7, unparse_terrain_aggregate, None), ('terrain', None, 0))
	@property
	def polygon_size(self): return VAR_PROPERTY(WRECK.scn, self, 'polygon_size', (7, unparse_terrain_aggregate, None), ('polygon_size', None, 2))
	@property
	def disable_grass(self): return VAR_PROPERTY(WRECK.scn, self, 'disable_grass', (7, unparse_terrain_aggregate, None), ('disable_grass', None, 0))
	@property
	def shade_occlude(self): return VAR_PROPERTY(WRECK.scn, self, 'shade_occlude', (7, unparse_terrain_aggregate, None), ('shade_occlude', None, 0))
	@property
	def place_river(self): return VAR_PROPERTY(WRECK.scn, self, 'place_river', (7, unparse_terrain_aggregate, None), ('place_river', None, 0))
	@property
	def deep_water(self): return VAR_PROPERTY(WRECK.scn, self, 'deep_water', (7, unparse_terrain_aggregate, None), ('deep_water', None, 0))

# VARIABLE sub-class for game factions, providing direct compile-time access to faction attributes.
class VAR_FACTION(VARIABLE):

	@property
	def flags(self): return VAR_PROPERTY(WRECK.fac, self, 'flags', (2, None, 0))
	@property
	def coherence(self): return VAR_PROPERTY(WRECK.fac, self, 'coherence', (3, lambda x: int(x*100+0.5), 0))
	@property
	def default_color(self): return VAR_PROPERTY(WRECK.fac, self, 'default_color', (6, None, 0xAAAAAA))

class VAR_ITEM_MODIFIER(VARIABLE):

	@property
	def price_coeff(self): return VAR_PROPERTY(WRECK.imod, self, 'price_coeff', (2, lambda x: int(x*100+0.5), 0))
	@property
	def rarity_coeff(self): return VAR_PROPERTY(WRECK.imod, self, 'rarity_coeff', (3, lambda x: int(x*100+0.5), 0))

class VAR_PARTY(VARIABLE):

	@property
	def flags_field(self): return VAR_PROPERTY(WRECK.p, self, 'flags_field', (2, None, 0)) # Use this if you need icon+flags combined value
	@property
	def icon(self): return VAR_PROPERTY(WRECK.p, self, 'icon', (2, lambda x: x&0xff, 0))
	@property
	def flags(self): return VAR_PROPERTY(WRECK.p, self, 'flags', (2, lambda x: (x>>8)<<8, 0))
	@property
	def default_menu(self): return VAR_PROPERTY(WRECK.p, self, 'menu', (3, None, 0))
	@property
	def template(self): return VAR_PROPERTY(WRECK.p, self, 'template', (4, None, 0))
	@property
	def faction(self): return VAR_PROPERTY(WRECK.p, self, 'faction', (5, None, 0))
	@property
	def personality(self): return VAR_PROPERTY(WRECK.p, self, 'personality', (6, None, 0))
	@property
	def ai(self): return VAR_PROPERTY(WRECK.p, self, 'ai', (7, None, ai_bhvr_hold))
	@property
	def ai_target(self): return VAR_PROPERTY(WRECK.p, self, 'ai_target', (8, None, 0))
	@property
	def start_x(self): return VAR_PROPERTY(WRECK.p, self, 'start_x', (9, None, None), (0, lambda x: int(x+0.5), 0))
	@property
	def start_x_cm(self): return VAR_PROPERTY(WRECK.p, self, 'start_x_cm', (9, None, None), (0, lambda x: int(x*100+0.5), 0))
	@property
	def start_y(self): return VAR_PROPERTY(WRECK.p, self, 'start_y', (9, None, None), (0, lambda x: int(x+0.5), 0))
	@property
	def start_y_cm(self): return VAR_PROPERTY(WRECK.p, self, 'start_y_cm', (9, None, None), (0, lambda x: int(x*100+0.5), 0))
	@property
	def angle(self): return VAR_PROPERTY(WRECK.p, self, 'angle', (11, lambda x: int(x+0.5), 0))
	@property
	def angle_100(self): return VAR_PROPERTY(WRECK.p, self, 'angle_100', (11, lambda x: int(x*100+0.5), 0))

class VAR_PARTY_TEMPLATE(VARIABLE):

	@property
	def flags_field(self): return VAR_PROPERTY(WRECK.pt, self, 'flags_field', (2, None, 0)) # Use this if you need icon+flags combined value
	@property
	def icon(self): return VAR_PROPERTY(WRECK.pt, self, 'icon', (2, lambda x: x&0xff, 0))
	@property
	def flags(self): return VAR_PROPERTY(WRECK.pt, self, 'flags', (2, lambda x: (x>>8)<<8, 0))
	@property
	def default_menu(self): return VAR_PROPERTY(WRECK.pt, self, 'default_menu', (3, None, 0))
	@property
	def faction(self): return VAR_PROPERTY(WRECK.pt, self, 'faction', (4, None, 0))
	@property
	def personality(self): return VAR_PROPERTY(WRECK.pt, self, 'personality', (5, None, 0))

class VAR_TROOP(VARIABLE):

	@property
	def flags(self): return VAR_PROPERTY(WRECK.trp, self, 'flags', (3, None, 0))
	@property
	def scene(self): return VAR_PROPERTY(WRECK.trp, self, 'scene', (4, None, 0))
	@property
	def faction(self): return VAR_PROPERTY(WRECK.trp, self, 'faction', (6, None, 0))
	@property
	def level(self): return VAR_PROPERTY(WRECK.trp, self, 'level', (8, unparse_attr_aggregate, 0), ('level', None, 0))
	@property
	def strength(self): return VAR_PROPERTY(WRECK.trp, self, 'strength', (8, unparse_attr_aggregate, 0), ('str', None, 0))
	@property
	def agility(self): return VAR_PROPERTY(WRECK.trp, self, 'agility', (8, unparse_attr_aggregate, 0), ('agi', None, 0))
	@property
	def intelligence(self): return VAR_PROPERTY(WRECK.trp, self, 'intelligence', (8, unparse_attr_aggregate, 0), ('int', None, 0))
	@property
	def charisma(self): return VAR_PROPERTY(WRECK.trp, self, 'charisma', (8, unparse_attr_aggregate, 0), ('cha', None, 0))
	@property
	def wp_1h(self): return VAR_PROPERTY(WRECK.trp, self, 'wp_1h', (9, unparse_wp_aggregate, 0), (wpt_one_handed_weapon, None, 0))
	@property
	def wp_2h(self): return VAR_PROPERTY(WRECK.trp, self, 'wp_2h', (9, unparse_wp_aggregate, 0), (wpt_two_handed_weapon, None, 0))
	@property
	def wp_polearms(self): return VAR_PROPERTY(WRECK.trp, self, 'wp_polearms', (9, unparse_wp_aggregate, 0), (wpt_polearm, None, 0))
	@property
	def wp_archery(self): return VAR_PROPERTY(WRECK.trp, self, 'wp_archery', (9, unparse_wp_aggregate, 0), (wpt_archery, None, 0))
	@property
	def wp_crossbows(self): return VAR_PROPERTY(WRECK.trp, self, 'wp_crossbows', (9, unparse_wp_aggregate, 0), (wpt_crossbow, None, 0))
	@property
	def wp_thrown(self): return VAR_PROPERTY(WRECK.trp, self, 'wp_thrown', (9, unparse_wp_aggregate, 0), (wpt_throwing, None, 0))
	@property
	def wp_firearms(self): return VAR_PROPERTY(WRECK.trp, self, 'wp_firearms', (9, unparse_wp_aggregate, 0), (wpt_firearm, None, 0))
	@property
	def skills(self): return VAR_PROPERTY(WRECK.trp, self, 'skills', (10, None, 0))
	@property
	def facecode_1(self): return VAR_PROPERTY(WRECK.trp, self, 'facecode_1', (11, None, 0))
	@property
	def facecode_2(self): return VAR_PROPERTY(WRECK.trp, self, 'facecode_2', (12, None, 0))
	@property
	def upgrade_path_1(self): return VAR_PROPERTY(WRECK.trp, self, 'upgrade_path_1', (14, None, 0))
	@property
	def upgrade_path_2(self): return VAR_PROPERTY(WRECK.trp, self, 'upgrade_path_2', (15, None, 0))


# Root class for all Warband entities. This represents all basic entities like `scn`, `script`, `scn`, `itm` et cetera.
class UID(list):

	def __init__(self, basename, defaults = {}, opmask = 0, varclass = VARIABLE):
		# dict(vars), set(unassigned vars), var_category_name, dict(default_settings_for_new_vars), allow_declaring_new_vars, opmask_to_apply, variable_class, data_source
		super(UID, self).__init__([{}, set(), basename, defaults, True, opmask, varclass, []])

	def __getattr__(self, name):
		#name = name.lower()
		try:
			variable = self[0][name]
		except KeyError:
			if not self[4]: raise MSException('illegal reference {0}`{9}.{10}`{1}{8}'.format(*COLORAMA, self[2], name))
			self[0][name] = variable = self[6](module = self, name = name, **self[3])
			self[1].add(name)
		if WRECK.current_module: variable.references.add(WRECK.current_module)
		return variable

	#def __getattribute__(self, name):
	#	if name in ('count', 'index'): raise AttributeError() # Prevent standard methods from working on UID. These two names are thus allowed to be used as uid names.
	#	return super(UID, self).__getattribute__(name)

	def __setattr__(self, name, value):
		#name = name.lower()
		try:
			self[0][name].value = value
		except KeyError:
			if not self[4]: raise MSException('illegal reference {0}`{9}.{10}`{1}{8}'.format(*COLORAMA, self[2], name))
			self[0][name] = self[6](module = self, name = name, value = value, **self[3])
		try: self[1].remove(name)
		except KeyError: pass

	__call__ = __getattr__


# Compiler root static class, used to store all relevant information during compiler run.
class WRECK(object):

	initialized = False
	successful = True

	destination = './'
	current_module = None

	suppress_duplicate_warnings = ('nodupe' in sys.argv)

    # PERFORMANCE PROFILING
	time_started = None
	time_loaded = None
	time_plugins = None
	time_identifiers = None
	time_syntax = None
	time_compile = None
	time_export = None
	scripts_depth = [] # check for performance_heavy_loops

	# ENTITY REFERENCES
	if 'tag' in sys.argv:
		anim =    UID('anim',    opmask = tag_animation    << op_num_value_bits)
		fac =     UID('fac',     opmask = tag_faction      << op_num_value_bits, varclass = VAR_FACTION)
		itm =     UID('itm',     opmask = tag_item         << op_num_value_bits, varclass = VAR_ITEM)
		icon =    UID('icon',    opmask = tag_map_icon     << op_num_value_bits)
		mnu =     UID('mnu',     opmask = tag_menu         << op_num_value_bits)
		mesh =    UID('mesh',    opmask = tag_mesh         << op_num_value_bits)
		mt =      UID('mt',      opmask = tag_mission_tpl  << op_num_value_bits)
		track =   UID('track',   opmask = tag_track        << op_num_value_bits)
		psys =    UID('psys',    opmask = tag_particle_sys << op_num_value_bits)
		p =       UID('p',       opmask = tag_party        << op_num_value_bits, varclass = VAR_PARTY)
		pt =      UID('pt',      opmask = tag_party_tpl    << op_num_value_bits, varclass = VAR_PARTY_TEMPLATE)
		prsnt =   UID('prsnt',   opmask = tag_presentation << op_num_value_bits)
		qst =     UID('qst',     opmask = tag_quest        << op_num_value_bits)
		spr =     UID('spr',     opmask = tag_scene_prop   << op_num_value_bits)
		scn =     UID('scn',     opmask = tag_scene        << op_num_value_bits, varclass = VAR_SCENE)
		script =  UID('script',  opmask = tag_script       << op_num_value_bits)
		skl =     UID('skl',     opmask = tag_skill        << op_num_value_bits)
		snd =     UID('snd',     opmask = tag_sound        << op_num_value_bits)
		tableau = UID('tableau', opmask = tag_tableau      << op_num_value_bits)
		trp =     UID('trp',     opmask = tag_troop        << op_num_value_bits, varclass = VAR_TROOP)
	else:
		anim = UID('anim')
		fac = UID('fac', varclass = VAR_FACTION)
		itm = UID('itm', varclass = VAR_ITEM)
		icon = UID('icon')
		mnu = UID('mnu')
		mesh = UID('mesh')
		mt = UID('mt')
		track = UID('track')
		psys = UID('psys')
		p = UID('p', varclass = VAR_PARTY)
		pt = UID('pt', varclass = VAR_PARTY_TEMPLATE)
		prsnt = UID('prsnt')
		qst = UID('qst')
		spr = UID('spr')
		scn = UID('scn', varclass = VAR_SCENE)
		script = UID('script')
		skl = UID('skl')
		snd = UID('snd')
		tableau = UID('tableau')
		trp = UID('trp', varclass = VAR_TROOP)
	imod = UID('imod', varclass = VAR_ITEM_MODIFIER)
	imodbit = UID('imodbit')
	ip = UID('ip')
	pfx = UID('pfx')
	s = UID('s', opmask = tag_string << op_num_value_bits)
	l = UID('l', { 'static': False })
	g = UID('g', { 'static': False })
	registers = UID('reg', { 'static': False })
	qstrings = UID('qstr', { 'static': False })

	# COMPILED MODULE WRECK
	variables = None
	quick_strings = None

	animations = None
	dialogs = None
	dialog_states = None
	factions = None
	game_menus = None
	info_pages = None
	items = None
	map_icons = None
	meshes = None
	mission_templates = None
	tracks = None
	particle_systems = None
	parties = None
	party_templates = None
	postfx_params = None
	presentations = None
	quests = None
	scene_props = None
	scenes = None
	scripts = None
	simple_triggers = None
	skills = None
	skins = None
	sounds = None
	strings = None
	tableaus = None
	triggers = None
	troops = None

	item_modifiers = None

	variables_modified = False
	qstrings_modified = False

	generate_item_modifiers = True
	generate_ui_strings = True
	generate_user_hints = True

	# SUPPORT FOR TROOP UPGRADES
	upgrades = []

	# SUPPORT FOR QUICK STRINGS
	qstr_ktv = {}
	qstr_vtv = {}
	qstr_seq = []

	# SUPPORT FOR DIALOG STATES
	dialog_states_list = ['start','party_encounter','prisoner_liberated','enemy_defeated','party_relieved','event_triggered','close_window','trade','exchange_members', 'trade_prisoners','buy_mercenaries','view_char','training','member_chat','prisoner_chat']
	dialog_states_dict = dict(zip(dialog_states_list, range(len(dialog_states_list))))
	dialog_uids = {}
	dialog_states_usage = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

	# PLUGIN SUPPORT
	plugins = []
	requirements = {} # To track what plugins are required by other plugins, and fail compilation if requirements are not met
	injections = {}
	injected = set() # To track what injections were actually used, as any non-injected elements may potentially break the module

	# SYNTAX EXTENSION SUPPORT
	syntax_extensions = {}
	plugin_globals = {}

	# WARNINGS DURING COMPILATION
	errors = []
	warnings = []
	notices = []

	# MISSION DUPLICATE MESSAGE TRACKING
	mt_errors = []
	mt_warnings = []
	mt_notices = []

	# SUPPORT FOR GLOBAL VARIABLES
	globals_list = []
	deprecated = set()
	uninitialized = set()

	# SUPPORT FOR LOCAL VARIABLES DURING SCRIPT COMPILATION
	local_uses = {}
	local_tmp_uses = []
	local_tmp_reserved = []
	local_last_id = -1
	local_128_vars_warning_issued = False

	trigger_ID = 0 #numbering triggers in mission templates

	used_troop_slots = []
	used_agent_slots = []
	used_party_slots = []
	used_faction_slots = []

	skills_maximums = [] # Checking that troop skill is not exceeding maximum.

	@classmethod
	def start_script(cls):
		cls.local_uses = {}
		cls.local_tmp_uses = []
		local_tmp_reserved = []
		cls.local_last_id = -1
		cls.local_128_vars_warning_issued = False

	@classmethod
	def get_local_id(cls, script_name, name):
		try:
			return cls.local_uses[name]
		except KeyError:
			cls.local_last_id += 1
			cls.local_uses[name] = cls.local_last_id
			if (cls.local_last_id > 127) and not cls.local_128_vars_warning_issued:
				cls.warnings.append('Code object <%r> using more than 128 local variables.' % script_name)
				cls.local_128_vars_warning_issued = True
			return cls.local_last_id

	@classmethod
	def get_local_tmp_id(cls, script_name, index):
		try:
			if not cls.local_tmp_uses[index] in cls.local_tmp_reserved:
				return cls.local_tmp_uses[index]
			else:
				return False
		except IndexError:
			cls.local_last_id += 1
			cls.local_tmp_uses.append(cls.local_last_id)
			if (cls.local_last_id > 127) and not cls.local_128_vars_warning_issued:
				cls.warnings.append('Code object <%r> using more than 128 local variables.' % script_name)
				cls.local_128_vars_warning_issued = True
			return cls.local_last_id

EXPORT = WRECK # for backwards compatibility


def register_plugin(name = None, glob = None):
	name = path_split(extract_stack()[-2][0])[1][:-3]
	WRECK.plugins.append(name)
	WRECK.current_module = name
	if glob is None:
		frame_current = frame_previous = None
		try:
			frame_current = inspect_currentframe()
			frame_previous = dict(inspect_getmembers(frame_current))['f_back']
			glob = dict(inspect_getmembers(frame_previous))['f_globals']
		except:
			glob = globals()
		finally:
			del frame_previous
			del frame_current
	for opname, opdef in WRECK.syntax_extensions.items():
		glob[opname] = opdef
	for varname, varvalue in WRECK.plugin_globals.items():
		glob[varname] = varvalue

def require_plugin(*plugins):
	for plugin in plugins:
		WRECK.requirements.setdefault(plugin, set()).add(WRECK.current_module)



class CUSTOM_OPERATION(object):
	module, name, callback = None, None, None
	def __init__(self, module, name, callback): self.module, self.name, self.callback = module, name, callback
	def __call__(self, *argl):
		try:
			return self.callback(*argl) if self.callback else []
		except Exception as e:
			_argl = [str(arg) for arg in argl]
			raise MSException('illegal syntax for custom operation %s.%s(%s)\n%s' % (self.module, self.name, ", ".join(_argl), e.message), *e.args)
	def __or__(self, other):
		if other == neg: other = 'neg'
		elif other == this_or_next: other = 'this_or_next'
		elif other == this_or_next|neg: other = 'this_or_next|neg'
		else: other = str(other)
		raise MSException('`%s`.`%s` is a custom operation and cannot be used with `%s` modifier' % (self.module, self.name, other))
	__ror__ = __or__

def extend_syntax(callback):
	name = callback.__name__
	WRECK.syntax_extensions[name] = globals()[name] = CUSTOM_OPERATION(WRECK.current_module, name, callback)

#def register_syntax_extensions():
#	glob = globals()
#	for opname, opdef in WRECK.syntax_extensions.iteritems():
#		glob[opname] = opdef



# This method is called from plugins to export some of it's global variables for the rest of the module system without necessarily declaring them in module_constants
def export_plugin_globals(update_array = None, **plugin_globals):
	WRECK.plugin_globals.update(plugin_globals)
	if update_array is not None: update_array.update(plugin_globals)

# This method re-imports previously exported plugin globals to current global namespace.
# It is called from register_plugin() function to make currently existing globals available to newly loaded plugin.
# It is also called from compile.py code after importing all plugins to make globals available for the rest of module system.
#def import_plugin_globals():
#	#globals().update(WRECK.plugin_globals)
#	glob = globals()
#	for varname, varvalue in WRECK.plugin_globals.iteritems():
#		glob[varname] = varvalue
#	pass



def undefined_identifiers():
	undefined = []
	for uidlist in REQUIRED_UIDS.values():
		for varname in uidlist[1]:
			undefined.append((uidlist[0][varname].formatted_name(), uidlist[0][varname].references))
	return undefined

def external_string(value):
	return value.replace(' ', '_').replace('\t', '_')

def external_identifier(name, lowercase = True):
	name = name.replace(" ","_").replace("'","_").replace("`","_").replace("(","_").replace(")","_").replace("-","_").replace(",","").replace("|","").replace("\t","_")
	return name.lower() if lowercase else name

def internal_identifier(name):
	name = external_identifier(name).replace('=','_')
	#if name[0] not in 'abcdefghijklmnopqrstuvwxyz_': name = ''.join(['_', name])
	return name

def compiled_identifier(name, module, lowercase = True):
	if 'cap' in sys.argv: lowercase = False
	if lowercase:
		formated_name = name.lower()
		if name != formated_name:
			if module != 'scene_prop':
				WRECK.notices.append('Capital characters in {0}{9}{6} identifier {0}{10}{6}.'.format(*COLORAMA, module, name))
			else:
				WRECK.notices.append('Capital characters in {0}{9}{6} identifier {0}{10}{6}. Use Swyter\'s SceneObj tools to rename scene prop in ".sco" files.'.format(*COLORAMA, module, name))
		name = name.lower()
	formated_name = name.replace(' ', '_')
	if name != formated_name:
		WRECK.notices.append('White spaces in {0}{9}{6} identifier {0}{10}{6}.'.format(*COLORAMA, module, name))
	name = name.replace(' ', '_')
	return name

def calculate_identifiers(source, uid, mask_uid = None, *argl):
	index = -1
	try:
		opmask = uid[5]
		for index in range(len(source)):
			name = internal_identifier(source[index][0])
			if (name in uid[0]) and (name not in uid[1]):
				if not WRECK.suppress_duplicate_warnings:
					WRECK.warnings.append('Duplicate entity found: {0}{9}{3}.'.format(*COLORAMA, uid[0][name].formatted_name()))
			else:
				setattr(uid, name, index | opmask)
				if mask_uid:
					setattr(mask_uid, name, 1 << index)
	except MSException as e:
		raise MSException('failed to parse identifier for %r element #%d' % (uid[2], index), *e.args)
	except Exception as e:
		raise MSException('failed to parse identifier for %r element #%d' % (uid[2], index), str(e))
	uid[4] = False
	if mask_uid: mask_uid[4] = False


def allocate_quick_strings():
	qstr = []
	try:
		try:
			strings_file = open('%s/quick_strings.txt' % WRECK.destination, encoding='utf-8')
			qstr = [line.strip().split(' ', 1) for line in strings_file.readlines() if line.strip()]
			strings_file.close()
		except UnicodeDecodeError:
			WRECK.errors.append("Error: wrong encoding of file {0}'{9}/quick_strings.txt'{1}{8}.".format(*COLORAMA, WRECK.destination))
			WRECK.notices.append("Hint: Delete file or save with Utf-8 encoding." % WRECK.destination)
		except IOError:
			pass
		index = 0
		for q in qstr:
			if len(q) > 1:
				WRECK.qstr_seq.append(q[0])
				WRECK.qstr_ktv[q[0]] = q[1]
				q_name = 'qs%d' % index
				setattr(qstrings, q_name, opmask_quick_string | index)
				WRECK.qstr_vtv[q[1]] = getattr(qstrings, q_name)
				index += 1
	except MSException as e:
		raise MSException('failed to allocate quick strings', *e.args)
	except Exception as e:
		raise MSException('failed to allocate quick strings', str(e))

def allocate_global_variables(enforce_sgc = True):
	max_global_index = 0
	globals_list = []
	if enforce_sgc:
		try:
			variables_file = open('%s/variables.txt' % WRECK.destination, encoding='utf-8')
			globals_list = [line.strip() for line in variables_file.readlines() if line.strip()]
			variables_file.close()
		except IOError:
			pass
		except Exception as e:
			raise MSException('general error reading %s/variables.txt file' % WRECK.destination, formatted_exception())
	try:
		for var_name in globals_list:
			decap_name = var_name.lower()
			if (decap_name != var_name) and not('cap' in sys.argv):
				WRECK.notices.append('Gloval variable {0}{9}{6} has capital characters.'.format(*COLORAMA, var_name))
			var_name = decap_name
			#print('Variable %r has default index %d' % (var_name, max_global_index))
			WRECK.g.__setattr__(var_name, opmask_variable|max_global_index)
			WRECK.uninitialized.add(var_name)
			max_global_index += 1
	except Exception as e:
		args = e.args if isinstance(e, MSException) else []
		raise MSException('failed to allocate global variable `%s`' % var_name, *args)
	# FIX: THIS IS TOO EARLY TO WRECK GLOBALS, SOME MAY STILL BE PARSED FROM TEXT! NEED TO MOVE CODE BELOW TO WRECK PHASE
	try:
		new_vars = list(WRECK.g[1])
	except Exception as e:
		raise MSException('failed to allocate global variable `%s`' % var_name)
	try:
		for var_name in new_vars:
			#print('New variable %r given index %d' % (var_name, max_global_index))
			globals_list.append(var_name)
			WRECK.uninitialized.add(var_name)
			WRECK.g.__setattr__(var_name, opmask_variable|max_global_index)
			max_global_index += 1
	except Exception as e:
		args = e.args if isinstance(e, MSException) else []
		raise MSException('failed to allocate new global variable `%s`' % var_name, *args)
	WRECK.globals_list = globals_list
	#globals_list.append('')
	#WRECK.variables = '\r\n'.join(globals_list)


def preprocess_entities_internal(glob):
	for module, base, upg1, upg2 in WRECK.upgrades:
		if module is None: module = 'main_module'
		if not isinstance(base, VARIABLE): base = convert_string_id_to_variable(base, WRECK.trp)
		if not isinstance(upg1, VARIABLE): upg1 = convert_string_id_to_variable(upg1, WRECK.trp)
		if upg2 and not(isinstance(upg2, VARIABLE)): upg2 = convert_string_id_to_variable(upg2, WRECK.trp)
		if (base.value is None) or (upg1.value is None) or (upg2 != 0) and (upg2.value is None):
			if upg2: raise MSException('illegal upgrade in %s: %s not defined in upgrade(%s, %s, %s)', module, base.formatted_name(), base.formatted_name(), upg1.formatted_name(), upg2.formatted_name())
			else:    raise MSException('illegal upgrade in %s: %s not defined in upgrade(%s, %s)', module, base.formatted_name(), base.formatted_name(), upg1.formatted_name())
		try:
			troop_tuple = glob['troops'][parse_int(base)]
			if troop_tuple[14] != 0 or troop_tuple[15] != 0: WRECK.warnings.append('To many upgrades for {0}trp_{9}{3}'.format(*COLORAMA, base.name))
			troop_tuple[14] = upg1
			if upg2: troop_tuple[15] = upg2
		except Exception as e:
			raise MSException('upgrade operation failed', formatted_exception())

	#dialog_states compatibility with vanilla compiler
	for e in glob['dialogs']:
		if not('cap' in sys.argv):
			inp_state = e[1].lower()
			if e[1] != inp_state:
				WRECK.notices.append('Capital characters in dialog input state {0}{9}{6}.'.format(*COLORAMA, e[1]))
			oup_state = e[4].lower()
			if e[4] != oup_state:
				WRECK.notices.append('Capital characters in dialog output state {0}{9}{6}.'.format(*COLORAMA, e[4]))
			e[1] = inp_state
			e[4] = oup_state
		inp_state = e[1].replace(' ', '_')
		if e[1] != inp_state:
			WRECK.notices.append('White space in dialog input state {0}{9}{6}.'.format(*COLORAMA, e[1]))
		oup_state = e[4].replace(' ', '_')
		if e[4] != oup_state:
			WRECK.notices.append('White space in dialog output state {0}{9}{6}.'.format(*COLORAMA, e[4]))
		e[1] = e[1].replace(' ', '_')
		e[4] = e[4].replace(' ', '_')
		output_token = e[4]
		found = 0
		for i_t in range(len(WRECK.dialog_states_list)):
			if output_token == WRECK.dialog_states_list[i_t]:
				found = 1
				break
		if not found:
			WRECK.dialog_states_dict[output_token] = len(WRECK.dialog_states_list)
			WRECK.dialog_states_list.append(output_token)
			WRECK.dialog_states_usage.append(0)
	for e in glob['items']:
		if e[2] is None:
			e[2] = e[1]

#	#parties check
#	for e in glob['parties']:
#		party_id = e[0].lower()
#		if e[0] != party_id:
#			WRECK.notices.append('Capital characters in party_id %r.' % e[0])
#		party_id = e[0].replace(' ', '_')
#		if e[0] != party_id:
#			WRECK.notices.append('White space in party_id %r.' % e[0])
#		e[0] = e[0].lower().replace(' ', '_')

	# Creating maximums array for troops check.
	for e in glob['skills']:
		WRECK.skills_maximums.append((e[0],e[3]))

	#troops check
	for e in glob['troops']:
		troop_is_hero = 0
		duplicate_items = []
		weapon_items = []
		head_armors = []
		body_armors = []
		hand_armors = []
		leg_armors = []
		head_armors_civilian = []
		body_armors_civilian = []
		hand_armors_civilian = []
		leg_armors_civilian = []
		horses = []
		if (e[3] & tf_is_merchant) == tf_is_merchant: continue
		if (e[3] & tf_hero) and not(e[3] & tf_inactive): troop_is_hero = 1
		if not isinstance(e[8], AGGREGATE): e[8] = unparse_attr_aggregate(e[8])
		for item, modifier in e[7]:
			item_list = glob['items'][parse_int(item)]
			item_type = (item_list[4] & 0xFF)
			if troop_is_hero:
				if item in duplicate_items: WRECK.warnings.append("Duplicate weapon item {0}{9}{3} in the hero troop {0}{10}{3}".format(*COLORAMA, item.name, e[0]))
				if ((itp_type_one_handed_wpn <= item_type <= itp_type_polearm) or (itp_type_bow <= item_type <= itp_type_crossbow) or (itp_type_pistol <= item_type <= itp_type_musket)):
					duplicate_items.append(item)
					weapon_items.append(item)
				elif (itp_type_arrows <= item_type <= itp_type_bolts) or (item_type == itp_type_thrown) or (item_type == itp_type_bullets):
					weapon_items.append(item)
				elif item_type == itp_type_head_armor:
					if int(item.flags & itp_civilian): head_armors_civilian.append(item)
					else: head_armors.append(item)
				elif item_type == itp_type_body_armor:
					if int(item.flags & itp_civilian): body_armors_civilian.append(item)
					else: body_armors.append(item)
				elif item_type == itp_type_hand_armor:
					if int(item.flags & itp_civilian): hand_armors_civilian.append(item)
					else: hand_armors.append(item)
				elif item_type == itp_type_foot_armor:
					if int(item.flags & itp_civilian): leg_armors_civilian.append(item)
					else: leg_armors.append(item)
				elif item_type == itp_type_horse: horses.append(item)
			difficulty = item_list[7].get('diff', 0)
			if modifier == imod_stubborn: difficulty += 1
			elif modifier == imod_timid: difficulty -= 1
			elif modifier == imod_champion: difficulty += 2
			elif modifier == imod_masterwork: difficulty += 4
			elif modifier == imod_heavy: difficulty += 1
			elif modifier == imod_strong: difficulty += 2
			notice = ""
			if modifier == 0:
				str_modifier = ""
			else:
				str_modifier = " with modifier imod_" + glob['item_modifiers'][modifier][0]
			if item_type == itp_type_horse:
				riding = (e[10] >> (skl_riding << 2)) & 0xf
				if riding < difficulty:
					notice = "{0}trp.{9}{6} doesn't have riding skill to handle {0}itm.{10}{11}{6}. Required {0}{12}{6}.".format(*COLORAMA, e[0], item_list[0], str_modifier, difficulty)
			elif (item_type == itp_type_one_handed_wpn) or (item_type == itp_type_two_handed_wpn) or (item_type == itp_type_polearm):
				strength = e[8].get('str', 0)
				if strength < difficulty:
					notice = "{0}trp.{9}{6} doesn't have enough strength to handle {0}itm.{10}{11}{6}. Required {0}{12}{6}.".format(*COLORAMA, e[0], item_list[0], str_modifier, difficulty)
			elif item_type == itp_type_shield:
				shield = (e[10] >> (skl_shield <<2)) & 0xf
				if shield < difficulty:
					notice = "{0}trp.{9}{6} doesn't have shield skill to handle {0}itm.{10}{11}{6}. Required {0}{12}{6}.".format(*COLORAMA, e[0], item_list[0], str_modifier, difficulty)
			elif item_type == itp_type_bow:
				power_draw = (e[10] >> (skl_power_draw <<2)) & 0xf
				if power_draw < difficulty:
					notice = "{0}trp.{9}{6} doesn't have power draw skill to handle {0}itm.{10}{11}{6}. Required {0}{12}{6}.".format(*COLORAMA, e[0], item_list[0], str_modifier, difficulty)
			elif item_type == itp_type_thrown:
				power_throw = (e[10] >> (skl_power_throw <<2)) & 0xf
				if power_throw < difficulty:
					notice = "{0}trp.{9}{6} doesn't have power throw skill to handle {0}itm.{10}{11}{6}. Required {0}{12}{6}.".format(*COLORAMA, e[0], item_list[0], str_modifier, difficulty)
			elif (item_type == itp_type_head_armor) or (item_type == itp_type_body_armor) or (item_type == itp_type_foot_armor) or (item_type == itp_type_hand_armor):
				strength = e[8].get('str', 0)
				if strength < difficulty:
					notice = "{0}trp.{9}{6} doesn't have enough strength to handle {0}itm.{10}{11}{6}. Required {0}{12}{6}.".format(*COLORAMA, e[0], item_list[0], str_modifier, difficulty)
			elif (item_type == itp_type_musket) or (item_type == itp_type_pistol) or (item_type == itp_type_crossbow):
				strength = e[8].get('str', 0)
				if strength < difficulty:
					notice = "{0}trp.{9}{6} doesn't have enough strength to handle {0}itm.{10}{11}{6}. Required {0}{12}{6}.".format(*COLORAMA, e[0], item_list[0], str_modifier, difficulty)
			if notice != "":
				if not notice in WRECK.notices: WRECK.notices.append(notice)
		skill_mask = e[10]
		for i in range(42):
			skill = skill_mask & 0xF
			if skill > WRECK.skills_maximums[i][1]:
				notice = "{0}trp.{9}{6} skill {0}{10} {11}{6} is exceeding maximum {0}{12}{6} allowed by 'module_skills.py'.".format(*COLORAMA, e[0], WRECK.skills_maximums[i][0], skill, WRECK.skills_maximums[i][1])
				WRECK.notices.append(notice)
			skill_mask >>= 4
		if len(weapon_items) > 4: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} weapon items: {0}{11}{3}.".format(*COLORAMA, e[0], len(weapon_items), list(map(lambda n: n.name, weapon_items))))
		if len(head_armors) > 1: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} head armors: {0}{11}{3}.".format(*COLORAMA, e[0], len(head_armors), list(map(lambda n: n.name, head_armors))))
		if len(body_armors) > 1: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} body armors: {0}{11}{3}.".format(*COLORAMA, e[0], len(body_armors), list(map(lambda n: n.name, body_armors))))
		if len(hand_armors) > 1: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} hand armors: {0}{11}{3}.".format(*COLORAMA, e[0], len(hand_armors), list(map(lambda n: n.name, hand_armors))))
		if len(leg_armors) > 1: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} foot armors: {0}{11}{3}.".format(*COLORAMA, e[0], len(leg_armors), list(map(lambda n: n.name, leg_armors))))
		if len(head_armors_civilian) > 1: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} civilian head armors: {0}{11}{3}.".format(*COLORAMA, e[0], len(head_armors_civilian), list(map(lambda n: n.name, head_armors_civilian))))
		if len(body_armors_civilian) > 1: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} civilian body armors: {0}{11}{3}.".format(*COLORAMA, e[0], len(body_armors_civilian), list(map(lambda n: n.name, body_armors_civilian))))
		if len(hand_armors_civilian) > 1: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} civilian hand armors: {0}{11}{3}.".format(*COLORAMA, e[0], len(hand_armors_civilian), list(map(lambda n: n.name, hand_armors_civilian))))
		if len(leg_armors_civilian) > 1: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} civilian foot armors: {0}{11}{3}.".format(*COLORAMA, e[0], len(leg_armors_civilian), list(map(lambda n: n.name, leg_armors_civilian))))
		if len(horses) > 1: WRECK.warnings.append("The hero {0}{9}{3} has {0}{10}{3} horses: {0}{11}{3}.".format(*COLORAMA, e[0], len(horses), list(map(lambda n: n.name, horses))))
#	for e in glob['scripts']:
#		script_id = e[0].lower()
#		if e[0] != script_id:
#			WRECK.notices.append('Capital characters in script_id %r.' % e[0])
#		script_id = e[0].replace(' ', '_')
#		if e[0] != script_id:
#			WRECK.notices.append('White space in script_id %r.' % e[0])
#		e[0] = e[0].lower().replace(' ', '_')		

#def preprocess_entities(*argl):
#	pass

def aggregate_simple(entities):
	entities.insert(0, '%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)

def process_animations(e, index):
	result = [' %s %s %s  %d' % (compiled_identifier(e[0], 'animation'), e[1], e[2], len(e[3]))]
	if e[3]:
		for se in e[3]:
			#result.append('  %f %s %s %s %s %s %f %f %f %f ' % (se[0], se[1], se[2], se[3], se[4], se[5], se[6][0], se[6][1], se[6][2], se[7]))
			#sequence = '  %f %s %s %s %s %s %f %f %f  %f ' % (se[0], se[1], se[2], se[3], se[4], se[5], se[6][0], se[6][1], se[6][2], se[7])
			sequence = '  %f %s %s %s %s ' % (se[0], se[1], se[2], se[3], se[4])
			if len(se) > 5:
				sequence += '%s ' % se[5]
			else:
				sequence += '0 '
			if len(se) > 6 and se[6] != None:
				sequence += '%f %f %f  ' % (se[6][0], se[6][1], se[6][2])
			else:
				sequence += '0.0 0.0 0.0 '
			if len(se) > 7 and se[7] != None:
				sequence += '%f ' % se[7]
			else:
				sequence += '0.0 '
			result.append(sequence)
	return '\r\n'.join(result)

def process_info_pages(entity, index):
	return 'ip_%s %s %s' % (compiled_identifier(entity[0], 'info_page'), external_string(entity[1]), external_string(entity[2]))
def aggregate_info_pages(entities):
	entities.insert(0, 'infopagesfile version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)

def process_meshes(entity, index):
	entity[0] = compiled_identifier(entity[0], 'mesh')
	return 'mesh_%s %s %s %f %f %f %f %f %f %f %f %f' % tuple(entity)

def process_music(entity, index):
	return '%s %s %s' % (compiled_identifier(entity[1], 'music', False), entity[2], entity[2] | entity[3])

def process_postfx_params(e, index):
	return 'pfx_%s %s %s  %f %f %f %f  %f %f %f %f  %f %f %f %f' % (compiled_identifier(e[0], 'post_fx'), e[1], e[2], e[3][0], e[3][1], e[3][2], e[3][3], e[4][0], e[4][1], e[4][2], e[4][3], e[5][0], e[5][1], e[5][2], e[5][3])
def aggregate_postfx_params(entities):
	entities.insert(0, 'postfx_paramsfile version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)

def process_quests(e, index):
	return 'qst_%s %s %s %s ' % (compiled_identifier(e[0], 'quest'), external_string(e[1]), e[2], external_string(e[3]))
def aggregate_quests(entities):
	entities.insert(0, 'questsfile version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)

def process_skills(e, index):
	return 'skl_%s %s %s %s %s' % (compiled_identifier(e[0], 'skill'), external_string(e[1]), e[2], e[3], external_string(e[4]))

def process_strings(e, index):
	return 'str_%s %s' % (compiled_identifier(e[0], 'string'), external_string(e[1]))
def aggregate_strings(entities):
	entities.insert(0, 'stringsfile version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)

def process_ui_strings(e, index):
	return 'ui_%s|%s' % (compiled_identifier(e[0], 'ui_string'), e[1])
def aggregate_ui_strings(entities):
	entities.append('')
	return '\r\n'.join(entities)

def process_user_hints(e, index):
	return 'hint_%d|%s' % (index+1, e[0])

def process_factions(e, index):
	st = 'fac_%s %s %s %s ' % (compiled_identifier(e[0], 'faction'), external_string(e[1]), e[2], e[6])
	relations = {}
	for target, relation in e[4]:
		if type(target) == str: target = getattr(WRECK.fac, target)
		relations[parse_int(target)] = relation
	return [st, relations, e[3]]

def aggregate_factions(entities):
	relations = []
	faction_names = []
	for i in range(len(entities)):
		name = entities[i][0].split()[0]
		faction_names.append(name)
		r = [0.0 for j in range(len(entities))]
		relations.append(r)
	for index in range(len(entities)):
		for key, value in entities[index][1].items():
			key = parse_int(key)
			stored_val = relations[index][key]
			if (stored_val != value) and (stored_val != 0) and not('fac' in sys.argv):
				WRECK.notices.append('Faction relations conflict: {0}{9}{6} with {0}{10}{6} values {0}{11}{6} and {0}{12}{6}.'.format(*COLORAMA, faction_names[index], faction_names[key], stored_val, value))
			relations[index][key] = value
			relations[key][index] = value
	for index in range(len(entities)):
		rels = [0.0] * len(entities)
		for key in range(len(entities)):
			rels[key] = relations[index][key]
		rels[index] = entities[index][2]
		entities[index][1] = rels
	for index in range(len(entities)):
		entities[index] = '%s\r\n%s\r\n0 ' % (entities[index][0], ''.join([' %f ' % fr for fr in entities[index][1]]))
	entities.insert(0, 'factionsfile version 1\r\n%d\r\n' % len(entities))
	return ''.join(entities)

def process_parties(e, index):
	return ' 1 %d %d p_%s %s %d %d %d %d %d %d %d %d %d %f %f %f %f %f %f 0.0 %d %s\r\n%f' % (index, index, compiled_identifier(e[0], 'party'), external_string(e[1]), parse_int(e[2]), e[3], parse_int(e[4]), parse_int(e[5]), e[6], e[6], e[7], e[8], e[8], e[9][0], e[9][1], e[9][0], e[9][1], e[9][0], e[9][1], len(e[10]), ''.join(['%d %d 0 %d ' % (parse_int(ti[0]), ti[1], ti[2]) for ti in e[10]]), (3.1415926 / 180.0) * float(e[11]))
def aggregate_parties(entities):
	entities.insert(0, 'partiesfile version 1\r\n%d %d' % (len(entities), len(entities)))
	entities.append('')
	return '\r\n'.join(entities)

def process_party_templates(e, index):
	troops = ' '.join([(('%d %d %d %d' % tuple(parse_int(e[6][i]))) if i < len(e[6]) else '-1') for i in range(6)])
	return 'pt_%s %s %d %d %d %d %s ' % (compiled_identifier(e[0], 'party_template'), external_string(e[1]), parse_int(e[2]), e[3], parse_int(e[4]), e[5], troops)
def aggregate_party_templates(entities):
	entities.insert(0, 'partytemplatesfile version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)

def process_scenes(e, index):
	return 'scn_%s %s %s %s %s %f %f %f %f %f %s \r\n  %s %s\r\n  %s %s\r\n %s ' % (compiled_identifier(e[0], 'scene'), external_string(e[0]), e[1], e[2], e[3], e[4][0], e[4][1], e[5][0], e[5][1], e[6], e[7], len(e[8]), (' %d ' * len(e[8])) % tuple(parse_int(e[8])), len(e[9]), (' %d ' * len(e[9])) % tuple(parse_int(e[9])), e[10])
def aggregate_scenes(entities):
	entities.insert(0, 'scenesfile version 1\r\n %d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)

def process_particle_systems(e, index):
	sequence = 'psys_%s %s %s  %s %f %f %f %f %f \r\n%f %f   %f %f\r\n%f %f   %f %f\r\n%f %f   %f %f\r\n%f %f   %f %f\r\n%f %f   %f %f\r\n%f %f %f   %f %f %f   %f \r\n' % (compiled_identifier(e[0], 'particle_sys'), e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8], e[9][0], e[9][1], e[10][0], e[10][1], e[11][0], e[11][1], e[12][0], e[12][1], e[13][0], e[13][1], e[14][0], e[14][1], e[15][0], e[15][1], e[16][0], e[16][1], e[17][0], e[17][1], e[18][0], e[18][1], e[19][0], e[19][1], e[19][2], e[20][0], e[20][1], e[20][2], e[21])
	if e[22] != None:
		sequence += '%f ' % e[22]
	else:
		sequence += '0.0 '
	if e[23] != None:
		sequence += '%f ' % e[23]
	else:
		sequence += '0.0 '
	return sequence
def aggregate_particle_systems(entities):
	entities.insert(0, 'particle_systemsfile version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)

def process_troops(e, index):
	result = ['trp_%s %s %s %s %s %s %s %d %s %s' % (compiled_identifier(e[0], 'troop'), external_string(e[1]), external_string(e[2]), external_string(e[13]), e[3], e[4], e[5], parse_int(e[6]), parse_int(e[14]), parse_int(e[15]))]
	result.append('  ' + ''.join([('%d %d ' % ((parse_int(e[7][i][0]), e[7][i][1] << 24) if i < len(e[7]) else (-1, 0))) for i in range(64)]))
	if not isinstance(e[8], AGGREGATE): e[8] = unparse_attr_aggregate(e[8])
	if not isinstance(e[9], AGGREGATE): e[9] = unparse_wp_aggregate(e[9])
	result.append('  %d %d %d %d %d' % (e[8].get('str', 0), e[8].get('agi', 0), e[8].get('int', 0), e[8].get('cha', 0), e[8].get('level', 0)))
	result.append((' %d' * num_weapon_proficiencies) % tuple([e[9][index] for index in range(num_weapon_proficiencies)]))
	result.append(''.join(['%d ' % ((parse_int(e[10]) >> (32*i))&0xffffffff) for i in range(num_skill_words)]))
	face_words = []
	for face_key in (e[11], e[12]):
		word_keys = []
		for word_no in range(4):
			word_keys.append((face_key >> (64 * word_no)) & 0xFFFFFFFFFFFFFFFF)
		for word_no in range(4):
			face_words.append("%d "%(word_keys[3 - word_no]))
	result.append('  %s\r\n' % ''.join(face_words))
	return '\r\n'.join(result)
def aggregate_troops(entities):
	entities.insert(0, 'troopsfile version 2\r\n%d ' % len(entities))
	return '\r\n'.join(entities)
def process_sounds(entity, index):
	return entity
def aggregate_sounds(entities):
	sound_files = {} # filename -> index
	files = []
	sounds = []
	for sound in entities:
		refs = []
		for f in sound[2]:
			if (type(f) != type([])):
				f = [f, '0']
			try:
				refs.append('%s %s ' % (sound_files[f[0]], f[1]))
			except KeyError:
				sound_files[f[0]] = len(files)
				refs.append('%d %s ' % (len(files), f[1]))
				files.append(' %s %s' % (f[0], sound[1]))
		sounds.append('snd_%s %s %d %s' % (compiled_identifier(sound[0], 'sound'), sound[1], len(refs), ''.join(refs)))
	return 'soundsfile version 3\r\n%d\r\n%s\r\n%d\r\n%s\r\n' % (len(files), '\r\n'.join(files), len(sounds), '\r\n'.join(sounds))
def process_skins(e, index):
	skinkeys = [('skinkey_%s %s %s %f %f %s ' % (internal_identifier(sk[4]), sk[0], sk[1], sk[2], sk[3], external_string(sk[4]))) for sk in e[6]]
	hairs =  (' %s ' * len(e[7])) % tuple(e[7])
	beards = ('  %s\r\n' * len(e[8])) % tuple(e[8])
	hair_textures = '  '.join([str(len(e[9]))] + e[9])
	beard_textures = '  '.join([str(len(e[10]))] + e[10])
	face_textures = [' %d ' % len(e[11])]
	for face in e[11]:
		face_textures.append(' %s %s %d %d ' % (face[0], face[1], len(face[2]), len(face[3])))
		face_textures.append((' %s ' * len(face[2])) % tuple(face[2]))
		face_textures.append((' %s ' * len(face[3])) % tuple(face[3]))
	voices = '  '.join([str(len(e[12]))] + [('%d snd_%s' % (v[0], v[1].name)) for v in e[12]])
	constraints = []
	for c in e[17]:
		cvalues = ''.join([' %f %d' % (cvalue[0], cvalue[1]) for cvalue in c[2]])
		constraints.append('%f %d %s %s' % (c[0], c[1], len(c[2]), cvalues))
	if constraints != []:
		constraints = '\r\n'.join(constraints)
		constraints = '\r\n' + constraints
	else:
		constraints = ''
	return '%s %s\r\n %s %s %s\r\n %s %s %s\r\n%s\r\n%s\r\n %s\r\n%s\r\n %s \r\n %s \r\n%s\r\n %s \r\n %s %f \r\n%d %d\r\n%s\r\n%s' % (compiled_identifier(e[0], 'skin'), e[1], e[2], e[3], e[4], e[5], len(e[6]), ''.join(skinkeys), len(e[7]), hairs, len(e[8]), beards, hair_textures, beard_textures, ''.join(face_textures), voices, e[13], e[14], parse_int(e[15]), parse_int(e[16]), len(e[17]), constraints)
def aggregate_skins(entities):
	entities.insert(0, 'skins_file version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_scripts(entity, index):
	#return entity
	try: return '%s -1\r\n %s ' % (compiled_identifier(entity[0], 'script'), parse_module_code(entity[1], 'script.%s' % entity[0], True))
	except MSException as e: raise MSException('failed to compile script %s (#%d)' % (entity[0], index), *e.args)
def aggregate_scripts(entities):
	#return None
	entities.insert(0, 'scriptsfile version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_items(e, index):
	output = [' itm_%s %s %s %d  %s  %s %s %s %s ' % (compiled_identifier(e[0], 'item'), external_string(e[1]), external_string(e[2]), len(e[3]), '  '.join(['%s %s' % (imesh[0], imesh[1]) for imesh in e[3]]), e[4], e[5], e[6], e[8])]
	if not isinstance(e[7], AGGREGATE): e[7] = unparse_item_aggregate(e[7])
	if e[7].get('abundance', 0) == 0: e[7]['abundance'] = 100
	output.append('%f %s %s %s %s %s %s %s %s %s %s %s %s' % (e[7].get('weight', 0.0), e[7].get('abundance', 0), e[7].get('head', 0), e[7].get('body', 0), e[7].get('leg', 0), e[7].get('diff', 0), e[7].get('hp', 0), e[7].get('speed', 0), e[7].get('msspd', 0), e[7].get('size', 0), e[7].get('qty', 0), e[7].get('thrust', 0), e[7].get('swing', 0)))
	output.append('\r\n %d' % len(e[10]))
	if len(e[10]):
		#print("\n%s (#%d) factions: %s" % (e[0], index, ', '.join(['%d' % faction for faction in e[10]])),)
		output.append('\r\n')
		output.append(''.join([' %d' % parse_int(faction) for faction in e[10]]))
	output.append('\r\n%d\r\n' % len(e[9]))
	for trigger, code_block in e[9]:
		try: output.append('%f  %s \r\n' % (trigger, parse_module_code(code_block, 'itm.%s(#%d).%s' % (e[0], index, simple_trigger_to_string(trigger)))))
		except MSException as er: raise MSException('failed to compile trigger for item %s (#%d)' % (e[0], index), *er.args)
	return ''.join(output)
def aggregate_items(entities):
	entities.insert(0, 'itemsfile version 3\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_map_icons(e, index):
	if (e[5] != None) and (e[6] != None) and (e[7] != None):
		output = ['%s %s %s %f %d %f %f %f %d' % (e[0], e[1], e[2], e[3], parse_int(e[4]), e[5], e[6], e[7], len(e[8]))]
	else:
		output = ['%s %s %s %f %d 0 0 0 %d' % (e[0], e[1], e[2], e[3], parse_int(e[4]), len(e[8]))]
	for trigger, code_block in e[8]:
		try: output.append('%f  %s ' % (trigger, parse_module_code(code_block, 'icon.%s(#%d).%s' % (compiled_identifier(e[0], 'map_icon'), index, simple_trigger_to_string(trigger)))))
		except MSException as er: raise MSException('failed to compile trigger for map icon %s (#%d)' % (e[0], index), *er.args)
	output.append('\r\n')
	return '\r\n'.join(output)
def aggregate_map_icons(entities):
	entities.insert(0, 'map_icons_file version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_scene_props(e, index):
	output = ['spr_%s %s %s %s %s %d' % (compiled_identifier(e[0], 'scene_prop'), e[1], get_spr_hit_points(e[1]), e[2], e[3], len(e[4]))]
	for trigger, code_block in e[4]:
		try: output.append('%f  %s ' % (trigger, parse_module_code(code_block, 'spr.%s(#%d).%s' % (e[0], index, simple_trigger_to_string(trigger)))))
		except MSException as er: raise MSException('failed to compile trigger for scene prop %s (#%d)' % (e[0], index), *er.args)
	output.append('\r\n')
	return '\r\n'.join(output)
def aggregate_scene_props(entities):
	entities.insert(0, 'scene_propsfile version 1\r\n %d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_simple_triggers(e, index):
	try: return '%f  %s ' % (e[0], parse_module_code(e[1], '%s(#%d)' % (simple_trigger_to_string(e[0]), index)))
	except MSException as er: raise MSException('failed to compile simple trigger #%d' % (index), *er.args)
def aggregate_simple_triggers(entities):
	entities.insert(0, 'simple_triggers_file version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_tableaus(e, index):
	try: return 'tab_%s %s %s %s %s %s %s %s %s %s ' % (compiled_identifier(e[0], 'tableu'), e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8], parse_module_code(e[9], 'tableau.%s(#%d)' % (e[0], index)))
	except MSException as er: raise MSException('failed to compile tableau %s (#%d)' % (e[0], index), *er.args)
def process_triggers(e, index):
	try: return '%f %f %f  %s  %s ' % (e[0], e[1], e[2], parse_module_code(e[3], '%s(#%d).condition' % (trigger_to_string(e[0], e[1], e[2]), index)), parse_module_code(e[4], '%s(#%d).consequence' % (trigger_to_string(e[0], e[1], e[2]), index)))
	except MSException as er: raise MSException('failed to compile trigger #d' % (index), *er.args)
def aggregate_triggers(entities):
	entities.insert(0, 'triggersfile version 1\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_presentations(e, index):
	output = ['prsnt_%s %s %s %d' % (compiled_identifier(e[0], 'presentation'), e[1], parse_int(e[2]), len(e[3]))]
	for trigger, code_block in e[3]:
		try: output.append('%f  %s ' % (trigger, parse_module_code(code_block, 'prsnt.%s(#%d).%s' % (e[0], index, simple_trigger_to_string(trigger)))))
		except MSException as er: raise MSException('failed to compile trigger for presentation %s (#%d)' % (e[0], index), *er.args)
	output.append('\r\n')
	return '\r\n'.join(output)
def aggregate_presentations(entities):
	entities.insert(0, 'presentationsfile version 1\r\n %d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_mission_templates(e, index):
	output = ['mst_%s %s %s  %s\r\n%s \r\n\r\n%d ' % (compiled_identifier(e[0], 'mission_template'), e[0], e[1], e[2], external_string(e[3]), len(e[4]))]
	for epd in e[4]:
		output.append('%s %s %s %s %s %d %s \r\n' % (epd[0], epd[1], epd[2], epd[3], epd[4], len(epd[5]), (' %s' * len(epd[5])) % tuple(parse_int(epd[5]))))
	output.append(str(len(e[5])))
	output = [''.join(output)]
	WRECK.trigger_ID = 0
	for t0, t1, t2, script1, script2 in e[5]:
		try: output.append('%f %f %f  %s  %s ' % (t0, t1, t2, parse_module_code(script1, 'mt.%s(#%d).%s(#%d).condition' % (e[0], index, trigger_to_string(t0, t1, t2), WRECK.trigger_ID)), parse_module_code(script2, 'mt.%s(#%d).%s(#%d).consequence' % (e[0], index, trigger_to_string(t0, t1, t2), WRECK.trigger_ID))))
		#except MSException as er: raise MSException('failed to compile trigger for mission template {0}{9} (#{10}){1}{8}'.format(*COLORAMA, e[0], index), *er.args)
		except MSException as er: raise MSException('failed to compile trigger for mission template', *er.args)
		WRECK.trigger_ID += 1
	output.append('\r\n')
	return '\r\n'.join(output)
def aggregate_mission_templates(entities):
	entities.insert(0, 'missionsfile version 1\r\n %d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_game_menus(e, index):
	try: output = ['menu_%s %s %s none %s %d\r\n' % (compiled_identifier(e[0], 'game_menu'), e[1], external_string(e[2]), parse_module_code(e[4], 'mnu.%s(#%d)'%(e[0],index)), len(e[5]))]
	#except MSException as er: raise MSException('failed to compile entry code for menu %s (#%d)' % (e[0], index), *er.args)
	except MSException as er: raise MSException('failed to compile entry code for menu', *er.args)
	for mno in e[5]:
		last_text = mno[4]
		if not last_text: last_text = '.'
		try: output.append(' mno_%s  %s  %s  %s  %s ' % (mno[0], parse_module_code(mno[1], 'mnu.%s(#%d).mno_%s.condition'%(e[0],index,mno[0])), external_string(mno[2]), parse_module_code(mno[3], 'mnu.%s(#%d).mno_%s.choice'%(e[0],index,mno[0])), external_string(last_text)))
		except MSException as er: raise MSException('failed to compile code for menu item {0}{9}{1}{8} in menu {0}{10} (#{11}){1}{8}'.format(*COLORAMA, mno[0], e[0], index), *er.args)
	return ''.join(output)
def aggregate_game_menus(entities):
	entities.insert(0, 'menusfile version 1\r\n %d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_dialogs(e, index):
	try:
		dialog_state = WRECK.dialog_states_dict[e[1]]
		WRECK.dialog_states_usage[dialog_state] = 1
	except KeyError:
		dialog_state = len(WRECK.dialog_states_list)
		WRECK.dialog_states_dict[e[1]] = dialog_state
		WRECK.dialog_states_list.append(e[1])
		WRECK.dialog_states_usage.append(1)
	try:
		target_state = WRECK.dialog_states_dict[e[4]]
	except KeyError:
		target_state = len(WRECK.dialog_states_list)
		WRECK.dialog_states_dict[e[4]] = target_state
		WRECK.dialog_states_list.append(e[4])
		WRECK.dialog_states_usage.append(0)
	dialog_uid = 'dlga_%s:%s' % (e[1], e[4])
	if (dialog_uid in WRECK.dialog_uids) and (WRECK.dialog_uids[dialog_uid] != e[3]):
		new_uid = dialog_uid
		iterator = 0
		while new_uid in WRECK.dialog_uids:
			iterator += 1
			new_uid = '%s.%d' % (dialog_uid, iterator)
		dialog_uid = new_uid
	WRECK.dialog_uids[dialog_uid] = e[3]
	try: return '%s %d %d  %s %s  %d  %s %s ' % (dialog_uid, parse_int(e[0]), dialog_state, parse_module_code(e[2], 'dialog.%s(#%d).condition'%(e[1],index)), external_string(e[3]), target_state, parse_module_code(e[5], 'dialog.%s(#%d).result'%(e[1],index)), e[6])
	except MSException as er: raise MSException('failed to compile code for dialog %s (#%d)' % (dialog_uid, index), *er.args)
def aggregate_dialogs(entities):
	for i in range(len(WRECK.dialog_states_list)):
		if WRECK.dialog_states_usage[i] == 0: raise MSException('Output token (dialog state) not found %r.' % (WRECK.dialog_states_list[i], ))
	entities.insert(0, 'dialogsfile version 2\r\n%d' % len(entities))
	entities.append('')
	return '\r\n'.join(entities)
def process_item_modifiers(e, index):
	return 'imod_%s %s %.06f %.06f' % (compiled_identifier(e[0], 'item_modifier'), external_string(e[1]), e[2], e[3])
def aggregate_item_modifiers(entities):
	entities.append('')
	return '\r\n'.join(entities)


def postprocess_entities():
	WRECK.dialog_states_list.append('')
	WRECK.dialog_states = '\r\n'.join(WRECK.dialog_states_list)
	output = [str(len(WRECK.qstr_seq))]
	for qkey in WRECK.qstr_seq:
		output.append('%s %s' % (qkey, WRECK.qstr_ktv[qkey]))
	output.append('')
	WRECK.quick_strings = '\r\n'.join(output)
	WRECK.globals_list.append('')
	WRECK.variables = '\r\n'.join(WRECK.globals_list)



if not WRECK.initialized:
	REPEATABLE = object()
	SCRIPT = object()

class inject(object):
	name = None
	def __init__(self, name):
		self.name = name

class troop_item(object): pass
class sound_file(object): pass

def OPTIONAL(check, fallback = None): return { 'check': check, 'default': fallback }

TRIGGER = (float, float, float, SCRIPT, SCRIPT)

parsers = {
	'animations':        { 'parser': (id, int, int, REPEATABLE, (float, id, int, int, int, OPTIONAL(int, 0), OPTIONAL((float, float, float), None), OPTIONAL(float, None))), 'processor': process_animations, 'aggregator': aggregate_simple },
	'dialogs':           { 'parser': (int, id, SCRIPT, str, id, SCRIPT, OPTIONAL(str, 'NO_VOICEOVER')), 'processor': process_dialogs, 'aggregator': aggregate_dialogs, 'uid': 1 },
	'factions':          { 'parser': (id, str, int, float, [(WRECK.fac, float)], [str], OPTIONAL(int, 0xAAAAAA)), 'processor': process_factions, 'aggregator': aggregate_factions },
	'game_menus':        { 'parser': (id, int, str, 'none', SCRIPT, [(id, SCRIPT, str, SCRIPT, OPTIONAL(str, ''))]), 'processor': process_game_menus, 'aggregator': aggregate_game_menus },
	'info_pages':        { 'parser': (id, str, str), 'processor': process_info_pages, 'aggregator': aggregate_info_pages },
	'items':             { 'parser': (id, str, OPTIONAL(str, None), [(id, int)], int, int, int, AGGREGATE, int, OPTIONAL([(float, SCRIPT)], []), OPTIONAL([int], [])), 'processor': process_items, 'aggregator': aggregate_items },
	'map_icons':         { 'parser': (id, int, id, float, int, OPTIONAL(float, None), OPTIONAL(float, None), OPTIONAL(float, None), OPTIONAL([(float, SCRIPT)], []) ), 'processor': process_map_icons, 'aggregator': aggregate_map_icons },
	'meshes':            { 'parser': (id, int, id, float, float, float, float, float, float, float, float, float), 'processor': process_meshes, 'aggregator': aggregate_simple },
	'mission_templates': { 'parser': (id, int, int, str, [(int, int, int, int, int, [int])], [TRIGGER]), 'processor': process_mission_templates, 'aggregator': aggregate_mission_templates },
	'tracks':            { 'parser': (id, open, int, int), 'processor': process_music, 'aggregator': aggregate_simple },
	'particle_systems':  { 'parser': (id, int, id, int, float, float, float, float, float, (float, float), (float, float), (float, float), (float, float), (float, float), (float, float), (float, float), (float, float), (float, float), (float, float), (float, float, float), (float, float, float), float, OPTIONAL(float, None), OPTIONAL(float, None)), 'processor': process_particle_systems, 'aggregator': aggregate_particle_systems },
	'parties':           { 'parser': (id, str, int, int, int, int, int, int, int, (float, float), [(int, int, int)], OPTIONAL(float, 0)), 'processor': process_parties, 'aggregator': aggregate_parties },
	'party_templates':   { 'parser': (id, str, int, int, int, int, [(int, int, int, OPTIONAL(int, 0))]), 'processor': process_party_templates, 'aggregator': aggregate_party_templates },
	'postfx_params':     { 'parser': (id, int, int, (float, float, float, float), (float, float, float, float), (float, float, float, float)), 'processor': process_postfx_params, 'aggregator': aggregate_postfx_params },
	'presentations':     { 'parser': (id, int, int, [(float, SCRIPT)]), 'processor': process_presentations, 'aggregator': aggregate_presentations },
	'quests':            { 'parser': (id, str, int, str), 'processor': process_quests, 'aggregator': aggregate_quests },
	'scene_props':       { 'parser': (id, int, id, id, [(float, SCRIPT)]), 'processor': process_scene_props, 'aggregator': aggregate_scene_props },
	'scenes':            { 'parser': (id, int, id, id, (float, float), (float, float), float, id, [WRECK.scn], [WRECK.trp], OPTIONAL(id, '0')), 'processor': process_scenes, 'aggregator': aggregate_scenes },
	'scripts':           { 'parser': (id, SCRIPT), 'processor': process_scripts, 'aggregator': aggregate_scripts },
	'simple_triggers':   { 'parser': (float, SCRIPT), 'processor': process_simple_triggers, 'aggregator': aggregate_simple_triggers, 'uid': None },
	'skills':            { 'parser': (id, str, int, int, str), 'processor': process_skills, 'aggregator': aggregate_simple },
	'skins':             { 'parser': (id, int, id, id, id, id, [(int, int, float, float, str)], [id], [id], [id], [id], [(id, int, [id], [int])], [(int, int)], id, float, int, int, OPTIONAL([(float, int, REPEATABLE, (float, int))], []) ), 'processor': process_skins, 'aggregator': aggregate_skins },
	'sounds':            { 'parser': (id, int, [sound_file]), 'processor': process_sounds, 'aggregator': aggregate_sounds },
	'strings':           { 'parser': (id, str), 'processor': process_strings, 'aggregator': aggregate_strings },
	'tableaus':          { 'parser': (id, int, id, int, int, int, int, int, int, SCRIPT), 'processor': process_tableaus, 'aggregator': aggregate_simple },
	'triggers':          { 'parser': TRIGGER, 'processor': process_triggers, 'aggregator': aggregate_triggers, 'uid': None },
	'troops':            { 'parser': (id, str, str, int, int, int, int, [troop_item], AGGREGATE, AGGREGATE, int, int, OPTIONAL(int, 0), OPTIONAL(str, '0'), OPTIONAL(int, 0), OPTIONAL(int, 0)), 'processor': process_troops, 'aggregator': aggregate_troops },
	'item_modifiers':    { 'parser': (id, str, float, float), 'processor': process_item_modifiers, 'aggregator': aggregate_item_modifiers },
	'ui_strings':        { 'parser': (id, str), 'processor': process_ui_strings, 'aggregator': aggregate_ui_strings, 'uid': None },
	'user_hints':        { 'parser': (str,), 'processor': process_user_hints, 'aggregator': aggregate_ui_strings, 'uid': None },
}


def convert_string_id_to_variable(st, default_src = None):
	st = st.lower()
	if st == '': return 0
	if st[0] == '$':
		new_var = WRECK.g.__getattr__(st[1:])
		if new_var.value is None:
			WRECK.g.__setattr__(new_var.name, opmask_variable | len(WRECK.globals_list))
			WRECK.globals_list.append(new_var.name)
		return new_var
	if st[0] == ':': return WRECK.l.__getattr__(st[1:])
	try:
		source, name = st.split('_', 1)
		if source == 'str': source = 's'
		globs = get_globals()
		if (source in globs) and isinstance(globs[source], UID): return globs[source].__getattr__(internal_identifier(name))
	except ValueError:
		pass
	# Let's assume our string is actually identifier name and attempt to divine it from there
	try:
		if default_src is not None: return default_src.__getattr__(st)
	except MSException as e:
		raise MSException('illegal string parameter %r: no matching variable or identifier' % st, *e.args)
	raise MSException('illegal string parameter %r: no matching variable or identifier' % st)

# Returns a VARIABLE, performs some operations if it's a quick string
def parse_string_operand(op, qstr_allowed = True):
	if not op: raise MSException('cannot convert an empty string to identifier or qstr')
	if op[0] == '@':
		if not qstr_allowed: raise MSException('"%s" is a quickstring, identifier expected' % op)
		qval = external_string(op[1:])
		try:
			return WRECK.qstr_vtv[qval]
		except KeyError:
			pass
		max_offset = len(qval)
		offset = 20
		qkey_etalone = qkey = 'qstr_%s' % external_identifier(qval[0:offset], False)
		iterator = 0
		while WRECK.qstr_ktv.get(qkey, None) not in (None, qval):
			if offset < max_offset:
				newchar = external_identifier(qval[offset], False)
				qkey_etalone = qkey = qkey + newchar
				offset += 1
			else:
				iterator += 1
				qkey = '%s%d' % (qkey_etalone, iterator)
		new_index = len(WRECK.qstr_seq)
		WRECK.qstr_seq.append(qkey)
		WRECK.qstr_ktv[qkey] = qval
		q_name = 'qs%d' % new_index
		setattr(qstrings, q_name, opmask_quick_string | new_index)
		WRECK.qstr_vtv[qval] = getattr(qstrings, q_name)
		#print('NEW QSTR', WRECK.qstr_vtv[qval], qkey, qval)
		return WRECK.qstr_vtv[qval]
	else:
		return convert_string_id_to_variable(op)

def opcode_to_string(opcode):
	result = []
	if opcode & this_or_next: result.append('this_or_next')
	if opcode & neg: result.append('neg')
	opcode = opcode & 0x3FFFFFFF
	for key, value in OPLIST.__dict__.items():
		if value == opcode:
			result.append(key)
			break
	return '|'.join(result)

def simple_trigger_to_string(trigger):
	for key, value in TRLIST.__dict__.items():
		if (key[0:3] == 'ti_') and (value == trigger): return key
	return 'simple_trigger(%.01f)' % trigger

def trigger_to_string(t0, t1, t2):
	for key, value in TRLIST.__dict__.items():
		if (key[0:3] == 'ti_') and (value == t0): return key
	return 'trigger(%.01f %.01f %.01f)' % (t0, t1, t2)

def parse_variable_from_int(value):
	tag = value >> op_num_value_bits
	if tag == 0: return value
	if tag == tag_register: return getattr(WRECK.registers, 'reg%d' % (value & 0xFF))
	raise MSException('value %d not convertible to variable' % value)

def handle_list_injections(entity):
	index = 0
	while index < len(entity):
		if isinstance(entity[index], inject):
			WRECK.injected.add(entity[index].name)
			injection = WRECK.injections.get(entity[index].name, [])
			entity = entity[0:index] + injection + entity[index+1:]
		else:
			index += 1
	return entity

def handle_syntax_extensions(code_block):
	if not WRECK.syntax_extensions: return code_block
	result = []
	for operation in code_block:
		try: opcode, params = operation[0], operation[1:]
		except: opcode, params = operation, []
		if callable(opcode):
			new_ops = opcode(*params)
			if new_ops is None:
				if isinstance(opcode, CUSTOM_OPERATION):
					raise MSException('syntax extension %s.%s(%r) failed to return a legitimate value' % (opcode.module, opcode.name, params))
				else:
					raise MSException('syntax extension <unknown_plugin>.%s(%r) failed to return a legitimate value' % (opcode.name, params))
			else:
				result.extend(opcode(*params))
		else:
			result.append(operation)
	return result

# Check for things:
#   certain script should be register-safe - WARNING ??? - might be easier with a separate check
def parse_module_code(code_block, script_name, check_can_fail = False):
	WRECK.start_script()
	code_block = handle_list_injections(code_block)
	code_block = handle_syntax_extensions(code_block)
	locals_def = set() # Contains all locals used in the code block
	locals_use = set() # Contains all used locals except instances where that local is being assigned a value (i.e. not as first operand in lhs operations)
	export = ['']
	total_commands = len(code_block)
	current_depth = 0
	maximum_performance_depth = 0
	current_performance_depth = 0
	checked_performance_depth = []
	can_fail = False
	tag = script_name.split('.')[0]
	if tag == 'mt':
		trigger = script_name.split('.', 2)[2].rsplit('(', 1)[0]
		block = script_name.rsplit('.', 1)[1]
		num = len(code_block)
	this_or_next_started = False
	for index in range(len(code_block)):
		operation = code_block[index]
		is_assign = False
		if type(operation) is int:
			command = [operation, 0]
		else:
			command = [operation[0], len(operation) - 1]
			command.extend(operation[1:])
		
		# swy: enhancement to track down mistyped 'neg' operations when the intention was to use 'neq';
		#      neg|<something> is a modifier that needs to accompany other instructions and not go alone
		#      NOTE: keep in mind that this doesn't catch mistypings like (neq|faction_slot_eq)
		if command[0] == 0x80000000: raise MSException('\'neg = 0x80000000\' used as operation instead of \'neq = neg|eq\' in %s at line %d' %(script_name, index + 1))
		# swy: detect technically valid opcodes with buggy or unwanted behavior caused by bitwise OR'ing with neq instead of neg, like (neq|faction_slot_eq),
		#      that we would not be able to detect otherwise. we just define neq with an extra dummy compile-time modifier,
		#      and we make sure there's only eq in there as the only valid operation when stripped of modifiers.
		if (command[0] & 0x20000000) and (command[0] & 0xFFFF) != 31: # eq = 31
			raise MSException('make sure you use \'neg = 0x80000000\' instead of \'neq = neg|eq\' in %s at line %d' %(script_name, index + 1))
		# swy: then, no matter what, get rid of the dummy marker bit, so that it doesn't appear in the .txt files and cause weird script interpreter bugs
		command[0] &= ~0x20000000

		# Monitor execution depth
		if command[0] in depth_operations:
			current_depth += 1
		elif command[0] == try_end:
			current_depth -= 1
		
		# Check for assignment and can_fail operations
		if command[0] in lhs_operations:
			if len(command) < 3:
				raise MSException('operation %s without an operand in %s on line %d' % (opcode_to_string(command[0]), script_name, index + 1))
			if type(command[2]) == str:
				try:
					command[2] = parse_string_operand(command[2], False)
				except MSException as e:
					raise MSException('operation %s cannot assign to operand %r in %s on line %d' % (opcode_to_string(command[0]), command[2], script_name, index + 1), *e.args)
			elif type(command[2]) is int:
				try:
					command[2] = parse_variable_from_int(command[2])
				except MSException as e:
					raise MSException('operation %s cannot assign to operand %r in %s on line %d' % (opcode_to_string(command[0]), command[2], script_name, index + 1), *e.args)
			if isinstance(command[2], VARIABLE):
				if command[2].is_expression:
					raise MSException('operation %s cannot assign to expression %r in %s on line %d' % (opcode_to_string(command[0]), command[2], script_name, index + 1))
				elif command[2].is_static:
					raise MSException('operation %s cannot assign to static identifier %r in %s on line %d' % (opcode_to_string(command[0]), command[2], script_name, index + 1))
			else:
				#raise MSException('operation %s cannot assign to operand %r in %s on line %d' % (opcode_to_string(command[0]), command[2], script_name, index + 1))
				pass # Because fucking MS actually contains fucking assignment of values to 0.
			is_assign = True
		# Make sure that all operands are legit, allocate local variable ids as necessary
		local_tmp_depth = 0
		try:
			for opindex in range(len(command)):
				if opindex < 2: continue
				operand = command[opindex]
				if type(operand) == tuple: command[opindex] = operand = operand[0] # BUGFIX for Taleworlds illegal ACHIEVEMENT_* values
				if type(operand) == str:
					try:
						command[opindex] = operand = parse_string_operand(operand)
					except MSException as e:
						#raise MSException('failed to parse operand {0}{9}{1}{8} for operation {0}{10}{1}{8} in {0}{11}{1}{8} on line {0}{12}{1}{8}'.format(*COLORAMA, operand, opcode_to_string(command[0]), script_name, index+1), *e.args)
						raise MSException('failed to parse operand {0}{9}{1}{8} for operation {0}{10}{1}{8} command {0}{11}{1}{8}'.format(*COLORAMA, operand, opcode_to_string(command[0]), command), *e.args)
				if isinstance(operand, VARIABLE):
					if operand.is_expression:
						if operand.is_static: continue
						#print(('ID of operand: ', id(operand)))
						#print(repr(operand), operand.__dict__)
						operand = command[opindex] = operand.newcopy() #Fix for mission_template triggers usage more than once
						#print(('ID of new_operand: ', id(operand)))
						#print(repr(operand), operand.__dict__)
						local_tmp_id = 0
						while not local_tmp_id:
							local_tmp_id = WRECK.get_local_tmp_id(script_name, local_tmp_depth)
							if not local_tmp_id:
								local_tmp_depth += 1
						if command[0] in depth_operations: #don't rewrite temp locals in loop conditions
							WRECK.local_tmp_reserved.append(local_tmp_id)
						tmp_local = opmask_local_variable | local_tmp_id
						extra_commands, operations, tmp_used_loc = operand(script_name, tmp_local, local_tmp_depth)
						#print(extra_commands)
						#print(operations)
						#print((' %d' * len(operations)) % tuple(operations))
						command[opindex] = operand = tmp_local
						export.append((' %d' * len(operations)) % tuple(operations))
						total_commands += extra_commands
						locals_use.update(tmp_used_loc)
						local_tmp_depth += 1
						#print('Operand %r for operation %s in %s on line %d depth %d' % (operand, opcode_to_string(command[0]), script_name, index+1, local_tmp_depth))
					elif operand.module == WRECK.l:
						if (operand.name not in locals_def) and (not(is_assign) or (opindex > 2)):
							error_message = 'Unassigned local variable {0}{9}{1}{8} used by operation {0}{10}{1}{8} in {0}{11}{1}{8} on line {0}{12}{1}{8}.'.format(*COLORAMA, operand.name, opcode_to_string(command[0]), script_name, index + 1)
							if tag == 'mt':
								if not (operand.name, trigger, block, num) in WRECK.mt_errors:
									WRECK.errors.append(error_message)
									WRECK.mt_errors.append((operand.name, trigger, block, num))
							else:
								WRECK.errors.append(error_message)
						if not(is_assign) or (command[0] == try_for_range) or (command[0] == try_for_range_backwards) or (opindex > 2) or (operand.name.find('unused') != -1): locals_use.add(operand.name) # If local was used in non-assigned position, remember it (used to track declared but never used locals)
						operand.value = opmask_local_variable | WRECK.get_local_id(script_name, operand.name)
		except MSException as e:
			#raise MSException('command {0}{9}{1}{8} compilation fails in {0}{10}{1}{8} on line {0}{11}{1}{8}'.format(*COLORAMA, command, script_name, index + 1), *e.args)
			raise MSException('compilation fails in {0}{9}{1}{8} on line {0}{10}{1}{8}'.format(*COLORAMA, script_name, index + 1), *e.args)
		# Identify can_fail scripts
		can_fail |= (current_depth < 1) and (((command[0] & 0x3FFFFFFF) in can_fail_operations) or ((command[0] == call_script) and isinstance(command[2], VARIABLE) and (command[2].module == WRECK.script) and (command[2].name[0:3] == 'cf_')))
		# If command was an assignment, mark the variable as initialized
		if is_assign:
			if type(command[2]) is int:
				pass
			elif isinstance(command[2], VARIABLE):
				if command[2].module == WRECK.g:
					try:
						WRECK.uninitialized.remove(command[2].name)
					except KeyError:
						pass
				elif command[2].module == WRECK.l:
					locals_def.add(command[2].name)
			else:
				raise MSException('illegal assignment target %r for operation %s in %s on line %d' % (operation, opcode_to_string(command[0]), script_name, index + 1))
		# Generate command compiled text
		try: export.append((' %d' * len(command)) % tuple(command))
		except Exception as e:
			print(repr(operation))
			print(repr(command))
			print(repr([v.__int__() if isinstance(v, VARIABLE) else v for v in command]))
			raise

		# Performance heavy loops check
		if command[0] in performance_heavy_loops:
			is_heavy = True
			if command[0] == try_for_prop_instances:
				is_heavy = False
				if command[1] == 1: is_heavy = True # all instances
				elif command[1] > 1:
					if command[3] == 0: is_heavy = True # all instances with flags
					elif isinstance(command[3], VAR_ITEM): is_heavy = True # items
			if is_heavy:
				current_performance_depth += 1
				checked_performance_depth.insert(0, current_depth)
				maximum_performance_depth = max(maximum_performance_depth, current_performance_depth)
		if len(checked_performance_depth) > 0:
			if (command[0] == try_end) and (checked_performance_depth[0] == (current_depth + 1)):
				current_performance_depth -= 1
				checked_performance_depth.pop(0)
		if command[0] & this_or_next:
			this_or_next_started = True
		elif this_or_next_started and command[0] & 0xFFFF in can_fail_operations:
			this_or_next_started = False
		elif this_or_next_started:
			this_or_next_started = False
			error_message = '<this_or_next> doesn\'t have closing condition: {0}{9}{1}{8} line {0}{10}{1}{8}.'.format(*COLORAMA, script_name, index - 1)
			if tag != 'mt':
				WRECK.errors.append(error_message)
			else:
				if not (this_or_next, trigger, block, index - 1) in WRECK.mt_errors:
					WRECK.errors.append(error_message)
					WRECK.mt_errors.append((this_or_next, trigger, block, index - 1))

		if command[0] == troop_set_slot and type(command[3]) is int:
			if type(command[2]) is VAR_TROOP:
				if command[2].name in troop_arrays: pass
			elif command[3] < opmask_register:
				if tag != 'script':
					if (command[3] not in WRECK.used_troop_slots): WRECK.used_troop_slots.append(command[3])
				else:
					cur_script = script_name.split('.')[1]
					if cur_script not in troop_slots_exclude:
						if (command[3] not in WRECK.used_troop_slots): WRECK.used_troop_slots.append(command[3])
		if command[0] == party_set_slot and type(command[3]) is int:
			if command[3] < opmask_register:
				if (command[3] not in WRECK.used_party_slots): WRECK.used_party_slots.append(command[3])
		if command[0] == agent_set_slot and type(command[3]) is int:
			if command[3] < opmask_register:
				if (command[3] not in WRECK.used_agent_slots): WRECK.used_agent_slots.append(command[3])
		if command[0] == faction_set_slot and type(command[3]) is int:
			if command[3] < opmask_register:
				if (command[3] not in WRECK.used_faction_slots): WRECK.used_faction_slots.append(command[3])

		if command[0] in length_array:
			check = length_array.get(command[0])
			cur_len = len(command) - 2
			notice_message = " in {0}{9}{6} index {0}{10}{6} operation {0}{11}{6}".format(*COLORAMA, script_name, index, command_to_string(command))
			if type(check) is int:
				if cur_len > check:
					notice_case = "Too many parameters"
					notice_combined = notice_case + notice_message
					if tag == 'mt':
						if not (command, trigger, block, num) in WRECK.mt_notices:
									WRECK.notices.append(notice_combined)
									WRECK.mt_notices.append((command, trigger, block, num))
					else:
						WRECK.notices.append(notice_combined)
				elif cur_len < check:
					notice_case = "Not enough parameters"
					notice_combined = notice_case + notice_message
					if tag == 'mt':
						if not (command, trigger, block, num) in WRECK.mt_notices:
									WRECK.notices.append(notice_combined)
									WRECK.mt_notices.append((command, trigger, block, num))
					else:
						WRECK.notices.append(notice_combined)
			else:
				if cur_len > check[1]:
					notice_case = "Too many parameters"
					notice_combined = notice_case + notice_message
					if tag == 'mt':
						if not (command, trigger, block, num) in WRECK.mt_notices:
									WRECK.notices.append(notice_combined)
									WRECK.mt_notices.append((command, trigger, block, num))
					else:
						WRECK.notices.append(notice_combined)
				elif cur_len < check[0]:
					notice_case = "Not enough parameters"
					notice_combined = notice_case + notice_message
					if tag == 'mt':
						if not (command, trigger, block, num) in WRECK.mt_notices:
									WRECK.notices.append(notice_combined)
									WRECK.mt_notices.append((command, trigger, block, num))
					else:
						WRECK.notices.append(notice_combined)
	if current_depth != 0:
		explanation = 'missing' if (current_depth > 0) else 'extra'
		error_message = 'try/end operations do not match in {0}{9}{1}{8}: {0}{10}{1}{8} try_end(s) {0}{11}{1}{8}.'.format(*COLORAMA, script_name, abs(current_depth), explanation)
		if tag == 'mt':
			if not (explanation, trigger, block, num) in WRECK.mt_errors:
				WRECK.errors.append(error_message)
				WRECK.mt_errors.append((explanation, trigger, block, num))
		else:
			WRECK.errors.append(error_message)
	if check_nested_loops and maximum_performance_depth > 1:
		warning_message = 'Nested performance heavy loops in {0}{9}{3}.'.format(*COLORAMA, script_name)
		if tag == 'mt':
			if not (maximum_performance_depth, trigger, block, num) in WRECK.mt_warnings:
				WRECK.warnings.append(warning_message)
				WRECK.mt_warnings.append((maximum_performance_depth, trigger, block, num))
		else:
			WRECK.warnings.append(warning_message)
	if check_can_fail and can_fail and (script_name[7:10] != 'cf_') and (script_name[7:12] != 'game_'):
		WRECK.warnings.append('{0}{9}{3} can fail but it\'s name does not start with "cf_"'.format(*COLORAMA, script_name))
	for unused_local in locals_def - locals_use:
		notice_message = 'Local {0}l.{9}{6} declared but never used in {0}{10}{6}'.format(*COLORAMA, unused_local, script_name)
		if tag == 'mt':
			if not (unused_local, trigger, block, num) in WRECK.mt_notices:
				WRECK.notices.append(notice_message)
				WRECK.mt_notices.append((unused_local, trigger, block, num))
		else:
			WRECK.notices.append(notice_message)
	##Adding triggers ID in mission templates
	if script_name.split('.')[0] == 'mt' and script_name.rsplit('.', 1)[1] == 'consequence':
		export.append(' 2147483678 2 -1 %d' % (WRECK.trigger_ID))
		total_commands += 1
	export[0] = '%d' % total_commands
	return ''.join(export)

def compressed_tuple(entity):
	if type(entity[0]) == str: return entity[0]
	else:
		output = []
		for sub in entity:
			if type(sub) == list:
				output.append('list[len=%d]' % len(sub))
			elif type(sub) == tuple:
				output.append('tuple(len=%d)' % len(sub))
			elif type(sub) == dict:
				output.append('dict(len=%d)' % len(sub))
			else:
				output.append(sub)
		return repr(tuple(output))

def command_to_string(command):
	output = [opcode_to_string(command[0]),]
	for i in range(2, len(command)):
		if type(command[i]) is str: output.append(command[i])
		elif type(command[i]) is int: output.append(command[i])
		elif type(command[i]) is float: output.append(str(command[i]))
		else: output.append(command[i].formatted_name())
		#output.append(repr(command[i])) # alternative
	return output

def check_syntax(entity, parser, uid = 0):
	# Handle injections
	if type(entity) == tuple: entity = list(entity) # To guarantee we can make insertions
	if type(entity) == list: entity = handle_list_injections(entity)
	# Process entity
	if type(parser) == tuple:
		if type(uid) == int:
			if not isinstance(entity, list): raise MSException('illegal top-level entity %r, tuple or list expected' % entity)
			try:
				possible_uid = entity[uid]
			except IndexError:
				raise MSException('failed to retrieve identifier at position #%d in %s' % (uid, compressed_tuple(entity)))
			if type(possible_uid) != str:
				raise MSException('%r is not a legal identifier at position #%d in %s' % (possible_uid, uid, compressed_tuple(entity)))
			uid = internal_identifier(possible_uid)
		index = 0
		repeating = None
		output = []
		try:
			for subparser in parser:
				if subparser == SCRIPT:
					if type(entity[index]) != list:
						raise MSException('expected script but found {0}{9}{1}{8} at position {0}{10}{1}{8} in {0}{11}{1}{8}'.format(*COLORAMA, entity[index], index, compressed_tuple(entity)))
					output.append(entity[index])
					index += 1
				elif subparser == AGGREGATE:
					if type(entity[index]) not in (int, AGGREGATE):
						raise MSException('expected aggregate value but found {0}{9}{1}{8} at position {0}{10}{1}{8} in {0}{11}{1}{8}'.format(*COLORAMA, entity[index], index, compressed_tuple(entity)))
					output.append(entity[index])
					index += 1
				elif subparser == REPEATABLE:
					repeating = []
					output.append(repeating)
				elif type(subparser) == dict:
					try:
						output.append(check_syntax(entity[index], subparser['check'], uid))
						index += 1
					except IndexError:
						output.append(deepcopy(subparser['default']))
					except MSException:
						output.append(deepcopy(subparser['default']))
				else:
					if repeating is None:
						output.append(check_syntax(entity[index], subparser, uid))
						index += 1
					else:
						try:
							while True:
								repeating.append(check_syntax(entity[index], subparser, uid))
								index += 1
						except IndexError:
							break
						except MSException as e:
							raise MSException('incorrect syntax at position #%d in %s' % (index, compressed_tuple(entity)), *e.args)
		except IndexError:
			print(formatted_exception())
			raise MSException('not enough elements in module `%s` entity `%s` (%d total): %s' % (WRECK.current_module, uid, len(entity), compressed_tuple(entity)))
		if index < len(entity):
			WRECK.errors.append('Too many elements in module {0}`{9}`{1}{8} entity {0}`{10}`{1}{8} ({0}{11}{1}{8} parsed out of total {0}{12}{1}{8}): {0}{13}{1}{8}.'.format(*COLORAMA, WRECK.current_module, uid, index, len(entity), compressed_tuple(entity)))
		return output
	if type(parser) == list:
		output = []
		for index in range(len(entity)):
			try:
				output.append(check_syntax(entity[index], parser[0], uid))
			except MSException as e:
				raise MSException('failed to parse element {0}#{9}{1}{8}'.format(*COLORAMA, index), *e.args)
		return output
	if parser == troop_item:
		if type(entity) == list:
			return check_syntax(entity, (int, int), uid)
		else:
			return [check_syntax(entity, int, uid), 0]
	elif parser == sound_file:
		if type(entity) == list:
			return check_syntax(entity, (open, WRECK.fac), uid)
		else:
			return [check_syntax(entity, open, uid), 0]
	elif parser == int:
		if type(entity) == str: entity = convert_string_id_to_variable(entity)
		if isinstance(entity, VARIABLE):
			if not entity.is_static: raise MSException('value of %r is undefined at compile time' % entity)
		elif type(entity) not in (int,):
			raise MSException('cannot convert value %r to integer' % (entity, ))
	elif isinstance(parser, UID):
		if type(entity) == str: entity = convert_string_id_to_variable(entity, parser)
		if isinstance(entity, VARIABLE):
			if not entity.is_static: raise MSException('value of %r is undefined at compile time' % entity)
		elif type(entity) not in (int, int):
			raise MSException('cannot convert value %r to integer' % (entity, ))
	elif parser == float:
		if type(entity) == str: entity = convert_string_id_to_variable(entity)
		if isinstance(entity, VARIABLE):
			if not entity.is_static: raise MSException('value of %r is undefined at compile time' % entity)
		elif type(entity) not in (int, int, float):
			raise MSException('cannot convert value %r to float' % (entity, ))
	elif parser == str:
		if entity == 0: entity = '0' # DIRTY HACK
		elif entity == '': entity = '_' # Fix for CTD
		elif type(entity) != str:
			raise MSException('value %r must be a string' % (entity, ))
	elif parser == id:
		# TODO: identifier validity check
		if type(entity) == list: raise MSException('element %r expected ID but found a list %r' % (uid, entity))
		elif (type(entity) != str) and (entity not in set([0])): raise MSException('value %r is not a valid identifier' % (entity, ))
	elif parser == open:
		if type(entity) != str: raise MSException('value %r is not a valid filename' % (entity, ))
		fmod_music_formats = ('wav', 'mp3', 'ogg', 'wma', 'flac', 'aif', 'aiff')
		if not entity.lower().endswith(fmod_music_formats): WRECK.warnings.append('File {0}{9}{3} has unsupported audio file extension.'.format(*COLORAMA, entity))
	elif type(parser) == str:
		if entity != parser: raise MSException('value %r must always be a string constant %r' % (entity, parser))
	else:
		raise MSException('unknown validator type %r' % (parser, ))
	return entity

anim = WRECK.anim
fac = WRECK.fac
ip = WRECK.ip
itm = WRECK.itm
icon = WRECK.icon
mnu = WRECK.mnu
mesh = WRECK.mesh
mt = WRECK.mt
track = WRECK.track
psys = WRECK.psys
p = WRECK.p
pt = WRECK.pt
pfx = WRECK.pfx
prsnt = WRECK.prsnt
qst = WRECK.qst
spr = WRECK.spr
scn = WRECK.scn
script = WRECK.script
skl = WRECK.skl
snd = WRECK.snd
tableau = WRECK.tableau
trp = WRECK.trp

s = WRECK.s

l = WRECK.l
g = WRECK.g
registers = WRECK.registers
qstrings = WRECK.qstrings
imod = WRECK.imod
imodbit = WRECK.imodbit

scn.none = 0
scn.exit = 100000

REQUIRED_UIDS = { 'anim': WRECK.anim, 'fac': WRECK.fac, 'ip': WRECK.ip, 'itm': WRECK.itm, 'icon': WRECK.icon, 'mnu': WRECK.mnu, 'mesh': WRECK.mesh, 'mt': WRECK.mt, 'track': WRECK.track, 'psys': WRECK.psys, 'p': WRECK.p, 'pt': WRECK.pt, 'pfx': WRECK.pfx, 'prsnt': WRECK.prsnt, 'qst': WRECK.qst, 'spr': WRECK.spr, 'scn': WRECK.scn, 'script': WRECK.script, 'skl': WRECK.skl, 'snd': WRECK.snd, 's': WRECK.s, 'tableau': WRECK.tableau, 'trp': WRECK.trp, 'imod': WRECK.imod, 'imodbit': WRECK.imodbit }
WRECK.initialized = True

try:
	from header_ground_types import *
	from header_item_modifiers import *
	from header_mission_types import *
	from header_terrain_types import *
	from header_operations import *
	from header_animations import *
	from header_dialogs import *
	from header_factions import *
	from header_game_menus import *
	from header_items import *
	from header_map_icons import *
	from header_meshes import *
	from header_mission_templates import *
	from header_music import *
	from header_particle_systems import *
	from header_parties import *
	from header_postfx import *
	from header_presentations import *
	from header_quests import *
	from header_scene_props import *
	from header_scenes import *
	from header_skills import *
	from header_skins import *
	from header_sounds import *
	from header_strings import *
	from header_tableau_materials import *
	from header_triggers import *
	from header_troops import *
	import header_operations as OPLIST
	# swy: defined_operations is used to add a check and detect opcodes unrecognized by the game,
	#      but at compile time, see the save_statement_block() function
	defined_operations = [obj for name, obj in OPLIST.__dict__.items() if isinstance(obj, int) and obj < 0xffff]
	import header_triggers as TRLIST
except:
	print(("\nError importing module header files:\n\n%s" % formatted_exception()))
	if 'wait' in sys.argv: input('Press Enter to finish>')
	exit()

if 'depth_operations' not in globals():
	depth_operations = [try_begin, try_for_range, try_for_range_backwards, try_for_parties, try_for_agents]
	try: depth_operations.extend([try_for_prop_instances, try_for_players])
	except: pass

if 'performance_heavy_loops' not in globals():
	performance_heavy_loops = [try_for_agents, try_for_parties, try_for_prop_instances]

try:
	from module_constants import *
except:
	print(("\nError in module_constants.py file:\n\n%s" % formatted_exception()))
	if 'wait' in sys.argv: input('Press Enter to finish>')
	exit()

# OVERRIDING SOME VALUES FROM MODULE SYSTEM HEADERS

def reg(index):
	return getattr(registers, 'reg%d' % index)
def pos(index):
	return getattr(registers, 'pos%d' % index)
for index in range(128):
	setattr(registers, 'reg%d' % index, opmask_register|index)
	setattr(registers, 'pos%d' % index, index)
	globals()['reg%d' % index] = reg(index)
	globals()['pos%d' % index] = pos(index)
	globals()['s%d'   % index] = index
pos_belfry_begin = pos64

def SKILLS(**argd):
	result = 0x000000000000000000000000000000000000000000
	for skill_name, value in argd.items():
		result |= (value & 0xF) << (WRECK.skl.__getattr__(skill_name) << 2)
	return result

def weight(x): return AGGREGATE([('weight', 0.01 * int(x * 100 + 0.5))]) # Allow weights > 63 kg and weight precision up to 0.01 kg (Warband however only displays up to 0.1 kg).
def head_armor(x): return AGGREGATE([('head', x)]) # Allow armor values > 255
def body_armor(x): return AGGREGATE([('body', x)]) # Allow armor values > 255
def leg_armor(x): return AGGREGATE([('leg', x)]) # Allow armor values > 255
def difficulty(x): return AGGREGATE([('diff', x)])
def hit_points(x): return AGGREGATE([('hp', x)]) # Prevent swing damage value overflow into hit points
def spd_rtng(x): return AGGREGATE([('speed', x)])
def shoot_speed(x): return AGGREGATE([('msspd', x)])
def horse_scale(x): return AGGREGATE([('size', x)])
def weapon_length(x): return AGGREGATE([('size', x)])
def shield_width(x): return AGGREGATE([('size', x)])
def shield_height(x): return AGGREGATE([('msspd', x)])
def max_ammo(x): return AGGREGATE([('qty', x)]) # Enable quantity > 255
def swing_damage(damage,damage_type): return AGGREGATE([('swing', (damage_type << iwf_damage_type_bits)|(damage & ibf_armor_mask))]) # Damage is still limited to 255
def thrust_damage(damage,damage_type): return AGGREGATE([('thrust', (damage_type << iwf_damage_type_bits)|(damage & ibf_armor_mask))]) # Damage is still limited to 255
def horse_speed(x): return AGGREGATE([('msspd', x)])
def horse_maneuver(x): return AGGREGATE([('speed', x)])
def horse_charge(x): return thrust_damage(x, blunt)
def food_quality(x): return AGGREGATE([('head', x)]) # DEPRECATED
def abundance(x): return AGGREGATE([('abundance', x)])
def accuracy(x): return AGGREGATE([('leg', x)])

def ATTR(_str, _agi, _int, _cha, _lvl = 0): return AGGREGATE([('str', _str), ('agi', _agi), ('int', _int), ('cha', _cha), ('level', _lvl)])
for index in range(31):
	if index < 3: continue
	for attr in ('str', 'agi', 'int', 'cha'):
		globals()['%s_%d' % (attr, index)] = AGGREGATE({attr:index})
def_attrib = str_5 | agi_5 | int_4 | cha_4
def level(value):
	return AGGREGATE({'level':value})


def define_troop_upgrade(*argl):
	if not argl: raise MSException('upgrade() called without parameters in %s' % WRECK.current_module)
	argl = list(argl)
	if type(argl[0]) == list: argl.pop(0) # Catch for old-style use
	if len(argl) < 2: raise MSException('not enough parameters for upgrade%r in %s' % (argl, WRECK.current_module))
	base = argl.pop(0)
	upg1 = argl.pop(0)
	try: upg2 = argl.pop(0) # Optional
	except: upg2 = 0
	WRECK.upgrades.append((WRECK.current_module, base, upg1, upg2))
upgrade2 = upgrade = define_troop_upgrade


def generate_skill_constants_for_backwards_compatibility(skills):
	constants = {}
	for index in range(len(skills)):
		sid = internal_identifier(skills[index][0])
		limit = min(15, int(skills[index][3])) + 1
		constants['skl_%s' % sid] = index
		for level in range(limit):
			if not level: continue
			constants['knows_%s_%d' % (sid, level)] = level << (index << 2)
	globals().update(constants)

def generate_imod_constants_for_backwards_compatibility(modifiers):
	constants = {}
	for index in range(len(modifiers)):
		sid = internal_identifier(modifiers[index][0])
		constants['imod_%s' % sid] = index
		constants['imodbit_%s' % sid] = (1 << index)
	globals().update(constants)

# Default item_modifiers array
DEFAULT_ITEM_MODIFIERS = [
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

# swy: dummy compile-time marker (that won't appear in the .txt files) to detect mistakes, and bad lines
#      that use (neq|<operation>), instead of the expected (neg|<operation>),
noteq_marker = 0x20000000 
neq = neg|eq|noteq_marker

if __name__ == '__main__':
	value = '0x00000003b9a94de8000903220000424380000c5000002e08'
	print(unparse_terrain_aggregate(value))

# Add scripts names without 'script_' that will be excluded from troop slots counting.
troop_slots_exclude = ['init_troop_flags']
# Add troops without 'trp_' to exclude from used slots searching.
troop_arrays = ['temp_troop']
# Tags for error messages.
tags = ['anim', 'fac', 'itm', 'icon', 'mnu', 'mesh', 'mt', 'track', 'psys', 'p', 'pt', 'prsnt', 'qst', 'spr', 'scn', 'script', 'skl', 'snd', 'tableau', 'trp', 'str']
# Length of operations check, operations counters included, i.e. +1 to length.
length_array = dict([
	(store_mul, 3), (store_div, 3), (val_mul, 2), (val_div, 2), (store_add, 3), (store_sub, 3), (val_sub, 2), (val_add, 2), (store_mod, 3), (val_mod, 2), (store_or, 3),
	(store_and, 3), (val_or, 2), (val_and, 2),
	(faction_set_slot, 3), (faction_get_slot, 3), (faction_slot_eq, 3), (faction_slot_ge, 3),
	(party_template_set_slot, 3), (party_template_get_slot, 3), (party_template_slot_eq, 3), (party_template_slot_ge, 3),
	(party_set_slot, 3), (party_get_slot, 3), (party_slot_eq, 3), (party_slot_ge, 3),
	(troop_set_slot, 3), (troop_get_slot, 3), (troop_slot_eq, 3), (troop_slot_ge, 3),
	(quest_set_slot, 3), (quest_get_slot, 3), (quest_slot_eq, 3), (quest_slot_ge, 3),
	(item_set_slot, 3), (item_get_slot, 3), (item_slot_eq, 3), (item_slot_ge, 3),
	(scene_set_slot, 3), (scene_get_slot, 3), (scene_slot_eq, 3), (scene_slot_ge, 3),
	(scene_prop_set_slot, 3), (scene_prop_get_slot, 3), (scene_prop_slot_eq, 3), (scene_prop_slot_ge, 3),
	(team_set_slot, 3), (team_get_slot, 3), (team_slot_eq, 3), (team_slot_ge, 3),
	(agent_set_slot, 3), (agent_get_slot, 3), (agent_slot_eq, 3), (agent_slot_ge, 3),
	(player_set_slot, 3), (player_get_slot, 3), (player_slot_eq, 3), (player_slot_ge, 3),
	(try_for_range, 3), (try_for_range_backwards, 3), (try_for_parties, 1), (try_for_agents, (1, 3)), (try_for_prop_instances, (1, 3)), (try_for_players, (1, 2)),
	(gt, 2), (ge, 2), (eq, 2), (is_between, 3), (assign, 2), (val_min, 2), (val_max, 2), (val_clamp, 3), (val_abs, 1), (val_lshift, 2), (val_rshift, 2),
	(store_sqrt, 2), (store_pow, 3), (store_sin, 2), (store_cos, 2), (store_tan, 2), (store_asin, 2), (store_acos, 2), (store_atan, 2), (store_atan2, 3),
	(store_random, 2), (store_random_in_range, 3), (shuffle_range, 2), (set_fixed_point_multiplier, 1), (convert_to_fixed_point, 1), (convert_from_fixed_point, 1),
	(store_script_param_1, 1), (store_script_param_2, 1), (store_script_param, 2), (set_result_string, 1), (store_trigger_param_1, 1), (store_trigger_param_2, 1),
	(store_trigger_param_3, 1), (store_trigger_param, 2), (get_trigger_object_position, 1), (set_trigger_result, 1),
	(key_is_down, 1), (key_clicked, 1), (game_key_is_down, 1), (game_key_clicked, 1), (omit_key_once, 1), (mouse_get_position, 1),
	(get_global_cloud_amount, 1), (set_global_cloud_amount, 1), (get_global_haze_amount, 1), (set_global_haze_amount, 1),
	(store_current_hours, 1), (store_time_of_day, 1), (store_current_day, 1), (rest_for_hours, (1, 3)), (rest_for_hours_interactive, (1, 3)),
	(get_operation_set_version, 1), (set_player_troop, 1), (show_object_details_overlay, 1), (allow_ironman, 1),
	(options_get_damage_to_player, 1), (options_set_damage_to_player, 1), (options_get_damage_to_friends, 1), (options_set_damage_to_friends, 1),
	(options_get_combat_ai, 1), (options_set_combat_ai, 1), (game_get_reduce_campaign_ai, 1), (options_get_campaign_ai, 1), (options_set_campaign_ai, 1),
	(options_get_combat_speed, 1), (options_set_combat_speed, 1), (options_get_battle_size, 1), (options_set_battle_size, 1), (get_average_game_difficulty, 1),
	(get_achievement_stat, 3), (set_achievement_stat, 3), (unlock_achievement, 1), (get_player_agent_kill_count , (1, 2)), (get_player_agent_own_troop_kill_count, (1, 2)),
	(set_relation, 3), (store_relation, 3), (faction_set_name, 2), (faction_set_color, 2), (faction_get_color, 2),
	(hero_can_join, (0, 1)), (hero_can_join_as_prisoner, (0, 1)), (troops_can_join, 1), (troops_can_join_as_prisoner, 1), (party_can_join_party, (2, 3)),
	(main_party_has_troop, 1), (party_is_in_town, 2), (party_is_in_any_town, 1), (party_is_active, 1),
	(set_party_creation_random_limits, 2), (set_spawn_radius, 1), (spawn_around_party, 2), (disable_party, 1), (enable_party, 1), (remove_party, 1),
	(party_get_current_terrain, 2), (party_relocate_near_party, 3), (party_get_position, 2), (party_set_position, 2), (set_camera_follow_party, 1),
	(party_attach_to_party, 2), (party_detach, 1), (party_collect_attachments_to_party, 2), (party_get_cur_town, 2), (party_get_attached_to, 2), (party_get_num_attached_parties, 2),
	(party_get_attached_party_with_rank, 3), (party_set_name, 2), (party_set_extra_text, 2), (party_get_icon, 2), (party_set_icon, 2), (party_set_banner_icon, 2),
	(party_set_extra_icon, 6), (party_add_particle_system, 2), (party_clear_particle_systems, 1), (context_menu_add_item, 2), (party_get_template_id, 2), (party_set_faction, 2),
	(store_faction_of_party, 2), (store_random_party_in_range, 3), (store01_random_parties_in_range, 2), (store_distance_to_party_from_party, 3),
	(store_num_parties_of_template, 2), (store_random_party_of_template, 2), (store_num_parties_created, 2), (store_num_parties_destroyed, 2), (store_num_parties_destroyed_by_player, 2),
	(party_get_morale, 2), (party_set_morale, 2), (troop_join, 1), (troop_join_as_prisoner, 1), (add_companion_party, 1), (party_add_members, 3), (party_add_prisoners, 3),
	(party_add_leader, (2, 3)), (party_force_add_members, 3), (party_force_add_prisoners, 3), (party_add_template, (2, 3)), (distribute_party_among_party_group, 2),
	(remove_member_from_party, (1, 2)), (remove_regular_prisoners, 1), (remove_troops_from_companions, 2), (remove_troops_from_prisoners, 2),
	(party_remove_members, 3), (party_remove_prisoners, 3), (party_clear, 1), (add_gold_to_party, 2), (party_get_num_companions, 2), (party_get_num_prisoners, 2),
	(party_count_members_of_type, 3), (party_count_companions_of_type, 3), (party_count_prisoners_of_type, 3), (party_get_free_companions_capacity, 2), (party_get_free_prisoners_capacity, 2),
	(party_get_num_companion_stacks, 2), (party_get_num_prisoner_stacks, 2), (party_stack_get_troop_id, 3), (party_stack_get_size, 3), (party_stack_get_num_wounded, 3),
	(party_stack_get_troop_dna, 3), (party_prisoner_stack_get_troop_id, 3), (party_prisoner_stack_get_size, 3), (party_prisoner_stack_get_troop_dna, 3),
	(store_num_free_stacks, 2), (store_num_free_prisoner_stacks, 2), (store_party_size, (1, 2)), (store_party_size_wo_prisoners, (1, 2)), (store_troop_kind_count, 2),
	(store_num_regular_prisoners, 1), (store_troop_count_companions, (2, 3)), (store_troop_count_prisoners, (2, 3)), (store_main_party_wounded, 1),
	(party_add_xp_to_stack, 3), (party_upgrade_with_xp, (2, 3)), (party_add_xp, 2), (party_get_skill_level, 3), (heal_party, 1), (party_wound_members, 3),
	(party_remove_members_wounded_first, 3), (party_quick_attach_to_current_battle, 2), (party_leave_cur_battle, 1), (party_set_next_battle_simulation_time, 2),
	(party_get_battle_opponent, 2), (inflict_casualties_to_party_group, 3), (party_end_battle, 1),
	(party_set_marshall, 2), (party_set_flags, 3), (party_set_aggressiveness, 2), (party_set_courage, 2), (party_get_ai_initiative, 2), (party_set_ai_initiative, 2),
	(party_set_ai_behavior, 2), (party_set_ai_object, 2), (party_set_ai_target_position, 2), (party_set_ai_patrol_radius, 2), (party_ignore_player, 2),
	(party_set_bandit_attraction, 2), (party_get_helpfulness, 2), (party_set_helpfulness, 2), (get_party_ai_behavior, 2), (get_party_ai_object, 2), (party_get_ai_target_position, 2),
	(get_party_ai_current_behavior, 2), (get_party_ai_current_object, 2), (party_set_ignore_with_player_party, 2), (party_get_ignore_with_player_party, 2),
	(troop_has_item_equipped, 2), (troop_is_mounted, 1), (troop_is_guarantee_ranged, 1), (troop_is_guarantee_horse, 1), (troop_is_hero, 1), (troop_is_wounded, 1), (player_has_item, 1),
	(troop_set_type, 2), (troop_get_type, 2), (troop_set_class, 2), (troop_get_class, 2), (class_set_name, 2), (add_xp_to_troop, (1, 2)), (add_xp_as_reward, 1), (troop_get_xp, 2),
	(store_attribute_level, 3), (troop_raise_attribute, 3), (store_skill_level, (2, 3)), (troop_raise_skill, 3), (store_proficiency_level, 3), (troop_raise_proficiency, 3),
	(troop_raise_proficiency_linear, 3), (troop_add_proficiency_points, 2), (store_troop_health, (2, 3)), (troop_set_health, (2, 3)), (troop_get_upgrade_troop, 3),
	(store_character_level, (1, 2)), (get_level_boundary, 2), (add_gold_as_xp, (1, 2)), (troop_set_auto_equip, 2), (troop_ensure_inventory_space, 2), (troop_sort_inventory, 1),
	(troop_add_item, (2, 3)), (troop_remove_item, 2), (troop_clear_inventory, 1), (troop_equip_items, 1), (troop_inventory_slot_set_item_amount, 3),
	(troop_inventory_slot_get_item_amount, 3), (troop_inventory_slot_get_item_max_amount, 3), (troop_add_items, 3), (troop_remove_items, 3), (troop_loot_troop, 3),
	(troop_get_inventory_capacity, 2), (troop_get_inventory_slot, 3), (troop_get_inventory_slot_modifier, 3), (troop_set_inventory_slot, 3), (troop_set_inventory_slot_modifier, 3),
	(store_item_kind_count, (2, 3)), (store_free_inventory_capacity, (1, 2)), (set_price_rate_for_item, 2), (set_price_rate_for_item_type, 2), (set_merchandise_modifier_quality, 1),
	(set_merchandise_max_value, 1), (reset_item_probabilities, 1), (set_item_probability_in_merchandise, 2), (troop_add_merchandise, 3), (troop_add_merchandise_with_faction, 4),
	(troop_set_name, 2), (troop_set_plural_name, 2), (troop_set_face_key_from_current_profile, 1), (troop_add_gold, 2), (troop_remove_gold, 2), (store_troop_gold, (1, 2)),
	(troop_set_faction, 2), (store_troop_faction, 2), (store_faction_of_troop, 2), (troop_set_age, 2), (store_troop_value, 2), (str_store_player_face_keys, 2), (player_set_face_keys, 2),
	(str_store_troop_face_keys, (2, 3)), (troop_set_face_keys, (2, 3)), (face_keys_get_hair, 2), (face_keys_set_hair, 2), (face_keys_get_beard, 2), (face_keys_set_beard, 2),
	(face_keys_get_face_texture, 2), (face_keys_set_face_texture, 2), (face_keys_get_hair_texture, 2), (face_keys_set_hair_texture, 2), (face_keys_get_hair_color, 2),
	(face_keys_set_hair_color, 2), (face_keys_get_age, 2), (face_keys_set_age, 2), (face_keys_get_skin_color, 2), (face_keys_set_skin_color, 2), (face_keys_get_morph_key, 3),
	(face_keys_set_morph_key, 3),
	(check_quest_active, 1), (check_quest_finished, 1), (check_quest_succeeded, 1), (check_quest_failed, 1), (check_quest_concluded, 1), (start_quest, (1, 2)), (conclude_quest, 1),
	(succeed_quest, 1), (fail_quest, 1), (complete_quest, 1), (cancel_quest, 1), (setup_quest_text, 1), (store_partner_quest, 1), (setup_quest_giver, 2), (store_random_quest_in_range, 3),
	(set_quest_progression, 2), (store_random_troop_to_raise, 3), (store_random_troop_to_capture, 3), (store_quest_number, 2), (store_quest_item, 2), (store_quest_troop, 2),
	(item_has_property, 2), (item_has_capability, 2), (item_has_modifier, 2), (item_has_faction, 2), (item_get_type, 2), (store_item_value, 2), (store_random_horse, 1),
	(store_random_equipment, 1), (store_random_armor, 1), (cur_item_add_mesh, (1, 4)), (cur_item_set_material, (2, 4)), (item_get_weight, 2), (item_get_value, 2),
	(item_get_difficulty, 2), (item_get_head_armor, 2), (item_get_body_armor, 2), (item_get_leg_armor, 2), (item_get_hit_points, 2), (item_get_weapon_length, 2), (item_get_speed_rating, 2),
	(item_get_missile_speed, 2), (item_get_max_ammo, 2), (item_get_accuracy, 2), (item_get_shield_height, 2), (item_get_horse_scale, 2), (item_get_horse_speed, 2),
	(item_get_horse_maneuver, 2), (item_get_food_quality, 2), (item_get_abundance, 2), (item_get_thrust_damage, 2), (item_get_thrust_damage_type, 2), (item_get_swing_damage, 2),
	(item_get_swing_damage_type, 2), (item_get_horse_charge_damage, 2),
	(play_sound_at_position, (2, 3)), (play_sound, (1, 2)), (play_track, (1, 2)), (play_cue_track, 1), (music_set_situation, 1), (music_set_culture, 1), (stop_all_sounds, (0, 1)),
	(store_last_sound_channel, 1), (stop_sound_channel, 1),
	(init_position, 1), (copy_position, 2), (position_copy_origin, 2), (position_copy_rotation, 2), (position_transform_position_to_parent, 3), (position_transform_position_to_local, 3),
	(position_get_x, 2), (position_get_y, 2), (position_get_z, 2), (position_set_x, 2), (position_set_y, 2), (position_set_z, 2), (position_move_x, (2, 3)), (position_move_y, (2, 3)),
	(position_move_z, (2, 3)), (position_set_z_to_ground_level, 1), (position_get_distance_to_terrain, 2), (position_get_distance_to_ground_level, 2), (position_get_rotation_around_x, 2),
	(position_get_rotation_around_y, 2), (position_get_rotation_around_z, 2), (position_rotate_x, 2), (position_rotate_y, 2), (position_rotate_z, (2, 3)),
	(position_rotate_x_floating, 2), (position_rotate_y_floating, 2), (position_rotate_z_floating, (2, 3)), (position_get_scale_x, 2), (position_get_scale_y, 2), (position_get_scale_z, 2),
	(position_set_scale_x, 2), (position_set_scale_y, 2), (position_set_scale_z, 2), (get_angle_between_positions, 3), (position_has_line_of_sight_to_position, 2),
	(get_distance_between_positions, 3), (get_distance_between_positions_in_meters, 3), (get_sq_distance_between_positions, 3), (get_sq_distance_between_positions_in_meters, 3),
	(position_is_behind_position, 2), (get_sq_distance_between_position_heights, 3), (position_normalize_origin, 2), (position_get_screen_projection, 2),
	(map_get_random_position_around_position, 3), (map_get_land_position_around_position, 3), (map_get_water_position_around_position, 3),
	(troop_set_note_available, 2), (add_troop_note_tableau_mesh, 2), (add_troop_note_from_dialog, 3), (add_troop_note_from_sreg, 4), (faction_set_note_available, 2),
	(add_faction_note_tableau_mesh, 2), (add_faction_note_from_dialog, 3), (add_faction_note_from_sreg, 4), (party_set_note_available, 2), (add_party_note_tableau_mesh, 2),
	(add_party_note_from_dialog, 3), (add_party_note_from_sreg, 4), (quest_set_note_available, 2), (add_quest_note_tableau_mesh, 2), (add_quest_note_from_dialog, 3),
	(add_quest_note_from_sreg, 4), (add_info_page_note_tableau_mesh, 2), (add_info_page_note_from_dialog, 3), (add_info_page_note_from_sreg, 4),
	(cur_item_set_tableau_material, 2), (cur_scene_prop_set_tableau_material, 2), (cur_map_icon_set_tableau_material, 2), (cur_agent_set_banner_tableau_material, 2),
	(cur_tableau_add_tableau_mesh, 3), (cur_tableau_render_as_alpha_mask, 0), (cur_tableau_set_background_color, 1), (cur_tableau_set_ambient_light, 3), (cur_tableau_set_camera_position, 1),
	(cur_tableau_set_camera_parameters, 5), (cur_tableau_add_point_light, 4), (cur_tableau_add_sun_light, 4), (cur_tableau_add_mesh, 4), (cur_tableau_add_mesh_with_vertex_color, 5),
	(cur_tableau_add_mesh_with_scale_and_vertex_color, 5), (cur_tableau_add_map_icon, 3), (cur_tableau_add_troop, 4), (cur_tableau_add_horse, 3), (cur_tableau_set_override_flags, 1),
	(cur_tableau_clear_override_items, 0), (cur_tableau_add_override_item, 1),
	(str_is_empty, 1), (str_clear, 1), (str_store_string, 2), (str_store_string_reg, 2), (str_store_troop_name, 2), (str_store_troop_name_plural, 2), (str_store_troop_name_by_count, 3),
	(str_store_item_name, 2), (str_store_item_name_plural, 2), (str_store_item_name_by_count, 2), (str_store_party_name, 2), (str_store_agent_name, 2), (str_store_faction_name, 2),
	(str_store_quest_name, 2), (str_store_info_page_name, 2), (str_store_date, 2), (str_store_troop_name_link, 2), (str_store_party_name_link, 2), (str_store_faction_name_link, 2),
	(str_store_quest_name_link, 2), (str_store_info_page_name_link, 2), (str_store_class_name, 2), (game_key_get_mapped_key_name, 2), (str_store_player_username, 2),
	(str_store_server_password, 1), (str_store_server_name, 1), (str_store_welcome_message, 1), (str_encode_url, 1),
	(display_debug_message, (1, 2)), (display_log_message, (1, 2)), (display_message, (1, 2)), (set_show_messages, 1), (tutorial_box, 2), (dialog_box, (1, 2)), (question_box, (1, 3)),
	(tutorial_message, (1, 3)), (tutorial_message_set_position, 2), (tutorial_message_set_size, 2), (tutorial_message_set_center_justify, 1), (tutorial_message_set_background, 1),
	(entering_town, 1), (encountered_party_is_attacker, 0), (conversation_screen_is_active, 0), (in_meta_mission, 0), (change_screen_return, 0), (change_screen_loot, 1),
	(change_screen_trade, (0, 1)), (change_screen_exchange_members, (0, 2)), (change_screen_trade_prisoners, 0), (change_screen_buy_mercenaries, 0), (change_screen_view_character, 0),
	(change_screen_training, 0), (change_screen_mission, 0), (change_screen_map_conversation, 1), (change_screen_exchange_with_party, 1), (change_screen_equip_other, (0, 1)),
	(change_screen_map, 0), (change_screen_notes, 2), (change_screen_quit, 0), (change_screen_give_members, (0, 1)), (change_screen_controls, 0), (change_screen_options, 0),
	(set_mercenary_source_party, 1), (start_map_conversation, (1, 2)), (set_background_mesh, 1), (set_game_menu_tableau_mesh, 3), (jump_to_menu, 1), (disable_menu_option, 0),
	(set_tooltip_text, 1), (set_party_battle_mode, 0), (finish_party_battle_mode, 0), (start_encounter, 1), (leave_encounter, 0), (encounter_attack, 0), (select_enemy, 1),
	(set_passage_menu, 1), (start_mission_conversation, 1), (set_conversation_speaker_troop, 1), (set_conversation_speaker_agent, 1), (store_conversation_agent, 1),
	(store_conversation_troop, 1), (store_partner_faction, 1), (store_encountered_party, 1), (store_encountered_party2, 1), (set_encountered_party, 1), (end_current_battle, 0),
	(store_repeat_object, 1), (talk_info_show, 1), (talk_info_set_relation_bar, 1), (talk_info_set_line, 2),
	(all_enemies_defeated, (0, 1)), (race_completed_by_player, 0), (num_active_teams_le, 1), (main_hero_fallen, 0), (scene_allows_mounted_units, 0), (is_zoom_disabled, 0),
	(mission_tpl_are_all_agents_spawned, 0), (add_troop_to_site, 3), (remove_troop_from_site, 2), (modify_visitors_at_site, 1), (reset_visitors, 0), (set_visitor, (2, 3)),
	(set_visitors, 3), (add_visitors_to_current_scene, (3, 5)), (mission_tpl_entry_set_override_flags, 3), (mission_tpl_entry_clear_override_items, 2),
	(mission_tpl_entry_add_override_item, 3), (set_mission_result, 1), (finish_mission, (0, 1)), (set_jump_mission, 1), (jump_to_scene, (1, 2)), (set_jump_entry, 1),
	(store_current_scene, 1), (close_order_menu, 0), (entry_point_get_position, 2), (entry_point_set_position, 2), (entry_point_is_auto_generated, 1), (scene_set_day_time, 1),
	(set_rain, 2), (set_fog_distance, (1, 2)), (set_skybox, 2), (set_startup_sun_light, 3), (set_startup_ambient_light, 3), (set_startup_ground_ambient_light, 3),
	(get_startup_sun_light, 1), (get_startup_ambient_light, 1), (get_startup_ground_ambient_light, 1), (get_battle_advantage, 1), (set_battle_advantage, 1),
	(get_scene_boundaries, 2), (mission_enable_talk, 0), (mission_disable_talk, 0), (mission_get_time_speed, 1), (mission_set_time_speed, 1), (mission_time_speed_move_to_value, 2),
	(mission_set_duel_mode, 1), (store_zoom_amount, 1), (set_zoom_amount, 1), (reset_mission_timer_a, 0), (reset_mission_timer_b, 0), (reset_mission_timer_c, 0),
	(store_mission_timer_a, 1), (store_mission_timer_b, 1), (store_mission_timer_c, 1), (store_mission_timer_a_msec, 1), (store_mission_timer_b_msec, 1), (store_mission_timer_c_msec, 1),
	(is_camera_in_first_person, 0), (set_camera_in_first_person, 1), (mission_cam_set_mode, (1, 3)), (mission_cam_set_screen_color, 1), (mission_cam_get_position, 1),
	(mission_cam_set_position, 1), (mission_cam_animate_to_position, 3), (mission_cam_get_aperture, 1), (mission_cam_set_aperture, 1), (mission_cam_animate_to_aperture, 3),
	(mission_cam_animate_to_position_and_aperture, 4), (mission_cam_set_target_agent, 2), (mission_cam_clear_target_agent, 0), (mission_cam_set_animation, 1),
	(mouse_get_world_projection, 2), (cast_ray, (3, 4)), (set_postfx, 1), (set_river_shader_to_mud, 0), (rebuild_shadow_map, 0),
	(set_shader_param_int, 2), (set_shader_param_float, 2), (set_shader_param_float4, 5), (set_shader_param_float4x4, 13),
	(prop_instance_is_valid, 1), (prop_instance_is_animating, 2), (prop_instance_intersects_with_prop_instance, 2), (scene_prop_has_agent_on_it, 2),
	(prop_instance_get_scene_prop_kind, 2), (scene_prop_get_num_instances, 2), (scene_prop_get_instance, 3), (scene_prop_enable_after_time, 2), (set_spawn_position, 1),
	(spawn_scene_prop, 1), (prop_instance_get_variation_id, 2), (prop_instance_get_variation_id_2, 2), (replace_prop_instance, 2), (replace_scene_props, 2), (scene_prop_fade_out, (2, 3)),
	(scene_prop_fade_in, 2), (prop_instance_set_material, 3), (scene_prop_get_visibility, 2), (scene_prop_set_visibility, 2), (scene_prop_get_hit_points, 2), 
	(scene_prop_get_max_hit_points, 2), (scene_prop_set_hit_points, 2), (scene_prop_set_cur_hit_points, 2), (prop_instance_receive_damage, 3), (prop_instance_refill_hit_points, 1),
	(scene_prop_get_team, 2), (scene_prop_set_team, 2), (scene_prop_set_prune_time, 2), (prop_instance_get_position, 2), (prop_instance_get_starting_position, 2),
	(prop_instance_set_position, (2, 3)), (prop_instance_animate_to_position, 3), (prop_instance_get_animation_target_position, 2), (prop_instance_stop_animating, 1),
	(prop_instance_get_scale, 2), (prop_instance_set_scale, 4), (prop_instance_enable_physics, 2), (prop_instance_initialize_rotation_angles, 1), (prop_instance_rotate_to_position, 4),
	(prop_instance_clear_attached_missiles, 1), (prop_instance_dynamics_set_properties, 2), (prop_instance_dynamics_set_velocity, 2), (prop_instance_dynamics_set_omega, 2),
	(prop_instance_dynamics_apply_impulse, 2), (prop_instance_deform_to_time, 2), (prop_instance_deform_in_range, 4), (prop_instance_deform_in_cycle_loop, 4),
	(prop_instance_get_current_deform_progress, 2), (prop_instance_get_current_deform_frame, 2), (prop_instance_play_sound, (2, 3)), (prop_instance_stop_sound, 1),
	(scene_item_get_num_instances, 2), (scene_item_get_instance, 3), (scene_spawned_item_get_num_instances, 2), (scene_spawned_item_get_instance, 3),
	(replace_scene_items_with_scene_props, 2), (spawn_item, (1, 3)), (spawn_item_without_refill, (1, 3)), (set_current_color, 3), (set_position_delta, 3), (add_point_light, (0, 2)),
	(add_point_light_to_entity, (0, 2)), (particle_system_add_new, (1, 2)), (particle_system_emit, (2, 3)), (particle_system_burst, (2, 3)), (particle_system_burst_no_sync, (2, 3)),
	(prop_instance_add_particle_system, 3), (prop_instance_stop_all_particle_systems, 1),
	(agent_is_in_special_mode, 1), (agent_is_routed, 1), (agent_is_alive, 1), (agent_is_wounded, 1), (agent_is_human, 1), (agent_is_ally, 1), (agent_is_non_player, 1),
	(agent_is_defender, 1), (agent_is_active, 1), (agent_has_item_equipped, 2), (agent_is_in_parried_animation, 1), (agent_is_alarmed, 1), (class_is_listening_order, 2),
	(teams_are_enemies, 2), (agent_is_in_line_of_sight, 2), (add_reinforcements_to_entry, 2), (spawn_agent, 1), (spawn_horse, (1, 2)), (remove_agent, 1), (agent_fade_out, 1),
	(agent_play_sound, 2), (agent_stop_sound, 1), (agent_set_visibility, 2), (get_player_agent_no, 1), (agent_get_kill_count, (2, 3)), (agent_get_position, 2),
	(agent_set_position, 2), (agent_get_horse, 2), (agent_get_rider, 2), (agent_get_party_id, 2), (agent_get_entry_no, 2), (agent_get_troop_id, 2), (agent_get_item_id, 2),
	(store_agent_hit_points, (2, 3)), (agent_set_hit_points, (2, 3)), (agent_set_max_hit_points, (2, 3)), (agent_deliver_damage_to_agent, (2, 4)),
	(agent_deliver_damage_to_agent_advanced, (4, 5)), (add_missile, (6, 7)), (agent_get_speed, 2), (agent_get_damage_modifier, 2), (agent_get_accuracy_modifier, 2),
	(agent_get_speed_modifier, 2), (agent_get_reload_speed_modifier, 2), (agent_get_use_speed_modifier, 2), (agent_set_no_death_knock_down_only, 2),
	(agent_set_horse_speed_factor, 2), (agent_set_speed_limit, 2), (agent_set_damage_modifier, 2), (agent_set_accuracy_modifier, 2), (agent_set_speed_modifier, 2),
	(agent_set_reload_speed_modifier, 2), (agent_set_use_speed_modifier, 2), (agent_set_ranged_damage_modifier, 2), (agent_get_time_elapsed_since_removed, 2),
	(str_store_agent_face_keys, 2), (agent_refill_wielded_shield_hit_points, 1), (agent_set_invulnerable_shield, 2), (agent_get_wielded_item, (2, 3)),
	(agent_get_ammo, (2, 3)), (agent_get_item_cur_ammo, 3), (agent_refill_ammo, 1), (agent_set_wielded_item, 2), (agent_equip_item, (2, 3)), (agent_unequip_item, (2, 3)),
	(agent_set_ammo, 3), (agent_get_item_slot, 3), (agent_get_ammo_for_slot, 3), (agent_set_no_dynamics, 2), (agent_get_animation, (2, 3)), (agent_set_animation, (2, 3)),
	(agent_set_stand_animation, 2), (agent_set_walk_forward_animation, 2), (agent_set_animation_progress, 2), (agent_ai_set_can_crouch, 2), (agent_get_crouch_mode, 2),
	(agent_set_crouch_mode, 2), (agent_get_attached_scene_prop, 2), (agent_set_attached_scene_prop, 2), (agent_set_attached_scene_prop_x, 2),
	(agent_set_attached_scene_prop_y, 2), (agent_set_attached_scene_prop_z, 2), (agent_get_bone_position, (3, 4)), (agent_ai_set_interact_with_player, 2),
	(agent_set_is_alarmed, 2), (agent_clear_relations_with_agents, 1), (agent_add_relation_with_agent, 3), (agent_get_number_of_enemies_following, 2),
	(agent_ai_get_num_cached_enemies, 2), (agent_ai_get_cached_enemy, 3), (agent_get_attack_action, 2), (agent_get_defend_action, 2), (agent_get_action_dir, 2),
	(agent_set_attack_action, (2, 3)), (agent_set_defend_action, (2, 3)), (agent_set_scripted_destination, (2, 4)), (agent_set_scripted_destination_no_attack, (2, 3)),
	(agent_get_scripted_destination, 2), (agent_force_rethink, 1), (agent_clear_scripted_mode, 1), (agent_ai_set_always_attack_in_melee, 2),
	(agent_get_simple_behavior, 2), (agent_ai_get_behavior_target, 2), (agent_get_combat_state, 2), (agent_ai_get_move_target, 2), (agent_get_look_position, 2),
	(agent_set_look_target_position, 2), (agent_ai_get_look_target, 2), (agent_set_look_target_agent, 2), (agent_start_running_away, (1, 2)), (agent_stop_running_away, 1),
	(agent_ai_set_aggressiveness, 2), (agent_set_kick_allowed, 2), (set_cheer_at_no_enemy, 1), (agent_add_offer_with_timeout, 3), (agent_check_offer_from_agent, 2),
	(agent_get_group, 2), (agent_set_group, 2), (agent_get_team, 2), (agent_set_team, 2), (agent_get_class, 2), (agent_get_division, 2), (agent_set_division, 2),
	(team_get_hold_fire_order, 3), (team_get_movement_order, 3), (team_get_riding_order, 3), (team_get_weapon_usage_order, 3), (team_give_order, 3), (team_set_order_position, 3),
	(team_get_leader, 2), (team_set_leader, 2), (team_get_order_position, 3), (team_set_order_listener, (2, 3)), (team_set_relation, 3), (store_remaining_team_no, 1),
	(team_get_gap_distance, 3), (store_normalized_team_count, 2), 
	(is_presentation_active, 1), (start_presentation, 1), (start_background_presentation, 1), (presentation_set_duration, 1), (create_text_overlay, (2, 3)), (create_mesh_overlay, 2),
	(create_mesh_overlay_with_item_id, 2), (create_mesh_overlay_with_tableau_material, (3, 4)), (create_button_overlay, (2, 3)), (create_game_button_overlay, 2),
	(create_in_game_button_overlay, 2), (create_image_button_overlay, 3), (create_image_button_overlay_with_tableau_material, 4), (create_slider_overlay, 3),
	(create_progress_overlay, 3), (create_number_box_overlay, 3), (create_text_box_overlay, 1), (create_simple_text_box_overlay, 1), (create_check_box_overlay, 3),
	(create_listbox_overlay, 3), (create_combo_label_overlay, 1), (create_combo_button_overlay, 1), (overlay_add_item, 2), (set_container_overlay, 1), (overlay_set_container_overlay, 2),
	(overlay_get_position, 2), (overlay_set_val, 2), (overlay_set_text, 2), (overlay_set_boundaries, 3), (overlay_set_position, 2), (overlay_set_size, 2), (overlay_set_area_size, 2),
	(overlay_set_additional_render_height, 2), (overlay_animate_to_position, 3), (overlay_animate_to_size, 3), (overlay_set_mesh_rotation, 2), (overlay_set_material, 2),
	(overlay_set_color, 2), (overlay_set_alpha, 2), (overlay_set_hilight_color, 2), (overlay_set_hilight_alpha, 2), (overlay_animate_to_color, 3), (overlay_animate_to_alpha, 3),
	(overlay_animate_to_highlight_color, 3), (overlay_animate_to_highlight_alpha, 3), (overlay_set_display, 2), (overlay_obtain_focus, 1), (overlay_set_tooltip, 2),
	(show_item_details, 3), (show_item_details_with_modifier, 4), (close_item_details, 0), (show_troop_details, 3),
	(player_is_active, 1), (multiplayer_is_server, 0), (multiplayer_is_dedicated_server, 0), (game_in_multiplayer_mode, 0), (player_is_admin, 1), (player_is_busy_with_menus, 1),
	(player_item_slot_is_picked_up, 2), (send_message_to_url, 2), (multiplayer_send_message_to_server, 1), (multiplayer_send_int_to_server, 2), (multiplayer_send_2_int_to_server, 3),
	(multiplayer_send_3_int_to_server, 4), (multiplayer_send_4_int_to_server, 5), (multiplayer_send_string_to_server, 2), (multiplayer_send_message_to_player, 2),
	(multiplayer_send_int_to_player, 3), (multiplayer_send_2_int_to_player, 4), (multiplayer_send_3_int_to_player, 5), (multiplayer_send_4_int_to_player, 6),
	(multiplayer_send_string_to_player, 3), (get_max_players, 1), (player_get_team_no, 2), (player_set_team_no, 2), (player_get_troop_id, 2), (player_set_troop_id, 2),
	(player_get_agent_id, 2), (agent_get_player_id, 2), (player_get_gold, 2), (player_set_gold, (2, 3)), (player_spawn_new_agent, 2), (player_add_spawn_item, 3),
	(multiplayer_get_my_team, 1), (multiplayer_get_my_troop, 1), (multiplayer_set_my_troop, 1), (multiplayer_get_my_gold, 1), (multiplayer_get_my_player, 1),
	(multiplayer_make_everyone_enemy, 0), (player_control_agent, 2), (player_get_item_id, 3), (player_get_banner_id, 2), (player_set_is_admin, 2), (player_get_score, 2),
	(player_set_score, 2), (player_get_kill_count, 2), (player_set_kill_count, 2), (player_get_death_count, 2), (player_set_death_count, 2), (player_get_ping, 2),
	(player_get_is_muted, 2), (player_set_is_muted, (2, 3)), (player_get_unique_id, 2), (player_get_gender, 2), (player_save_picked_up_items_for_next_spawn, 1),
	(player_get_value_of_original_items, 2), (profile_get_banner_id, 1), (profile_set_banner_id, 1), (team_get_bot_kill_count, 2), (team_set_bot_kill_count, 2),
	(team_get_bot_death_count, 2), (team_set_bot_death_count, 2), (team_get_kill_count, 2), (team_get_score, 2), (team_set_score, 2), (team_set_faction, 2), (team_get_faction, 2),
	(multiplayer_clear_scene, 0), (multiplayer_find_spawn_point, (3, 4)), (set_spawn_effector_scene_prop_kind, 2), (set_spawn_effector_scene_prop_id, 2),
	(start_multiplayer_mission, 3), (kick_player, 1), (ban_player, 3), (save_ban_info_of_player, 1), (ban_player_using_saved_ban_info, 0), (server_add_message_to_log, 1),
	(server_get_renaming_server_allowed, 1), (server_get_changing_game_type_allowed, 1), (server_get_combat_speed, 1), (server_set_combat_speed, 1), (server_get_friendly_fire, 1),
	(server_set_friendly_fire, 1), (server_get_control_block_dir, 1), (server_set_control_block_dir, 1), (server_set_password, 1), (server_get_add_to_game_servers_list, 1),
	(server_set_add_to_game_servers_list, 1), (server_get_ghost_mode, 1), (server_set_ghost_mode, 1), (server_set_name, 1), (server_get_max_num_players, 1), (server_set_max_num_players, 1),
	(server_set_welcome_message, 1), (server_get_melee_friendly_fire, 1), (server_set_melee_friendly_fire, 1), (server_get_friendly_fire_damage_self_ratio, 1),
	(server_set_friendly_fire_damage_self_ratio, 1), (server_get_friendly_fire_damage_friend_ratio, 1), (server_set_friendly_fire_damage_friend_ratio, 1), (server_get_anti_cheat, 1),
	(server_set_anti_cheat, 1),
	(set_physics_delta_time, 1), (ai_mesh_face_group_show_hide, 2), (auto_set_meta_mission_at_end_commited, 0),
])
try:
	if is_vanilla_warband:
		length_array.update(dict([
			(break_loop, 0), (continue_loop, 0), (try_for_dict_keys, 2), (key_is_down, (1, 2)), (key_clicked, (1, 2)), (game_key_is_down, (1, 2)), (game_key_clicked, (1, 2)),
			(server_set_max_num_players, (1, 2)), (position_rotate_x, (2, 3)), (position_rotate_y, (2, 3)), (position_rotate_z, (2, 3)), (position_rotate_z_floating, (2, 3)),
			(position_rotate_x_floating, (2, 3)), (position_rotate_y_floating, (2, 3)),  (is_vanilla_warband, 0), (start_map_conversation, (1, 5)),
			(agent_set_animation_progress, (2, 3)), (prop_instance_receive_damage, (3, 4)), (add_point_light, (0, 3)), (add_point_light_to_entity, (0, 3)),
			(val_shr, 2), (store_shr, 3), (val_lshr, 2), (store_lshr, 3), (val_shl, 2), (store_shl, 3), (val_xor, 2), (store_xor, 3), (val_not, 1), (store_not, 2),
			(player_set_skin, 2), (player_stop_controlling_agent, 1), (player_set_banner_id, 2), (player_set_username, 2), (player_temp_ban, 2), (player_get_wse2_version, 2),
			(player_get_party_id, 2), (player_set_party_id, 2), (register_get, 2), (register_set, 2), (store_wse_version, 2), (item_slot_gt, 3),
			(party_template_slot_gt, 3), (troop_slot_gt, 3), (faction_slot_gt, 3), (quest_slot_gt, 3), (scene_slot_gt, 3), (party_slot_gt, 3), (player_slot_gt, 3),
			(team_slot_gt, 3), (agent_slot_gt, 3), (scene_prop_slot_gt, 3), (store_current_trigger, 1), (return_values, (0, 16)), (store_num_return_values, 1),
			(store_return_value, 2), (set_forced_lod, 1), (send_message_to_url_advanced, (2, 6)), (mtsrand, 1), (mtrand, 3), (get_time, (1, 2)), (order_flag_is_active, 0),
			(play_bink_file, (1, 2)), (process_advanced_url_messages, 0), (sleep_ms, 1), (timer_reset, (1, 2)), (timer_get_elapsed_time, 2), (shell_open_url, 1),
			(set_main_party, 1), (get_main_party, 1), (make_screenshot, 2), (send_post_message_to_url_advanced, (3, 7)), (set_random_seed, 1), (store_application_time, 1),
			(is_party_skill, 1), (get_campaign_time, 1), (set_campaign_time, 1), (get_mouse_map_coordinates, 1), (profiler_start, 0), (profiler_stop, 0),
			(profiler_is_recording, 0), (profiler_mark, 1), (conversation_screen_auto_update_choice, 0), (game_key_get_key, 2), (key_released, (1, 2)),
			(game_key_released, (1, 2)), (dict_create, 1), (dict_free, 1), (dict_load_file, (2, 4)), (dict_load_dict, (2, 3)), (dict_save, (2, 3)), (dict_clear, 1),
			(dict_is_empty, 1), (dict_has_key, 2), (dict_get_size, 2), (dict_delete_file, (1, 2)), (dict_get_str, (3, 4)), (dict_get_int, (3, 4)),
			(dict_set_str, 3), (dict_set_int, 3), (dict_get_key_by_iterator, 3), (dict_get_pos, (3, 4)), (dict_set_pos, 3), (dict_load_file_json, (2, 3)), (dict_save_json, 2),
			(dict_from_url_encoded_json, (2, 3)), (dict_to_url_encoded_json, 2), (dict_erase, 2), (dict_delete_file_json, 1),
			(agent_get_item_modifier, 2), (agent_get_item_slot_modifier, 3), (agent_get_animation_progress, (2, 3)), (agent_get_dna, 2), (agent_get_ground_scene_prop, 2),
			(agent_set_item_slot_ammo, 3), (agent_get_item_slot_hit_points, 3), (agent_set_item_slot_hit_points, 3), (agent_get_wielded_item_slot_no, (2, 3)), (agent_get_scale, 2),
			(agent_set_forced_lod, 2), (agent_get_item_slot_flags, 3), (agent_ai_get_move_target_position, 2), (agent_set_horse, 2), (agent_ai_set_simple_behavior, (2, 3)),
			(agent_accelerate, (2, 3)), (agent_set_item_slot_modifier, 3), (agent_body_meta_mesh_set_vertex_keys_time_point, 3), (agent_body_meta_mesh_set_visibility, 3),
			(agent_set_personal_animation, 3), (agent_get_personal_animation, 3), (agent_set_default_animations, 1), (agent_cancel_current_animation, 2),
			(agent_get_ranged_damage_modifier, 2), (agent_add_stun, 2), (agent_body_meta_mesh_deform_in_range, 5), (agent_body_meta_mesh_deform_in_cycle_loop, 5),
			(agent_body_meta_mesh_get_current_deform_progress, 3), (agent_body_meta_mesh_get_current_deform_frame, 3), (agent_set_footstep_sound, 3),
			(agent_get_horse_rotation_velocity, 2), (agent_get_current_vertical_speed, 2), (agent_set_current_vertical_speed, 2), (agent_get_position_in_group, 2),
			(agent_get_current_ai_mesh_face_group, 2), (agent_set_time_speed_multiplier, 2), (agent_get_time_speed_multiplier, 2), (agent_kick, 1), (agent_set_dropped_items_prune_time, 2),
			(agent_set_missile_items_prune_time, 2), (agent_set_action_speed_modifier, 2), (agent_get_action_speed_modifier, 2), (agent_set_left_hand_weapon_collision, 2),
			(agent_ai_set_can_weapon_switch, 2), (agent_ai_set_can_fight, 2), (agent_fade_out_advanced, 2), (agent_fade_in_advanced, 2), (agent_set_voice_sound, 3),
			(agent_set_enable_tilt, 2), (agent_set_rider_rotation_angles, 4), (agent_get_rider_rotation_angles, 4), (agent_set_default_rider_rotation_angles, 1),
			(agent_ai_set_can_aim, 2), (agent_set_can_multihit, (2, 3)), (agent_has_multihit, 1), (agent_set_crush_through, 2), (agent_get_crush_through, 2),
			(agent_set_trigger_disabled, 3), (agent_is_trigger_disabled, 2), (agent_set_can_piercing, (2, 3)), (agent_has_piercing, 1),
			(multiplayer_send_chat_message_to_player, (3, 4)), (multiplayer_send_composite_message_to_player, 3), (multiplayer_send_composite_message_to_server, 2),
			(multiplayer_get_cur_profile, 1), (multiplayer_get_num_profiles, 1), (multiplayer_message_init, 1), (multiplayer_message_put_string, 2), (multiplayer_message_put_int, (2, 3)),
			(multiplayer_message_put_position, (2, 3)), (multiplayer_message_put_coordinate, (2, 3)), (multiplayer_cur_message_get_string, 1), (multiplayer_cur_message_get_int, (1, 2)),
			(multiplayer_cur_message_get_position, (1, 2)), (multiplayer_cur_message_get_coordinate, (1, 2)), (multiplayer_cur_profile_get_skin, 1),
			(multiplayer_connect_to_server, (2, 3)), (multiplayer_is_campaign, 0),
			(server_set_password_admin, 1), (server_set_password_private, 1), (server_map_rotation_get_count, 1), (server_map_rotation_get_index, 1), (server_map_rotation_set_index, 1),
			(server_map_rotation_get_map, 2), (server_map_rotation_add_map, (1, 2)), (server_map_rotation_remove_map, (0, 1)), (server_get_horse_friendly_fire, 1),
			(server_set_horse_friendly_fire, 1), (server_get_show_crosshair, 1), (server_set_show_crosshair, 1), (get_server_option_at_connect, (1, 2)), (server_set_password_rcon, 1),
			(execute_server_console_command, 2), (add_anonymous_player, 2), (remove_anonymous_player, 1), (clear_anonymous_players, 0), (server_set_ghost_mode_advanced, 5),
			(store_cur_mission_template_no, 1), (set_show_use_tooltip, (1, 2)), (set_ally_collision_threshold, 2), (particle_system_remove, (0, 1)), (get_spectated_agent_no, 1),
			(prop_instance_set_forced_lod, 2), (prop_instance_set_variation_id, 2), (prop_instance_set_variation_id_2, 2), (stop_time, 1), (missile_get_path_point_position, 3),
			(get_water_level, 1), (missile_remove_on_hit, 0), (missile_is_valid, 1), (missile_get_cur_position, 2), (set_prop_collision_threshold, 3), (get_camera_position, 1),
			(prop_instance_remove_particle_system, (1, 2)), (prop_instance_remove_light, 1), (prop_instance_get_sound_progress, 2), (set_horse_friendly_fire, 1),
			(cast_ray_agents, (3, 4)), (ai_mesh_face_group_translate, 2), (set_show_crosshair, 1), (shift_entry_point, 1), (missile_remove, 1), (scene_prop_remove, 1),
			(troop_get_skill_points, 2), (troop_set_skill_points, 2), (troop_get_attribute_points, 2), (troop_set_attribute_points, 2), (troop_get_proficiency_points, 2),
			(troop_set_proficiency_points, 2), (troop_has_flag, 2), (troop_set_skill, 3), (troop_set_attribute, 3), (troop_set_proficiency, 3),
			(item_set_thrust_damage, 2), (item_set_thrust_damage_type, 2), (item_set_swing_damage, 2), (item_set_swing_damage_type, 2), (item_set_head_armor, 2),
			(item_set_body_armor, 2), (item_set_leg_armor, 2), (item_set_speed_rating, 2), (item_set_missile_speed, 2), (item_set_horse_blood_particles, 3),
			(item_set_horse_blood_color, 2), (cur_item_mesh_set_color, 2), (cur_item_add_mesh_with_material, (2, 5)), (item_set_horse_skeleton_model, 2),
			(party_stack_get_experience, 3), (party_stack_get_num_upgradeable, 3), (party_has_flag, 2), (party_heal_members, 3), (party_switch_stacks, 3),
			(party_stack_upgrade, 4), (party_stack_set_num_upgradeable, 3), (party_get_banner_icon, 2), (party_get_extra_icon, 2), (party_get_player_id, 2), (party_is_non_player, 1),
			(position_get_vector_to_position, 4), (position_align_to_ground, (1, 3)), (position_get_length, 2), (get_dot_product_of_positions, 3), (get_cross_product_of_positions, 3),
			(str_equals, (2, 3)), (str_contains, (2, 3)), (str_starts_with, (2, 3)), (str_ends_with, (2, 3)), (str_is_alpha, (1, 2)), (str_is_digit, (1, 2)), (str_is_whitespace, (1, 2)),
			(str_length, 2), (str_index_of, (3, 5)), (str_last_index_of, (3, 5)), (str_get_char, (2, 3)), (str_to_num, (2, 3)), (str_compare, (3, 4)), (str_split, (4, 6)),
			(str_sort, (1, 4)), (str_store_lower, 2), (str_store_upper, 2), (str_store_trim, (2, 3)), (str_store_replace, 4), (str_store_md5, 2), (str_store_substring, (2, 4)),
			(str_store_reverse, 2), (str_store_join, (3, 4)), (str_store_replace_spaces_with_underscores, 2), (str_store_replace_underscores_with_spaces, 2),
			(str_store_multiplayer_profile_name, 2), (str_store_module_setting, 2), (str_store_server_password_admin, 1), (str_store_server_password_private, 1),
			(str_store_overlay_text, 2), (str_store_player_ip, 2), (str_store_game_variable, 2), (str_store_skill_name, 2), (str_store_float, (2, 3)), (str_sanitize, 1),
			(str_store_item_id, 2), (str_is_integer, 1), (str_store_multiplayer_profile_face_keys, 2), (str_store_server_password_rcon, 1), (str_store_item_mesh_name, 2),
			(str_regex_match, 2), (str_regex_search, 2), (str_regex_get_matches, (4, 5)), (str_store_regex_replace, 4), (str_decode_url, 2), (str_store_skill_desc, 2),
			(options_get_verbose_casualties, 1), (options_set_verbose_casualties, 1), (options_get_cheat_mode, 1), (options_set_cheat_mode, 1), (options_get_realistic_headshots, 1),
			(options_set_realistic_headshots, 1),
			(fld, 2), (fld_str, 2), (fld_pos_x, 2), (fld_pos_y, 2), (fld_pos_z, 2), (fst, 2), (fcpy, 2), (feq, 2), (fgt, 2), (flt, 2), (fge, 2), (fle, 2), (fsub, 3), (fmul, 3),
			(fdiv, 3), (fmin, 3), (fmax, 3), (fclamp, 4), (fsqrt, 2), (fabs, 2), (fceil, 2), (ffloor, 2), (fexp, 2), (fpow, 3), (fln, 2), (flog, (2, 3)), (fmod, 3), (fsin, 2),
			(fcos, 2), (ftan, 2), (fsinh, 2), (fcosh, 2), (ftanh, 2), (fasin, 2), (facos, 2), (fatan, 2), (fatan2, 3), (feval, 1), (fadd, 3),
			(scene_set_flags, 2), (scene_set_water_level, 2), (scene_set_bounds, 5), (scene_set_outer_terrain, 2), (scene_set_terrain_seed, 2), (scene_set_river_seed, 2),
			(scene_set_flora_seed, 2), (scene_set_deep_water, 2), (scene_set_place_river, 2), (scene_set_disable_grass, 2), (scene_set_valley_size, 2), (scene_set_hill_height, 2),
			(scene_set_ruggedness, 2), (scene_set_vegetation, 2), (scene_set_size, 3), (scene_set_region_type, 2), (scene_set_region_detail, 2),
			(edit_mode_get_num_selected_prop_instances, 1), (edit_mode_get_selected_prop_instance, 2), (edit_mode_select_prop_instance, 1), (edit_mode_deselect_prop_instance, 1),
			(edit_mode_get_highlighted_prop_instance, 1), (edit_mode_set_highlighted_prop_instance, (0, 1)), (edit_mode_set_enabled, 1), (edit_mode_in_edit_objects_mode, 0),
			(update_material, 2), (reload_item_kinds, (0, 2)), (reload_troops, (0, 2)), (reload_parties, (0, 2)),
			(menu_create_new, (2, 6)), (menu_add_item, (2, 5)), (menu_clear_items, 1), (menu_clear_generated, 0),
			(overlay_get_val, 2), (presentation_activate, 1), (overlay_button_set_type, 3), (overlay_get_scroll_pos, (2, 3)), (overlay_set_scroll_pos, (2, 3)), (overlay_enable, 2),
			(overlay_item_set_text, 3),
			(array_create, (3, 16)), (array_free, 1), (array_copy, 2), (array_save_file, 2), (array_load_file, 2), (array_delete_file, 1), (array_set_val, (3, 16)),
			(array_set_val_all, 2), (array_get_val, (3, 16)), (array_push, 2), (array_pop, 2), (array_resize_dim, 3), (array_get_dim_size, 3), (array_get_dim_count, 2),
			(array_get_type_id, 2), (array_sort, (2, 15)), (array_sort_custom, (2, 15)), (array_eq, (3, 16)), (array_neq, (3, 16)), (array_gt, (3, 16)), (array_ge, (3, 16)),
			(array_lt, (3, 16)), (array_le, (3, 16)),
			(lua_get_top, 1), (lua_set_top, 1), (lua_insert, 1), (lua_remove, 1), (lua_pop, 1), (lua_to_int, 2), (lua_to_str, 2), (lua_to_pos, 2), (lua_push_int, 1),
			(lua_push_str, 1), (lua_push_pos, 1), (lua_get_type, 2), (lua_call, 2), (lua_triggerCallback, (2, 3)), (lua_test, 1),
			(skin_set_blood_color, 2),
			(game_key_get_mapped_key_name, (2, 3)), (options_get_damage_to_player, (1, 2)), (options_set_damage_to_player, (1, 2)), (options_get_damage_to_friends, (1, 2)),
			(options_set_damage_to_friends, (1, 2)), (set_camera_follow_party, (1, 2)), (start_encounter, (1, 2)),
			(party_get_battle_opponent, 2), (agent_get_attached_scene_prop, (2, 3)), (agent_set_attached_scene_prop, (2, 5)), (agent_set_attached_scene_prop_x, (2, 3)),
			(agent_set_attached_scene_prop_z, (2, 3)), (entry_point_get_position, (2, 3)), (agent_set_attached_scene_prop_y, (2, 3)), (prop_instance_intersects_with_prop_instance, (2, 3)),
			(str_store_player_username, (2, 3)), (game_key_get_key, (2, 4)), (str_store_module_setting, 3), (overlay_get_scroll_pos, (2, 3)), (overlay_set_scroll_pos, (2, 3)),
		]))
except Exception as e:
	#(print("failed", e))
	pass