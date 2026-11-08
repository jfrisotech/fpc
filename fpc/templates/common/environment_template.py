def get_environment_content() -> str:
    """Return type-safe Environment configuration for multi-environments via --dart-define."""
    return '''enum AppEnvironment {
  dev,
  staging,
  prod,
}

class Environment {
  const Environment._();

  /// Environment identifier passed via `--dart-define=ENV=dev|staging|prod`
  static const String name = String.fromEnvironment(
    'ENV',
    defaultValue: 'dev',
  );

  /// API Base URL passed via `--dart-define=API_URL=https://...`
  static const String apiBaseUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'https://api.dev.example.com',
  );

  /// Logging toggle passed via `--dart-define=ENABLE_LOGGING=true|false`
  static const bool enableLogging = bool.fromEnvironment(
    'ENABLE_LOGGING',
    defaultValue: true,
  );

  /// Parsed current environment
  static AppEnvironment get current {
    switch (name.toLowerCase()) {
      case 'prod':
      case 'production':
        return AppEnvironment.prod;
      case 'staging':
      case 'stage':
        return AppEnvironment.staging;
      case 'dev':
      case 'development':
      default:
        return AppEnvironment.dev;
    }
  }

  static bool get isProduction => current == AppEnvironment.prod;
  static bool get isDevelopment => current == AppEnvironment.dev;
  static bool get isStaging => current == AppEnvironment.staging;
}
'''

