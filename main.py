from app import create_app

#starte die app mit dem development config
app = create_app('development')

if __name__ == '__main__':
    port = 5000
    host = "127.0.0.1"
    # host = '0.0.0.0'
    app.run(host=host, port=port, threaded=True, debug=True)
