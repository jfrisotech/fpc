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

    # Model extends Entity
    with open(os.path.join(models_path, 'user_model.dart'), 'w') as file:
        file.write('''import '../../domain/entities/user.dart';

class UserModel extends User {
  UserModel({
    required super.id,
    required super.name,
    required super.email,
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
  
  User toEntity() {
    return User(
      id: id,
      name: name,
      email: email,
    );
  }
}
''')

    # Remote Data Source
    with open(os.path.join(datasources_path, 'auth_remote_data_source.dart'), 'w') as file:
        file.write('''import '../models/user_model.dart';

abstract class AuthRemoteDataSource {
  Future<UserModel> login(String email, String password);
  Future<bool> register(String name, String email, String password);
  Future<void> logout();
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  @override
  Future<UserModel> login(String email, String password) async {
    // TODO: Implement API call
    // Example: final response = await http.post(...)
    // For now, return mock data
    return UserModel(
      id: '1',
      name: 'Mock User',
      email: email,
    );
  }

  @override
  Future<bool> register(String name, String email, String password) async {
    // TODO: Implement API call
    return true;
  }

  @override
  Future<void> logout() async {
    // TODO: Implement logout logic
  }
}
''')

    # Repository Implementation with Either
    with open(os.path.join(repositories_path, 'auth_repository_impl.dart'), 'w') as file:
        file.write('''import 'package:dartz/dartz.dart';
import '../../core/error/failures.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_remote_data_source.dart';

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;

  AuthRepositoryImpl(this.remoteDataSource);

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    try {
      final userModel = await remoteDataSource.login(email, password);
      return Right(userModel.toEntity());
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, bool>> register(String name, String email, String password) async {
    try {
      final result = await remoteDataSource.register(name, email, password);
      return Right(result);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      await remoteDataSource.logout();
      return const Right(null);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
}
''')
