def get_home_view_content(preferences: dict = None) -> str:
    utils_prefix = '../../../shared/utils' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../shared/utils'

    return f'''import 'package:flutter/material.dart';
import '{utils_prefix}/responsively.dart';

class HomeView extends StatelessWidget {{
  const HomeView({{super.key}});

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
                // TODO: Call your AuthController/AuthService logout method here
                // Example (GetIt): sl<AuthController>().logout();
                Navigator.pushReplacementNamed(context, '/login');
              }},
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: OrientationLayout(
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
