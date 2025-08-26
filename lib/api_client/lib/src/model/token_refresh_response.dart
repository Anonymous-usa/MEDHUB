//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'token_refresh_response.g.dart';

/// TokenRefreshResponse
///
/// Properties:
/// * [access] - Новый access-токен
@BuiltValue()
abstract class TokenRefreshResponse implements Built<TokenRefreshResponse, TokenRefreshResponseBuilder> {
  /// Новый access-токен
  @BuiltValueField(wireName: r'access')
  String get access;

  TokenRefreshResponse._();

  factory TokenRefreshResponse([void updates(TokenRefreshResponseBuilder b)]) = _$TokenRefreshResponse;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(TokenRefreshResponseBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<TokenRefreshResponse> get serializer => _$TokenRefreshResponseSerializer();
}

class _$TokenRefreshResponseSerializer implements PrimitiveSerializer<TokenRefreshResponse> {
  @override
  final Iterable<Type> types = const [TokenRefreshResponse, _$TokenRefreshResponse];

  @override
  final String wireName = r'TokenRefreshResponse';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    TokenRefreshResponse object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'access';
    yield serializers.serialize(
      object.access,
      specifiedType: const FullType(String),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    TokenRefreshResponse object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required TokenRefreshResponseBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'access':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.access = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  TokenRefreshResponse deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = TokenRefreshResponseBuilder();
    final serializedList = (serialized as Iterable<Object?>).toList();
    final unhandled = <Object?>[];
    _deserializeProperties(
      serializers,
      serialized,
      specifiedType: specifiedType,
      serializedList: serializedList,
      unhandled: unhandled,
      result: result,
    );
    return result.build();
  }
}

