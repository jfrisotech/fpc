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

def _create_mvvm_template_files(lib_path: str, preferences: dict):
    """Create template files for MVVM architecture."""
    # Separate folder creation
    model_path = os.path.join(lib_path, 'models')
    viewmodel_path = os.path.join(lib_path, 'viewmodels')
    view_path = os.path.join(lib_path, 'views')
    
    os.makedirs(model_path, exist_ok=True)
    os.makedirs(viewmodel_path, exist_ok=True)
    os.makedirs(view_path, exist_ok=True)
    
    # File creations
    with open(os.path.join(model_path, 'user_model.dart'), 'w') as file:
        file.write('''
class UserModel {
  final String id;
  final String name;
  final String email;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
    };
  }
}
''')

    with open(os.path.join(viewmodel_path, 'auth_viewmodel.dart'), 'w') as file:
        if preferences['state_management'] == 'Provider':
            file.write('''
import 'package:flutter/foundation.dart';
import '../models/user_model.dart';
import '../services/auth_service.dart';

class AuthViewModel extends ChangeNotifier {
  final AuthService _authService = AuthService();
  
  UserModel? _user;
  bool _isLoading = false;
  String? _errorMessage;
  
  UserModel? get user => _user;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  
  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();
    
    try {
      _user = await _authService.login(email, password);
      _isLoading = false;
      notifyListeners();
      return _user != null;
    } catch (e) {
      _isLoading = false;
      _errorMessage = e.toString();
      notifyListeners();
      return false;
    }
  }
  
  Future<bool> register(String name, String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();
    
    try {
      final result = await _authService.register(name, email, password);
      _isLoading = false;
      notifyListeners();
      return result;
    } catch (e) {
      _isLoading = false;
      _errorMessage = e.toString();
      notifyListeners();
      return false;
    }
  }
  
  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();
    
    try {
      await _authService.logout();
      _user = null;
    } catch (e) {
      _errorMessage = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
''')

    if preferences['state_management'] == 'Provider':
        with open(os.path.join(view_path, 'login_view.dart'), 'w') as file:
            file.write('''
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../viewmodels/auth_viewmodel.dart';

class LoginView extends StatefulWidget {
  const LoginView({super.key});

  @override
  State<LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AuthViewModel(),
      child: Builder(builder: (context) {
        final viewModel = Provider.of<AuthViewModel>(context);
        
        return Scaffold(
          appBar: AppBar(
            title: const Text('Login'),
          ),
          body: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  TextFormField(
                    controller: _emailController,
                    decoration: const InputDecoration(
                      labelText: 'Email',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.emailAddress,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your email';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _passwordController,
                    decoration: const InputDecoration(
                      labelText: 'Password',
                      border: OutlineInputBorder(),
                    ),
                    obscureText: true,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your password';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 24),
                  if (viewModel.errorMessage != null)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 16.0),
                      child: Text(
                        viewModel.errorMessage!,
                        style: const TextStyle(color: Colors.red),
                      ),
                    ),
                  ElevatedButton(
                    onPressed: viewModel.isLoading
                        ? null
                        : () async {
                            if (_formKey.currentState!.validate()) {
                              final success = await viewModel.login(
                                _emailController.text.trim(),
                                _passwordController.text.trim(),
                              );
                              
                              if (success && mounted) {
                                Navigator.pushReplacementNamed(context, '/home');
                              }
                            }
                          },
                    child: viewModel.isLoading
                        ? const CircularProgressIndicator()
                        : const Text('Login'),
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: () {
                      // Navigate to registration screen
                    },
                    child: const Text('Create an account'),
                  ),
                ],
              ),
            ),
          ),
        );
      }),
    );
  }
}
''')
    else:
        with open(os.path.join(view_path, 'login_view.dart'), 'w') as file:
            file.write('''
import 'package:flutter/material.dart';
import '../viewmodels/auth_viewmodel.dart';

class LoginView extends StatefulWidget {
  const LoginView({super.key});

  @override
  State<LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _authViewModel = AuthViewModel();
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
        _errorMessage = null;
      });

      final success = await _authViewModel.login(
        _emailController.text.trim(),
        _passwordController.text.trim(),
      );

      if (mounted) {
        setState(() {
          _isLoading = false;
          _errorMessage = _authViewModel.errorMessage;
        });

        if (success) {
          Navigator.pushReplacementNamed(context, '/home');
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your email';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _passwordController,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your password';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              if (_errorMessage != null)
                Padding(
                  padding: const EdgeInsets.only(bottom: 16.0),
                  child: Text(
                    _errorMessage!,
                    style: const TextStyle(color: Colors.red),
                  ),
                ),
              ElevatedButton(
                onPressed: _isLoading ? null : _login,
                child: _isLoading
                    ? const CircularProgressIndicator()
                    : const Text('Login'),
              ),
              const SizedBox(height: 16),
              TextButton(
                onPressed: () {
                  // Navigate to registration screen
                },
                child: const Text('Create an account'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
''')

    home_view_path = os.path.join(view_path, 'home_view.dart')
    os.makedirs(view_path, exist_ok=True)
    with open(home_view_path, 'w') as file:
        if preferences['state_management'] == 'Provider':
            file.write('''
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../viewmodels/auth_viewmodel.dart';

class HomeView extends StatelessWidget {
  const HomeView({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AuthViewModel(),
      child: Builder(builder: (context) {
        final viewModel = Provider.of<AuthViewModel>(context);
        
        return Scaffold(
          appBar: AppBar(
            title: const Text('Home'),
            actions: [
              IconButton(
                icon: const Icon(Icons.logout),
                onPressed: () async {
                  await viewModel.logout();
                  if (context.mounted) {
                    Navigator.pushReplacementNamed(context, '/login');
                  }
                },
              ),
            ],
          ),
          body: viewModel.isLoading
              ? const Center(child: CircularProgressIndicator())
              : const Center(
                  child: Text('Welcome to your app!'),
                ),
        );
      }),
    );
  }
}
''')
        else:
            file.write('''
import 'package:flutter/material.dart';
import '../viewmodels/auth_viewmodel.dart';

class HomeView extends StatefulWidget {
  const HomeView({super.key});

  @override
  State<HomeView> createState() => _HomeViewState();
}

class _HomeViewState extends State<HomeView> {
  final _authViewModel = AuthViewModel();
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _isLoading
                ? null
                : () async {
                    setState(() {
                      _isLoading = true;
                    });
                    
                    await _authViewModel.logout();
                    
                    if (mounted) {
                      Navigator.pushReplacementNamed(context, '/login');
                    }
                  },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : const Center(
              child: Text('Welcome to your app!'),
            ),
    );
  }
}
''')

from templates.clean_arch.clean_architecture_data import create_clean_architecture_data
from templates.clean_arch.clean_architecture_domain import create_clean_architecture_domain
from templates.clean_arch.clean_architecture_presentation import create_clean_architecture_presentation

def _create_clean_architecture_template_files(lib_path: str, preferences: dict):
    """Create template files for Clean Architecture."""
    create_clean_architecture_data(lib_path)
    create_clean_architecture_domain(lib_path)
    create_clean_architecture_presentation(lib_path)



