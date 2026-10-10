import base64
import binascii
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from uom_engine import Ensemble
VERSION = '1.2.0'

def create_app(engine=None):
    _v0 = Flask(__name__)
    _v0.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
    CORS(_v0, origins=['https://uom.caac.gov.cn'])
    _v1 = engine or Ensemble()

    @_v0.get('/health')
    def health():
        return jsonify(status='ok' if _v1.ready else 'starting', engine='dual_ensemble', version=VERSION)

    @_v0.post('/ocr')
    def recognize():
        _v2 = request.get_json(silent=True)
        if not isinstance(_v2, dict) or not isinstance(_v2.get('image'), str):
            return (jsonify(success=False, error='image 必须为 base64 字符串'), 400)
        _v3 = _v2['image']
        if _v3.startswith('data:'):
            if ',' not in _v3 or ';base64' not in _v3.split(',', 1)[0]:
                return (jsonify(success=False, error='无效 data URL'), 400)
            _v3 = _v3.split(',', 1)[1]
        try:
            image = base64.b64decode(_v3, validate=True)
            if not image:
                raise ValueError('图片内容为空')
        except (binascii.Error, ValueError) as _v7:
            return (jsonify(success=False, error=str(_v7)), 400)
        try:
            _v4, _v5, _v6 = _v1.predict(image)
            if len(_v4) != 4:
                return jsonify(success=False, error='未识别出四位验证码')
            return jsonify(success=True, text=_v4, confidence=_v5, method=_v6)
        except TimeoutError:
            return (jsonify(success=False, error='模型正在处理其它请求'), 429)
        except ValueError as _v7:
            return (jsonify(success=False, error=str(_v7)), 400)
        except Exception:
            _v0.logger.exception('OCR inference failed')
            return (jsonify(success=False, error='模型识别失败'), 500)

    @_v0.errorhandler(413)
    def too_large(_):
        return (jsonify(success=False, error='图片请求超过 4MB'), 413)
    return _v0
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    engine = Ensemble()
    engine.initialize()
    print('UOM AI OCR v1.2: http://127.0.0.1:8899')
    create_app(engine).run(host='127.0.0.1', port=8899, debug=False, threaded=True)
