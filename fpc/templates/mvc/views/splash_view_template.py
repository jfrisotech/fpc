def get_splash_view_content(preferences: dict = None) -> str:
    """Return splash view content that verifies session from SecureStorageService."""
    is_modular = preferences and preferences.get('folder_structure') == 'Modular (Feature First)'
    state_management = preferences.get('state_management', 'None') if preferences else 'None'
    is_getx = state_management == 'GetX'

    utils_prefix = '../../../shared/utils' if is_modular else '../shared/utils'
    storage_prefix = '../../../shared/storage' if is_modular else '../shared/storage'
    assets_prefix = '../../../shared/assets' if is_modular else '../shared/assets'

    getx_import = "import 'package:get/get.dart';" if is_getx else ""
    navigate_home = "Get.offAllNamed('/home');" if is_getx else "Navigator.pushReplacementNamed(context, '/home');"
    navigate_login = "Get.offAllNamed('/login');" if is_getx else "Navigator.pushReplacementNamed(context, '/login');"

    return f'''import 'package:flutter/material.dart';
{getx_import}
import '{utils_prefix}/responsively.dart';
import '{storage_prefix}/secure_storage_service.dart';
import '{assets_prefix}/app_assets.dart';

class SplashView extends StatefulWidget {{
  const SplashView({{super.key}});

  @override
  State<SplashView> createState() => _SplashViewState();
}}

class _SplashViewState extends State<SplashView> {{
  final SecureStorageService _storage = SecureStorageService();

  @override
  void initState() {{
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _checkSession());
  }}

  Future<void> _checkSession() async {{
    // Simulated smooth splash delay
    await Future.delayed(const Duration(milliseconds: 600));
    if (!mounted) return;

    final token = await _storage.getToken();

    if (!mounted) return;
    if (token != null && token.isNotEmpty) {{
      {navigate_home}
    }} else {{
      {navigate_login}
    }}
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Semantics(
                label: 'Application brand logo',
                image: true,
                child: ExcludeSemantics(
                  child: Icon(
                    Icons.flutter_dash,
                    size: context.resp(72),
                    color: Theme.of(context).primaryColor,
                  ),
                ),
              ),
              SizedBox(height: context.resp(24)),
              Semantics(
                label: 'Application loading indicator',
                child: CircularProgressIndicator(
                  key: const Key('splash_loading_indicator'),
                  strokeWidth: context.resp(3),
                ),
              ),
              SizedBox(height: context.resp(16)),
              Text(
                'Checking session...',
                key: const Key('splash_title_text'),
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: Theme.of(context).hintColor,
                    ),
              ),
            ],
          ),
        ),
      ),
    );
  }}
}}
'''

