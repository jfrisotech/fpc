import os

def create_clean_architecture_domain(lib_path: str):
    """Create domain layer template files for Clean Architecture."""
    domain_path = os.path.join(lib_path, 'domain')
    os.makedirs(domain_path, exist_ok=True)

    entities_path = os.path.join(domain_path, 'entities')
    repositories_path = os.path.join(domain_path, 'repositories')
    usecases_path = os.path.join(domain_path, 'usecases')
    os.makedirs(entities_path, exist_ok=True)
    os.makedirs(repositories_path, exist_ok=True)
    os.makedirs(usecases_path, exist_ok=True)

    with open(os.path.join(entities_path, 'user.dart'), 'w') as file:
        file.write('''
class User {
  final String id;
  final String name;
  final String email;

  User({
    required this.id,
    required this.name,
    required this.email,
  });
}
''')

    with open(os.path.join(repositories_path, 'auth_repository.dart'), 'w') as file:
        file.write('''
abstract class AuthRepository {
  Future<bool> login(String email, String password);
  Future<bool> register(String name, String email, String password);
}
''')

    with open(os.path.join(usecases_path, 'auth_usecases.dart'), 'w') as file:
        file.write('''
import '../repositories/auth_repository.dart';

class AuthUseCases {
  final AuthRepository repository;

  AuthUseCases(this.repository);

  Future<bool> login(String email, String password) async {
    return await repository.login(email, password);
  }

  Future<bool> register(String name, String email, String password) async {
    return await repository.register(name, email, password);
  }
}
''')
