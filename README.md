# Assembler
 Assembly interpreter written in Python.
 
This interpreter uses a custom subset of Assembly laid out below.  
Remember: this was made purely for fun, so don't expect fast or generally useful code!  


<table>
    <tr>
        <th>Code</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>
            <code>mov a b</code>
        </td>
        <td>
            Move the value <code>b</code> (registry or number) to registry <code>a</code>
        </td>
    </tr>
    <tr>
        <th colspan="2">Basic arithmetics</th>
    </tr>
    <tr>
        <td>
            <code>inc a</code>
        </td>
        <td>
            Increase the value stored in registry <code>a</code> by 1
        </td>
    </tr>
    <tr>
        <td>
            <code>dec a</code>
        </td>
        <td>
            Decrease the value stored in registry <code>a</code> by 1
        </td>
    </tr>
    <tr>
        <td>
            <code>add a b</code>
        </td>
        <td>
            Adds the value <code>b</code> (registry or number) to registry <code>a</code>
        </td>
    </tr>
    <tr>
        <td>
            <code>sub a b</code>
        </td>
        <td>
            Subtracts the value <code>b</code> (registry or number) from registry <code>a</code>
        </td>
    </tr>
    <tr>
        <td>
            <code>mul a b</code>
        </td>
        <td>
            Multiplies the value in registry <code>a</code> by value <code>b</code> (registry or number)
        </td>
    </tr>
    <tr>
        <td>
            <code>div a b</code>
        </td>
        <td>
            Divides the value in registry <code>a</code> by value <code>b</code> (registry or number)
        </td>
    </tr>
    <tr>
        <td>
            <code>mod a b</code>
        </td>
        <td>
            Reduces the value in registry <code>a</code> modulo value <code>b</code> (registry or number)
        </td>
    </tr>
    <tr>
        <th colspan="2">Control flow</th>
    </tr>
    <tr>
        <td>
            <code>label:</code>
        </td>
        <td>
            Define a label (replace <code>label</code> with any string)
        </td>
    </tr>
    <tr>
        <td>
            <code>jmp label</code>
        </td>
        <td>
            Jump to the given label
        </td>
    </tr>
    <tr>
        <td>
            <code>cmp a b</code>
        </td>
        <td>
            Compares values <code>a</code> and <code>b</code> (storing both for later use)
        </td>
    </tr>
    <tr>
        <td>
            <code>je label</code>
        </td>
        <td>
            Jump to the given label if the numbers in the comparison equal each other
        </td>
    </tr>
    <tr>
        <td>
            <code>jne label</code>
        </td>
        <td>
            Jump to the given label if the numbers in the comparison don't equal each other
        </td>
    </tr>
    <tr>
        <td>
            <code>jg label</code>
        </td>
        <td>
            Jump to the given label if the first comparison number is greater than the second
        </td>
    </tr>
    <tr>
        <td>
            <code>jge label</code>
        </td>
        <td>
            Jump to the given label if the first comparison number is greater than or equal to the second
        </td>
    </tr>
    <tr>
        <td>
            <code>jl label</code>
        </td>
        <td>
            Jump to the given label if the first comparison number is lesser than the second
        </td>
    </tr>
    <tr>
        <td>
            <code>jle label</code>
        </td>
        <td>
            Jump to the given label if the first comparison number is lesser than or equal to the second
        </td>
    </tr>
    <tr>
        <td>
            <code>call label</code>
        </td>
        <td>
            Jump to the given label and add the jumping off point to the stack
        </td>
    </tr>
    <tr>
        <td>
            <code>ret</code>
        </td>
        <td>
            Pop a jumping off point from the stack and continue from there
        </td>
    </tr>
    <tr>
        <th colspan="2">Miscellaneous</th>
    </tr>
    <tr>
        <td>
            <code>msg *s</code>
        </td>
        <td>
            Print any combination of strings and values to the console (eg. <code>msg 'five factorial is ', 120</code>)
        </td>
    </tr>
    <tr>
        <td>
            <code>end</code>
        </td>
        <td>
            Ends the program
        </td>
    </tr>
    <tr>
        <td>
            <code>;</code>
        </td>
        <td>
            Defines a comment
        </td>
    </tr>
</table>

<hr></hr>

# Example  
Here's a small example, calculating the factorial of a given number
<pre><code>mov   a, 7  ; calculate the factorial of 7
mov   b, a
mov   c, a
call  proc_fact
call  print
end

proc_fact:
    dec   b
    mul   c, b
    cmp   b, 1
    jne   proc_fact
    ret

print:
    msg   a, '! = ', c ; output text
    ret</code></pre>
