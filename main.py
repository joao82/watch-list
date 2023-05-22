import os
from webapp import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG"), port=os.getenv("PORT", default=5000))
