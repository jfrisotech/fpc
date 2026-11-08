import os

def create_clean_architecture_presentation(lib_path: str, preferences: dict = None, home_path: str = None):
    """Create presentation layer template files for Clean Architecture."""
    presentation_path = os.path.join(lib_path, 'presentation')
    os.makedirs(presentation_path, exist_ok=True)

    pages_path = os.path.join(presentation_path, 'pages')
    os.makedirs(pages_path, exist_ok=True)
    
    from fpc.templates.clean_arch.presentation.splash_page_template import get_splash_page_content
    with open(os.path.join(pages_path, 'splash_page.dart'), 'w') as file:
        file.write(get_splash_page_content(preferences))

    target_home_pages = os.path.join(home_path, 'presentation', 'pages') if home_path else pages_path
    os.makedirs(target_home_pages, exist_ok=True)
    from fpc.templates.clean_arch.presentation.home_page_template import get_clean_home_page_content
    with open(os.path.join(target_home_pages, 'home_page.dart'), 'w') as file:
        file.write(get_clean_home_page_content(preferences))

    state_management = preferences.get('state_management') if preferences else 'None'
    
    core_prefix = '../../../../../core' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../../../core'
    utils_prefix = '../../../../shared/utils' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../../shared/utils'

    if state_management == 'BLoC':
        _create_bloc_presentation(presentation_path, pages_path, core_prefix, utils_prefix)
    elif state_management == 'Cubit':
        _create_cubit_presentation(presentation_path, pages_path, core_prefix, utils_prefix)
    elif state_management == 'MobX':
        _create_mobx_presentation(presentation_path, pages_path, utils_prefix)
    elif state_management == 'GetX':
        _create_getx_presentation(presentation_path, pages_path, utils_prefix)
    elif state_management == 'Riverpod':
        _create_riverpod_presentation(presentation_path, pages_path, utils_prefix)
    elif state_management == 'Provider':
        _create_provider_presentation(presentation_path, pages_path, utils_prefix)
    else:
        _create_none_presentation(presentation_path, pages_path, utils_prefix)

