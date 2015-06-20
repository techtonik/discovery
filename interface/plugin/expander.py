def expand(text, needle, replacement):
    """replace `needle` with replacement preserving indentation"""
    output = []
    repl = replacement.splitlines(True)
    for i, line in enumerate(text.splitlines(True)):
        pos = line.find(needle)
        #print i, repr(pos)
        if pos == -1:
            output.append(line)
        else:
            # add first line of replacement
            outline = [line[0:pos], repl[0]]
            if len(replacement) == 1:
                outline.append(line[pos+len(needle):])
            else:
                # [ ] copy whitespace symbols
                indent = ' '*pos
                for rep in repl[1:]:
                    outline.append(indent)
                    outline.append(rep)
                outline.append(line[pos+len(needle):])
            output.append(''.join(outline))
    return ''.join(output)
