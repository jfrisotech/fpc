def get_provider_controller_template(class_name: str) -> str:
    return f"""import 'package:flutter/foundation.dart';

class {class_name}Controller extends ChangeNotifier {{
  int _value = 0;
  int get value => _value;

  void increment() {{
    _value++;
    notifyListeners();
  }}
}}
"""
