import os

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

    with open(os.path.join(controller_path, 'auth_controller.dart'), 'w') as file:
        file.write('''
import '../models/user_model.dart';
import '../services/auth_service.dart';

class AuthController {
  final AuthService _authService = AuthService();
  
  Future<UserModel?> login(String email, String password) async {
    try {
      return await _authService.login(email, password);
    } catch (e) {
      print('Login error: $e');
      return null;
    }
  }
  
  Future<bool> register(String name, String email, String password) async {
    try {
      return await _authService.register(name, email, password);
    } catch (e) {
      print('Registration error: $e');
      return false;
    }
  }
  
  Future<void> logout() async {
    try {
      await _authService.logout();
    } catch (e) {
      print('Logout error: $e');
    }
  }
}
''')

    with open(os.path.join(service_path, 'auth_service.dart'), 'w') as file:
        file.write('''
import '../models/user_model.dart';

class AuthService {
  Future<UserModel> login(String email, String password) async {
    await Future.delayed(Duration(seconds: 1));
    return UserModel(
      id: '1',
      name: 'Test User',
      email: email,
    );
  }
  
  Future<bool> register(String name, String email, String password) async {
    await Future.delayed(Duration(seconds: 1));
    return true;
  }
  
  Future<void> logout() async {
    await Future.delayed(Duration(milliseconds: 500));
  }
}
''')

    with open(os.path.join(view_path, 'login_view.dart'), 'w') as file:
        file.write('''
import 'package:flutter/material.dart';
import '../controllers/auth_controller.dart';

class LoginView extends StatefulWidget {
  const LoginView({super.key});

  @override
  State<LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final AuthController _authController = AuthController();
  bool _isLoading = false;

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
      });

      final user = await _authController.login(
        _emailController.text.trim(),
        _passwordController.text.trim(),
      );

      setState(() {
        _isLoading = false;
      });

      if (user != null && mounted) {
        Navigator.pushReplacementNamed(context, '/home');
      } else if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Login failed. Please try again.')),
        );
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

    with open(os.path.join(view_path, 'home_view.dart'), 'w') as file:
        file.write('''
import 'package:flutter/material.dart';
import '../controllers/auth_controller.dart';

class HomeView extends StatelessWidget {
  HomeView({super.key});

  final AuthController _authController = AuthController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await _authController.logout();
              if (context.mounted) {
                Navigator.pushReplacementNamed(context, '/login');
              }
            },
          ),
        ],
      ),
      body: const Center(
        child: Text('Welcome to your app!'),
      ),
    );
  }
}
''')
