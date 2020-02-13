from flask import make_response,jsonify,Blueprint

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/')
def say():
    response = make_response(jsonify({'first':'党语萱','second':'党秉宸'}), 200,{"name": "page four"})
    return response