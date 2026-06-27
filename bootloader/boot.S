.code16
.section .text
.global _start

_start:
    cli
    xor %ax, %ax
    mov %ax, %ds
    mov %ax, %es
    mov %ax, %ss
    mov $0x7C00, %sp
    sti

    mov $msg, %si
print_msg:
    lodsb
    cmp $0, %al
    je halt
    mov $0x0e, %ah
    int $0x10
    jmp print_msg

halt:
    hlt
    jmp halt

msg:
    .asciz "StartLoader: Booting Android...\r\n"

.fill 510 - (. - _start), 1, 0
.word 0xAA55
