# note: this needs to be run by jython
import sys
from java.util.concurrent import Callable, Executors
from java.lang import Runtime, System, IllegalArgumentException

class PositionGenerator:
	def __init__(self):
		self.position_cache = {}

	def generate(self, coins):
		positions = []
		# add the initial position just containing a single pile of all coins
		positions.append([coins])
		if coins > 1:
			is_enough_cached = self.position_cache.has_key(coins - 1)
			if not is_enough_cached:
				self.generate_previous(coins)
			self.create_rearrangements(coins, positions)
			self.position_cache[coins] = positions
		return positions

	def generate_previous(self, upto):
		for coins in range(1, upto):
			self.generate(coins)

	def create_rearrangements(self, coins, positions):
		pile_left = coins - 1
		pile_right = 1
		while pile_left >= pile_right:
			# add the pair as a position
			positions.append([pile_left, pile_right])
			# are there other ways of arranging the left pile? 
			if pile_left > 1:
				# get previously generated ways of arranging the left pile
				left_perms = self.position_cache[pile_left]
				# skip the initial position containing a pile with all coins
				left_perms = left_perms[1:]
				# merge each left permuations with the right pile
				self.merge_perms(left_perms, pile_right, positions)
			pile_left -= 1
			pile_right += 1

	def merge_perms(self, left_perms, pile_right, positions):
		'''
		Creates a new set of positions by combining each permutation 
		of the left pile with the right pile.
		'''		
		# repetively substitute the left pile for an alternative permutation 
		for perm in left_perms:
			is_desc_order = pile_right <= perm[-1]
			if is_desc_order:
				new_pos = perm + [pile_right]
				positions.append(new_pos)

class Game:
	def __init__(self, start_pos):
		self.current_position = start_pos
		self.move_history = [start_pos]
		self.loop = 0
		self.score = 0

	def play(self):
		last_move_repeated = False
		while not last_move_repeated:
			self.perform_move()
			last_move_repeated, repeated_move_number = self.check_repeated()
			if last_move_repeated:
				self.loop = self.score - repeated_move_number
			else:
				self.move_history.append(self.current_position)
			self.score += 1

	def check_repeated(self):
		is_repeated = False
		repeated_move_number = len(self.move_history) - 1
		for old_position in reversed(self.move_history):
			repeated_move_number -= 1
			if old_position == self.current_position:
				is_repeated = True
				break
		return (is_repeated, repeated_move_number)

	def perform_move(self):
		new_pos = []
		new_pile = len(self.current_position)
		added_new_pile = False
		for pile in self.current_position:
			updated_pile = pile - 1
			if updated_pile > 0:
				if not added_new_pile and updated_pile <= new_pile:
					new_pos.append(new_pile)
					added_new_pile = True
				new_pos.append(updated_pile)
		if not added_new_pile:
			new_pos.append(new_pile)
		self.current_position = new_pos

class GamePlayer:
	def __init__(self, positions):
		self.positions = positions
		# init stats
		self.max_score = 0
		self.max_score_positions = []
		self.max_loop = 0
		self.max_loop_positions = []

	def play(self):
		num_threads = Runtime.getRuntime().availableProcessors()
		executor = Executors.newFixedThreadPool(num_threads)
		callables = [_Worker(start_pos) for start_pos in self.positions]
		futures = executor.invokeAll(callables)
		# calculate stats
		for future in futures:
			worker = future.get()
			self.process_scores(worker)
		executor.shutdown()

	def process_scores(self, worker):
		game = worker.game
		pos = worker.start_pos
		# score stats
		if game.score > self.max_score:
			self.max_score = game.score
			self.max_score_positions = [pos]
		elif game.score == self.max_score:
			self.max_score_positions.append(pos)
		# loop stats
		if game.loop > self.max_loop:
			self.max_loop = game.loop
			self.max_loop_positions = [pos]
		elif game.loop == self.max_loop:
			self.max_loop_positions.append(pos)

class _Worker(Callable):
	def __init__(self, start_pos):
		self.start_pos = start_pos

	def call(self):
		self.game = Game(self.start_pos)
		self.game.play()
		return self

def main():
	try:
		arg_max_coins = sys.argv[1]
		max_coins = int(arg_max_coins)
		if max_coins < 1:
			raise IllegalArgumentException('Number of coins must be 1 or more')
	except Exception, e:
		print "Error: You must give a single integer argument for the max coins to calculate: ", e
	else:
		st = System.currentTimeMillis()
		pgen = PositionGenerator()
		for coins in range(1, max_coins + 1):
			# generate all the possible starting positions
			pgen_st = System.currentTimeMillis()
			positions = pgen.generate(coins)
			pgen_et = System.currentTimeMillis()
			# play the game for each starting position
			pgame_st = System.currentTimeMillis()
			player = GamePlayer(positions)
			player.play()
			pgame_et = System.currentTimeMillis()
			print "Coins=%d" % coins
			print "  Highest Score is %d found in %d/%d positions" % (player.max_score, len(player.max_score_positions), len(positions))
			print "  Highest Loop is %d found in %d/%d positions" % (player.max_loop, len(player.max_loop_positions), len(positions))
			print "  TIMES pgen: %sms, pgame: %dms" % (pgen_et - pgen_st, pgame_et - pgame_st)
		print "Total run time %dms" % (System.currentTimeMillis() - st)

if __name__ == '__main__':
	main()
