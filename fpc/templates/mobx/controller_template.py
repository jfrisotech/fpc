def get_mobx_controller_template(class_name: str) -> str:
    return f"""import 'package:mobx/mobx.dart';

part '{class_name.lower()}.g.dart';

class {class_name} = _{class_name} with _${class_name};

abstract class _{class_name} with Store {{
  @observable
  int value = 0;

  @action
  void increment() {{
    value++;
  }}
}}
"""
