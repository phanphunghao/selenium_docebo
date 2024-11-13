import json
import re

json_str = """
{
  "data": {
    "id_board": 0,
    "name": {
      "type": "single_value",
      "value": "string",
      "values": {
        "en": "string"
      }
    },
    "is_active": "true",
    "default": "true",
    "is_visible": "true",
    "anonymity": "true",
    "visible_by": {
      "selection": "all",
      "groups": "",
      "branches": ""
    },
    "badges": "",
    "time_validity": ""false"",
    "start_date": "string",
    "end_date": "string"
  },
  "version": "string",
  "_links": ""
}
""".replace("true", "\"true\"")\
    .replace("false", "\"false\"")


j = json.loads(json_str)
