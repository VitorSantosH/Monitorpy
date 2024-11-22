def hex_to_integer(hex_string):
    # Remove os zeros à esquerda
    trimmed_hex = hex_string.lstrip('0')
    
    # Pega apenas os últimos 8 caracteres hexadecimais (correspondente a 4 bytes)
    if len(trimmed_hex) > 8:
        trimmed_hex = trimmed_hex[-8:]
    
    # Converte o hexadecimal em bytes
    byte_array = bytearray.fromhex(trimmed_hex)
    
    # Converte os bytes para inteiro
    result = int.from_bytes(byte_array, byteorder='big')
    return result

# Testando a conversão
hex_string = "0000E5D15500"
output = hex_to_integer(hex_string)
print(output)
