#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Rohit Dua 8ohit.dua AT gmail DOT com
#
# ------------------------------------------------------------------------------------------
# The solution uses a Top Down Dynamic Programming Approach(recursive) with Memoization save
# Input from file: input.txt
# Output: stdout
# ------------------------------------------------------------------------------------------


import sys


class Machine(object):
	def __init__(self, sale_day, cost_price, selling_price, profit_per_day):
		self.sale_day = sale_day
		self.cost_price = cost_price
		self.selling_price = selling_price
		self.profit_per_day = profit_per_day

	def __repr__(self):
		output = 'Machine:- '
		output += "Sale Day: %s, "%self.sale_day
		output += "Cost Price: %s, "%self.cost_price
		output += "Selling Price: %s, "%self.selling_price
		output += "Profit Per Day: %s"%self.profit_per_day
		return output


class ACM(object):
	def __init__(self, balance, number_of_machines, number_of_days):
		self.balance = balance
		self.number_of_machines = number_of_machines
		self.number_of_days = number_of_days
		self.machines_per_day= dict()
		self.sale_days = list()
		# Memoization Save for Dynamic Programming
		# Top Down approach
		self.DP_save = dict()
		for i in range(1,self.number_of_days+1):
			self.DP_save[i] = dict()

	def add_machine_sale(self, sale_day, cost_price, selling_price, profit_per_day):
		"""Add machine to sale"""
		new_machine = Machine(sale_day, cost_price, selling_price, profit_per_day)
		if sale_day in self.machines_per_day.keys():
			self.machines_per_day[sale_day].append(new_machine)
		else:
			self.machines_per_day[sale_day] = list()
			self.machines_per_day[sale_day].append(new_machine)
		return True

	def get_sale_days(self):
		days = sorted(self.machines_per_day.keys())
		return days

	def calculate_max_profit(self):
		"""Function to call to calculate max profit"""
		self.sale_days = self.get_sale_days()
		max_profit = self.execute_calculate_max_profit(day=1, cash=self.balance, current_machine=None)
		return max_profit

	def execute_calculate_max_profit(self, day, cash, current_machine):
		# Each day 2 options: Sell/Buy or Stay
		# Can skip days of non sale
		if day>self.number_of_days:
			if current_machine is not None:
				cash += current_machine.selling_price
				current_machine = None
			return cash
		if current_machine is not None and current_machine in self.DP_save[day].keys():
			return self.DP_save[day][current_machine]
		if day not in self.sale_days:
			#stay and increase profit
			if current_machine is None:
				value = self.execute_calculate_max_profit(day+1, cash, current_machine)
			else:
				value = self.execute_calculate_max_profit(day+1, cash + current_machine.profit_per_day, current_machine)
			self.DP_save[day][current_machine] = value
			return value
		else:
			# Each selling day 2 options: Sell/Buy(for each item) or Stay
			#stay
			if current_machine is None:
				stay_result = self.execute_calculate_max_profit(day+1, cash, current_machine)
			else:
				stay_result = self.execute_calculate_max_profit(day+1, cash + current_machine.profit_per_day, current_machine)
			self.DP_save[day][current_machine] = stay_result
			#Sell and buy
			#sell
			if current_machine is not None:
				cash += current_machine.selling_price
				current_machine = None
			#For each buy, we have multiple options of machines.
			results = list()
			for machine in self.machines_per_day[day]:
				if machine.cost_price <= cash:
					value = self.execute_calculate_max_profit(day+1, cash-machine.cost_price, machine)
					self.DP_save[day][machine] = value
					results.append(value)
			#check if no machine bought, then no need to sell
			if results == []:
				return stay_result
			else:
				#Get max of selling or staying
				selling_result = max(results)
				max_result = max(stay_result, selling_result)
				return max_result


def main():
	input_file = 'input.txt'
	f = open(input_file, 'r')
	raw_input_text = f.read()
	f.close()
	input_per_line = raw_input_text.split('\n')
	result = list()
	A = None
	for values in input_per_line:
		values=values.strip()
		if values == '':
			continue
		values=values.split()
		values = map(int, values)
		if len(values)==3:
			if A is not None:
				result.append(A.calculate_max_profit())
			if values== [0,0,0]:
				break
			A = ACM(balance=values[1], number_of_machines=values[0], number_of_days=values[2])

		else:
			A.add_machine_sale(sale_day=values[0], cost_price=values[1], selling_price=values[2], profit_per_day=values[3])
	for index, res in enumerate(result):
		print "Case %s:%s" %(index+1, res)


if __name__ == '__main__':
    sys.exit(main())