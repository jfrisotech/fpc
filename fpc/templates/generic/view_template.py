def get_view_template(class_name: str) -> str:
    return f"""import 'package:flutter/material.dart';

class {class_name} extends StatelessWidget {{
  const {class_name}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('{class_name}'),
      ),
      body: Center(
        child: Text('This is the {class_name}.'),
      ),
    );
  }}
}}
"""
