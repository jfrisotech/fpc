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
    parts = []
    annotations = []
    database = None  # Bug #1 fix: always defined
    baas = None
    if preferences:
        database = preferences.get('database')
        baas = preferences.get('baas')
            
        if database == 'ObjectBox':
            imports.append("import 'package:objectbox/objectbox.dart';")
            annotations.append("@Entity()")
            
        if baas == 'Firebase':
            imports.append("import 'package:cloud_firestore/cloud_firestore.dart';")

    imports_str = '\n'.join(imports) + ('\n' if imports else '')
    parts_str = '\n'.join(parts) + ('\n' if parts else '')
    annotations_str = '\n'.join(annotations) + ('\n' if annotations else '')

    db_id_field = ""
    if database == 'ObjectBox':
        db_id_field = "  @Id()\n  int localId = 0;\n"

    # Model extends Entity
    with open(os.path.join(models_path, 'user_model.dart'), 'w') as file:
        file.write(f'''import '../../domain/entities/user.dart';
{imports_str}
{parts_str}
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
    remote_datasources_path = os.path.join(datasources_path, 'remote')
    os.makedirs(remote_datasources_path, exist_ok=True)

    has_local_db = database and str(database).lower() != 'none'
    if has_local_db:
        local_datasources_path = os.path.join(datasources_path, 'local')
        os.makedirs(local_datasources_path, exist_ok=True)
        from fpc.templates.clean_arch.data.auth_local_data_source_template import get_auth_local_data_source_content
        with open(os.path.join(local_datasources_path, 'auth_local_data_source.dart'), 'w') as file:
            file.write(get_auth_local_data_source_content())

    http_client = preferences.get('http_client') if preferences else None
    shared_prefix = '../../../../../shared' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../../../shared'
    http_import = ""
    http_field = ""
    http_constructor = ""
    if http_client == 'Dio':
        http_import = f"import '{shared_prefix}/network/dio_client.dart';\n"
        http_field = "  final DioClient? dioClient;\n"
        http_constructor = "\n  AuthRemoteDataSourceImpl([this.dioClient]);\n"
    elif http_client == 'http':
        http_import = f"import '{shared_prefix}/network/http_client.dart';\n"
        http_field = "  final HttpClient? httpClient;\n"
        http_constructor = "\n  AuthRemoteDataSourceImpl([this.httpClient]);\n"

    with open(os.path.join(remote_datasources_path, 'auth_remote_data_source.dart'), 'w') as file:
        file.write(f'''import '../../models/user_model.dart';
{http_import}
abstract class AuthRemoteDataSource {{
  Future<UserModel> login(String email, String password);
  Future<bool> register(String name, String email, String password);
  Future<void> logout();
}}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {{
{http_field}{http_constructor}
  @override
  Future<UserModel> login(String email, String password) async {{
    // TODO: Implement API call
    // For now, return mock data
    return UserModel(
      uid: '1',
      name: 'Mock User',
      email: email,
    );
  }}

  @override
  Future<bool> register(String name, String email, String password) async {{
    // TODO: Implement API call
    return true;
  }}

  @override
  Future<void> logout() async {{
    // TODO: Implement logout logic
  }}
}}
''')

    core_prefix = '../../../../core' if preferences and preferences.get('folder_structure') == 'Modular (Feature First)' else '../../core'
    local_ds_import = "import '../datasources/local/auth_local_data_source.dart';\n" if has_local_db else ""
    local_ds_field = "  final AuthLocalDataSource? localDataSource;\n" if has_local_db else ""
    local_ds_param = "    this.localDataSource,\n" if has_local_db else ""

    cache_on_login = "        await localDataSource?.cacheUser(userModel);\n" if has_local_db else ""
    offline_fallback = f"""      try {{
        final cached = await localDataSource?.getLastUser();
        if (cached != null) {{
          return Right(cached.toEntity());
        }}
        return const Left(NetworkFailure('No internet connection and no cached data'));
      }} catch (e) {{
        return Left(CacheFailure(e.toString()));
      }}""" if has_local_db else "      return const Left(NetworkFailure('No internet connection'));"

    # Repository Implementation with Either
    with open(os.path.join(repositories_path, 'auth_repository_impl.dart'), 'w') as file:
        file.write(f'''import 'package:dartz/dartz.dart';
import '{core_prefix}/error/failures.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/remote/auth_remote_data_source.dart';
{local_ds_import}import '{core_prefix}/network/network_info.dart';

class AuthRepositoryImpl implements AuthRepository {{
  final AuthRemoteDataSource remoteDataSource;
{local_ds_field}  final NetworkInfo networkInfo;

  AuthRepositoryImpl({{
    required this.remoteDataSource,
{local_ds_param}    required this.networkInfo,
  }});

  @override
  Future<Either<Failure, User>> login(String email, String password) async {{
    if (await networkInfo.isConnected) {{
      try {{
        final userModel = await remoteDataSource.login(email, password);
{cache_on_login}        return Right(userModel.toEntity());
      }} catch (e) {{
        return Left(ServerFailure(e.toString()));
      }}
    }} else {{
{offline_fallback}
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
