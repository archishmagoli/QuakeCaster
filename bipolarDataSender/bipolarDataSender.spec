WHILE_8 GETC
    ADD R3, R0, 0 ; store option in R3
    LD R2, ASCII_ZERO ; test whether option == '0'
    NOT R2, R2
    ADD R2, R2, 1
    ADD R2, R2, R3
    BRnp TEST_ONE ; if option != '0', go to TEST_ONE
    BRz PRINT_MODIFIED_LINE ; if option == '0', do nothing (pass) and prints modified line
    
    TEST_ONE AND R2, R2, 0
    LD R2, ASCII_ONE ; test whether option == '1'
    NOT R2, R2
    ADD R2, R2, 1
    ADD R2, R2, R3
    BRnp TEST_TWO ; if option != '1', go to TEST_TWO
    ADD R0, R1, 0 ; if option == '1', set R0 = startOfCurrLine
    LD R4, CAPITALIZE_ADDR
    JSRR R4 ; call CapitalizeLine
    BR PRINT_MODIFIED_LINE ; print the modified line
    
    TEST_TWO AND R2, R2, 0
        LD R2, ASCII_TWO ; test whether option == '2'
        NOT R2, R2
        ADD R2, R2, 1
        ADD R2, R2, R3
        BRnp TEST_THREE ; if option != '2', go to TEST_THREE
        ADD R0, R1, 0 ; if option == '2', set R0 = startOfCurrLine
        LD R4, REVERSE_ADDR
        JSRR R4
        BR PRINT_MODIFIED_LINE
    
    TEST_THREE AND R2, R2, 0
        LD R2, ASCII_THREE ; test whether option == '3'
        NOT R2, R2
        ADD R2, R2, 1
        ADD R2, R2, R3
        BRnp ELSE_BLOCK ; if option != '3', go to ELSE_BLOCK
        ADD R0, R1, 0 ; if option == '3', set R0 = startOfCurrLine
        LD R4, RIGHT_JUSTIFY_ADDR
        JSRR R4
        BR PRINT_MODIFIED_LINE
    
    ELSE_BLOCK
        BR WHILE_8 ; continue
        
    PRINT_MODIFIED_LINE AND R5, R5, 0
    ADD R5, R5, -9 ; i = -9
    
    WHILE_9
        LDR R0, R1, 0 ; R0 contains mem[startOfCurrLine]
        OUT ; OUT(mem[startOfCurrLine])
        ADD R1, R1, 1 ; startOfCurrLine++
        ADD R5, R5, 1 ; i++
        BRzp CHECK_NULL_POINTER
        BR WHILE_9
    
    CHECK_NULL_POINTER AND R5, R5, 0
        LDR R5, R1, -1 ; R5 contains mem[startOfCurrLine - 1]
        BRz FINALLY_FINISHED ; break if mem[startOfCurrLine - 1] = '\0'
        
    BR WHILE_8
