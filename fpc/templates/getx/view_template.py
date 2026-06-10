def get_getx_view_template(class_name: str, base_name: str = None) -> str:
    from fpc.core.utils import to_pascal_case, to_snake_case
    b_name = base_name or (class_name[:-4] if class_name.endswith('View') else class_name)
    controller_class = f"{to_pascal_case(b_name)}Controller"
    controller_file = f"{to_snake_case(b_name)}_controller.dart"
    
    view_class = class_name
    if not view_class.endswith('View'):
        view_class += 'View'

    return f"""import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/{controller_file}';

class {view_class} extends GetView<{controller_class}> {{
  const {view_class}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    // Ensure controller is put in memory if not already
    Get.put({controller_class}());
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('{view_class}'),
      ),
      body: Center(
        child: Obx(() => Text('Value: ${{controller.count}}')),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: controller.increment,
        child: const Icon(Icons.add),
      ),
    );
  }}
}}
"""
