def get_getx_view_template(class_name: str) -> str:
    return f"""import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/{class_name.lower()}_controller.dart';

class {class_name}View extends GetView<{class_name}Controller> {{
  const {class_name}View({{super.key}});

  @override
  Widget build(BuildContext context) {{
    // Ensure controller is put in memory if not already
    Get.put({class_name}Controller());
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('{class_name} View'),
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
