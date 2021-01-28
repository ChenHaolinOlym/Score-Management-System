from sms.app import create_app

app = create_app()
# Open webbrowser
# os.system("python -m webbrowser \"http://localhost:5000/\"")

# Start the app
# app.run(host = "0.0.0.0", port = 80, threaded = True)
app.run(host = "0.0.0.0", port = 5000, threaded = True)
