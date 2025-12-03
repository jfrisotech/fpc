import os

def create_clean_architecture_core(lib_path: str):
    """Create core layer template files for Clean Architecture."""
    core_path = os.path.join(lib_path, 'core')
    os.makedirs(core_path, exist_ok=True)

    # Create error handling
    error_path = os.path.join(core_path, 'error')
    os.makedirs(error_path, exist_ok=True)
    
    with open(os.path.join(error_path, 'failures.dart'), 'w') as file:
        file.write('''abstract class Failure {
  final String message;
  
  const Failure(this.message);
}

class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

class CacheFailure extends Failure {
  const CacheFailure(super.message);
}

class NetworkFailure extends Failure {
  const NetworkFailure(super.message);
}

class ValidationFailure extends Failure {
  const ValidationFailure(super.message);
}
''')

    # Create base UseCase
    usecases_path = os.path.join(core_path, 'usecases')
    os.makedirs(usecases_path, exist_ok=True)
    
    with open(os.path.join(usecases_path, 'usecase.dart'), 'w') as file:
        file.write('''import 'package:dartz/dartz.dart';
import '../error/failures.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams {}
''')
