def get_getx_controller_template(class_name: str) -> str:
    return f"""import 'package:get/get.dart';

class {class_name}Controller extends GetxController {{
  final count = 0.obs;

  void increment() => count.value++;
}}
"""
