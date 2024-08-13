from flask import jsonify, request, Blueprint

hal_ai_test = Blueprint('AEYE_HAL_AI_Test', __name__)

@hal_ai_test.route('/hal/ai-test', methods = ['POST'])
def hal_ai_test() :
    pass
