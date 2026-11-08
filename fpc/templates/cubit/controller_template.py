def get_cubit_controller_template(class_name: str, name: str = None, preferences: dict = None) -> str:
    base_class = class_name
    for suffix in ['Controller', 'ViewModel', 'Cubit']:
        if base_class.endswith(suffix):
            base_class = base_class[:-len(suffix)]
            break

    return f"""import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';

// States
abstract class {base_class}State extends Equatable {{
  const {base_class}State();

  @override
  List<Object?> get props => [];
}}

class {base_class}Initial extends {base_class}State {{
  const {base_class}Initial();
}}

class {base_class}Loading extends {base_class}State {{
  const {base_class}Loading();
}}

class {base_class}Loaded extends {base_class}State {{
  final int value;

  const {base_class}Loaded(this.value);

  @override
  List<Object?> get props => [value];
}}

class {base_class}Error extends {base_class}State {{
  final String message;

  const {base_class}Error(this.message);

  @override
  List<Object?> get props => [message];
}}

// Cubit
class {base_class}Cubit extends Cubit<{base_class}State> {{
  {base_class}Cubit() : super(const {base_class}Initial());

  void increment() {{
    // TODO: Implement logic
    emit(const {base_class}Loaded(1));
  }}
}}
"""

