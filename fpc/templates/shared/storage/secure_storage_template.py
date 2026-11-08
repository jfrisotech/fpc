def get_secure_storage_content() -> str:
    return '''import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorageService {
  static const String tokenKey = 'auth_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userKey = 'cached_user';

  final FlutterSecureStorage storage;

  SecureStorageService({FlutterSecureStorage? storageOverride})
      : storage = storageOverride ??
            const FlutterSecureStorage(
              aOptions: AndroidOptions(encryptedSharedPreferences: true),
              iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
            );

  Future<void> saveToken(String token) async =>
      await storage.write(key: tokenKey, value: token);

  Future<String?> getToken() async =>
      await storage.read(key: tokenKey);

  Future<void> deleteToken() async =>
      await storage.delete(key: tokenKey);

  Future<void> saveRefreshToken(String token) async =>
      await storage.write(key: refreshTokenKey, value: token);

  Future<String?> getRefreshToken() async =>
      await storage.read(key: refreshTokenKey);

  Future<void> saveUserJson(String userJson) async =>
      await storage.write(key: userKey, value: userJson);

  Future<String?> getUserJson() async =>
      await storage.read(key: userKey);

  Future<void> deleteUserJson() async =>
      await storage.delete(key: userKey);

  Future<void> clearAll() async =>
      await storage.deleteAll();
}
'''

