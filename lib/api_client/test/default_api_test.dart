import 'package:test/test.dart';
import 'package:medhub_api/medhub_api.dart';


/// tests for DefaultApi
void main() {
  final instance = MedhubApi().getDefaultApi();

  group(DefaultApi, () {
    // Список учреждений (публичный)
    //
    //Future<BuiltList<InstitutionPublic>> apiV1InstitutionsGet() async
    test('test apiV1InstitutionsGet', () async {
      // TODO
    });

    // Детальная информация об учреждении
    //
    //Future<InstitutionPublic> apiV1InstitutionsIdGet(int id) async
    test('test apiV1InstitutionsIdGet', () async {
      // TODO
    });

    // Список записей пациента
    //
    //Future<BuiltList<AppointmentRequestDetail>> apiV1PatientAppointmentsGet() async
    test('test apiV1PatientAppointmentsGet', () async {
      // TODO
    });

    // Новая запись на приём
    //
    //Future<AppointmentRequestCreate> apiV1PatientAppointmentsPost(AppointmentRequestCreate appointmentRequestCreate) async
    test('test apiV1PatientAppointmentsPost', () async {
      // TODO
    });

    // Список отзывов текущего пациента
    //
    //Future<BuiltList<ReviewDetail>> apiV1PatientReviewsGet() async
    test('test apiV1PatientReviewsGet', () async {
      // TODO
    });

    // Оставить отзыв
    //
    //Future<ReviewCreate> apiV1PatientReviewsPost(ReviewCreate reviewCreate) async
    test('test apiV1PatientReviewsPost', () async {
      // TODO
    });

    // Профиль текущего пользователя
    //
    //Future<Profile> apiV1ProfileGet() async
    test('test apiV1ProfileGet', () async {
      // TODO
    });

    // Обновить профиль текущего пользователя
    //
    //Future<Profile> apiV1ProfilePut(Profile profile) async
    test('test apiV1ProfilePut', () async {
      // TODO
    });

    // Регистрация нового пациента
    //
    //Future<PatientRegister> apiV1RegisterPatientPost(PatientRegister patientRegister) async
    test('test apiV1RegisterPatientPost', () async {
      // TODO
    });

    // Получить пару JWT-токенов
    //
    //Future<TokenObtain> apiV1TokenPost(TokenObtain tokenObtain) async
    test('test apiV1TokenPost', () async {
      // TODO
    });

    // Обновить access-токен по refresh-токену
    //
    //Future<TokenRefreshResponse> apiV1TokenRefreshPost(TokenRefreshRequest tokenRefreshRequest) async
    test('test apiV1TokenRefreshPost', () async {
      // TODO
    });

  });
}
