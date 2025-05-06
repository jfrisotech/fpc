import os

def create_clean_architecture_presentation(lib_path: str):
    """Create presentation layer template files for Clean Architecture."""
    presentation_path = os.path.join(lib_path, 'presentation')
    os.makedirs(presentation_path, exist_ok=True)

    views_path = os.path.join(presentation_path, 'views')
    viewmodels_path = os.path.join(presentation_path, 'viewmodels')
    os.makedirs(views_path, exist_ok=True)
    os.makedirs(viewmodels_path, exist_ok=True)

    with open(os.path.join(viewmodels_path, 'auth_viewmodel.dart'), 'w') as file:
        file.write('''
import 'package:flutter/foundation.dart';
import '../../domain/entities/user.dart';
import '../../domain/usecases/auth_usecases.dart';

class AuthViewModel extends ChangeNotifier {
  final AuthUseCases authUseCases;

  User? _user;
  bool _isLoading = false;
  String? _errorMessage;

  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  AuthViewModel(this.authUseCases);

  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final success = await authUseCases.login(email, password);
      _isLoading = false;
      notifyListeners();
      return success;
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
      final success = await authUseCases.register(name, email, password);
      _isLoading = false;
      notifyListeners();
      return success;
    } catch (e) {
      _isLoading = false;
      _errorMessage = e.toString();
      notifyListeners();
      return false;
    }
  }
}
''')

    with open(os.path.join(views_path, 'login_view.dart'), 'w') as file:
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
      create: (_) => AuthViewModel(
        // You should provide AuthUseCases instance here
        throw UnimplementedError('Provide AuthUseCases instance'),
      ),
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
                    child: const Text('Create an account')
                  )
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
