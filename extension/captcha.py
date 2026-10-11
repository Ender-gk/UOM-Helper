from decimal import Decimal
import re
import unicodedata

def normalize_captcha(raw):
    _v4 = re.sub('\\s+', '', unicodedata.normalize('NFKC', str(raw)))
    for old, new in [('乘以', '*'), ('除以', '/'), ('等于', '='), ('加', '+'), ('减', '-'), ('−', '-'), ('乘', '*'), ('×', '*'), ('除', '/'), ('÷', '/')]:
        _v4 = _v4.replace(old, new)
    match = re.fullmatch('(\\d{1,3})([+*/xX-])(\\d{1,3})(?:=[?？]?)?', _v4)
    if match:
        a, op, b = (Decimal(match[1]), match[2], Decimal(match[3]))
        if op == '/' and (not b):
            raise ValueError('验证码除数为零')
        _v14 = a + b if op == '+' else a - b if op == '-' else a / b if op == '/' else a * b
        if abs(_v14) > 1000000 or _v14 != _v14.quantize(Decimal('.000001')):
            raise ValueError('验证码计算结果不明确')
        return (format(_v14, 'f').rstrip('0').rstrip('.') if '.' in format(_v14, 'f') else str(_v14), 'arithmetic')
    if not re.fullmatch('[a-zA-Z0-9]{4,6}', _v4):
        raise ValueError('验证码识别结果不可靠')
    return (_v4, 'literal')
