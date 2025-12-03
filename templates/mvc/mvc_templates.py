import os
from templates.mvc.models.user_model_template import get_user_model_content
from templates.mvc.controllers.auth_controller_template import get_auth_controller_content
from templates.mvc.services.auth_service_template import get_auth_service_content
from templates.mvc.views.login_view_template import get_login_view_content
from templates.mvc.views.home_view_template import get_home_view_content

def create_mvc_templates(lib_path: str):
    """Create template files for MVC architecture."""
    model_path = os.path.join(lib_path, 'models')
    controller_path = os.path.join(lib_path, 'controllers')
    service_path = os.path.join(lib_path, 'services')
    view_path = os.path.join(lib_path, 'views')
    
    os.makedirs(model_path, exist_ok=True)
    os.makedirs(controller_path, exist_ok=True)
    os.makedirs(service_path, exist_ok=True)
    os.makedirs(view_path, exist_ok=True)
    
    with open(os.path.join(model_path, 'user_model.dart'), 'w') as file:
        file.write(get_user_model_content())

    with open(os.path.join(controller_path, 'auth_controller.dart'), 'w') as file:
        file.write(get_auth_controller_content())

    with open(os.path.join(service_path, 'auth_service.dart'), 'w') as file:
        file.write(get_auth_service_content())

    with open(os.path.join(view_path, 'login_view.dart'), 'w') as file:
        file.write(get_login_view_content())

    with open(os.path.join(view_path, 'home_view.dart'), 'w') as file:
        file.write(get_home_view_content())
