def get_bloc_controller_template(class_name: str) -> str:
    base_class = class_name[:-10] if class_name.endswith('Controller') else class_name
    return f"""import 'package:flutter_bloc/flutter_bloc.dart';

// Events
abstract class {base_class}Event {{}}

class {base_class}Increment extends {base_class}Event {{}}

// States
abstract class {base_class}State {{}}

class {base_class}Initial extends {base_class}State {{}}

class {base_class}Loaded extends {base_class}State {{
  final int value;
  {base_class}Loaded(this.value);
}}

// Bloc
class {base_class}Bloc extends Bloc<{base_class}Event, {base_class}State> {{
  {base_class}Bloc() : super({base_class}Initial()) {{
    on<{base_class}Increment>((event, emit) {{
      // TODO: Implement logic
      emit({base_class}Loaded(1));
    }});
  }}
}}
"""