def _create_bloc_presentation(presentation_path, pages_path, core_prefix, utils_prefix):
    bloc_path = os.path.join(presentation_path, 'bloc', 'auth')
    os.makedirs(bloc_path, exist_ok=True)

    with open(os.path.join(bloc_path, 'auth_event.dart'), 'w') as file:
        file.write("""abstract class AuthEvent {}

class LoginEvent extends AuthEvent {
  final String email;
  final String password;

  LoginEvent({required this.email, required this.password});
}

class RegisterEvent extends AuthEvent {
  final String name;
  final String email;
  final String password;

  RegisterEvent({
    required this.name,
    required this.email,
    required this.password,
  });
}

class LogoutEvent extends AuthEvent {}
""")

    with open(os.path.join(bloc_path, 'auth_state.dart'), 'w') as file:
        file.write("""import '../../../domain/entities/user.dart';

abstract class AuthState {}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class AuthSuccess extends AuthState {
  final User user;

  AuthSuccess(this.user);
}

class AuthRegistered extends AuthState {}

class AuthLoggedOut extends AuthState {}

class AuthFailure extends AuthState {
  final String message;

  AuthFailure(this.message);
}
""")

    with open(os.path.join(bloc_path, 'auth_bloc.dart'), 'w') as file:
        file.write(f"""import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../domain/usecases/login_usecase.dart';
import '../../../domain/usecases/register_usecase.dart';
import '../../../domain/usecases/logout_usecase.dart';
import '{core_prefix}/usecases/usecase.dart';
import 'auth_event.dart';
import 'auth_state.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {{
  final LoginUseCase loginUseCase;
  final RegisterUseCase registerUseCase;
  final LogoutUseCase logoutUseCase;

  AuthBloc({{
    required this.loginUseCase,
    required this.registerUseCase,
    required this.logoutUseCase,
  }}) : super(AuthInitial()) {{
    on<LoginEvent>(_onLogin);
    on<RegisterEvent>(_onRegister);
    on<LogoutEvent>(_onLogout);
  }}

  Future<void> _onLogin(LoginEvent event, Emitter<AuthState> emit) async {{
    emit(AuthLoading());
    
    final result = await loginUseCase(
      LoginParams(email: event.email, password: event.password),
    );
    
    result.fold(
      (failure) => emit(AuthFailure(failure.message)),
      (user) => emit(AuthSuccess(user)),
    );
  }}

  Future<void> _onRegister(RegisterEvent event, Emitter<AuthState> emit) async {{
    emit(AuthLoading());
    
    final result = await registerUseCase(
      RegisterParams(
        name: event.name,
        email: event.email,
        password: event.password,
      ),
    );
    
    result.fold(
      (failure) => emit(AuthFailure(failure.message)),
      (success) => emit(AuthRegistered()),
    );
  }}

  Future<void> _onLogout(LogoutEvent event, Emitter<AuthState> emit) async {{
    emit(AuthLoading());
    
    final result = await logoutUseCase(NoParams());
    
    result.fold(
      (failure) => emit(AuthFailure(failure.message)),
      (_) => emit(AuthLoggedOut()),
    );
  }}
}}
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write(f"""import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '{utils_prefix}/responsively.dart';
import '../bloc/auth/auth_bloc.dart';
import '../bloc/auth/auth_event.dart';
import '../bloc/auth/auth_state.dart';

class LoginPage extends StatefulWidget {{
  const LoginPage({{super.key}});

  @override
  State<LoginPage> createState() => _LoginPageState();
}}

class _LoginPageState extends State<LoginPage> {{
  Widget _buildHeader(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ExcludeSemantics(
          child: Icon(Icons.shield_outlined, size: context.resp(64), color: Theme.of(context).primaryColor),
        ),
        SizedBox(height: context.resp(12)),
        Text(
          'Clean Architecture (BLoC)',
          key: const Key('login_title_text'),
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }}

  Widget _buildActions(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Semantics(
          button: true,
          label: 'Login button',
          child: ElevatedButton(
            key: const Key('login_submit_button'),
            onPressed: () {{
              context.read<AuthBloc>().add(LoginEvent(email: "test", password: "123"));
            }},
            style: ElevatedButton.styleFrom(
              padding: EdgeInsets.symmetric(vertical: context.resp(12)),
            ),
            child: const Text('Login'),
          ),
        ),
      ],
    );
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: SafeArea(
        child: BlocConsumer<AuthBloc, AuthState>(
          listener: (context, state) {{
            if (state is AuthFailure) {{
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(state.message)));
            }}
          }},
          builder: (context, state) {{
            return OrientationLayout(
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
                        _buildActions(ctx),
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
                        Expanded(child: _buildActions(ctx)),
                      ],
                    ),
                  ),
                ),
              ),
            );
          }},
        ),
      ),
    );
  }}
}}
""")

def _create_cubit_presentation(presentation_path, pages_path, core_prefix, utils_prefix):
    cubit_path = os.path.join(presentation_path, 'cubit', 'auth')
    os.makedirs(cubit_path, exist_ok=True)

    with open(os.path.join(cubit_path, 'auth_state.dart'), 'w') as file:
        file.write("""import 'package:equatable/equatable.dart';
import '../../../domain/entities/user.dart';

abstract class AuthState extends Equatable {
  const AuthState();

  @override
  List<Object?> get props => [];
}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class AuthSuccess extends AuthState {
  final User user;

  const AuthSuccess(this.user);

  @override
  List<Object?> get props => [user];
}

class AuthRegistered extends AuthState {}

class AuthLoggedOut extends AuthState {}

class AuthFailure extends AuthState {
  final String message;

  const AuthFailure(this.message);

  @override
  List<Object?> get props => [message];
}
""")

    with open(os.path.join(cubit_path, 'auth_cubit.dart'), 'w') as file:
        file.write(f"""import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../domain/usecases/login_usecase.dart';
import '../../../domain/usecases/register_usecase.dart';
import '../../../domain/usecases/logout_usecase.dart';
import '{core_prefix}/usecases/usecase.dart';
import 'auth_state.dart';

class AuthCubit extends Cubit<AuthState> {{
  final LoginUseCase loginUseCase;
  final RegisterUseCase registerUseCase;
  final LogoutUseCase logoutUseCase;

  AuthCubit({{
    required this.loginUseCase,
    required this.registerUseCase,
    required this.logoutUseCase,
  }}) : super(AuthInitial());

