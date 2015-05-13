import re
import sys

spaces_per_tab = 2

def remove_trailing(s):
    return s.strip()

def remove_double_spaces(s):
    return re.sub(r' +',' ',s)

def begin_position(s):
    """
    Return -1 if s is only spaces
    >>> begin_position(" aer")
    1
    >>> begin_position("aer")
    0
    >>> begin_position("   ")
    -1
    """
    i = 0
    while(i < s.__len__() and s[i] == ' '):
        i = i+1
    if i == s.__len__():
        return -1
    else:
        return i

def get_kws(s):
    """
    Get the (first) word of the line, if there is one
    >>> get_kws('ultimately show "random thing"')
    'ultimately'
    >>> get_kws('qed')
    'qed'
    >>> get_kws(' proof(')
    'proof'
    """
    s = s.strip()
    delimiters = ['"',' ','(']
    #index = [qm=s.find('"'),sp=s.find(' '),pa=s.find('(')]
    index = [s.find(a) for a in delimiters]
    index = [i for i in index if i != -1]
    if index != []:
        return s[0:min(index)].strip()
    else:
        return s[0:].strip()

def comment_depth(s, current):
    """
    Return the comment depth implied by this string
    We're gonna make some sane assumptions, namely that there are not more than
    one opening and one ending of a comment, and that there are in the good
    order.
    >>> comment_depth('text {* Random text', 0)
    1
    >>> comment_depth('text {* Random text *}', 1)
    1
    >>> comment_depth('show (* imba lemma ', 0)
    1
    >>> comment_depth(' imba lemma *) ', 1)
    0
    >>> comment_depth('proof (rule *)', 0)
    0
    """
    depth = current
    op = re.compile('|'.join(['{\*','\(\*']))
    cl = re.compile('|'.join(['\*}','\*\)']))
    if op.search(s):
        depth += 1
    if cl.search(s):
        depth -= 1
    if 0 <= depth:
        return depth
    else:
        return 0

def or_re(patterns):
    return re.compile('|'.join(patterns))

def adjust_indent(s):
    """
    Tells how the indent level has to be changed
    >>> adjust_indent("proof azer")
    (1, 0)
    >>> adjust_indent("qed")
    (-1, -1)
    >>> adjust_indent("proof (induct H rule: finite_induct)") == adjust_indent("proof")
    True
    >>> adjust_indent('m)" (is "?fin \<Longrightarrow> ?s1 = (\<Sum> m=0..<bd. ?ff m H)")')
    (0, 0)
    """
    noindent_kw = ['lemma','theory','imports','begin','subsection','type_synonym','locale','definition','abbreviation','theorem','end','shows']
    #Indent what follows, not the line itself
    indent_kw = ['proof','proof-']
    #Deindent what follows, and the line itself
    deindent_kw = ['qed',' next']
    indent_tmp_kw = [
        'assumes','shows','fixes','and','"'
    ]
    db_indent_tmp_kw = ['by','using','unfolding']
    deindent_tmp_kw = ['next']
    pnoin = or_re(noindent_kw)
    pin = or_re(indent_kw)
    pdein = or_re(deindent_kw)
    pin_tmp = or_re(indent_tmp_kw)
    pdbin_tmp = or_re(db_indent_tmp_kw)
    pdein_tmp = or_re(deindent_tmp_kw)
    kw = get_kws(s)
    if(pnoin.search(kw)):
        return 0, 0
    if pdein.search(kw):
        return -1, -1
    if pin.search(kw):
        return 1, 0
    if pin_tmp.search(kw):
        return 0, 1
    if pdbin_tmp.search(kw):
        return 0, 2
    if pdein_tmp.search(kw):
        return 0, -1
    return 0, 1

def indent(s,indent_level,spaces_per_tab):
    """
    >>> indent("i",2,2)
    '    i'
    """
    if(indent_level < 0):
        raise Exception
    spaces = ""
    """
    for i in range(0,indent_level*spaces_per_tab):
        spaces = ''.join([' ',spaces])
    """
    spaces = ' '*indent_level*spaces_per_tab
    return ''.join([spaces,s])

def process_line(s,indent):
    return new_s


def main(fname):
    #fname = "Shannon.thy"
    global spaces_per_tab
    indent_level = 0
    is_comment_or_text = False
    com_depth = 0
    with open(fname) as f:
        content = f.read().splitlines()
        #print(content)
        content_mod = []
        for line in content:
            line = remove_double_spaces(line)
            line = remove_trailing(line)
            if(not line.__len__() == 0):
                new_com_depth = comment_depth(line, com_depth)
                if com_depth != new_com_depth or 0 < com_depth:
                    adj = (0,0)
                else:
                    adj = adjust_indent(line)
                com_depth = max(0, new_com_depth)
                line = indent(line,indent_level + adj[1],spaces_per_tab)
                indent_level = indent_level + adj[0]
            content_mod.append(line)
            #print(indent_level)
            print(line)
        #print(content)
    return

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        import doctest
        doctest.testmod()
    else:
        main(args[0])