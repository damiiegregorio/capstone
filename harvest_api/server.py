from flask import render_template, request

import config

app = config.connex_app

app.add_api('swagger.yml')


@app.route('/')
def home():
    return render_template('home.html')

# Comment if docker:
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
