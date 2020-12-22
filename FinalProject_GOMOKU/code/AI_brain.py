from AI_v1 import *
def brain_turn():
    	if pp.terminateAI:
		return
	i = 0
	while True:
		x = random.randint(0, pp.width)
		y = random.randint(0, pp.height)
		i += 1
		if pp.terminateAI:
			return
		if isFree(x,y):
			break
	if i > 1:
		pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
	pp.do_mymove(x, y)