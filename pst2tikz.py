# -*- coding: utf-8 -*-
#################################################################
# pst2tikz.py                                                   #
#                                                               #
# fonction      :   Independant program                         #
# version       :   1.3                                         #
# author        :   Thomas Guenet                               #
# date          :   06 august 2017                              #
#                                                               #
# description   :                                               #
#                                                               #
#################################################################
#
#------------------------------------
# Importation of external functions :  
#------------------------------------
import os # os.chdir, os.listdir...
import sys # sys.exit()
import getopt # managing arguments


#-------------------------------------
# Definitions of internal functions :  
#-------------------------------------

#---------------
# Main program :
#---------------
#if __name__ == "__main__":
#    main(sys.argv[1:])

#---------------------
# Managing arguments :
#---------------------
try:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:o:s:f:', ['help', 'ifile=', 'ofile=', 'scale=', 'formatOfNumbers='])
    # i: mean an argument is needed, same for o:, and no argument needed for h
except getopt.GetoptError:
    print("pst2tikz.py -i inputfilename.tex [-o outputfilename.tex -s 1.0 -f %.6e]")
    print("pst2tikz.py --ifile=inputfilename.tex [--ofile=outputfilename.tex --scale=1.0 --formatOfNumbers=%.6e]")

for opt, arg in opts: 
    if opt in ('-h', '--help'):
        print("pst2tikz.py -i inputfile.tex [-o outputfile.tex -s 1.0 -f %.6e]")
        print("pst2tikz.py --ifile=inputfile.tex [--ofile=outputfile.tex --scale=1.0 --formatOfNumbers=%.6e]")
        sys.exit(2)
    elif opt in ('-i', '--ifile'):
        inputfilename = arg
        print "inputfilename : ",arg
    elif opt in ('-o', '--ofile'):
        outputfilename = arg
        print "outputfilename : ",arg
        # TODO : manage case when no argument are given -o and instead '-s' is used as filename
    elif opt in ('-s', '--scale'):
        scale = arg
        print "scale : ",arg
    elif opt in ('-f', '--formatOfNumbers'):
        fmt = arg
        print "format : ",arg
        
# Default Options
#================
try:
    outputfilename.__init__ # to see if defined (if exist)
except NameError:
    # TODO : manage case where the input filename as several '.'
    # TODO : manage case where the user put same name as input and output filename
    outputfilename = inputfilename.split('.')[0] + '_tikz.tex'
    print "Default output file name : {0}".format(outputfilename)

try:
    fmt.__init__
except NameError:
    fmt = '%.3e'
    print "Default format of number in output file : '{0}'".format(fmt)

try:
    scale.__init__
except NameError:
    scale = 65
    print "Default scale value of the figure : {0}".format(scale)

thickness  = True
coloring   = True
styleligne = True


# Reading input file
#===================
try:
    with open(inputfilename, 'r') as inputfile:
        filecontent = inputfile.readlines()
except IOError:
    print "\nNo such file or directory : '{0}'".format(inputfilename)
    sys.exit()
except ValueError:
    sys.exit()

nbline = len(filecontent) # number of line in inputfile


# Latex Preambule
#================
script="""\\documentclass{standalone}
\\usepackage{lmodern}
\\usepackage[francais]{babel}
\\usepackage[T1]{fontenc}
\\usepackage[utf8]{inputenc}

\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{graphicx}

\\usepackage{tikz}

\\begin{document}

\\begin{tikzpicture}[scale=1]
"""

# Coeur du fichier
#=================

line = 0
while line < nbline: # browse file
    if filecontent[line][0] == '{': # a new path is detected
        # Managing the style of the path
        style = ''
        drawfill = '\\draw'
        if coloring:
            r, g, b = (filecontent[line+1].split('}{')[1][:-2]).split(' ')
            r, g, b = float(r), float(g), float(b)
            color = '{rgb:red,%f;green,%f;blue,%f}'%(r,g,b)
            if r == 0 and g == 0 and b == 0 : color = 'black'
            if r == 1 and g == 0 and b == 0 : color = 'red'
            if r == 0 and g == 1 and b == 0 : color = 'green'
            if r == 0 and g == 0 and b == 1 : color = 'blue'
            if r == 1 and g == 1 and b == 1 : color = 'white'
            if r == g and g == b and not(r in [0,1]): color = 'gray'
        if coloring and filecontent[line+2].count('linecolor='):
            if color != 'black': style += 'color=' + color + ','
        if coloring and filecontent[line+2].count('fillcolor=') :
            style += 'fill=' + color + ','
        if thickness and filecontent[line+2].count('linewidth='):
            ep      = (filecontent[line+2].split('linewidth=')[1]).split(',')[0]
            style += "line width=%fcm,"%(float(ep)/scale)
        if styleligne and filecontent[line+2].count('linestyle=') :
            linestyle = (filecontent[line+2].split('linestyle=')[1]).split(',')[0]
            if linestyle != 'none' : 
                style += linestyle + ','
            else:
                drawfill = '\\fill'

        # The path
        line += 5 
        movetoFirst = True # several moveto may be included in a same path whereas a \draw command must always be on a new line
        while 1:  # repeat until end of path
            if filecontent[line][:7] == '\\moveto':
                x,y = filecontent[line][8:-2].split(',')
                x,y = float(x)/scale, float(y)/scale
                if movetoFirst == True:
                    movetoFirst = False
                    B = drawfill + '[' + style + '](' + fmt%x + ',' + fmt%y + ')'
                else:
                    B = ';\n'+ drawfill + '[' + style + '](' + fmt%x + ',' + fmt%y + ')'
            elif filecontent[line][:7] == '\\lineto' :
                x,y = filecontent[line][8:-2].split(',')
                x,y = float(x)/scale, float(y)/scale
                B = " -- " +  '(' + fmt%x + ',' + fmt%y + ')'
            elif filecontent[line][:8] == '\\curveto' :
                P1,P2,P3 = filecontent[line][9:-2].split(')(')
                x1,y1 = float(P1.split(',')[0])/scale , float(P1.split(',')[1])/scale 
                x2,y2 = float(P2.split(',')[0])/scale , float(P2.split(',')[1])/scale 
                x3,y3 = float(P3.split(',')[0])/scale , float(P3.split(',')[1])/scale 
                B = " .. controls " + '(' + fmt%x1 + ',' + fmt%y1 + ')'\
                    + " and "       + '(' + fmt%x2 + ',' + fmt%y2 + ')'\
                    + " .. "        + '(' + fmt%x3 + ',' + fmt%y3 + ')'
            if filecontent[line+1] == '\\closepath\n':
                B += ' -- cycle'
            script += B
            # go to next line
            line += 1
            # detecting whether it is the end of the path
            if filecontent[line] in ['}\n','\\closepath\n']:
                script += ';\n'
                break # go to next path
    line += 1

script += "\\end{tikzpicture}\n\\end{document}\n"


# Writing the file :
#===================
with open(outputfilename, 'w') as outputfile :
    outputfile.write(script)

# Historique du fichier :
#========================
#v1.0 - original - 01/06/2015
#v1.1 - Add of thickness and color managing of paths - 02/10/2015
#v1.2 - Taking into account '\closepath' => ' -- cycle' - 04/10/2015
#v1.3 - English version - use of with command - 06/08/2017
