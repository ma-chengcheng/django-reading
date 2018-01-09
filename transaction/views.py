# **coding: utf-8**
import time
import random
from django.conf import settings
from alipay import AliPay
from rest_framework.views import APIView
from rest_framework.response import Response


class PayAPIView(APIView):

    def get(self, request):

        alipay = AliPay(
            appid="2016080700191008",
            app_notify_url="http://pay.beluga.studio/notify_url.php",
            app_private_key_path=settings.RSA2_DIR + "app_private_key.pem",
            alipay_public_key_path=settings.RSA2_DIR + "alipay_public_key.pem",
            sign_type="RSA2"
        )

        subject = u"猫币".encode("utf8")
        money = int(request.GET.get('money'))
        print type(money)
        out_trade_no = time.strftime("%H%M%S") + str(random.randint(1000, 9999))

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=out_trade_no,
            total_amount=money,
            subject=subject,
            return_url="http://read.beluga.ai"
        )

        content = dict()
        content['request_url'] = u"https://openapi.alipaydev.com/gateway.do?"+order_string
        return Response(data=content)
