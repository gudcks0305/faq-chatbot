from nest.core import Module, PyNestFactory

from .app_controller import AppController
from .app_service import AppService
from .domain.faq.faq_module import FaqModule


@Module(imports=[FaqModule], controllers=[AppController], providers=[AppService])
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="This is my PyNest app.",
    title="PyNest Application",
    version="1.0.0",
    debug=True,
)

http_server = app.get_server()
