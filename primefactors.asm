; calculate the prime numbers of a given number

mov goal, 64    ; the number of which the prime factors will be calculated
jmp main

isprime:   ; uses prefix 'p?', and parameter/return 'p?p'
    cmp p?p, 2
    je p?true
    jl p?false

    mov p?i, 2       ; iterator

    p?loop:
        mov p?a, p?p
        mod p?a, p?i
        cmp p?a, 0
        je p?false

        inc p?i
        cmp p?i, p?p
        je p?true
        jmp p?loop

    p?false:
        mov p?p, 0
        ret

    p?true:
        mov p?p, 1
        ret


primefactors:    ;  uses prefix 'pf', and parameter/return 'pfp'
    mov pfi, 2

    factorloop:
        mov p?p, pfp   ; set isprime's parameter
        call isprime   ; check if pfp is prime
        cmp p?p, 1     ; if so, print pfp and leave
        je isfprime

        mov pfa, pfp
        mod pfa, pfi
        cmp pfa, 0
        je isfactor

        inc pfi
        jmp factorloop

        isfactor:
            msg pfi
            div pfp, pfi
            jmp factorloop

        isfprime:
            msg pfp
            ret


main:
    mov pfp, goal
    call primefactors
    end
