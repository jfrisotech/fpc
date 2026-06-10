def get_provider_view_template(class_name: str, base_name: str = None) -> str:
    from fpc.core.utils import to_pascal_case, to_snake_case
    b_name = base_name or (class_name[:-4] if class_name.endswith('View') else class_name)
    controller_class = f"{to_pascal_case(b_name)}Controller"
    controller_file = f"{to_snake_case(b_name)}_controller.dart"
    
    view_class = class_name
    if not view_class.endswith('View'):
        view_class += 'View'

    return f"""import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/{controller_file}';

class {view_class} extends StatelessWidget {{
  const {view_class}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return ChangeNotifierProvider(
      create: (_) => {controller_class}(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('{view_class}'),
        ),
        body: Center(
          child: Consumer<{controller_class}>(
            builder: (context, controller, child) {{
              return Text('Value: ${{controller.value}}');
            }},
          ),
        ),
        floatingActionButton: Consumer<{controller_class}>(
          builder: (context, controller, child) {{
            return FloatingActionButton(
              onPressed: controller.increment,
              child: const Icon(Icons.add),
            );
          }},
        ),
      ),
    );
  }}
}}
"""
