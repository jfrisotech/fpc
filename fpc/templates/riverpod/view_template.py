def get_riverpod_view_template(class_name: str, base_name: str) -> str:
    provider_name = f"{base_name.lower()}Provider"
    return f"""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../controllers/{base_name.lower()}_controller.dart';

class {class_name} extends ConsumerWidget {{
  const {class_name}({{super.key}});

  @override
  Widget build(BuildContext context, WidgetRef ref) {{
    final value = ref.watch({provider_name});
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('{class_name}'),
      ),
      body: Center(
        child: Text('Value: $value'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {{
          ref.read({provider_name}.notifier).increment();
        }},
        child: const Icon(Icons.add),
      ),
    );
  }}
}}
"""
