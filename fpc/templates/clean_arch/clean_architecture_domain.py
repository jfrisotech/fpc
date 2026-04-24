import os

def create_clean_architecture_domain(lib_path: str, preferences: dict = None):
    """Create domain layer template files for Clean Architecture."""
    domain_path = os.path.join(lib_path, 'domain')
    os.makedirs(domain_path, exist_ok=True)

    entities_path = os.path.join(domain_path, 'entities')
    repositories_path = os.path.join(domain_path, 'repositories')
    usecases_path = os.path.join(domain_path, 'usecases')
    os.makedirs(entities_path, exist_ok=True)
    os.makedirs(repositories_path, exist_ok=True)
    os.makedirs(usecases_path, exist_ok=True)

    core_prefix = '../../../../core' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../../core'

    # Entity
    with open(os.path.join(entities_path, 'user.dart'), 'w') as file:
        file.write('''class User {
  final String uid;
  final String name;
  final String email;

  User({
    required this.uid,
    required this.name,
    required this.email,
  });
}
''')

    # Repository interface
    with open(os.path.join(repositories_path, 'auth_repository.dart'), 'w') as file:
        file.write(f'''import 'package:dartz/dartz.dart';
import '{core_prefix}/error/failures.dart';
import '../entities/user.dart';

abstract class AuthRepository {{
  Future<Either<Failure, User>> login(String email, String password);
  Future<Either<Failure, bool>> register(String name, String email, String password);
  Future<Either<Failure, void>> logout();
}}
''')

    # Individual Use Cases
    with open(os.path.join(usecases_path, 'login_usecase.dart'), 'w') as file:
        file.write(f'''import 'package:dartz/dartz.dart';
import '{core_prefix}/error/failures.dart';
import '{core_prefix}/usecases/usecase.dart';
import '../entities/user.dart';
import '../repositories/auth_repository.dart';

class LoginUseCase implements UseCase<User, LoginParams> {{
  final AuthRepository repository;

  LoginUseCase(this.repository);

  @override
  Future<Either<Failure, User>> call(LoginParams params) async {{
    return await repository.login(params.email, params.password);
  }}
}}

class LoginParams {{
  final String email;
  final String password;

  LoginParams({{required this.email, required this.password}});
}}
''')

    with open(os.path.join(usecases_path, 'register_usecase.dart'), 'w') as file:
        file.write(f'''import 'package:dartz/dartz.dart';
import '{core_prefix}/error/failures.dart';
import '{core_prefix}/usecases/usecase.dart';
import '../repositories/auth_repository.dart';

class RegisterUseCase implements UseCase<bool, RegisterParams> {{
  final AuthRepository repository;

  RegisterUseCase(this.repository);

  @override
  Future<Either<Failure, bool>> call(RegisterParams params) async {{
    return await repository.register(params.name, params.email, params.password);
  }}
}}

class RegisterParams {{
  final String name;
  final String email;
  final String password;

  RegisterParams({{
    required this.name,
    required this.email,
    required this.password,
  }});
}}
''')

    with open(os.path.join(usecases_path, 'logout_usecase.dart'), 'w') as file:
        file.write(f'''import 'package:dartz/dartz.dart';
import '{core_prefix}/error/failures.dart';
import '{core_prefix}/usecases/usecase.dart';
import '../repositories/auth_repository.dart';

class LogoutUseCase implements UseCase<void, NoParams> {{
  final AuthRepository repository;

  LogoutUseCase(this.repository);

  @override
  Future<Either<Failure, void>> call(NoParams params) async {{
    return await repository.logout();
  }}
}}
''')
