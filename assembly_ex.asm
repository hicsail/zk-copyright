; Length of string
mov eax, 0      ; Counter for string length
mov ebx, [string_ptr]  ; Load the address of the string into ebx
count_string_length:
    cmp byte [ebx], 0   ; Compare the byte at ebx to 0 (null terminator)
    je  end_of_string   ; If it's the null terminator, jump to end
    inc eax            ; Otherwise, increment our counter
    inc ebx            ; Move to the next byte of the string
jmp count_string_length
end_of_string:
; At this point, eax contains the length of the string



;For Loop
mov ecx, eax  ; Move the length of the string into ecx (our loop counter)
mov ebx, [string_ptr]  ; Reset ebx to the start of the string
loop_start:
    ; ... Do whatever you want with the character at ebx here ...
    
    dec ecx             ; Decrement our loop counter
    inc ebx             ; Move to the next character
    cmp ecx, 0         ; Check if we've finished looping
jnz loop_start         ; If ecx isn't zero, jump back to the start of the loop



;Array Operation

section .data
myArray db 10, 20, 30, 40, 50   ; An array of 5 bytes


mov al, [myArray + 2]  ; Load the third byte (0-based index) into AL register


mov ecx, 5            ; Counter for the number of elements
mov ebx, myArray      ; Start address of the array
loop_start:
    ; Do something with byte [ebx]
    inc ebx           ; Move to the next byte in the array
    dec ecx
    jnz loop_start    ; Loop while ecx is not zero
