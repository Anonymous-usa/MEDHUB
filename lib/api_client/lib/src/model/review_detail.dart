//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'review_detail.g.dart';

/// ReviewDetail
///
/// Properties:
/// * [id] 
/// * [appointment] 
/// * [patientPhone] 
/// * [doctorPhone] 
/// * [rating] 
/// * [comment] 
/// * [createdAt] 
@BuiltValue()
abstract class ReviewDetail implements Built<ReviewDetail, ReviewDetailBuilder> {
  @BuiltValueField(wireName: r'id')
  int get id;

  @BuiltValueField(wireName: r'appointment')
  int get appointment;

  @BuiltValueField(wireName: r'patient_phone')
  String get patientPhone;

  @BuiltValueField(wireName: r'doctor_phone')
  String get doctorPhone;

  @BuiltValueField(wireName: r'rating')
  ReviewDetailRatingEnum get rating;
  // enum ratingEnum {  1,  2,  3,  4,  5,  };

  @BuiltValueField(wireName: r'comment')
  String? get comment;

  @BuiltValueField(wireName: r'created_at')
  DateTime get createdAt;

  ReviewDetail._();

  factory ReviewDetail([void updates(ReviewDetailBuilder b)]) = _$ReviewDetail;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ReviewDetailBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ReviewDetail> get serializer => _$ReviewDetailSerializer();
}

class _$ReviewDetailSerializer implements PrimitiveSerializer<ReviewDetail> {
  @override
  final Iterable<Type> types = const [ReviewDetail, _$ReviewDetail];

  @override
  final String wireName = r'ReviewDetail';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ReviewDetail object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'id';
    yield serializers.serialize(
      object.id,
      specifiedType: const FullType(int),
    );
    yield r'appointment';
    yield serializers.serialize(
      object.appointment,
      specifiedType: const FullType(int),
    );
    yield r'patient_phone';
    yield serializers.serialize(
      object.patientPhone,
      specifiedType: const FullType(String),
    );
    yield r'doctor_phone';
    yield serializers.serialize(
      object.doctorPhone,
      specifiedType: const FullType(String),
    );
    yield r'rating';
    yield serializers.serialize(
      object.rating,
      specifiedType: const FullType(ReviewDetailRatingEnum),
    );
    if (object.comment != null) {
      yield r'comment';
      yield serializers.serialize(
        object.comment,
        specifiedType: const FullType(String),
      );
    }
    yield r'created_at';
    yield serializers.serialize(
      object.createdAt,
      specifiedType: const FullType(DateTime),
    );
  }

  @override
  Object serialize(
    Serializers serializers,
    ReviewDetail object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ReviewDetailBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'id':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.id = valueDes;
          break;
        case r'appointment':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.appointment = valueDes;
          break;
        case r'patient_phone':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.patientPhone = valueDes;
          break;
        case r'doctor_phone':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.doctorPhone = valueDes;
          break;
        case r'rating':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ReviewDetailRatingEnum),
          ) as ReviewDetailRatingEnum;
          result.rating = valueDes;
          break;
        case r'comment':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.comment = valueDes;
          break;
        case r'created_at':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(DateTime),
          ) as DateTime;
          result.createdAt = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ReviewDetail deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ReviewDetailBuilder();
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

class ReviewDetailRatingEnum extends EnumClass {

  @BuiltValueEnumConst(wireNumber: 1)
  static const ReviewDetailRatingEnum number1 = _$reviewDetailRatingEnum_number1;
  @BuiltValueEnumConst(wireNumber: 2)
  static const ReviewDetailRatingEnum number2 = _$reviewDetailRatingEnum_number2;
  @BuiltValueEnumConst(wireNumber: 3)
  static const ReviewDetailRatingEnum number3 = _$reviewDetailRatingEnum_number3;
  @BuiltValueEnumConst(wireNumber: 4)
  static const ReviewDetailRatingEnum number4 = _$reviewDetailRatingEnum_number4;
  @BuiltValueEnumConst(wireNumber: 5)
  static const ReviewDetailRatingEnum number5 = _$reviewDetailRatingEnum_number5;

  static Serializer<ReviewDetailRatingEnum> get serializer => _$reviewDetailRatingEnumSerializer;

  const ReviewDetailRatingEnum._(String name): super(name);

  static BuiltSet<ReviewDetailRatingEnum> get values => _$reviewDetailRatingEnumValues;
  static ReviewDetailRatingEnum valueOf(String name) => _$reviewDetailRatingEnumValueOf(name);
}

