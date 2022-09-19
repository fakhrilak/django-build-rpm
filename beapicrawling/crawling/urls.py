# from django.contrib import admin
from django.urls import path
import json
import os
from ninja import NinjaAPI
from ninja import Form, Schema
# from portalBerita.portalBerita import router as portalBerita
from portalBeritaV2.index import router as V2PortarBerita
from opensearch.index import router as opensearch
from portalTwitter.index import router as Twitter
from aisportal.index import router as AIS
api = NinjaAPI()

# api.add_router("/", portalBerita)
api.add_router("/v2", V2PortarBerita)
api.add_router("/v2", Twitter)
api.add_router("/v2",AIS)
# test =  os.environ.get('haloyaaa')
# print(test," ===================== ",type(test))

@api.get("/restart-nginx")
def restartNginx(request):
    os.system("service nginx start")
    return {
        "content": True,
        "kafka": False,
        "topicId": "48"
    }
urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/", api.urls),
]
