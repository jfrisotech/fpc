def get_provider_view_template(class_name: str) -> str:
    return f"""import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../controllers/{class_name.lower()}_controller.dart';

class {class_name}View extends StatelessWidget {{
  const {class_name}View({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return ChangeNotifierProvider(
      create: (_) => {class_name}Controller(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('{class_name} View'),
        ),
        body: Center(
          child: Consumer<{class_name}Controller>(
            builder: (context, controller, child) {{
              return Text('Value: ${{controller.value}}');
            }},
          ),
        ),
        floatingActionButton: Consumer<{class_name}Controller>(
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
