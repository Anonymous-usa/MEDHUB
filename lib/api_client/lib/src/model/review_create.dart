//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//

// ignore_for_file: unused_element
import 'package:built_collection/built_collection.dart';
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';

part 'review_create.g.dart';

/// ReviewCreate
///
/// Properties:
/// * [appointment] 
/// * [rating] 
/// * [comment] 
@BuiltValue()
abstract class ReviewCreate implements Built<ReviewCreate, ReviewCreateBuilder> {
  @BuiltValueField(wireName: r'appointment')
  int get appointment;

  @BuiltValueField(wireName: r'rating')
  ReviewCreateRatingEnum get rating;
  // enum ratingEnum {  1,  2,  3,  4,  5,  };

  @BuiltValueField(wireName: r'comment')
  String? get comment;

  ReviewCreate._();

  factory ReviewCreate([void updates(ReviewCreateBuilder b)]) = _$ReviewCreate;

  @BuiltValueHook(initializeBuilder: true)
  static void _defaults(ReviewCreateBuilder b) => b;

  @BuiltValueSerializer(custom: true)
  static Serializer<ReviewCreate> get serializer => _$ReviewCreateSerializer();
}

class _$ReviewCreateSerializer implements PrimitiveSerializer<ReviewCreate> {
  @override
  final Iterable<Type> types = const [ReviewCreate, _$ReviewCreate];

  @override
  final String wireName = r'ReviewCreate';

  Iterable<Object?> _serializeProperties(
    Serializers serializers,
    ReviewCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) sync* {
    yield r'appointment';
    yield serializers.serialize(
      object.appointment,
      specifiedType: const FullType(int),
    );
    yield r'rating';
    yield serializers.serialize(
      object.rating,
      specifiedType: const FullType(ReviewCreateRatingEnum),
    );
    if (object.comment != null) {
      yield r'comment';
      yield serializers.serialize(
        object.comment,
        specifiedType: const FullType(String),
      );
    }
  }

  @override
  Object serialize(
    Serializers serializers,
    ReviewCreate object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    return _serializeProperties(serializers, object, specifiedType: specifiedType).toList();
  }

  void _deserializeProperties(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
    required List<Object?> serializedList,
    required ReviewCreateBuilder result,
    required List<Object?> unhandled,
  }) {
    for (var i = 0; i < serializedList.length; i += 2) {
      final key = serializedList[i] as String;
      final value = serializedList[i + 1];
      switch (key) {
        case r'appointment':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(int),
          ) as int;
          result.appointment = valueDes;
          break;
        case r'rating':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(ReviewCreateRatingEnum),
          ) as ReviewCreateRatingEnum;
          result.rating = valueDes;
          break;
        case r'comment':
          final valueDes = serializers.deserialize(
            value,
            specifiedType: const FullType(String),
          ) as String;
          result.comment = valueDes;
          break;
        default:
          unhandled.add(key);
          unhandled.add(value);
          break;
      }
    }
  }

  @override
  ReviewCreate deserialize(
    Serializers serializers,
    Object serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = ReviewCreateBuilder();
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

class ReviewCreateRatingEnum extends EnumClass {

  @BuiltValueEnumConst(wireNumber: 1)
  static const ReviewCreateRatingEnum number1 = _$reviewCreateRatingEnum_number1;
  @BuiltValueEnumConst(wireNumber: 2)
  static const ReviewCreateRatingEnum number2 = _$reviewCreateRatingEnum_number2;
  @BuiltValueEnumConst(wireNumber: 3)
  static const ReviewCreateRatingEnum number3 = _$reviewCreateRatingEnum_number3;
  @BuiltValueEnumConst(wireNumber: 4)
  static const ReviewCreateRatingEnum number4 = _$reviewCreateRatingEnum_number4;
  @BuiltValueEnumConst(wireNumber: 5)
  static const ReviewCreateRatingEnum number5 = _$reviewCreateRatingEnum_number5;

  static Serializer<ReviewCreateRatingEnum> get serializer => _$reviewCreateRatingEnumSerializer;

  const ReviewCreateRatingEnum._(String name): super(name);

  static BuiltSet<ReviewCreateRatingEnum> get values => _$reviewCreateRatingEnumValues;
  static ReviewCreateRatingEnum valueOf(String name) => _$reviewCreateRatingEnumValueOf(name);
}

