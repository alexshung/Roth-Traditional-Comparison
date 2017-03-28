"""
Todos: non-401k capped
variable tax brackets (including future vs now)
Investing interval
Varied tax filing statuses
Variable income over years
"""
import math
class TaxBracket:
	def __init__(self, start, end, percent):
		self.start = start
		self.end = end
		self.percent = percent

def gatherInputs():
	yearsInvesting = input('Enter years remaining: ')
	yearlyContribution = input('Enter yearly contribution: ')
	expectedGrowthRate = intput('Enter yearly expected growth')
	return (yearsInvesting, yearlyContribution, expectedGrowthRate)

def makeTaxBrackets():
	taxRates = [.1, .15, .25, .28, .33, .35, .396]
	starts = [0, 9326, 37951, 91901, 191651, 416701, 418401]
	taxBrackets = []
	for i in range(0, len(starts)):
		end = starts[i+1] if i != len(starts)-1 else -1
		taxBrackets.append(TaxBracket(starts[i], end, taxRates[i]))
	return taxBrackets

def printTaxBrackets(taxBrackets):
	for bracket in taxBrackets:
		print("Tax bracket information: starting income "+str(bracket.start)+" ending income "+str(bracket.end)+" percentage taxed "+str(bracket.percent))

def currentTax(amt, taxBrackets):
	retAmt = 0
	for bracket in taxBrackets:
		amtInBracket = min(bracket.end, amt) - bracket.start
		if amtInBracket <=0:
			if bracket.end == -1:
				retAmt += (amt-bracket.start)*bracket.percent
			break
		retAmt += amtInBracket * bracket.percent
		amtAdded = amtInBracket * bracket.percent
	return retAmt

def effectiveTax(annualIncome, taxBrackets):
	return currentTax(annualIncome, taxBrackets) / annualIncome

# Uses the annual contribution on compounded interest formula: (A/i) * (1+ i)^n - A/i
# Where A is the annual contr, i is the yearly interest rate, and n is the number of years
# Then once the contributions end, uses just the compound interest formula: P*(1+i)^n
def growth(annualGrowth, annualContr, yearsContr, yearsGrow):
	amtIncrease = annualContr / annualGrowth
	growthWhileContr = amtIncrease * math.pow((1+annualGrowth), yearsContr) - amtIncrease
	growthOverall = growthWhileContr * math.pow(1+annualGrowth, yearsGrow)
	return growthOverall

def traditionalAmount(annualIncome, annualContrAmt, taxBrackets, withdrawalAmt, annualGrowth, yearsContr, yearsGrow=0):
	taxedIncome = annualIncome - annualContrAmt
	effectTax = effectiveTax(taxedIncome, taxBrackets)
	effectTaxOverall = effectiveTax(annualIncome, taxBrackets)
	bracketTaxDiff = (effectTaxOverall * annualIncome -effectTax * taxedIncome) * (1-effectTax)
	print(bracketTaxDiff)
	initSavings = effectTax * annualContrAmt
	reinvestedSavings = (1-effectTax) * initSavings
	print(reinvestedSavings)
	totalContr = annualContrAmt + bracketTaxDiff # + reinvestedSavings
	totalSavings = growth(annualGrowth, totalContr, yearsContr, yearsGrow)
	netGain = totalSavings - (effectiveTax(withdrawalAmt, taxBrackets) * (totalSavings - (bracketTaxDiff) * yearsContr))
	netGainOrig = (1-effectiveTax(withdrawalAmt, taxBrackets)) * totalSavings
	return netGain

def traditionalAmountSubLimit(annualIncome, annualContrAmt, taxBrackets, withdrawalAmt, annualGrowth, yearsContr, yearsGrow=0):
	# If the limit is hit, roth just grows naturally
	# If the limit isn't hit, roth will have taxed amount less
	tradSavings = growth(annualGrowth, annualContrAmt, yearsContr, yearsGrow) * (1-effectiveTax(withdrawalAmt, taxBrackets))
	rothAnnualContr = (1-effectiveTax(annualIncome, taxBrackets)) * annualContrAmt
	rothSavings = growth(annualGrowth, rothAnnualContr, yearsContr, yearsGrow)
	return (tradSavings, rothSavings)

def rothAmount(annualContrAmt, annualGrowth, yearsContr, yearsGrow=0):
	return growth(annualGrowth, annualContrAmt, yearsContr, yearsGrow)

	return netGain
if __name__ == "__main__":
	taxBrackets = makeTaxBrackets()
	annualIncome = 100000
	yearlyContr = 18000
	withdrawalAmt = 44600
	annualGrowth = 0.07
	yearsContr = 10
	yearsGrow = 20
	traditionalAmt = traditionalAmount(annualIncome, yearlyContr, taxBrackets, withdrawalAmt, annualGrowth, yearsContr, yearsGrow)
	rothAmt = rothAmount(yearlyContr, annualGrowth, yearsContr, yearsGrow)
	print('Estiamted traditional: '+str(traditionalAmt)+' roth: '+str(rothAmt))
	yearlyContrUnder = 15000
	(tradAmtUnder, rothAmtUnder) = traditionalAmountSubLimit(annualIncome, yearlyContr, taxBrackets, withdrawalAmt, annualGrowth, yearsContr, yearsGrow)
	print('Estimated TradUnder: '+str(tradAmtUnder)+' rothUnder: '+str(rothAmtUnder))

