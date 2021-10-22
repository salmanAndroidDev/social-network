# social-network
Small social network that enables users to register, follow each other, and share posts.<br><br>

to clone this project type below command on your terminal.<br>
`git clone https://github.com/salmanAndroidDev/social-network.git`<br><br>

## setup the project
To setup and run this project you only need to have `docker` and `docker-compose` installed, then type below command on your terminal to run the project<br>
`docker-compose up`<br><br>
to see API documentation checkout `http://localhost:8000/swagger/` url.<br><br>
There are tests for all edge-cases and all requirements, for applying these tests and linting check first run the project typing `docker-compose up` then open another terminal then type below command.<br>
`docker-compose run backend sh -c "cd backend && ./manage.py test && flake8"`
