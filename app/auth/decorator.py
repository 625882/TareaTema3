from functools import wraps

from flask_login import current_user
from werkzeug.exceptions import abort

import app

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, 'is_admin', False)
        if not is_admin:
            app.logger.warning("Se ha intentado acceder a la pagina de administración.")
            abort(401)
        return f(*args, **kws)
    return decorated_function