  Future<void> login(String email, String password) async {{
    emit(AuthLoading());
    
    final result = await loginUseCase(
      LoginParams(email: email, password: password),
    );
    
    result.fold(
      (failure) => emit(AuthFailure(failure.message)),
      (user) => emit(AuthSuccess(user)),
    );
  }}

  Future<void> register(String name, String email, String password) async {{
    emit(AuthLoading());
    
    final result = await registerUseCase(
      RegisterParams(
        name: name,
        email: email,
        password: password,
      ),
    );
    
    result.fold(
      (failure) => emit(AuthFailure(failure.message)),
      (success) => emit(AuthRegistered()),
    );
  }}

  Future<void> logout() async {{
    emit(AuthLoading());
    
    final result = await logoutUseCase(NoParams());
    
    result.fold(
      (failure) => emit(AuthFailure(failure.message)),
      (_) => emit(AuthLoggedOut()),
    );
  }}
}}
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write(f"""import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '{utils_prefix}/responsively.dart';
import '../cubit/auth/auth_cubit.dart';
import '../cubit/auth/auth_state.dart';

class LoginPage extends StatefulWidget {{
  const LoginPage({{super.key}});

  @override
  State<LoginPage> createState() => _LoginPageState();
}}

class _LoginPageState extends State<LoginPage> {{
  Widget _buildHeader(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ExcludeSemantics(
          child: Icon(Icons.shield_outlined, size: context.resp(64), color: Theme.of(context).primaryColor),
        ),
        SizedBox(height: context.resp(12)),
        Text(
          'Clean Architecture (Cubit)',
          key: const Key('login_title_text'),
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }}

  Widget _buildActions(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Semantics(
          button: true,
          label: 'Login button',
          child: ElevatedButton(
            key: const Key('login_submit_button'),
            onPressed: () {{
              context.read<AuthCubit>().login("test", "123");
            }},
            style: ElevatedButton.styleFrom(
              padding: EdgeInsets.symmetric(vertical: context.resp(12)),
            ),
            child: const Text('Login'),
          ),
        ),
      ],
    );
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: SafeArea(
        child: BlocConsumer<AuthCubit, AuthState>(
          listener: (context, state) {{
            if (state is AuthFailure) {{
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(state.message)));
            }}
          }},
          builder: (context, state) {{
            return OrientationLayout(
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
                        _buildActions(ctx),
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
                        Expanded(child: _buildActions(ctx)),
                      ],
                    ),
                  ),
                ),
              ),
            );
          }},
        ),
      ),
    );
  }}
}}
""")

