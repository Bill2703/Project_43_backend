# Movie Application
## Setup

- Clone the repository to your computer:
```bash
git clone git@github.com:TatyanaA/book_app_flask.git
```
- Enter to the folder with clonned repo:

```bash
cd `path_to_your_folder`
```

- Open the application in VScode
```bash
code .
```  
- Install packages: 
```bash
pip install pipenv 
pipenv shell
pipenv install 
pipenv install flask flask-cors
pipenv install python-dotenv 
pipenv install flask-sqlalchemy psycopg2-binary
pipenv install flask-jwt-extended
pipenv install scikit-learn pandas
```
- Create .env
```bash
touch .env
```
- Add to the .env file 
    SQLALCHEMY_DATABASE_URI=<link to your DB>
    FLASK_DEBUG=1
    JWT_SECRET_KEY=
    FLASK_APP=app.py
- Seed the database: 
```bash
python seed.py
```
-Run the app
```bash
python app.py
```
You can see the app here:
`http://localhost:4000/`



