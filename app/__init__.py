from .remote.remote import Remote
import app.speaker as speaker
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/remote', methods=['POST'])
def remote():
    action = request.form.get('action')
    remote = Remote()

    if action == 'tv-power':
        remote.tv_toggle_power()
    elif action == 'tv-input':
        remote.tv_toggle_input()
    elif action == 'receiver-input-tv':
        remote.receiver_input_tv()
    elif action == 'receiver-input-ps3':
        remote.receiver_input_ps3()
    elif action == 'receiver-input-mac':
        remote.receiver_input_mac()
    elif action == 'receiver-input-chromecast':
        remote.receiver_input_chromecast()
    elif action == 'receiver-mute':
        remote.receiver_mute()
    elif action == 'receiver-vol-up':
        remote.receiver_vol_up()
    elif action == 'receiver-vol-down':
        remote.receiver_vol_down()
    elif action == 'tv-channel-nbc':
        remote.tv_channel_nbc()
    elif action == 'tv-channel-abc':
        remote.tv_channel_abc()
    elif action == 'tv-channel-fox':
        remote.tv_channel_fox()
    elif action == 'tv-channel-cbs':
        remote.tv_channel_cbs()
    elif action == 'tv-channel-amc':
        remote.tv_channel_amc()
    elif action == 'tv-channel-fx':
        remote.tv_channel_fx()

    return jsonify(success=True)


@app.route('/say', methods=['POST'])
def say():
    message = request.form.get('message')
    speaker.say(message)

    return jsonify(success=True)
