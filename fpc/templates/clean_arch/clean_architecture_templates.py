import os

def create_clean_architecture_template_files(lib_path: str, preferences: dict):
    """Create template files for Clean Architecture."""
    # Define folder paths
    data_path = os.path.join(lib_path, 'data')
    domain_path = os.path.join(lib_path, 'domain')
    presentation_path = os.path.join(lib_path, 'presentation')
    
    # Create folders
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(domain_path, exist_ok=True)
    os.makedirs(presentation_path, exist_ok=True)
    
    # Create data subfolders
    models_path = os.path.join(data_path, 'models')
    datasources_path = os.path.join(data_path, 'datasources')
    repositories_path = os.path.join(data_path, 'repositories')
    os.makedirs(models_path, exist_ok=True)
    os.makedirs(datasources_path, exist_ok=True)
    os.makedirs(repositories_path, exist_ok=True)
    
    # Create example model file
    with open(os.path.join(models_path, 'user_model.dart'), 'w') as file:
        file.write('''
class UserModel {
  final String id;
  final String name;
  final String email;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
    };
  }
}
''')

    # Create example datasource file
    with open(os.path.join(datasources_path, 'auth_remote_data_source.dart'), 'w') as file:
        file.write('''
class AuthRemoteDataSource {
  Future<bool> login(String email, String password) async {
    // Implement remote login logic here
    return true;
  }

  Future<bool> register(String name, String email, String password) async {
    // Implement remote registration logic here
    return true;
  }
}
''')

    # Create example repository implementation file
    with open(os.path.join(repositories_path, 'auth_repository_impl.dart'), 'w') as file:
        file.write('''
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_remote_data_source.dart';

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;

  AuthRepositoryImpl(this.remoteDataSource);

  @override
  Future<bool> login(String email, String password) async {
    return await remoteDataSource.login(email, password);
  }

  @override
  Future<bool> register(String name, String email, String password) async {
    return await remoteDataSource.register(name, email, password);
  }
}
''')

    # Create domain subfolders
    entities_path = os.path.join(domain_path, 'entities')
    repositories_domain_path = os.path.join(domain_path, 'repositories')
    usecases_path = os.path.join(domain_path, 'usecases')
    os.makedirs(entities_path, exist_ok=True)
    os.makedirs(repositories_domain_path, exist_ok=True)
    os.makedirs(usecases_path, exist_ok=True)

    # Create example entity file
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

    # Create example repository interface file
    with open(os.path.join(repositories_domain_path, 'auth_repository.dart'), 'w') as file:
        file.write('''
abstract class AuthRepository {
  Future<bool> login(String email, String password);
  Future<bool> register(String name, String email, String password);
}
''')

    # Create example usecase file
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
