def get_riverpod_view_template(class_name: str) -> str:
    return f"""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../controllers/{class_name.lower()}_controller.dart';

class {class_name}View extends ConsumerWidget {{
  const {class_name}View({{super.key}});

  @override
  Widget build(BuildContext context, WidgetRef ref) {{
    final value = ref.watch({class_name.lower()}Provider);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('{class_name} View'),
      ),
      body: Center(
        child: Text('Value: $value'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {{
          ref.read({class_name.lower()}Provider.notifier).increment();
        }},
        child: const Icon(Icons.add),
      ),
    );
  }}
}}
"""
