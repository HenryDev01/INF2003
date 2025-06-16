import string
import random
from flask_paginate import Pagination

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


def paginate_list(data_list, page, page_size, search):
    offset = (page - 1) * page_size
    paginated_data = data_list[offset:offset + page_size]
    pagination = Pagination(
        page=page,
        total=len(data_list),
        per_page=page_size,
        css_framework='bootstrap4',
        search=search,
        record_name=data_list
    )
    return paginated_data, pagination