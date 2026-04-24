def get_app_dimensions_content() -> str:
    return '''class AppDimensions {
  // Border radius
  static const double radiusXs = 2.0;
  static const double radiusSm = 4.0;
  static const double radiusMd = 8.0;
  static const double radiusLg = 12.0;
  static const double radiusXl = 16.0;
  static const double radiusXxl = 24.0;
  static const double radiusRound = 999.0;
  
  // Icon sizes
  static const double iconXs = 16.0;
  static const double iconSm = 20.0;
  static const double iconMd = 24.0;
  static const double iconLg = 32.0;
  static const double iconXl = 48.0;
  
  // Button dimensions
  static const double buttonHeightSm = 32.0;
  static const double buttonHeightMd = 40.0;
  static const double buttonHeightLg = 48.0;
  static const double buttonMinWidth = 64.0;
  
  // Input dimensions
  static const double inputHeight = 48.0;
  static const double inputBorderWidth = 1.0;
  
  // Card dimensions
  static const double cardElevation = 2.0;
  static const double cardBorderRadius = radiusMd;
  
  // Avatar sizes
  static const double avatarSm = 32.0;
  static const double avatarMd = 48.0;
  static const double avatarLg = 64.0;
  static const double avatarXl = 96.0;
  
  // Divider
  static const double dividerThickness = 1.0;
  
  // AppBar
  static const double appBarHeight = 56.0;
  
  // Bottom navigation
  static const double bottomNavHeight = 56.0;
}
'''
