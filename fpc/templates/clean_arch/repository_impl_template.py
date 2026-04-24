def get_repository_impl_template(name: str) -> str:
    # We'll use a generic version of the AuthRepositoryImpl
    # Since it's dynamic generation, we don't know the exact project structure,
    # but we'll use relative paths that usually work.
    return f'''import 'package:dartz/dartz.dart';
import '../../../core/error/failures.dart';
import '../../../core/network/network_info.dart';
import '../../domain/repositories/{to_snake_case(name)}_repository.dart';
import '../datasources/{to_snake_case(name)}_remote_data_source.dart';

class {name}RepositoryImpl {{
  final {name}RemoteDataSource remoteDataSource;
  final NetworkInfo networkInfo;

  {name}RepositoryImpl({{
    required this.remoteDataSource,
    required this.networkInfo,
  }});

  // TODO: Implement repository methods
}}
'''

from fpc.core.utils import to_snake_case
