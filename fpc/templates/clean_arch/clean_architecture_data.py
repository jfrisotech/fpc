import os

def create_clean_architecture_data(lib_path: str, preferences: dict = None):
    """Create data layer template files for Clean Architecture."""
    data_path = os.path.join(lib_path, 'data')
    os.makedirs(data_path, exist_ok=True)

    models_path = os.path.join(data_path, 'models')
    datasources_path = os.path.join(data_path, 'datasources')
    repositories_path = os.path.join(data_path, 'repositories')
    os.makedirs(models_path, exist_ok=True)
    os.makedirs(datasources_path, exist_ok=True)
    os.makedirs(repositories_path, exist_ok=True)

    imports = []
    annotations = []
    if preferences:
        database = preferences.get('database')
        baas = preferences.get('baas')
            
        if database == 'Hive':
            imports.append("import 'package:hive/hive.dart';")
            imports.append("part 'user_model.g.dart';")
            annotations.append("@HiveType(typeId: 0)")
        elif database == 'Isar':
            imports.append("import 'package:isar/isar.dart';")
            imports.append("part 'user_model.g.dart';")
            annotations.append("@collection")
            
        elif database == 'ObjectBox':
            imports.append("import 'package:objectbox/objectbox.dart';")
            annotations.append("@Entity()")
            
        if baas == 'Firebase':
            imports.append("import 'package:cloud_firestore/cloud_firestore.dart';")

    imports_str = '\n'.join(imports) + ('\n' if imports else '')
    annotations_str = '\n'.join(annotations) + ('\n' if annotations else '')

    db_id_field = ""
    if database == 'Isar':
        db_id_field = "  Id id = Isar.autoIncrement;\n"
    elif database == 'ObjectBox':
        db_id_field = "  @Id()\n  int localId = 0;\n"

    # Model extends Entity
    with open(os.path.join(models_path, 'user_model.dart'), 'w') as file:
        file.write(f'''import '../../domain/entities/user.dart';
{imports_str}
{annotations_str}class UserModel extends User {{
{db_id_field}  UserModel({{
    required super.uid,
    required super.name,
    required super.email,
  }});

  factory UserModel.fromJson(Map<String, dynamic> json) {{
    return UserModel(
      uid: json['uid'] ?? json['id'] ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
    );
  }}

  Map<String, dynamic> toJson() {{
    return {{
      'uid': uid,
      'name': name,
      'email': email,
    }};
  }}
  
  User toEntity() {{
    return User(
      uid: uid,
      name: name,
      email: email,
    );
  }}
}}
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
      uid: '1',
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

    core_prefix = '../../../../core' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../../core'

    # Repository Implementation with Either
    with open(os.path.join(repositories_path, 'auth_repository_impl.dart'), 'w') as file:
        file.write(f'''import 'package:dartz/dartz.dart';
import '{core_prefix}/error/failures.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_remote_data_source.dart';
import '{core_prefix}/network/network_info.dart';

class AuthRepositoryImpl implements AuthRepository {{
  final AuthRemoteDataSource remoteDataSource;
  final NetworkInfo networkInfo;

  AuthRepositoryImpl({{
    required this.remoteDataSource,
    required this.networkInfo,
  }});

  @override
  Future<Either<Failure, User>> login(String email, String password) async {{
    if (await networkInfo.isConnected) {{
      try {{
        final userModel = await remoteDataSource.login(email, password);
        return Right(userModel.toEntity());
      }} catch (e) {{
        return Left(ServerFailure(e.toString()));
      }}
    }} else {{
      return const Left(NetworkFailure('No internet connection'));
    }}
  }}

  @override
  Future<Either<Failure, bool>> register(String name, String email, String password) async {{
    if (await networkInfo.isConnected) {{
      try {{
        final result = await remoteDataSource.register(name, email, password);
        return Right(result);
      }} catch (e) {{
        return Left(ServerFailure(e.toString()));
      }}
    }} else {{
      return const Left(NetworkFailure('No internet connection'));
    }}
  }}

  @override
  Future<Either<Failure, void>> logout() async {{
    try {{
      await remoteDataSource.logout();
      return const Right(null);
    }} catch (e) {{
      return Left(ServerFailure(e.toString()));
    }}
  }}
}}
''')
