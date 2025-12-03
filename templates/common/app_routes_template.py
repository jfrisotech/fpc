def get_app_routes_content() -> str:
    return '''
import 'package:flutter/material.dart';
import '../views/home_view.dart';
import '../views/login_view.dart';

class AppRoutes {
  static const String initialRoute = '/login';
  
  static final Map<String, WidgetBuilder> routes = {
    '/login': (context) => const LoginView(),
    '/home': (context) => HomeView(),
  };
}
'''
