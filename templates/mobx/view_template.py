def get_mobx_view_template(class_name: str) -> str:
    return f"""import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import '../controllers/{class_name.lower()}_controller.dart';

class {class_name}View extends StatelessWidget {{
  final {class_name}Controller controller = {class_name}Controller();

  {class_name}View({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('{class_name} View'),
      ),
      body: Center(
        child: Observer(
          builder: (_) {{
            return Text('Value: ${{controller.value}}');
          }},
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: controller.increment,
        child: const Icon(Icons.add),
      ),
    );
  }}
}}
"""
