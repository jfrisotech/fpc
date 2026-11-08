def get_user_model_content(preferences: dict = None) -> str:
    imports = []
    parts = []
    annotations = []
    
    if preferences:
        database = preferences.get('database')
        baas = preferences.get('baas')
            
        if database == 'ObjectBox':
            imports.append("import 'package:objectbox/objectbox.dart';")
            annotations.append("@Entity()")
            
        if baas == 'Firebase':
            imports.append("import 'package:cloud_firestore/cloud_firestore.dart';")

    imports_str = '\n'.join(imports) + ('\n\n' if imports else '')
    parts_str = '\n'.join(parts) + ('\n\n' if parts else '')
    annotations_str = '\n'.join(annotations) + ('\n' if annotations else '')
    
    db_id_field = ""
    if database == 'ObjectBox':
        db_id_field = "  @Id()\n  int localId = 0;\n"

    return f'''{imports_str}{parts_str}{annotations_str}class UserModel {{
{db_id_field}  final String uid;
  final String name;
  final String email;

  UserModel({{
    required this.uid,
    required this.name,
    required this.email,
  }});

  factory UserModel.fromJson(Map<String, dynamic> json) {{
    return UserModel(
      uid: json['uid'] ?? json['id'] ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
    );
  }}

  Map<String, dynamic> toJson() {{
    return {{
      'uid': uid,
      'name': name,
      'email': email,
    }};
  }}
}}
'''
