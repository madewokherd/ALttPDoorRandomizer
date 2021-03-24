org $aa8000
db $4f, $52 ;OR
OWShuffleMode:
dw 1
OWShuffleFlags:
dw 0
OWShuffleReserved:
dw 0



;Hooks
org $02a999
jsl OWEdgeTransition : nop #4 ;LDA $02A4E3,X : ORA $7EF3CA

;Code
org $aaa000
OWEdgeTransition:
{
    ;Assume you're at links house = $2c
    ;transitioning right will result in X = $2d
    ;transitioning left will result in X = $2b
    ;up X = $24
    ;down X = $34

    ;compares X to determine direction of edge transition
    cpx $8a : bcc .upOrLeft
    dex : cpx $8a : bne .downEdge
    bra .rightEdge
    .upOrLeft
    inx : cpx $8a : bne .upEdge
    bra .leftEdge

    ;sets new OWID and coords
    .downEdge
    dec $21 : dec $21
    dec $e7 : dec $e7
    dec $e9 : dec $e9
    dec $611 : dec $611
    dec $613 : dec $613
    lda $700 : sec : sbc #$10 : sta $700
    bra .return

    .rightEdge
    dec $23 : dec $23
    dec $e1 : dec $e1
    dec $e3 : dec $e3
    dec $615 : dec $615
    dec $617 : dec $617
    dec $700 : dec $700
    bra .return

    .upEdge
    inc $21 : inc $21
    inc $e7 : inc $e7
    inc $e9 : inc $e9
    inc $611 : inc $611
    inc $613 : inc $613
    lda $700 : clc : adc #$10 : sta $700
    bra .return

    .leftEdge
    inc $23 : inc $23
    inc $e1 : inc $e1
    inc $e3 : inc $e3
    inc $615 : inc $615
    inc $617 : inc $617
    inc $700 : inc $700

    .return
    ;Infinite loop at Link's
    lda #$2c
    rtl
}