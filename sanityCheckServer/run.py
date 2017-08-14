#!flask/bin/python
import sys
if len(sys.argv) <= 1:
    print "please provide server address: python run.py 185.74.13.86"

else:
    from app import app
    addr = sys.argv[1]
    print sys.argv
    app.run(debug=True, host=addr)
#app.run(debug=True)