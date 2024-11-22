def hex_to_integer(hex_string):
    # Remove os zeros à esquerda
    trimmed_hex = hex_string.lstrip('0')
    print(f"Hex sem zeros à esquerda: {trimmed_hex}")
    
    # Converter a string hexadecimal para um array de bytes
    byte_array = bytes.fromhex(trimmed_hex)
    
    # Reverter a ordem dos bytes
    reversed_byte_array = bytes(reversed(byte_array))
    print(f"Array de bytes invertido: {reversed_byte_array}")
    
    # Converter o array de bytes invertido para um número inteiro
    integer_value = int.from_bytes(reversed_byte_array, byteorder='big')
    print(f"Valor inteiro: {integer_value}")
    
    return integer_value


# Testando a conversão
hex_string = "0000E5D15500"
output = hex_to_integer(hex_string)
print(output)
