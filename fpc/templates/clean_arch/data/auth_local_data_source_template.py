def get_auth_local_data_source_content() -> str:
    return '''import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/user_model.dart';

abstract class AuthLocalDataSource {
  Future<void> cacheUser(UserModel user);
  Future<UserModel?> getLastUser();
  Future<void> cacheToken(String token);
  Future<String?> getToken();
  Future<void> clearCache();
}

class AuthLocalDataSourceImpl implements AuthLocalDataSource {
  static const String _userKey = 'cached_user';
  static const String _tokenKey = 'auth_token';

  final FlutterSecureStorage secureStorage;

  AuthLocalDataSourceImpl([FlutterSecureStorage? storage])
      : secureStorage = storage ??
            const FlutterSecureStorage(
              aOptions: AndroidOptions(encryptedSharedPreferences: true),
              iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
            );

  @override
  Future<void> cacheUser(UserModel user) async {
    await secureStorage.write(
      key: _userKey,
      value: jsonEncode(user.toJson()),
    );
  }

  @override
  Future<UserModel?> getLastUser() async {
    final jsonString = await secureStorage.read(key: _userKey);
    if (jsonString != null) {
      try {
        return UserModel.fromJson(jsonDecode(jsonString) as Map<String, dynamic>);
      } catch (_) {
        return null;
      }
    }
    return null;
  }

  @override
  Future<void> cacheToken(String token) async {
    await secureStorage.write(key: _tokenKey, value: token);
  }

  @override
  Future<String?> getToken() async {
    return await secureStorage.read(key: _tokenKey);
  }

  @override
  Future<void> clearCache() async {
    await secureStorage.delete(key: _userKey);
    await secureStorage.delete(key: _tokenKey);
  }
}
'''

