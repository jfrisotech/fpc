def get_app_spacing_content() -> str:
    return '''class AppSpacing {
  // Base spacing unit
  static const double unit = 8.0;
  
  // Spacing scale
  static const double xs = unit * 0.5;  // 4
  static const double sm = unit;        // 8
  static const double md = unit * 2;    // 16
  static const double lg = unit * 3;    // 24
  static const double xl = unit * 4;    // 32
  static const double xxl = unit * 6;   // 48
  static const double xxxl = unit * 8;  // 64
  
  // Common spacing values
  static const double padding = md;
  static const double margin = md;
  static const double gap = sm;
  
  // Component-specific spacing
  static const double cardPadding = md;
  static const double listItemPadding = md;
  static const double buttonPadding = md;
  static const double inputPadding = md;
  
  // Layout spacing
  static const double sectionSpacing = xl;
  static const double elementSpacing = md;
  static const double tightSpacing = sm;
}
'''
