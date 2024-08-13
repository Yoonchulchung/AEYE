from flask import Flask, jsonify
from AEYE_AI.config import opticnet_config

def aeye_opticnet_framework(aeye: Flask):
    from AEYE_APPLICATION.AEYE_AOT import api_aot
    from AEYE_APPLICATION.AEYE_AtoF import api_AtoF
    from AEYE_APPLICATION.AEYE_UinC import api_UinC
    from AEYE_APPLICATION.AEYE_UCTC import api_UCTC

    aeye.register_blueprint(api_aot)
    aeye.register_blueprint(api_AtoF)
    aeye.register_blueprint(api_UinC)
    aeye.register_blueprint(api_UCTC)
    
    from AEYE_HAL.AEYE_Inference import hal_ai_inference
    from AEYE_HAL.AEYE_Test import hal_ai_test
    from AEYE_HAL.AEYE_Train import hal_ai_train
    from AEYE_HAL.AEYE_Status import hal_ai_status

    aeye.register_blueprint(hal_ai_inference)
    #aeye.register_blueprint(hal_ai_train)
    #aeye.register_blueprint(hal_ai_test)
    #aeye.register_blueprint(hal_ai_status)
    
    from AEYE_MW.AEYE_Status import mw_status
    aeye.register_blueprint(mw_status)
    
    

    @aeye.before_request
    def before_my_request():
        pass

    @aeye.after_request
    def after_my_request(res):
        return res

def create_aeye_opticnet_framework():
    aeye = Flask(__name__)
    aeye.config.from_object((get_opticnet_env()))
    aeye_opticnet_framework(aeye)
    return aeye

def get_opticnet_env():
    if(opticnet_config.Config.ENV == "prod"):
        return 'config.opticnet.prodConfig'
    elif (opticnet_config.Config.ENV == "dev"):
        return 'config.opticnet.devConfig'

