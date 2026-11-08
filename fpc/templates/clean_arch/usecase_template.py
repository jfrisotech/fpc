from fpc.core.utils import to_pascal_case, to_snake_case

def get_usecase_template(name: str) -> str:
    base = name
    for suffix in ['UseCase', 'Usecase', '_usecase', 'usecase']:
        if base.endswith(suffix):
            base = base[:-len(suffix)]
            break
    pascal_name = to_pascal_case(base)
    snake_name = to_snake_case(base)
    return f'''import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/{snake_name}_entity.dart';
import '../repositories/{snake_name}_repository.dart';

class Get{pascal_name}UseCase implements UseCase<{pascal_name}Entity, {pascal_name}Params> {{
  final {pascal_name}Repository repository;

  Get{pascal_name}UseCase(this.repository);

  @override
  Future<Either<Failure, {pascal_name}Entity>> call({pascal_name}Params params) async {{
    // TODO: Connect to repository method
    throw UnimplementedError();
  }}
}}

class {pascal_name}Params {{
  final String id;
  const {pascal_name}Params({{required this.id}});
}}
'''

get_clean_usecase_template = get_usecase_template
