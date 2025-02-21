import schemdraw
import schemdraw.elements as elm

# Initialize the drawing
d = schemdraw.Drawing()

# Create the NAND gates for the expression using only NAND gates
# The expression is (A AND B) OR (NOT A AND NOT B), but using NAND gates
# (A NAND B) NAND ((A NAND A) NAND (B NAND B))

# First NAND gate (A NAND B)
NAND1 = d.add(elm.NAND2, inputs=['A', 'B'])
# Second NAND gate (A NAND A)
NAND2 = d.add(elm.NAND2, at=NAND1.in1, d='left')
d.add(elm.Line, at=NAND2.in1, l=d.unit/4, xy=NAND2.in2)
# Third NAND gate (B NAND B)
NAND3 = d.add(elm.NAND2, at=NAND1.in2, d='left')
d.add(elm.Line, at=NAND3.in1, l=d.unit/4, xy=NAND3.in2)
# Fourth NAND gate ((A NAND A) NAND (B NAND B))
NAND4 = d.add(elm.NAND2, at=(NAND2.out, NAND3.out), d='right', anchor='in1')
d.add(elm.Line, at=NAND4.in2, tox=NAND3.out)
# Fifth NAND gate which is the output NAND gate ((A NAND B) NAND ((A NAND A) NAND (B NAND B)))
NAND5 = d.add(elm.NAND2, at=(NAND1.out, NAND4.out), d='right', anchor='in1')
d.add(elm.Line, at=NAND5.in2, tox=NAND4.out)

# Output
d.add(elm.Line, at=NAND5.out, l=d.unit/2)
d.add(elm.Dot, label='Output\n$\overline{A \oplus B}$')

# Draw the final schematic
d.draw()