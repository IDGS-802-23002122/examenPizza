Examen pizzas con flask y python

# Crear entorno
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (macOS/Linux)
source venv/bin/activate

# Instalación de dependencias (forma 1)
pip install -r requirements.txt
# Para ver lo que se instalo
pip list 

# Instalación de dependencias (forma 2) 
pip install flask flask-sqlalchemy flask-wtf pymysql cryptography email-validator

# Creacion entorno virtual 
python -m venv venv (solo la primera vez)
# Para activarlo
cd venv/Scripts/activate