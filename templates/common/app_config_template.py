def get_app_config_content(preferences: dict) -> str:
    baas = preferences['baas']
    config_content = '''
class AppConfig {
'''
    if baas == 'Firebase':
        config_content += '''
  // Firebase configuration is handled by firebase_options.dart
'''
    elif baas == 'Supabase':
        config_content += '''
  static const String supabaseUrl = 'YOUR_SUPABASE_URL';
  static const String supabaseAnonKey = 'YOUR_SUPABASE_ANON_KEY';
'''
    elif baas == 'Appwrite':
        config_content += '''
  static const String appwriteEndpoint = 'YOUR_APPWRITE_ENDPOINT';
  static const String appwriteProjectId = 'YOUR_APPWRITE_PROJECT_ID';
'''
    
    config_content += '''
  // Add more app configuration here
}
'''
    return config_content