def _create_mobx_presentation(presentation_path, pages_path, utils_prefix):
    store_path = os.path.join(presentation_path, 'store', 'auth')
    os.makedirs(store_path, exist_ok=True)
    
    with open(os.path.join(store_path, 'auth_store.dart'), 'w') as file:
        file.write("""// ignore_for_file: library_private_types_in_public_api
import 'package:mobx/mobx.dart';
import '../../../domain/usecases/login_usecase.dart';

part 'auth_store.g.dart';

class AuthStore = _AuthStoreBase with _$AuthStore;

abstract class _AuthStoreBase with Store {
  final LoginUseCase loginUseCase;

  _AuthStoreBase(this.loginUseCase);

  @observable
  bool isLoading = false;

  @action
  Future<void> login(String email, String password) async {
    isLoading = true;
    await loginUseCase(LoginParams(email: email, password: password));
    isLoading = false;
  }
}
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write(f"""import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import '{utils_prefix}/responsively.dart';

class LoginPage extends StatefulWidget {{
  const LoginPage({{super.key}});

  @override
  State<LoginPage> createState() => _LoginPageState();
}}

class _LoginPageState extends State<LoginPage> {{
  Widget _buildHeader(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ExcludeSemantics(
          child: Icon(Icons.shield_outlined, size: context.resp(64), color: Theme.of(context).primaryColor),
        ),
        SizedBox(height: context.resp(12)),
        Text(
          'Clean Architecture (MobX)',
          key: const Key('login_title_text'),
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }}

  Widget _buildActions(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Observer(
          builder: (_) => Semantics(
            button: true,
            label: 'Login button',
            child: ElevatedButton(
              key: const Key('login_submit_button'),
              onPressed: () {{}},
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(vertical: context.resp(12)),
              ),
              child: const Text('Login'),
            ),
          ),
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
                    _buildActions(ctx),
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
                    Expanded(child: _buildActions(ctx)),
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
""")

def _create_getx_presentation(presentation_path, pages_path, utils_prefix):
    controllers_path = os.path.join(presentation_path, 'controllers', 'auth')
    bindings_path = os.path.join(presentation_path, 'bindings', 'auth')
    os.makedirs(controllers_path, exist_ok=True)
    os.makedirs(bindings_path, exist_ok=True)
    
    with open(os.path.join(controllers_path, 'auth_controller.dart'), 'w') as file:
        file.write("""import 'package:get/get.dart';
import '../../../domain/usecases/login_usecase.dart';

class AuthController extends GetxController {
  final LoginUseCase loginUseCase;

  AuthController(this.loginUseCase);

  var isLoading = false.obs;

  Future<void> login(String email, String password) async {
    isLoading.value = true;
    await loginUseCase(LoginParams(email: email, password: password));
    isLoading.value = false;
  }
}
""")

    with open(os.path.join(bindings_path, 'auth_binding.dart'), 'w') as file:
        file.write("""import 'package:get/get.dart';
import '../../controllers/auth/auth_controller.dart';
import '../../../domain/usecases/login_usecase.dart';

class AuthBinding extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut<AuthController>(
      () => AuthController(Get.find<LoginUseCase>()),
    );
  }
}
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write(f"""import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '{utils_prefix}/responsively.dart';
import '../controllers/auth/auth_controller.dart';

class LoginPage extends GetView<AuthController> {{
  const LoginPage({{super.key}});

  Widget _buildHeader(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ExcludeSemantics(
          child: Icon(Icons.shield_outlined, size: context.resp(64), color: Theme.of(context).primaryColor),
        ),
        SizedBox(height: context.resp(12)),
        Text(
          'Clean Architecture (GetX)',
          key: const Key('login_title_text'),
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }}

  Widget _buildActions(BuildContext context) {{
    return Obx(() {{
      return Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Semantics(
            button: true,
            label: controller.isLoading.value ? 'Authenticating, please wait' : 'Login button',
            child: ElevatedButton(
              key: const Key('login_submit_button'),
              onPressed: () => controller.login("test", "test"),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(vertical: context.resp(12)),
              ),
              child: controller.isLoading.value
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
      );
    }});
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
                    _buildActions(ctx),
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
                    Expanded(child: _buildActions(ctx)),
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
""")

def _create_riverpod_presentation(presentation_path, pages_path, utils_prefix):
    notifiers_path = os.path.join(presentation_path, 'notifiers', 'auth')
    os.makedirs(notifiers_path, exist_ok=True)
    
    with open(os.path.join(notifiers_path, 'auth_notifier.dart'), 'w') as file:
        file.write("""import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../domain/usecases/login_usecase.dart';
import '../../../domain/entities/user.dart';

class AuthState {
  final bool isLoading;
  final User? user;
  AuthState({this.isLoading = false, this.user});
}

class AuthNotifier extends Notifier<AuthState> {
  LoginUseCase? _loginUseCase;

  AuthNotifier([this._loginUseCase]);

  @override
  AuthState build() {
    return AuthState();
  }

  Future<void> login(String email, String password) async {
    state = AuthState(isLoading: true);
    if (_loginUseCase != null) {
      final result = await _loginUseCase!(LoginParams(email: email, password: password));
      result.fold(
        (failure) => state = AuthState(isLoading: false),
        (user) => state = AuthState(isLoading: false, user: user),
      );
    } else {
      state = AuthState(isLoading: false);
    }
  }
}

final authNotifierProvider = NotifierProvider<AuthNotifier, AuthState>(() => AuthNotifier());
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write(f"""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '{utils_prefix}/responsively.dart';
import '../notifiers/auth/auth_notifier.dart';

class LoginPage extends ConsumerWidget {{
  const LoginPage({{super.key}});

  Widget _buildHeader(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ExcludeSemantics(
          child: Icon(Icons.shield_outlined, size: context.resp(64), color: Theme.of(context).primaryColor),
        ),
        SizedBox(height: context.resp(12)),
        Text(
          'Clean Architecture (Riverpod)',
          key: const Key('login_title_text'),
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }}

  Widget _buildActions(BuildContext context, WidgetRef ref) {{
    final state = ref.watch(authNotifierProvider);

    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Semantics(
          button: true,
          label: state.isLoading ? 'Authenticating, please wait' : 'Login button',
          child: ElevatedButton(
            key: const Key('login_submit_button'),
            onPressed: state.isLoading
                ? null
                : () => ref.read(authNotifierProvider.notifier).login("test", "test"),
            style: ElevatedButton.styleFrom(
              padding: EdgeInsets.symmetric(vertical: context.resp(12)),
            ),
            child: state.isLoading
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
    );
  }}

  @override
  Widget build(BuildContext context, WidgetRef ref) {{
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
                    _buildActions(ctx, ref),
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
                    Expanded(child: _buildActions(ctx, ref)),
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
""")

def _create_provider_presentation(presentation_path, pages_path, utils_prefix):
    providers_path = os.path.join(presentation_path, 'providers', 'auth')
    os.makedirs(providers_path, exist_ok=True)
    
    with open(os.path.join(providers_path, 'auth_provider.dart'), 'w') as file:
        file.write("""import 'package:flutter/material.dart';
import '../../../domain/usecases/login_usecase.dart';

class AuthProvider extends ChangeNotifier {
  final LoginUseCase loginUseCase;

  AuthProvider(this.loginUseCase);

  bool isLoading = false;

  Future<void> login(String email, String password) async {
    isLoading = true;
    notifyListeners();
    await loginUseCase(LoginParams(email: email, password: password));
    isLoading = false;
    notifyListeners();
  }
}
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write(f"""import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '{utils_prefix}/responsively.dart';
import '../providers/auth/auth_provider.dart';

class LoginPage extends StatelessWidget {{
  const LoginPage({{super.key}});

  Widget _buildHeader(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ExcludeSemantics(
          child: Icon(Icons.shield_outlined, size: context.resp(64), color: Theme.of(context).primaryColor),
        ),
        SizedBox(height: context.resp(12)),
        Text(
          'Clean Architecture (Provider)',
          key: const Key('login_title_text'),
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }}

  Widget _buildActions(BuildContext context, AuthProvider auth) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Semantics(
          button: true,
          label: auth.isLoading ? 'Authenticating, please wait' : 'Login button',
          child: ElevatedButton(
            key: const Key('login_submit_button'),
            onPressed: auth.isLoading ? null : () => auth.login('test', '123'),
            style: ElevatedButton.styleFrom(
              padding: EdgeInsets.symmetric(vertical: context.resp(12)),
            ),
            child: auth.isLoading
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
    );
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: SafeArea(
        child: Consumer<AuthProvider>(
          builder: (context, auth, _) {{
            return OrientationLayout(
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
                        _buildActions(ctx, auth),
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
                        Expanded(child: _buildActions(ctx, auth)),
                      ],
                    ),
                  ),
                ),
              ),
            );
          }},
        ),
      ),
    );
  }}
}}
""")

def _create_none_presentation(presentation_path, pages_path, utils_prefix):
    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write(f"""import 'package:flutter/material.dart';
import '{utils_prefix}/responsively.dart';

class LoginPage extends StatefulWidget {{
  const LoginPage({{super.key}});

  @override
  State<LoginPage> createState() => _LoginPageState();
}}

class _LoginPageState extends State<LoginPage> {{
  bool isLoading = false;

  void _login() async {{
    setState(() => isLoading = true);
    // await your injected loginUseCase
    setState(() => isLoading = false);
  }}

  Widget _buildHeader(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ExcludeSemantics(
          child: Icon(Icons.shield_outlined, size: context.resp(64), color: Theme.of(context).primaryColor),
        ),
        SizedBox(height: context.resp(12)),
        Text(
          'Clean Architecture',
          key: const Key('login_title_text'),
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }}

  Widget _buildActions(BuildContext context) {{
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Semantics(
          button: true,
          label: isLoading ? 'Authenticating, please wait' : 'Login button',
          child: ElevatedButton(
            key: const Key('login_submit_button'),
            onPressed: isLoading ? null : _login,
            style: ElevatedButton.styleFrom(
              padding: EdgeInsets.symmetric(vertical: context.resp(12)),
            ),
            child: isLoading
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
                    _buildActions(ctx),
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
                    Expanded(child: _buildActions(ctx)),
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
""")
