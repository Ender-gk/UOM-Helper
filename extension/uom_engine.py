from collections import OrderedDict
import hashlib
import io
import logging
import threading

class Ensemble:

    def __init__(self):
        self.ready = False
        self._p0 = threading.Lock()
        self._p1 = OrderedDict()
        self._p2 = None
        self._p3 = None

    def initialize(self):
        with self._p0:
            self._p4()

    def _p4(self):
        if self.ready:
            return
        import ddddocr
        self._p2 = ddddocr.DdddOcr(show_ad=False)
        self._p3 = ddddocr.DdddOcr(beta=True, show_ad=False)
        for _vc in (self._p2, self._p3):
            _vc.set_ranges('0123456789abcdefghijklmnopqrstuvwxyz')
        self.ready = True

    @staticmethod
    def _p5(image):
        from PIL import Image
        try:
            with Image.open(io.BytesIO(image)) as _v8:
                if _v8.width < 1 or _v8.height < 1 or _v8.width > 2048 or (_v8.height > 2048):
                    raise ValueError('图片尺寸超出限制')
                _v8.verify()
        except ValueError:
            raise
        except Exception as _v7:
            raise ValueError('图片格式无效') from _v7

    @staticmethod
    def _p6(image):
        import cv2
        import numpy as np
        _v8 = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
        if _v8 is None:
            return None
        _v16 = cv2.cvtColor(_v8, cv2.COLOR_BGR2LAB)
        _v17, a, b = cv2.split(_v16)
        _v18 = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(6, 6)).apply(_v17)
        _v19 = cv2.cvtColor(cv2.merge((_v18, a, b)), cv2.COLOR_LAB2BGR)
        _v1a, _v3 = cv2.imencode('.jpg', _v19)
        return _v3.tobytes() if _v1a else None

    @staticmethod
    def _p7(_vc, image):
        _v14 = _vc.classification(image, probability=True)
        if not isinstance(_v14, dict):
            raise ValueError('ddddocr 返回格式不兼容，请使用 requirements.txt 的固定版本')
        _v4 = str(_v14.get('text', '')).lower().strip()
        _v5 = float(_v14.get('confidence', 0.9))
        if any((_v1c not in '0123456789abcdefghijklmnopqrstuvwxyz' for _v1c in _v4)):
            return ('', 0)
        return (_v4, max(0, min(1, _v5)))

    def _p8(self, image):
        _v9 = {}
        _va = []
        _vb = []
        for _vc in (self._p2, self._p3):
            try:
                _va.append(self._p7(_vc, image))
            except Exception as _v7:
                _vb.append(_v7)
                logging.getLogger(__name__).warning('OCR model failed: %s', _v7)
                _va.append(('', 0))
        if len(_vb) == 2:
            raise RuntimeError('Both OCR engines failed') from _vb[0]
        (_vd, _v10), (_ve, _v11) = _va
        for _v4, _v12 in ((_vd, _v10), (_ve, _v11)):
            if len(_v4) == 4:
                _v9[_v4] = _v9.get(_v4, 0) + _v12
        if _vd == _ve and len(_vd) == 4:
            return (_vd, 0.99, 'std+beta一致')
        try:
            _v13 = self._p6(image)
            if _v13:
                _vf, _v12 = self._p7(self._p2, _v13)
                if len(_vf) == 4:
                    _v9[_vf] = _v9.get(_vf, 0) + _v12
        except Exception as _v7:
            logging.getLogger(__name__).warning('Enhanced OCR unavailable: %s', _v7)
        if _v9:
            return (max(_v9, key=_v9.get), 0.95, '加权投票裁决')
        return (_vd or _ve or '', 0.6, '保底输出')

    def predict(self, image):
        self._p5(image)
        if not self._p0.acquire(timeout=0.2):
            raise TimeoutError('OCR busy')
        try:
            self._p4()
            _v15 = hashlib.sha256(image).digest()
            if _v15 in self._p1:
                self._p1.move_to_end(_v15)
                return self._p1[_v15]
            _v14 = self._p8(image)
            if len(_v14[0]) == 4:
                self._p1[_v15] = _v14
                while len(self._p1) > 128:
                    self._p1.popitem(last=False)
            return _v14
        finally:
            self._p0.release()
