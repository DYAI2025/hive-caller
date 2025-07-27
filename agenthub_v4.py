from agenthub.hub import create_app

app = create_app(with_ui=True, persistent=True, with_comm=True)

if __name__ == "__main__":
    app.run(port=5000)
