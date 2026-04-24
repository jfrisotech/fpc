import os

def create_clean_architecture_presentation(lib_path: str, preferences: dict = None):
    """Create presentation layer template files for Clean Architecture."""
    presentation_path = os.path.join(lib_path, 'presentation')
    os.makedirs(presentation_path, exist_ok=True)

    pages_path = os.path.join(presentation_path, 'pages')
    widgets_path = os.path.join(presentation_path, 'widgets')
    os.makedirs(pages_path, exist_ok=True)
    os.makedirs(widgets_path, exist_ok=True)
    
    state_management = preferences.get('state_management') if preferences else 'None'
    
    core_prefix = '../../../../core' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../../core'
    
    if state_management == 'BLoC':
        _create_bloc_presentation(presentation_path, pages_path, core_prefix)
    elif state_management == 'MobX':
        _create_mobx_presentation(presentation_path, pages_path)
    elif state_management == 'GetX':
        _create_getx_presentation(presentation_path, pages_path)
    elif state_management == 'Riverpod':
        _create_riverpod_presentation(presentation_path, pages_path)
    elif state_management == 'Provider':
        _create_provider_presentation(presentation_path, pages_path)
    else:
        _create_none_presentation(presentation_path, pages_path)

def _create_bloc_presentation(presentation_path, pages_path, core_prefix):
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
        file.write("""import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/auth/auth_bloc.dart';
import '../bloc/auth/auth_event.dart';
import '../bloc/auth/auth_state.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: BlocConsumer<AuthBloc, AuthState>(
        listener: (context, state) {
          if (state is AuthFailure) {
             ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(state.message)));
          }
        },
        builder: (context, state) {
          return Center(
             child: ElevatedButton(
               onPressed: () {
                 context.read<AuthBloc>().add(LoginEvent(email: "test", password: "123"));
               },
               child: const Text('Login'),
             ),
          );
        },
      ),
    );
  }
}
""")

def _create_mobx_presentation(presentation_path, pages_path):
    store_path = os.path.join(presentation_path, 'store', 'auth')
    os.makedirs(store_path, exist_ok=True)
    
    with open(os.path.join(store_path, 'auth_store.dart'), 'w') as file:
        file.write("""import 'package:mobx/mobx.dart';
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
    final result = await loginUseCase(LoginParams(email: email, password: password));
    isLoading = false;
  }
}
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write("""import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
// TODO: Import your AuthStore and inject dependencies

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Observer(
        builder: (_) {
          return Center(
             child: ElevatedButton(
               onPressed: () {}, // store.login
               child: const Text('Login'),
             ),
          );
        },
      ),
    );
  }
}
""")


def _create_getx_presentation(presentation_path, pages_path):
    controllers_path = os.path.join(presentation_path, 'controllers', 'auth')
    os.makedirs(controllers_path, exist_ok=True)
    
    with open(os.path.join(controllers_path, 'auth_controller.dart'), 'w') as file:
        file.write("""import 'package:get/get.dart';
import '../../../domain/usecases/login_usecase.dart';

class AuthController extends GetxController {
  final LoginUseCase loginUseCase;

  AuthController(this.loginUseCase);

  var isLoading = false.obs;

  Future<void> login(String email, String password) async {
    isLoading.value = true;
    final result = await loginUseCase(LoginParams(email: email, password: password));
    isLoading.value = false;
  }
}
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write("""import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/auth/auth_controller.dart';

class LoginPage extends GetView<AuthController> {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Obx(() {
        return Center(
             child: ElevatedButton(
               onPressed: () {
                   controller.login("test", "test");
               },
               child: controller.isLoading.value ? const CircularProgressIndicator() : const Text('Login'),
             ),
        );
      }),
    );
  }
}
""")

def _create_riverpod_presentation(presentation_path, pages_path):
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

class AuthNotifier extends StateNotifier<AuthState> {
  final LoginUseCase loginUseCase;

  AuthNotifier(this.loginUseCase) : super(AuthState());

  Future<void> login(String email, String password) async {
    state = AuthState(isLoading: true);
    final result = await loginUseCase(LoginParams(email: email, password: password));
    result.fold(
      (l) => state = AuthState(isLoading: false),
      (r) => state = AuthState(isLoading: false, user: r),
    );
  }
}
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write("""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class LoginPage extends ConsumerWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Center(
         child: ElevatedButton(
           onPressed: () {}, // Call your provider
           child: const Text('Login'),
         ),
      ),
    );
  }
}
""")


def _create_provider_presentation(presentation_path, pages_path):
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
    final result = await loginUseCase(LoginParams(email: email, password: password));
    isLoading = false;
    notifyListeners();
  }
}
""")

    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write("""import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth/auth_provider.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Consumer<AuthProvider>(
        builder: (context, auth, _) {
          return Center(
             child: ElevatedButton(
               onPressed: () => auth.login('test', '123'),
               child: auth.isLoading ? const CircularProgressIndicator() : const Text('Login'),
             ),
          );
        },
      ),
    );
  }
}
""")


def _create_none_presentation(presentation_path, pages_path):
    with open(os.path.join(pages_path, 'login_page.dart'), 'w') as file:
        file.write("""import 'package:flutter/material.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {

  bool isLoading = false;

  void _login() async {
    setState(() => isLoading = true);
    // await your injected loginUseCase
    setState(() => isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Center(
         child: ElevatedButton(
           onPressed: _login,
           child: isLoading ? const CircularProgressIndicator() : const Text('Login'),
         ),
      ),
    );
  }
}
""")
