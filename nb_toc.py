import nbformat
import json
import re

# got this from http://code.activestate.com/recipes/81611-roman-numerals/ <<< tyvm!
def int_to_roman(input): 
   ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
   nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
   result = ""
   for i in range(len(ints)):
      count = int(input / ints[i])
      result += nums[i] * count
      input -= ints[i] * count
   return result   

def __read_nb__(filename):
    """returns the notebook as a dictionary"""
    with open(filename) as f:
        notebook = json.load(f)
        f.close()
    return notebook

def __write_nb__(filename, contents):
    with open(filename, 'w') as outfile:
        json.dump(contents, outfile)

def __remove_anchors__(string):
    return re.sub(' <a id=".+"></a>', '', string)

def generate(filename, title='Table of Contents', additional_text=None, indent_size=8, ignore_lower=0, ignore_upper=7):

    notebook = __read_nb__(filename)

    tag_num = 0
    toc_text = ['# {}\n'.format(title), '\n']
    level_count = [1] * 6 # six potential header levels
    last_level = 0 # the index of the last level that you were on
    indent = '&nbsp;' * indent_size # how big the indentation for each level should be

    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            line_num = 0
            for line in cell['source']:
                # from beginning of line, up to 3 whitespaces, between 1 and 6 #'s
                c = re.match('^[\W]{0,3}#{1,6}', line)

                if c:
                    # figuring out the number of #'s
                    level = c.group(0).count('#')
                    
                    if level > ignore_lower and level < ignore_upper:
                        level = level - ignore_lower - 1
                        # removing newline from end of line
                        if line.endswith('\n'):
                            line = line[:-1]

                        # creating all of the text to add
                        title = line[len(c.group(0)) + 1:] # removing the #'s from the beginning
                        title = '[{}]'.format(title)
                        indentation = level * indent

                        # figuring out the correct level
                        if last_level > level:
                            for i in range(level+1, last_level+1):
                                level_count[i] = 1
                        last_level = level
                        numeral = int_to_roman(level_count[level])
                        numeral = '{}. '.format(numeral)
                        level_count[level] += 1

                        # concatenating and appending to toc_text
                        toc_text.append(indentation + numeral + title + '(#{})'.format(tag_num) + '\n')
                        toc_text.append('\n')

                        # removing any old anchors
                        cell['source'][line_num] = __remove_anchors__(cell['source'][line_num])

                        #formatting for linebreaks
                        if cell['source'][line_num].endswith('\n'):
                            cell['source'][line_num] = cell['source'][line_num][:-1]
                        if cell['source'][line_num].endswith('\n '):
                            cell['source'][line_num] = cell['source'][line_num][:-2]

                        # placing an anchor
                        cell['source'][line_num] += ' <a id="{}"></a>\n'.format(tag_num)

                        tag_num += 1
                line_num += 1

    if additional_text:
        toc_text.append(additional_text)
    # generates properly formatted markdown cell
    toc_cell = nbformat.v4.new_markdown_cell(toc_text)
    # adds table of contents to top of page
    notebook['cells'].insert(0, toc_cell)

    __write_nb__(filename, notebook)