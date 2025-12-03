def get_riverpod_controller_template(class_name: str) -> str:
    return f"""import 'package:flutter_riverpod/flutter_riverpod.dart';

final {class_name.lower()}Provider = StateNotifierProvider<{class_name}Controller, int>((ref) {{
  return {class_name}Controller();
}});

class {class_name}Controller extends StateNotifier<int> {{
  {class_name}Controller() : super(0);

  void increment() {{
    state++;
  }}
}}
"""
