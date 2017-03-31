from flask import Flask, render_template, request
import webbrowser
import requests
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('homePage.html')

@app.route('/who_is_data_handler', methods=['POST'])
def whois_data():
    whoisdomain = request.form.whoisdomain
    r = requests.get('8.8.8.8/pywhois/' + whoisdomain)

    if r.status_code == 200:
        return r.text
    else:
        return {'error': 'Non 200 status code'}

@app.route('/ipinfo_data_handler', methods=['POST'])
def ipinfo_data():
    ip = request.form.ip
    r = requests.get('8.8.8.8/ipinfo/' + ip)

    if r.status_code == 200:
        return r.text
    else:
        return {'error': 'Non 200 status code'}


if __name__ == "__main__":
    app.run()