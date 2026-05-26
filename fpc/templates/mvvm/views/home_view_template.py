def get_home_view_content(preferences: dict) -> str:
    if preferences.get('state_management', 'None') == 'Provider':
        return '''
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
                  final navigator = Navigator.of(context);
                  await viewModel.logout();
                  navigator.pushReplacementNamed('/login');
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
'''
    else:
        return '''
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
                    final navigator = Navigator.of(context);
                    
                    setState(() {
                      _isLoading = true;
                    });
                    
                    await _authViewModel.logout();
                    
                    navigator.pushReplacementNamed('/login');
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
'''
