import os
from core.utils import print_color, Colors

def create_template_files(project_path: str, preferences: dict):
    """Create template files based on project preferences."""
    print_color("Creating template files...", Colors.BLUE)
    
    lib_path = os.path.join(project_path, 'lib')
    
    # Create main.dart
    _create_main_file(lib_path, preferences)
    
    # Create app configuration files
    _create_app_config_files(lib_path, preferences)
    
    # Create architecture-specific files
    architecture = preferences['architecture']
    if architecture == 'MVC (Model-View-Controller)':
        _create_mvc_template_files(lib_path, preferences)
    elif architecture == 'MVVM (Model-View-ViewModel)':
        _create_mvvm_template_files(lib_path, preferences)
    elif architecture == 'Clean Architecture':
        _create_clean_architecture_template_files(lib_path, preferences)
    
    print_color("Template files created successfully!", Colors.GREEN)

def _create_main_file(lib_path: str, preferences: dict):
    """Create main.dart file."""
    main_content = _get_main_file_content(preferences)
    # Ensure lib_path exists
    os.makedirs(lib_path, exist_ok=True)
    with open(os.path.join(lib_path, 'main.dart'), 'w') as file:
        file.write(main_content)

def _get_main_file_content(preferences: dict) -> str:
    """Generate content for main.dart based on preferences."""
    setup_code = ''
    app_initialization_code = ''
    
    # BaaS setup code
    baas = preferences['baas']
    if baas == 'Firebase':
        setup_code += '''
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

Future<void> setupServices() async {
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
}
'''
        app_initialization_code = 'await setupServices();'
    elif baas == 'Supabase':
        setup_code += '''
import 'package:supabase_flutter/supabase_flutter.dart';
import 'config/app_config.dart';

Future<void> setupServices() async {
  await Supabase.initialize(
    url: AppConfig.supabaseUrl,
    anonKey: AppConfig.supabaseAnonKey,
  );
}
'''
        app_initialization_code = 'await setupServices();'
    elif baas == 'Appwrite':
        setup_code += '''
import 'package:appwrite/appwrite.dart';
import 'config/app_config.dart';

late Client appwriteClient;

Future<void> setupServices() async {
  appwriteClient = Client()
    .setEndpoint(AppConfig.appwriteEndpoint)
    .setProject(AppConfig.appwriteProjectId)
    .setSelfSigned(status: true);
}
'''
        app_initialization_code = 'await setupServices();'
    else:
        setup_code = '''
Future<void> setupServices() async {
  // Initialize your services here
}
'''
        app_initialization_code = '// await setupServices();'
    
    # State management setup
    state_management_setup = ''
    app_wrapper = 'MyApp()'
    
    state_management = preferences['state_management']
    if state_management == 'Provider':
        state_management_setup = '''
import 'package:provider/provider.dart';
'''
        app_wrapper = '''
MultiProvider(
      providers: [
        // Register your providers here
        // ChangeNotifierProvider(create: (_) => YourViewModel()),
      ],
      child: MyApp(),
    )'''
    elif state_management == 'BLoC':
        state_management_setup = '''
import 'package:flutter_bloc/flutter_bloc.dart';
'''
        app_wrapper = '''
MultiBlocProvider(
      providers: [
        // Register your blocs here
        // BlocProvider(create: (_) => YourBloc()),
      ],
      child: MyApp(),
    )'''
    elif state_management == 'GetX':
        state_management_setup = '''
import 'package:get/get.dart';
'''
        app_wrapper = 'GetMaterialApp(home: HomePage())'
    elif state_management == 'Riverpod':
        state_management_setup = '''
import 'package:flutter_riverpod/flutter_riverpod.dart';
'''
        app_wrapper = 'ProviderScope(child: MyApp())'
    elif state_management == 'MobX':
        state_management_setup = '''
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:provider/provider.dart';
'''
        app_wrapper = '''
MultiProvider(
      providers: [
        // Register your stores here
        // Provider<YourStore>(create: (_) => YourStore()),
      ],
      child: MyApp(),
    )'''
    
    # Main file content
    return f'''
import 'package:flutter/material.dart';
{state_management_setup}
import 'config/app_routes.dart';
import 'config/app_theme.dart';
{setup_code}

void main() async {{
  WidgetsFlutterBinding.ensureInitialized();
  {app_initialization_code}
  runApp({app_wrapper});
}}

class MyApp extends StatelessWidget {{
  const MyApp({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: 'Flutter App',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      routes: AppRoutes.routes,
      initialRoute: AppRoutes.initialRoute,
    );
  }}
}}
'''

import os

def _create_app_config_files(lib_path: str, preferences: dict):
    """Create app configuration files."""
    config_path = os.path.join(lib_path, 'config')
    # Separate folder creation
    os.makedirs(config_path, exist_ok=True)
    
    # File creations
    # Create app_routes.dart
    with open(os.path.join(config_path, 'app_routes.dart'), 'w') as file:
        file.write('''
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
''')
    
    # Create app_theme.dart
    with open(os.path.join(config_path, 'app_theme.dart'), 'w') as file:
        file.write('''
import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      primarySwatch: Colors.blue,
      brightness: Brightness.light,
      useMaterial3: true,
      visualDensity: VisualDensity.adaptivePlatformDensity,
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      primarySwatch: Colors.blue,
      brightness: Brightness.dark,
      useMaterial3: true,
      visualDensity: VisualDensity.adaptivePlatformDensity,
    );
  }
}
''')
    
    # Create app_config.dart for BaaS configuration
    baas = preferences['baas']
    if baas != 'None':
        with open(os.path.join(config_path, 'app_config.dart'), 'w') as file:
            config_content = '''
class AppConfig {
'''
            if baas == 'Firebase':
                config_content += '''
  // Firebase configuration is handled by firebase_options.dart
'''
            elif baas == 'Supabase':
                config_content += '''
  static const String supabaseUrl = 'YOUR_SUPABASE_URL';
  static const String supabaseAnonKey = 'YOUR_SUPABASE_ANON_KEY';
'''
            elif baas == 'Appwrite':
                config_content += '''
  static const String appwriteEndpoint = 'YOUR_APPWRITE_ENDPOINT';
  static const String appwriteProjectId = 'YOUR_APPWRITE_PROJECT_ID';
'''
            
            config_content += '''
  // Add more app configuration here
}
'''
            file.write(config_content)

from templates.mvc.mvc_templates import create_mvc_templates

def _create_mvc_template_files(lib_path: str, preferences: dict):
    """Create template files for MVC architecture."""
    create_mvc_templates(lib_path)

from templates.mvvm.mvvm_templates import create_mvvm_templates

def _create_mvvm_template_files(lib_path: str, preferences: dict):
    """Create template files for MVVM architecture."""
    create_mvvm_templates(lib_path)

from templates.clean_arch.clean_architecture_data import create_clean_architecture_data
from templates.clean_arch.clean_architecture_domain import create_clean_architecture_domain
from templates.clean_arch.clean_architecture_presentation import create_clean_architecture_presentation

def _create_clean_architecture_template_files(lib_path: str, preferences: dict):
    """Create template files for Clean Architecture."""
    create_clean_architecture_data(lib_path)
    create_clean_architecture_domain(lib_path)
    create_clean_architecture_presentation(lib_path)



