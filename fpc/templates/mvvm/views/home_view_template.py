def get_home_view_content(preferences: dict) -> str:
    utils_prefix = '../../../shared/utils' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../shared/utils'

    if preferences.get('state_management', 'None') == 'Provider':
        return f'''import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../viewmodels/auth_viewmodel.dart';
import '{utils_prefix}/responsively.dart';

class HomeView extends StatelessWidget {{
  const HomeView({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return ChangeNotifierProvider(
      create: (_) => AuthViewModel(),
      child: Builder(
        builder: (context) {{
          final viewModel = Provider.of<AuthViewModel>(context);

          return Scaffold(
            appBar: AppBar(
              title: const Text('Home'),
              actions: [
                Semantics(
                  button: true,
                  label: 'Logout button',
                  child: IconButton(
                    key: const Key('home_logout_button'),
                    icon: const Icon(Icons.logout),
                    onPressed: () async {{
                      final navigator = Navigator.of(context);
                      await viewModel.logout();
                      navigator.pushReplacementNamed('/login');
                    }},
                  ),
                ),
              ],
            ),
            body: SafeArea(
              child: viewModel.isLoading
                  ? const Center(
                      child: CircularProgressIndicator(
                        key: Key('home_loading_indicator'),
                      ),
                    )
                  : OrientationLayout(
                      portrait: (ctx) => Center(
                        child: SingleChildScrollView(
                          padding: EdgeInsets.all(ctx.resp(24)),
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              ExcludeSemantics(
                                child: Icon(Icons.home_outlined, size: ctx.resp(64), color: Theme.of(ctx).primaryColor),
                              ),
                              SizedBox(height: ctx.resp(16)),
                              Text(
                                'Welcome to your app!',
                                key: const Key('home_welcome_text'),
                                style: Theme.of(ctx).textTheme.headlineSmall,
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        ),
                      ),
                      landscape: (ctx) => Center(
                        child: SingleChildScrollView(
                          padding: EdgeInsets.symmetric(
                            horizontal: ctx.respW(32),
                            vertical: ctx.respH(16),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              ExcludeSemantics(
                                child: Icon(Icons.home_outlined, size: ctx.resp(64), color: Theme.of(ctx).primaryColor),
                              ),
                              SizedBox(width: ctx.respW(24)),
                              Text(
                                'Welcome to your app!',
                                key: const Key('home_welcome_text_landscape'),
                                style: Theme.of(ctx).textTheme.headlineSmall,
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
            ),
          );
        }},
      ),
    );
  }}
}}
'''
    else:
        return f'''import 'package:flutter/material.dart';
import '../viewmodels/auth_viewmodel.dart';
import '{utils_prefix}/responsively.dart';

class HomeView extends StatefulWidget {{
  const HomeView({{super.key}});

  @override
  State<HomeView> createState() => _HomeViewState();
}}

class _HomeViewState extends State<HomeView> {{
  final _authViewModel = AuthViewModel();
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        actions: [
          Semantics(
            button: true,
            label: 'Logout button',
            child: IconButton(
              key: const Key('home_logout_button'),
              icon: const Icon(Icons.logout),
              onPressed: () async {{
                setState(() => _isLoading = true);
                await _authViewModel.logout();
                if (mounted) {{
                  setState(() => _isLoading = false);
                  Navigator.pushReplacementNamed(context, '/login');
                }}
              }},
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: _isLoading
            ? const Center(
                child: CircularProgressIndicator(
                  key: Key('home_loading_indicator'),
                ),
              )
            : OrientationLayout(
                portrait: (ctx) => Center(
                  child: SingleChildScrollView(
                    padding: EdgeInsets.all(ctx.resp(24)),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        ExcludeSemantics(
                          child: Icon(Icons.home_outlined, size: ctx.resp(64), color: Theme.of(ctx).primaryColor),
                        ),
                        SizedBox(height: ctx.resp(16)),
                        Text(
                          'Welcome to your app!',
                          key: const Key('home_welcome_text'),
                          style: Theme.of(ctx).textTheme.headlineSmall,
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                ),
                landscape: (ctx) => Center(
                  child: SingleChildScrollView(
                    padding: EdgeInsets.symmetric(
                      horizontal: ctx.respW(32),
                      vertical: ctx.respH(16),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        ExcludeSemantics(
                          child: Icon(Icons.home_outlined, size: ctx.resp(64), color: Theme.of(ctx).primaryColor),
                        ),
                        SizedBox(width: ctx.respW(24)),
                        Text(
                          'Welcome to your app!',
                          key: const Key('home_welcome_text_landscape'),
                          style: Theme.of(ctx).textTheme.headlineSmall,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
      ),
    );
  }}
}}
'''
