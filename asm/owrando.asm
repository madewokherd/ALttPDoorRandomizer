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
    LDA $02A4E3,X : ORA $7EF3CA
    rtl
}