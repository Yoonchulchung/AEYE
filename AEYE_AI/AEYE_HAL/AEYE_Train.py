from flask import jsonify, request, Blueprint

hal_ai_train = Blueprint('AEYE_HAL_AI_Train', __name__)

@hal_ai_train.route('/hal/ai-test', methods = ['POST'])
def hal_ai_train() :
    pass
