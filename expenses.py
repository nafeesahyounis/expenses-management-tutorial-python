#!/usr/bin/python
from os import system

class ExpensesApp(object):
	"""
		An application that allows you to manage your expenses.
		This is how you initialize and start the app:

		app = ExpensesApp()
		app.start()
	"""

	def __init__(self):
		# Map of commands to their handlers
		self._commands = {
			"login": self._cmd_log_in,
			"logout": self._cmd_log_out,
			"add": self._cmd_add_expense,
			"list": self._cmd_list_expenses,
			"search": self._cmd_search_expenses,
			"clear": self._cmd_clear,
			"help": self._cmd_list_commands,
			"exit": self._cmd_exit,
		}

		# Expenses database
		self._db = []

		# Current username
		self._username = None

		# Exit flag
		self._exit = False


	def start(self):
		# Main program loop
		while not self._exit:
			# Read command and agruments from the user input
			user_input = input("cmd> ")
			try:
				command, *args = user_input.split()
			except:
				continue

			# React to an unknown command
			if command not in self._commands:
				print("Unknown command {} (type 'help' for the list of commands)".format(command))
				continue

			# Run command
			self._commands[command](*args)

		print("Goodbye!")

	def _cmd_log_in(self, username=None, *args):
		"""
			Log in command.
			Prerequisite to other expenses management commands
		"""
		if username is None:
			print("usage: login <name>")
			return
		self._username = username
		print("Logged in as {}".format(username))

	def _is_logged_in(self):
		"""
			Returns True if user is logged in
		"""
		return self._username is not None

	def _cmd_log_out(self):
		"""
			Logs out user
		"""
		print("User logged out")

	def _cmd_add_expense(self, name=None, amount=None, *args):
		"""
			Adds an expense for the logged in user
		"""
		if not self._is_logged_in():
			print("You must log in first.")
			return

		try:
			f_amount = float(amount)

			# Add expense to the database
			self._db.append({
				"name": name,
				"amount": f_amount,
				"username": self._username,
			})
			print("Added new expense.")
		except Exception as e:
			# If there was an exception, print usage
			print("usage: add <name> <amount> [<group>]")

	def _cmd_list_expenses(self, *args):
		"""
			Displays expenses of the logged in user
		"""

		if not self._is_logged_in():
			print("You must log in first.")
			return

		try:
			# Display header
			print("name\tamount")

			# Display rows
			for row in self._db:
				# Skip other users' rows
				if row["username"] != self._username:
					continue

				# Print the row
				print("{}\t{}".format(
					row["name"],
					row["amount"],
				))
		except:
			# If there was an exception, print usage
			print("usage: list")

	def _cmd_search_expenses(self, searchstring=None, *args):
		"""
			Searches expenses of the logged in user by their name
		"""

		if not self._is_logged_in():
			print("You must log in first.")
			return

		try:
			# Validate arguments
			if not isinstance(searchstring, str):
				raise

			# Display header
			print("name\tamount")

			# Display rows
			for row in self._db:
				# Skip other users' rows
				if row["username"] != self._username:
					continue

				# Skip records that don't contain the searchstring
				if searchstring not in row["name"]:
					continue

				# Print the row
				print("{}\t{}".format(
					row["name"],
					row["amount"],
				))
		except:
			# If there was an exception, print usage
			print("usage: search <searchstring>")

	def _cmd_list_commands(self):
		"""
			Prints all avaliable commands
		"""
		for command in self._commands:
			print(command)

	def _cmd_exit(self):
		"""
			Sets the exit flag to true
		"""
		self._exit = True

	def _cmd_clear(self):
		"""
			Clears the screen
		"""
		system('clear')


if __name__ == '__main__':
	app = ExpensesApp()
	app.start()