import logging

from django.http import JsonResponse

import client_services
import formatters

logger = logging.getLogger(__name__)

def search_client(request):
    logger.debug("search_client started...")
    filter_data = request.GET.get("filter")
    logger.debug(f"filter_data is {filter_data}")
    client = client_services.search(filter_data)
    logger.debug(f"client is {client}")
    formatted_client = formatters.format_client(client)
    logger.debug(f"formatted_client is {formatted_client}")
    return JsonResponse(
        data=formatters.format_client
    )
