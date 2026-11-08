def get_clean_home_page_content(preferences: dict = None) -> str:
    """Return HomePage content for Clean Architecture."""
    is_modular = preferences and preferences.get('folder_structure') == 'Modular (Feature First)'
    state_management = preferences.get('state_management', 'None') if preferences else 'None'
    is_getx = state_management == 'GetX'

    utils_prefix = '../../../../shared/utils' if is_modular else '../../shared/utils'
    storage_prefix = '../../../../shared/storage' if is_modular else '../../shared/storage'

    getx_import = "import 'package:get/get.dart';" if is_getx else ""
    navigate_login = "Get.offAllNamed('/login');" if is_getx else "Navigator.pushReplacementNamed(context, '/login');"

    return f'''import 'package:flutter/material.dart';
{getx_import}
import '{utils_prefix}/responsively.dart';
import '{storage_prefix}/secure_storage_service.dart';

class HomePage extends StatelessWidget {{
  const HomePage({{super.key}});

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
                final storage = SecureStorageService();
                await storage.deleteToken();
                if (context.mounted) {{
                  {navigate_login}
                }}
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
              padding: EdgeInsets.all(ctx.resp(24)),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ExcludeSemantics(
                    child: Icon(Icons.home_outlined, size: ctx.resp(64), color: Theme.of(ctx).primaryColor),
                  ),
                  SizedBox(width: ctx.resp(24)),
                  Text(
                    'Welcome to your app!',
                    key: const Key('home_welcome_text'),
                    style: Theme.of(ctx).textTheme.headlineSmall,
                    textAlign: TextAlign.left,
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

