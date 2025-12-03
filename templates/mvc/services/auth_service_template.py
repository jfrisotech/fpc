def get_auth_service_content() -> str:
    return '''
import '../models/user_model.dart';

class AuthService {
  Future<UserModel> login(String email, String password) async {
    await Future.delayed(Duration(seconds: 1));
    return UserModel(
      id: '1',
      name: 'Test User',
      email: email,
    );
  }
  
  Future<bool> register(String name, String email, String password) async {
    await Future.delayed(Duration(seconds: 1));
    return true;
  }
  
  Future<void> logout() async {
    await Future.delayed(Duration(milliseconds: 500));
  }
}
'''
