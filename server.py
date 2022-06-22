from flask_app import app
from flask_app.controllers import user_controller

# =================================================
# Always import controllers into server  (>^-^)>
# =================================================

if __name__ == "__main__":
    app.run(debug=True)