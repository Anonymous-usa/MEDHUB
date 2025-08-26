//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'appointment_request_create.g.dart';

/// AppointmentRequestCreate
///
/// Properties:
/// * [doctor] 
/// * [note] 
@BuiltValue()
abstract class AppointmentRequestCreate implements Built<AppointmentRequestCreate, AppointmentRequestCreateBuilder> {
  @BuiltValueField(wireName: r'doctor')
  int get doctor;

  @BuiltValueField(wireName: r'note')
  String? get note;

  AppointmentRequestCreate._();

  factory AppointmentRequestCreate([void updates(AppointmentRequestCreateBuilder b)]) = _$AppointmentRequestCreate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(AppointmentRequestCreateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<AppointmentRequestCreate> get serializer => _$AppointmentRequestCreateSerializer();
}

class _$AppointmentRequestCreateSerializer implements PrimitiveSerializer<AppointmentRequestCreate> {
  @override
  final Iterable<Type> types = const [AppointmentRequestCreate, _$AppointmentRequestCreate];

  @override
  final String wireName = r'AppointmentRequestCreate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    AppointmentRequestCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'doctor';
    yield serializers.serialize(
      object.doctor,
      specifiedType: const FullType(int),
    );
    if (object.note != null) {
      yield r'note';
      yield serializers.serialize(
        object.note,
        specifiedType: const FullType(String),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    AppointmentRequestCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required AppointmentRequestCreateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'doctor':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.doctor = valueDes;
          break;
        case r'note':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.note = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  AppointmentRequestCreate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = AppointmentRequestCreateBuilder();
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

