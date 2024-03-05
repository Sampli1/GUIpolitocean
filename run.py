from app import app
import os


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run("0.0.0.0", port=os.getenv('PORT', 6969), debug=True)

