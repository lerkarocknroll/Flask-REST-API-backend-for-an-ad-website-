from flask import Blueprint
from views import AdView

bp = Blueprint('bp', __name__)

bp.add_url_rule('/advertisements/<int:id_ad>/',
                view_func=AdView.as_view('advertisement_detail'),
                methods=['GET', 'PATCH', 'DELETE'])

bp.add_url_rule('/advertisements',
                view_func=AdView.as_view('advertisement_create'),
                methods=['POST'])
