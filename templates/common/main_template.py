def get_main_file_content(preferences: dict) -> str:
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
    
    # State management setup and app wrappers
    state_management_setup = ''
    app_wrapper = 'AppWidget()'
    
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
      child: const AppWidget(),
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
      child: const AppWidget(),
    )'''
    elif state_management == 'GetX':
        state_management_setup = '''
import 'package:get/get.dart';
'''
        app_wrapper = 'const AppWidget()'
    elif state_management == 'Riverpod':
        state_management_setup = '''
import 'package:flutter_riverpod/flutter_riverpod.dart';
'''
        app_wrapper = 'ProviderScope(child: const AppWidget())'
    elif state_management == 'MobX':
        state_management_setup = '''
import 'package:flutter_mobx/flutter_mobx.dart';
'''
        app_wrapper = 'const AppWidget()'
    
    # Main file content
    main_content = f'''
import 'package:flutter/material.dart';
{state_management_setup}
import 'app/app_widget.dart';
{setup_code}

void main() async {{
  WidgetsFlutterBinding.ensureInitialized();
  {app_initialization_code}
  runApp({app_wrapper});
}}
'''

    # App widget content
    material_app = '''
    return MaterialApp(
      title: 'Flutter App',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      routes: AppRoutes.routes,
      initialRoute: AppRoutes.initialRoute,
    );
'''
    if state_management == 'GetX':
        material_app = '''
    return GetMaterialApp(
      title: 'Flutter App',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      initialRoute: AppRoutes.initialRoute,
      // Use GetPages or fallback to routes
      routes: AppRoutes.routes,
    );
'''

    getx_import = "import 'package:get/get.dart';" if state_management == 'GetX' else ""
    app_widget_content = f'''
import 'package:flutter/material.dart';
{getx_import}
import 'config/app_routes.dart';
import 'config/app_theme.dart';

class AppWidget extends StatelessWidget {{
  const AppWidget({{super.key}});

  @override
  Widget build(BuildContext context) {{
{material_app}
  }}
}}
'''
    return main_content, app_widget_content
