import sys
print sys.path
try:
	import trytond
except:
	print "failed1"

try:
	from FSERP import trytond
except:
	print "failed2"

try:
	from .. import trytond
except:
	print "failed3"

try:
	import FSERP
except:
	print "failed4"

try:
	pass
except:
	print "failed5"

