#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: moling3650
# @Date:   2017-02-05 10:54:30
import json
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_folder='dist/static', template_folder='dist')

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json;charset=utf-8'

API_DATA = {}
for channel_id in (418, 369, 370, 371):
    with open('./mock/channel/%s.json' % channel_id, encoding='utf-8') as reader:
        API_DATA[channel_id] = json.loads(reader.read())

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
  'Cookie': 'app_id=mi_wap; build=8888; device_id=D950F1TFKU3IBFFU; user_type=2; device_hash=496f44881d27ff72819bace744e4b625; Hm_lvt_a1d10542fc664b658c3ce982b1cf4937=1485254476,1485297249,1485383348,1485493502; Hm_lpvt_a1d10542fc664b658c3ce982b1cf4937=1485501661'
}


@app.route('/api/channel/<int:id>')
def api_channel(id):
    if id in (369, 370, 371):
        return jsonify(API_DATA[id])
    else:
        return jsonify(API_DATA[418])


@app.route('/api/book/<id>')
def api_book(id):
    r = requests.get('http://dushu.xiaomi.com/hs/v0/android/fiction/book/%s' % id, headers=headers)
    return jsonify(json.loads(r.text))


@app.route('/api/detail/<id>')
def api_detail(id):
    r = requests.get('http://dushu.xiaomi.com/store/v0/fiction/detail/%s' % id, headers=headers)
    return jsonify(json.loads(r.text))


@app.route('/api/recommend')
def api_recommend():
    start = request.args.get('start', '0')
    r = requests.get('http://dushu.xiaomi.com/rock/book/recommend?start=%s&count=10' % start, headers=headers)
    return jsonify(json.loads(r.text))

@app.route('/api/link')
def api_link():
    fid = request.args.get('fiction_id', '18211')
    cid = request.args.get('chapter_id', '0')
    r = requests.get('http://dushu.xiaomi.com/drm/v0/fiction/link?fiction_id=%s&chapter_id=%s&format=jsonp' % (fid, cid), headers=headers)
    return jsonify(json.loads(r.text))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
