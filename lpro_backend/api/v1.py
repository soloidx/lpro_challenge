from ninja import Router

v1_router = Router()


@v1_router.get("/calculate")
def calculate():
    return 0
