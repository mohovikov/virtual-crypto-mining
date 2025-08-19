from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()