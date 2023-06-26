from elftools.elf.elffile import ELFFile
import frida
import sys
from time import sleep

#questa non mi sembra utile
def generate_function_list(binary):
    """
    Generate a list of all the functions defined by the target executable.
    """
    functions = []
    with open(binary, "rb") as f:
        elf = ELFFile(f)
        for section in elf.iter_sections():
            if section.header.sh_type == 'SHT_SYMTAB':
                for symbol in section.iter_symbols():
                    if symbol.entry.st_info.type == 'STT_FUNC':
                        functions.append(symbol.name)
    return functions


def make_script(f):
    return """
            console.log('Called function '+DebugSymbol.getFunctionByName('"""+f+"""'))
            Interceptor.attach(DebugSymbol.getFunctionByName('"""+f+"""'), {
                onEnter: function (args) {
                    send({function: '"""+f+"""', args: args[0]})
                    console.log('onEnter function '+DebugSymbol.getFunctionByName('"""+f+"""'))
                },
                onLeave: function (retval) {
                	send({function: '"""+f+"""', ret: retval})
                    console.log('onLeave function '+DebugSymbol.getFunctionByName('"""+f+"""'))

                }
            });
        """

def trace_function_calls(binary, args):
    """
    Run the binary and trace function calls with their arguments.
    """
    entries = []
    function_list = generate_function_list(binary)

    def on_message(message, data):
        print(message)
        if message["type"] == "send" and message["payload"] != "done":
            #function_payload = message["payload"] #["function"]
            function_name = message["payload"]["function"]
            #TODO: cambiare
            try:
                function_args = message["payload"]["args"]
                io="input"
            except:
                function_args=message["payload"]["ret"]
                io="output"
            entries.append((function_name,function_args))

    # Run the binary
    process = frida.spawn(binary, argv=[binary] + args)

    sleep(1)

    session = frida.attach(process)
    script_txt=""
    for f in ['h','g','f']:
        script_txt+= make_script(f)
        script_txt+="\n"
    
    script = session.create_script(script_txt)
    script.on("message",on_message)
    script.load()

    frida.resume(process)

    # Wait for the script to complete
    #script.join()

    sleep(5)
    #sys.stdin.read()
    # Detach and clean up
    try:
        session.detach()
        #frida.kill(process)
    except Exception as e:
        print(e)

    return entries

# Usage example
binary_path = "./test/test"
arguments = ["arg1", "arg2", "arg3"]

entries = trace_function_calls(binary_path, arguments)


# Print the generated entries
for entry in entries:
    print(entry)
    function_name, function_args = entry
    print(f"Function: {function_name}")
    print(f"Arguments: {function_args}")
    print()
