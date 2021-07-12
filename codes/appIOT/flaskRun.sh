export FLASK_APP=silentApp		#name of main script to run
export FLASK_ENV=development	#deploying as development environment
#flask run						#runs the flask app
flask run --host=0.0.0.0	#tells OS to listen on all public IPs, enabling us to access through phone.
