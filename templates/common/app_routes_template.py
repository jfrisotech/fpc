def get_app_routes_content(preferences: dict = None) -> str:
    is_clean = False
    is_modular = False
    
    if preferences:
        is_clean = preferences.get('architecture') == 'Clean Architecture'
        is_modular = preferences.get('folder_structure') == 'Modular (Feature First)'

    # Route prefix
    if is_modular:
        if is_clean:
            relative_path = "../modules/auth/presentation/pages"
        else:
            relative_path = "../modules/auth/views"
    else:
        if is_clean:
            relative_path = "../presentation/pages"
        else:
            relative_path = "../views"

    # View names
    if is_clean:
        login_view_name = "LoginPage"
    else:
        login_view_name = "LoginView"
        
    # We only have HomeView in MVC/MVVM templates for now
    has_home = not is_clean
    
    home_import = f"import '{relative_path}/home_view.dart';" if has_home else ""
    home_route = f"'/home': (context) => const HomeView()," if has_home else ""

    login_file_name = "login_page.dart" if is_clean else "login_view.dart"

    return f'''import 'package:flutter/material.dart';
{home_import}
import '{relative_path}/{login_file_name}';

class AppRoutes {{
  static const String initialRoute = '/login';
  
  static final Map<String, WidgetBuilder> routes = {{
    '/login': (context) => const {login_view_name}(),
    {home_route}
  }};
}}
'''
