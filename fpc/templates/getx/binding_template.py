def get_getx_binding_template(class_name: str, base_name: str = None, preferences: dict = None) -> str:
    from fpc.core.utils import to_pascal_case, to_snake_case
    b_name = base_name or (class_name[:-7] if class_name.endswith('Binding') else class_name)
    controller_class = f"{to_pascal_case(b_name)}Controller"
    controller_file = f"{to_snake_case(b_name)}_controller.dart"
    binding_class = f"{to_pascal_case(b_name)}Binding"

    architecture = preferences.get('architecture', '') if preferences else ''
    
    if 'Clean Architecture' in architecture:
        service_class = f"{to_pascal_case(b_name)}Service"
        service_file = f"{to_snake_case(b_name)}_service.dart"
        repo_class = f"{to_pascal_case(b_name)}Repository"
        repo_file = f"{to_snake_case(b_name)}_repository.dart"
        repo_impl_class = f"{to_pascal_case(b_name)}RepositoryImpl"
        repo_impl_file = f"{to_snake_case(b_name)}_repository_impl.dart"

        return f"""import 'package:get/get.dart';
import '../controllers/{controller_file}';
import '../../data/datasources/remote/{service_file}';
import '../../domain/repositories/{repo_file}';
import '../../data/repositories/{repo_impl_file}';

class {binding_class} extends Bindings {{
  @override
  void dependencies() {{
    // Data sources
    Get.lazyPut<{service_class}>(() => {service_class}Impl());

    // Repositories
    Get.lazyPut<{repo_class}>(
      () => {repo_impl_class}(
        remoteDataSource: Get.find<{service_class}>(),
        networkInfo: Get.find(),
      ),
    );

    // Controllers
    Get.lazyPut<{controller_class}>(
      () => {controller_class}(),
    );
  }}
}}
"""
    else:
        if 'MVC' in architecture:
            service_class = f"{to_pascal_case(b_name)}Service"
            service_file = f"{to_snake_case(b_name)}_service.dart"
            
            return f"""import 'package:get/get.dart';
import '../controllers/{controller_file}';
import '../services/{service_file}';

class {binding_class} extends Bindings {{
  @override
  void dependencies() {{
    Get.lazyPut<{service_class}>(() => {service_class}());
    Get.lazyPut<{controller_class}>(
      () => {controller_class}(),
    );
  }}
}}
"""
        elif 'MVVM' in architecture:
            vm_class = f"{to_pascal_case(b_name)}ViewModel"
            vm_file = f"{to_snake_case(b_name)}_viewmodel.dart"
            service_class = f"{to_pascal_case(b_name)}Service"
            service_file = f"{to_snake_case(b_name)}_service.dart"
            
            return f"""import 'package:get/get.dart';
import '../viewmodels/{vm_file}';
import '../services/{service_file}';

class {binding_class} extends Bindings {{
  @override
  void dependencies() {{
    Get.lazyPut<{service_class}>(() => {service_class}());
    Get.lazyPut<{vm_class}>(
      () => {vm_class}(),
    );
  }}
}}
"""
        else:
            return f"""import 'package:get/get.dart';
import '../controllers/{controller_file}';

class {binding_class} extends Bindings {{
  @override
  void dependencies() {{
    Get.lazyPut<{controller_class}>(
      () => {controller_class}(),
    );
  }}
}}
"""
