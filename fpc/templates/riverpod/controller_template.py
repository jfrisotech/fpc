def get_riverpod_controller_template(class_name: str) -> str:
    return f"""import 'package:flutter_riverpod/flutter_riverpod.dart';

final {class_name.lower()}Provider = StateNotifierProvider<{class_name}, int>((ref) {{
  return {class_name}();
}});

class {class_name} extends StateNotifier<int> {{
  {class_name}() : super(0);

  void increment() {{
    state++;
  }}
}}
"""
