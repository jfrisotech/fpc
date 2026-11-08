def get_app_assets_content() -> str:
    """Return type-safe AppAssets constants for images and icons."""
    return '''class AppAssets {
  AppAssets._();

  // Images
  static const String imagesPath = 'assets/images';
  static const String logo = '$imagesPath/logo.png';
  static const String placeholder = '$imagesPath/placeholder.png';

  // Icons
  static const String iconsPath = 'assets/icons';
  static const String appIcon = '$iconsPath/app_icon.png';
}
'''

