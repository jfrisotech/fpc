def get_login_view_content(preferences: dict) -> str:
    utils_prefix = '../../../shared/utils' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../shared/utils'

    if preferences.get('state_management', 'None') == 'Provider':
        return f'''import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../viewmodels/auth_viewmodel.dart';
import '{utils_prefix}/responsively.dart';

class LoginView extends StatefulWidget {{
  const LoginView({{super.key}});

  @override
  State<LoginView> createState() => _LoginViewState();
}}

class _LoginViewState extends State<LoginView> {{
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {{
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }}

  Widget _buildForm(BuildContext context, AuthViewModel viewModel) {{
    return Form(
      key: _formKey,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Semantics(
            label: 'Email input field',
            hint: 'Enter your email address',
            textField: true,
            child: TextFormField(
              key: const Key('login_email_input'),
              controller: _emailController,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
                prefixIcon: ExcludeSemantics(child: Icon(Icons.email_outlined)),
              ),
              keyboardType: TextInputType.emailAddress,
              validator: (value) =>
                  (value == null || value.isEmpty) ? 'Please enter your email' : null,
            ),
          ),
          SizedBox(height: context.resp(16)),
          Semantics(
            label: 'Password input field',
            hint: 'Enter your password',
            textField: true,
            child: TextFormField(
              key: const Key('login_password_input'),
              controller: _passwordController,
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
                prefixIcon: ExcludeSemantics(child: Icon(Icons.lock_outlined)),
              ),
              obscureText: true,
              validator: (value) =>
                  (value == null || value.isEmpty) ? 'Please enter your password' : null,
            ),
          ),
          SizedBox(height: context.resp(24)),
          Semantics(
            button: true,
            label: viewModel.isLoading ? 'Authenticating, please wait' : 'Login button',
            child: ElevatedButton(
              key: const Key('login_submit_button'),
              onPressed: viewModel.isLoading
                  ? null
                  : () async {{
                      if (_formKey.currentState!.validate()) {{
                        final navigator = Navigator.of(context);
                        final success = await viewModel.login(
                          _emailController.text.trim(),
                          _passwordController.text.trim(),
                        );
                        if (success) {{
                          navigator.pushReplacementNamed('/home');
                        }}
                      }}
                    }},
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(vertical: context.resp(12)),
              ),
              child: viewModel.isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        key: Key('login_loading_indicator'),
                        strokeWidth: 2,
                      ),
                    )
                  : const Text('Login'),
            ),
          ),
        ],
      ),
    );
  }}

  Widget _buildHeader(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ExcludeSemantics(
          child: Icon(Icons.person_pin_outlined, size: context.resp(64), color: Theme.of(context).primaryColor),
        ),
        SizedBox(height: context.resp(12)),
        Text(
          'Welcome Back',
          key: const Key('login_title_text'),
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }}

  @override
  Widget build(BuildContext context) {{
    return ChangeNotifierProvider(
      create: (_) => AuthViewModel(),
      child: Builder(
        builder: (context) {{
          final viewModel = Provider.of<AuthViewModel>(context);

          return Scaffold(
            appBar: AppBar(title: const Text('Login')),
            body: SafeArea(
              child: OrientationLayout(
                portrait: (ctx) => Center(
                  child: SingleChildScrollView(
                    padding: EdgeInsets.all(ctx.resp(24)),
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 420),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          _buildHeader(ctx),
                          SizedBox(height: ctx.resp(32)),
                          _buildForm(ctx, viewModel),
                        ],
                      ),
                    ),
                  ),
                ),
                landscape: (ctx) => Center(
                  child: SingleChildScrollView(
                    padding: EdgeInsets.symmetric(
                      horizontal: ctx.respW(32),
                      vertical: ctx.respH(16),
                    ),
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 820),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Expanded(child: _buildHeader(ctx)),
                          SizedBox(width: ctx.respW(32)),
                          Expanded(child: _buildForm(ctx, viewModel)),
                        ],
                      ),
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

class LoginView extends StatefulWidget {{
  const LoginView({{super.key}});

  @override
  State<LoginView> createState() => _LoginViewState();
}}

class _LoginViewState extends State<LoginView> {{
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _viewModel = AuthViewModel();

  @override
  void dispose() {{
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }}

  Widget _buildForm(BuildContext context) {{
    return Form(
      key: _formKey,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Semantics(
            label: 'Email input field',
            hint: 'Enter your email address',
            textField: true,
            child: TextFormField(
              key: const Key('login_email_input'),
              controller: _emailController,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
                prefixIcon: ExcludeSemantics(child: Icon(Icons.email_outlined)),
              ),
              keyboardType: TextInputType.emailAddress,
              validator: (value) =>
                  (value == null || value.isEmpty) ? 'Please enter your email' : null,
            ),
          ),
          SizedBox(height: context.resp(16)),
          Semantics(
            label: 'Password input field',
            hint: 'Enter your password',
            textField: true,
            child: TextFormField(
              key: const Key('login_password_input'),
              controller: _passwordController,
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
                prefixIcon: ExcludeSemantics(child: Icon(Icons.lock_outlined)),
              ),
              obscureText: true,
              validator: (value) =>
                  (value == null || value.isEmpty) ? 'Please enter your password' : null,
            ),
          ),
          SizedBox(height: context.resp(24)),
          Semantics(
            button: true,
            label: _viewModel.isLoading ? 'Authenticating, please wait' : 'Login button',
            child: ElevatedButton(
              key: const Key('login_submit_button'),
              onPressed: _viewModel.isLoading
                  ? null
                  : () async {{
                      if (_formKey.currentState!.validate()) {{
                        final navigator = Navigator.of(context);
                        final success = await _viewModel.login(
                          _emailController.text.trim(),
                          _passwordController.text.trim(),
                        );
                        if (success) {{
                          navigator.pushReplacementNamed('/home');
                        }}
                      }}
                    }},
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(vertical: context.resp(12)),
              ),
              child: _viewModel.isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        key: Key('login_loading_indicator'),
                        strokeWidth: 2,
                      ),
                    )
                  : const Text('Login'),
            ),
          ),
        ],
      ),
    );
  }}

  Widget _buildHeader(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ExcludeSemantics(
          child: Icon(Icons.person_pin_outlined, size: context.resp(64), color: Theme.of(context).primaryColor),
        ),
        SizedBox(height: context.resp(12)),
        Text(
          'Welcome Back',
          key: const Key('login_title_text'),
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: SafeArea(
        child: OrientationLayout(
          portrait: (ctx) => Center(
            child: SingleChildScrollView(
              padding: EdgeInsets.all(ctx.resp(24)),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 420),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _buildHeader(ctx),
                    SizedBox(height: ctx.resp(32)),
                    _buildForm(ctx),
                  ],
                ),
              ),
            ),
          ),
          landscape: (ctx) => Center(
            child: SingleChildScrollView(
              padding: EdgeInsets.symmetric(
                horizontal: ctx.respW(32),
                vertical: ctx.respH(16),
              ),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 820),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Expanded(child: _buildHeader(ctx)),
                    SizedBox(width: ctx.respW(32)),
                    Expanded(child: _buildForm(ctx)),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }}
}}
'''
