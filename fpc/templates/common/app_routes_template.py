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
            home_relative_path = "../modules/home/presentation/pages"
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

    # View & file names
    splash_view_name = "SplashPage" if is_clean else "SplashView"
    login_view_name = "LoginPage" if is_clean else "LoginView"
    home_view_name = "HomePage" if is_clean else "HomeView"

    splash_file_name = "splash_page.dart" if is_clean else "splash_view.dart"
    login_file_name = "login_page.dart" if is_clean else "login_view.dart"
    home_file_name = "home_page.dart" if is_clean else "home_view.dart"

    splash_import = f"import '{auth_relative_path}/{splash_file_name}';"
    login_import = f"import '{auth_relative_path}/{login_file_name}';"
    home_import = f"import '{home_relative_path}/{home_file_name}';"

    if is_getx:
        binding_import = f"import 'package:get/get.dart';\nimport '{auth_binding_relative_path}/auth_binding.dart';"
        
        return f'''import 'package:flutter/material.dart';
{binding_import}
{splash_import}
{login_import}
{home_import}

class AppRoutes {{
  static const String initialRoute = '/splash';
  
  static final List<GetPage> pages = [
    GetPage(
      name: '/splash',
      page: () => const {splash_view_name}(),
    ),
    GetPage(
      name: '/login',
      page: () => const {login_view_name}(),
      binding: AuthBinding(),
    ),
    GetPage(
      name: '/home',
      page: () => const {home_view_name}(),
    ),
  ];
  
  static final Map<String, WidgetBuilder> routes = {{
    '/splash': (context) => const {splash_view_name}(),
    '/login': (context) => const {login_view_name}(),
    '/home': (context) => const {home_view_name}(),
  }};
}}
'''
    else:
        return f'''import 'package:flutter/material.dart';
{splash_import}
{login_import}
{home_import}

class AppRoutes {{
  static const String initialRoute = '/splash';
  
  static final Map<String, WidgetBuilder> routes = {{
    '/splash': (context) => const {splash_view_name}(),
    '/login': (context) => const {login_view_name}(),
    '/home': (context) => const {home_view_name}(),
  }};
}}
'''
