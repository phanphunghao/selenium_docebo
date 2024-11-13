# unflat_json = {
#   "data": {
#     "uploaded": True
#   },
#   "version": "string",
#   "_links": {
#     "self": {
#       "href": "string"
#     },
#     "goto": {
#       "href": "string"
#     },
#     "first": {
#       "href": "string"
#     },
#     "last": {
#       "href": "string"
#     }
#   }
# }
 
def flatten_json(y):
    out = {}
 
    def flatten(x, name=''):
        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + ':')
        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + ':')
                i += 1
        else:
            out[name[:-1]] = x
 
    flatten(y)
    return out
 
 
# Driver code
# print(flatten_json(unflat_json))