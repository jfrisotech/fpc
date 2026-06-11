import os
from fpc.templates.mvc.models.user_model_template import get_user_model_content
from fpc.templates.mvc.controllers.auth_controller_template import get_auth_controller_content
from fpc.templates.mvc.services.auth_service_template import get_auth_service_content
from fpc.templates.mvc.views.login_view_template import get_login_view_content
from fpc.templates.mvc.views.home_view_template import get_home_view_content

def create_mvc_templates(auth_path: str, home_path: str, preferences: dict):
    """Create template files for MVC architecture."""
    # Auth module files
    model_path = os.path.join(auth_path, 'models')
    controller_path = os.path.join(auth_path, 'controllers')
    service_path = os.path.join(auth_path, 'services')
    auth_view_path = os.path.join(auth_path, 'views')
    
    os.makedirs(model_path, exist_ok=True)
    os.makedirs(controller_path, exist_ok=True)
    os.makedirs(service_path, exist_ok=True)
    os.makedirs(auth_view_path, exist_ok=True)
    
    with open(os.path.join(model_path, 'user_model.dart'), 'w') as file:
        file.write(get_user_model_content(preferences))

    with open(os.path.join(controller_path, 'auth_controller.dart'), 'w') as file:
        file.write(get_auth_controller_content())

    with open(os.path.join(service_path, 'auth_service.dart'), 'w') as file:
        file.write(get_auth_service_content())

    with open(os.path.join(auth_view_path, 'login_view.dart'), 'w') as file:
        file.write(get_login_view_content())

    state_management = preferences.get('state_management', 'None')
    if state_management == 'GetX':
        binding_path = os.path.join(auth_path, 'bindings')
        os.makedirs(binding_path, exist_ok=True)
        with open(os.path.join(binding_path, 'auth_binding.dart'), 'w') as file:
            file.write("""import 'package:get/get.dart';
import '../controllers/auth_controller.dart';
import '../services/auth_service.dart';

class AuthBinding extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut<AuthService>(() => AuthService());
    Get.lazyPut<AuthController>(() => AuthController());
  }
}
""")

    # Home module files
    home_view_path = os.path.join(home_path, 'views')
    os.makedirs(home_view_path, exist_ok=True)
    
    with open(os.path.join(home_view_path, 'home_view.dart'), 'w') as file:
        file.write(get_home_view_content())
