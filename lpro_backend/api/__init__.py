from ninja import NinjaAPI
from api.v1 import v1_router


api = NinjaAPI()


@api.get("/")
def index(request):
    return {"status": "ok"}


api.add_router("/v1/", v1_router)
