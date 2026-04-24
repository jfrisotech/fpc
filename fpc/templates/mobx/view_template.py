def get_mobx_view_template(class_name: str, base_name: str) -> str:
    from fpc.core.utils import to_pascal_case
    controller_name = f"{to_pascal_case(base_name)}Controller"
    return f"""import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import '../controllers/{base_name.lower()}_controller.dart';

class {class_name} extends StatelessWidget {{
  final {controller_name} controller = {controller_name}();

  {class_name}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('{class_name}'),
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
