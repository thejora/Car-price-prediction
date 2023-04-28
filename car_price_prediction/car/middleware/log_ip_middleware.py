import logging


logging.lastResort.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LogIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем IP-адрес клиента
        ip_address = request.META.get('REMOTE_ADDR')
        # Получаем информацию о запросе пользователя
        request_info = f'"{request.method} {request.path} {request.META.get("SERVER_PROTOCOL")}"'
        # Получаем HTTP статус код ответа
        status_code = '-'
        response = self.get_response(request)
        if hasattr(response, 'status_code'):
            status_code = response.status_code

        # Формируем лог-сообщение
        log_message = f'{ip_address} - {request_info} {status_code} {response.content.__len__()}'
        logger.info(log_message)
        return response

