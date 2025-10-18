import base64
import zlib


def decode_protobuf(base64_string, protobuf_object: object):

    try:
        compressed_bytes = base64.b64decode(base64_string)
        protobuf_binary = zlib.decompress(compressed_bytes)
    except zlib.error as e:
        # If standard zlib fails, try with the 'wbits' parameter for gzip headers
        if "header" in str(e):
            # wbits=32+MAX_WBITS handles both zlib and gzip headers
            protobuf_binary = zlib.decompress(compressed_bytes, wbits=32) 
        else:
            raise ValueError("Unable to decompress protobuf")
        
    protobuf_object.ParseFromString(protobuf_binary)

    return protobuf_object



