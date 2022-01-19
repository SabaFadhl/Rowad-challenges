
def averageValue(s):

	sumChar = 0

	for i in range(len(s)):
		sumChar += ord(s[i])

	return sumChar // len(s)

def printMinMax(string):

	lis = list(string.split(" "))

	maxId = 0
	minId = 0
	maxi = -1

	mini = 1e9

	for i in range(len(lis)):

		curr = averageValue(lis[i])

		if(curr > maxi):

			maxi = curr
			maxId = i

		if(curr < mini):

			mini = curr
			minId = i

	print("Minimum average ascii word = ", lis[minId])

	print("Maximum average ascii word = ", lis[maxId])



S = "every moment is fresh beginning"
printMinMax(S)
