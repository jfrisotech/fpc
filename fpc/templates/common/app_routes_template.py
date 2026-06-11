def get_app_routes_content(preferences: dict = None) -> str:
    is_clean = False
    is_modular = False
    state_management = 'None'
    
    if preferences:
        is_clean = preferences.get('architecture') == 'Clean Architecture'
        is_modular = preferences.get('folder_structure') == 'Modular (Feature First)'
        state_management = preferences.get('state_management', 'None')

    is_getx = state_management == 'GetX'

    # Route paths
    if is_modular:
        if is_clean:
            auth_relative_path = "../modules/auth/presentation/pages"
            home_relative_path = "../modules/home/presentation/pages" # Future-proofing
            auth_binding_relative_path = "../modules/auth/presentation/bindings/auth"
        else:
            auth_relative_path = "../modules/auth/views"
            home_relative_path = "../modules/home/views"
            auth_binding_relative_path = "../modules/auth/bindings"
    else:
        if is_clean:
            auth_relative_path = "../presentation/pages"
            home_relative_path = "../presentation/pages"
            auth_binding_relative_path = "../presentation/bindings/auth"
        else:
            auth_relative_path = "../views"
            home_relative_path = "../views"
            auth_binding_relative_path = "../bindings"

    # View names
    if is_clean:
        login_view_name = "LoginPage"
    else:
        login_view_name = "LoginView"
        
    # We only have HomeView in MVC/MVVM templates for now
    has_home = not is_clean
    
    home_import = f"import '{home_relative_path}/home_view.dart';" if has_home else ""
    home_route = f"'/home': (context) => const HomeView()," if has_home else ""
    
    login_file_name = "login_page.dart" if is_clean else "login_view.dart"
    login_import = f"import '{auth_relative_path}/{login_file_name}';"

    if is_getx:
        binding_import = f"import 'package:get/get.dart';\nimport '{auth_binding_relative_path}/auth_binding.dart';"
        home_page = "\n    GetPage(name: '/home', page: () => const HomeView())," if has_home else ""
        
        return f'''import 'package:flutter/material.dart';
{binding_import}
{home_import}
{login_import}

class AppRoutes {{
  static const String initialRoute = '/login';
  
  static final List<GetPage> pages = [
    GetPage(
      name: '/login',
      page: () => const {login_view_name}(),
      binding: AuthBinding(),
    ),{home_page}
  ];
  
  static final Map<String, WidgetBuilder> routes = {{
    '/login': (context) => const {login_view_name}(),
    {home_route}
  }};
}}
'''
    else:
        return f'''import 'package:flutter/material.dart';
{home_import}
{login_import}

class AppRoutes {{
  static const String initialRoute = '/login';
  
  static final Map<String, WidgetBuilder> routes = {{
    '/login': (context) => const {login_view_name}(),
    {home_route}
  }};
}}
'''
