import os
from templates.mvvm.models.user_model_template import get_user_model_content
from templates.mvvm.viewmodels.auth_viewmodel_template import get_auth_viewmodel_content
from templates.mvvm.views.login_view_template import get_login_view_content
from templates.mvvm.views.home_view_template import get_home_view_content

def create_mvvm_templates(lib_path: str, preferences: dict):
    """Create template files for MVVM architecture."""
    model_path = os.path.join(lib_path, 'models')
    viewmodel_path = os.path.join(lib_path, 'viewmodels')
    view_path = os.path.join(lib_path, 'views')
    service_path = os.path.join(lib_path, 'services')
    
    os.makedirs(model_path, exist_ok=True)
    os.makedirs(viewmodel_path, exist_ok=True)
    os.makedirs(view_path, exist_ok=True)
    os.makedirs(service_path, exist_ok=True)
    
    with open(os.path.join(model_path, 'user_model.dart'), 'w') as file:
        file.write(get_user_model_content(preferences))

    with open(os.path.join(viewmodel_path, 'auth_viewmodel.dart'), 'w') as file:
        file.write(get_auth_viewmodel_content(preferences))

    with open(os.path.join(service_path, 'auth_service.dart'), 'w') as file:
        # Reusing the MVC auth service since it is a pure dart class
        from templates.mvc.services.auth_service_template import get_auth_service_content
        file.write(get_auth_service_content())

    with open(os.path.join(view_path, 'login_view.dart'), 'w') as file:
        file.write(get_login_view_content(preferences))

    with open(os.path.join(view_path, 'home_view.dart'), 'w') as file:
        file.write(get_home_view_content(preferences))
