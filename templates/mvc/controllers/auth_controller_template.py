def get_auth_controller_content() -> str:
    return '''
import '../models/user_model.dart';
import '../services/auth_service.dart';

class AuthController {
  final AuthService _authService = AuthService();
  
  Future<UserModel?> login(String email, String password) async {
    try {
      return await _authService.login(email, password);
    } catch (e) {
      print('Login error: $e');
      return null;
    }
  }
  
  Future<bool> register(String name, String email, String password) async {
    try {
      return await _authService.register(name, email, password);
    } catch (e) {
      print('Registration error: $e');
      return false;
    }
  }
  
  Future<void> logout() async {
    try {
      await _authService.logout();
    } catch (e) {
      print('Logout error: $e');
    }
  }
}
'''
