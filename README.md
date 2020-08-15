# Vispy Note
## GLSL
### Three types of variable（uniform，attribute and varying)
1. uniform:
    > global var, **cannot** be modified inside shader, can be modified in external program
2. attribute: 
    > can be modified inside external program and shader
3. varying
    > can modify inside shader, used to communicate between "vertex" and "fragment"

 