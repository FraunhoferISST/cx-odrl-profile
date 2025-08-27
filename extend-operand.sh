#!/usr/bin/env bash
#
# enhanced transform-schema.sh to parse $comment JSON string into object

INPUT="$1"
OUTPUT="${2:-schema.transformed.json}"

jq '
  def move_string_attrs(obj):
    (
      [ "pattern","minLength","maxLength","format","enum","const","default","examples","description" ] 
      | map(
          if obj[.] != null then
            { (.): { "type": (if . == "enum" then "array" else "string" end), "const": obj[.] } }
          else {} end
        )
      | add
      + (if obj["$comment"] != null 
          then { legalText: { type: "object", properties: (obj["$comment"] | fromjson?) } } 
          else {} 
        end)
    );

  def move_integer_attrs(obj):
    (
      [ "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf", "enum", "const", "default", "examples", "description" ]
      | map(
          if obj[.] != null then
            { (.): { "type": (if . == "enum" then "array" else "integer" end), "const": obj[.] } }
          else {} end
        )
      | add
      + (if obj["$comment"] != null 
          then { legalText: { type: "object", properties: (obj["$comment"] | fromjson?) } }
          else {} 
        end)
    );

  .definitions |= with_entries(
    if (.key | endswith("RightOperand")) and (.value.type == "string") then
      .value as $orig 
      | .value = {
          type: "object",
          properties: move_string_attrs($orig) + { operandType: { type: "string", const: "string" } },
          additionalProperties: false
        }
    elif (.key | endswith("RightOperand")) and (.value.type == "integer") then
      .value as $orig
      | .value = {
          type: "object",
          properties: move_integer_attrs($orig) + { operandType: { type: "string", const: "integer" } },
          additionalProperties: false
        }
    else
      .
    end
  )
  | .definitions |= map_values(del(.required))
' "$INPUT" > "$OUTPUT"

echo "✅ Transformed schema written to $OUTPUT"
