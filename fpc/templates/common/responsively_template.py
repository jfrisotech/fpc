def get_responsively_content() -> str:
    return '''import 'package:flutter/material.dart';

/// [Responsively] handles dynamic screen responsiveness and orientation adaptations.
/// It uses reference mockup dimensions (default: 430x932) to compute proportional sizes.
class Responsively {
  static const double mockupWidth = 430.0;
  static const double mockupHeight = 932.0;

  static double width(double size, MediaQueryData mediaQueryData) {
    final mediaQuerySize = mediaQueryData.size;
    final coefficient = size / mockupWidth;
    return mediaQuerySize.width * coefficient;
  }

  static double height(double size, MediaQueryData data) {
    final mediaQuerySize = data.size;
    final coefficient = size / mockupHeight;
    return mediaQuerySize.height * coefficient;
  }

  static double auto(double size, MediaQueryData data) {
    final widthVal = data.size.width;
    final heightVal = data.size.height;

    return widthVal > heightVal
        ? width(size, data)
        : height(size, data);
  }
}

/// Extension on [BuildContext] for responsive measurements and orientation helpers.
extension ResponsiveContext on BuildContext {
  MediaQueryData get mediaQuery => MediaQuery.of(this);
  Size get screenSize => mediaQuery.size;
  double get screenWidth => screenSize.width;
  double get screenHeight => screenSize.height;
  Orientation get orientation => mediaQuery.orientation;

  bool get isLandscape => orientation == Orientation.landscape;
  bool get isPortrait => orientation == Orientation.portrait;

  /// Responsive value scaling automatically based on orientation
  double resp(double size) => Responsively.auto(size, mediaQuery);

  /// Responsive width proportional to mockup width
  double respW(double size) => Responsively.width(size, mediaQuery);

  /// Responsive height proportional to mockup height
  double respH(double size) => Responsively.height(size, mediaQuery);
}

/// A declarative widget to build distinct layouts for Portrait and Landscape orientations,
/// ensuring full compatibility with Android 16+ resizable/foldable standards.
class OrientationLayout extends StatelessWidget {
  final Widget Function(BuildContext context) portrait;
  final Widget Function(BuildContext context) landscape;

  const OrientationLayout({
    super.key,
    required this.portrait,
    required this.landscape,
  });

  @override
  Widget build(BuildContext context) {
    return OrientationBuilder(
      builder: (context, orientation) {
        if (orientation == Orientation.landscape) {
          return landscape(context);
        }
        return portrait(context);
      },
    );
  }
}
'''

