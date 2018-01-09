# **coding: utf-8**

import top.api

PARAM_SITTING = {
    "app_key": "23754165",
    "secret": "3a6606b743cbb00aaf04675d68f14810"
}


class SMSVerification:

    def __init__(self, phone, verify_code, param_sitting=PARAM_SITTING):

        self.app_key = param_sitting['app_key']
        self.secret = param_sitting['secret']
        self.verify_code = verify_code
        self.sms_type = "normal"
        self.sms_free_sign_name = "猫阅读"
        self.sms_param = self.make_sms_param()
        self.rec_num = phone
        self.sms_template_code = "SMS_9680408"

    def make_sms_param(self):
        sms_param = "{\"code\":\"" + self.verify_code + "\",\"product\":\"猫阅读\"}"
        return sms_param

    def send_verify_code(self):
        req = top.api.AlibabaAliqinFcSmsNumSendRequest()
        req.set_app_info(top.appinfo(self.app_key, self.secret))

        req.sms_type = self.sms_type
        req.sms_free_sign_name = self.sms_free_sign_name
        req.sms_param = self.sms_param
        req.rec_num = self.rec_num
        req.sms_template_code = "SMS_9680408"

        try:
            resp = req.getResponse()
            return resp
        except Exception, e:
            return e
