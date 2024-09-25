from flask import Flask, send_from_directory, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Конвертация RGB в CMYK
def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy
    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)

# Конвертация CMYK в RGB
def cmyk_to_rgb(c, m, y, k):
    c, m, y, k = c / 100, m / 100, y / 100, k / 100
    r = round(255 * (1 - c) * (1 - k))
    g = round(255 * (1 - m) * (1 - k))
    b = round(255 * (1 - y) * (1 - k))
    return r, g, b

# Конвертация RGB в HSV
def rgb_to_hsv(r, g, b):
    r_prime, g_prime, b_prime = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r_prime, g_prime, b_prime)
    cmin = min(r_prime, g_prime, b_prime)
    delta = cmax - cmin
    h = 0
    if delta == 0:
        h = 0
    elif cmax == r_prime:
        h = (60 * ((g_prime - b_prime) / delta) + 360) % 360
    elif cmax == g_prime:
        h = (60 * ((b_prime - r_prime) / delta) + 120) % 360
    elif cmax == b_prime:
        h = (60 * ((r_prime - g_prime) / delta) + 240) % 360
    s = 0 if cmax == 0 else delta / cmax
    v = cmax
    return round(h), round(s * 100), round(v * 100)

# Конвертация HSV в RGB
def hsv_to_rgb(h, s, v):
    s, v = s / 100, v / 100
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if 0 <= h < 60:
        r_prime, g_prime, b_prime = c, x, 0
    elif 60 <= h < 120:
        r_prime, g_prime, b_prime = x, c, 0
    elif 120 <= h < 180:
        r_prime, g_prime, b_prime = 0, c, x
    elif 180 <= h < 240:
        r_prime, g_prime, b_prime = 0, x, c
    elif 240 <= h < 300:
        r_prime, g_prime, b_prime = x, 0, c
    else:
        r_prime, g_prime, b_prime = c, 0, x
    r = round((r_prime + m) * 255)
    g = round((g_prime + m) * 255)
    b = round((b_prime + m) * 255)
    return r, g, b

# Конвертация HEX в RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@app.route('/')
def index():
    return send_from_directory('', 'index.html')
def index():
    color = None
    r, g, b = 50, 168, 82  # Значения по умолчанию для RGB
    c, m, y, k = rgb_to_cmyk(r, g, b)  # Значения по умолчанию для CMYK
    h, s, v = rgb_to_hsv(r, g, b)      # Значения по умолчанию для HSV

    if request.method == 'POST':
        try:
            if 'rgb_submit' in request.form:
                r = int(request.form['r'])
                g = int(request.form['g'])
                b = int(request.form['b'])
                c, m, y, k = rgb_to_cmyk(r, g, b)
                h, s, v = rgb_to_hsv(r, g, b)
            elif 'cmyk_submit' in request.form:
                c = int(request.form['c'])
                m = int(request.form['m'])
                y = int(request.form['y'])
                k = int(request.form['k'])
                r, g, b = cmyk_to_rgb(c, m, y, k)
                h, s, v = rgb_to_hsv(r, g, b)
            elif 'hsv_submit' in request.form:
                h = int(request.form['h'])
                s = int(request.form['s'])
                v = int(request.form['v'])
                r, g, b = hsv_to_rgb(h, s, v)
                c, m, y, k = rgb_to_cmyk(r, g, b)
            elif 'color_submit' in request.form:
                hex_color = request.form['color']
                r, g, b = hex_to_rgb(hex_color)
                c, m, y, k = rgb_to_cmyk(r, g, b)
                h, s, v = rgb_to_hsv(r, g, b)

            r = max(min(255, r), 0)
            g = max(min(255, g), 0)
            b = max(min(255, b), 0)
            c = max(min(100, c), 0)
            m = max(min(100, m), 0)
            y = max(min(100, y), 0)
            k = max(min(100, k), 0)
            h = max(min(100, h), 0)
            s = max(min(100, s), 0)
            v = max(min(100, v), 0)

            # Проверяем, что значения RGB находятся в пределах [0, 255]
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                color = f'#{r:02x}{g:02x}{b:02x}'
            else:
                print("error")

        except ValueError as e:
            error_message = str(e)

    return render_template('index.html', color=color, r=r, g=g, b=b, c=c, m=m, y=y, k=k, h=h, s=s, v=v)

if __name__ == '__main__':
    app.run(debug=True)
