"""
Основной файл flask-приложения...
"""
from flask import Flask, render_template, request

import utils

app = Flask(__name__)


@app.errorhandler(404)
def not_found_error(error):
    """ Обработчик ошибки 404.
    W0613: Unused argument 'error' (unused-argument) - pylint не прав на счёт error
    """
    return render_template("error404.html"), 404


@app.route('/', methods=['post', 'get'])
def main_route():
    """
    Главная и единственная страница нашего замечательного приложения
    """
    if request.method == 'POST':
        address = request.form.get('address')  # запрос к данным формы
        radius = request.form.get('radius')
        address_coors = utils.get_address(address)
        # Если геокоддер не нашёл адрес - пишем ошибку
        if address_coors is None:
            return render_template(
                "index.html", message="По вашему запросу не найдено ни одного похожего адреса!"
            )
        # Если задан радиус - ищем ближайшие точки(включая саму точку) и рисуем их
        if radius:
            dots_to_drow = utils. \
                get_closes_points(address_coors["geo_lat"], address_coors["geo_lon"], radius)
        # Если нет - то рисуем только точку
        else:
            dots_to_drow = [address_coors]
        return render_template("index.html", dotLat=address_coors['geo_lat'],
                               dotLon=address_coors['geo_lon'], map_active=True,
                               dots_to_drow=dots_to_drow, default_zoom=utils.get_zoom_level(radius))
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
