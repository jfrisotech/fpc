import os

def create_clean_architecture_data(lib_path: str):
    """Create data layer template files for Clean Architecture."""
    data_path = os.path.join(lib_path, 'data')
    os.makedirs(data_path, exist_ok=True)

    models_path = os.path.join(data_path, 'models')
    datasources_path = os.path.join(data_path, 'datasources')
    repositories_path = os.path.join(data_path, 'repositories')
    os.makedirs(models_path, exist_ok=True)
    os.makedirs(datasources_path, exist_ok=True)
    os.makedirs(repositories_path, exist_ok=True)

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
