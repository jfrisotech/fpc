def get_getx_controller_template(class_name: str) -> str:
    name = class_name
    if not name.endswith('Controller'):
        name += 'Controller'
    return f"""import 'package:get/get.dart';

class {name} extends GetxController {{
  final count = 0.obs;

  void increment() => count.value++;
}}
"""
