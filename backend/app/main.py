from . import create_app

# Create the Flask application using our factory function.
app = create_app()

if __name__ == "__main__":
    # Running this file directly: start the development server.
    # In production, you would use gunicorn or another WSGI server.
    app.run(debug=True)
