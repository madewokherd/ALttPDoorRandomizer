org $aa8000 ;150000
db $4f, $52 ;OR
OWMode:
db 0
OWFlags:
dw 0
org $aa8010
OWReserved:
dw 0

;Hooks
org $02a999
jsl OWEdgeTransition : nop #4 ;LDA $02A4E3,X : ORA $7EF3CA

;Code
org $aaa000
OWCoordIndex: ; Horizontal 1st
db 2, 2, 0, 0 ; Coordinate Index $20-$23
OWBGIndex: ; Horizontal 1st
db 0, 0, 6, 6 ; BG Scroll Index $e2-$ea
OWCameraIndex: ; Horizontal 1st
db 4, 4, 0, 0 ; Camera Index $0618-$61f
OWOppSlotOffset: ; Amount to offset OW Slot
db 8, -8, 1, -1 ; OW Slot x2 $700
OWEdgeTransition:
{
    php
    phy
    lda.l OWMode : beq +
        jsl OWShuffle
        bra .return
    + jsl OWVanilla
    .return
    ply
    plp
    rtl
}
OWVanilla:
{
    lda $02a4e3,X : ora $7ef3ca
    rtl
}
OWShuffle:
{
    ;Assume you're at links house = $2c
    ;transitioning right will result in X = $2d
    ;transitioning left will result in X = $2b
    ;up X = $24
    ;down X = $34

    ;compares X to determine direction of edge transition
    phx
    lsr $700 : cpx $700 : !blt .upOrLeft
        dex : cpx $700 : bne .downEdge
            lda #$3 : sta $418 ;right
            ;dec $23 : dec $23
            ;dec $e1 : dec $e1
            ;dec $e3 : dec $e3
            ;dec $615 : dec $615
            ;dec $617 : dec $617
            ;dec $700 : dec $700
            bra .setOWID
        .downEdge
            lda #$1 : sta $418 ;down
            ;dec $21 : dec $21
            ;dec $e7 : dec $e7
            ;dec $e9 : dec $e9
            ;dec $611 : dec $611
            ;dec $613 : dec $613
            ;lda $700 : sec : sbc #$10 : sta $700
            bra .setOWID
    .upOrLeft
        inx : cpx $700 : bne .upEdge
                lda #$2 : sta $418 ;left
                ;inc $23 : inc $23
                ;inc $e1 : inc $e1
                ;inc $e3 : inc $e3
                ;inc $615 : inc $615
                ;inc $617 : inc $617
                ;inc $700 : inc $700
                bra .setOWID
            .upEdge
                lda #$0 : sta $418 ;up
                ;inc $21 : inc $21
                ;inc $e7 : inc $e7
                ;inc $e9 : inc $e9
                ;inc $611 : inc $611
                ;inc $613 : inc $613
                ;lda $700 : clc : adc #$10 : sta $700

    .setOWID
    ;look up transitions in current area in table OWEdgeOffsets
    ;offset is (8bytes * OW Slot ID) + (2bytes * direction)
    asl : rep #$20 : pha : sep #$20 ;2 bytes per direction
    lda $8a : and #$40 : !add $700 : rep #$30 : and #$00ff : asl #3
    adc 1,S : tax
    asl $700 : pla
    ;x = offset to edgeoffsets table
    
    sep #$20
    lda.l OWEdgeOffsets,x : and #$ff : beq .noTransition : pha ;get number of transitions
    ;s1 = number of transitions left to check
    
    inx : lda.l OWEdgeOffsets,x ;record id of first transition in table
    ;multiply ^ by 12, 12bytes per record
    sta $211b : lda #0 : sta $211b : lda #12 : sta $211c : pla ;a = number of trans
    ldx $2134 ;x = offset to first record
    rep #$20
    and #$00ff

    .nextTransition
    pha
        jsr OWSearchTransition
        lda $140 : bne .newDestination
    pla : dec : bne .nextTransition : bra .noTransition

    .newDestination
    pla
    sep #$30
    lda #0 : sta $140
    plx : lda $8a
    bra .return

    .noTransition
    sep #$30
    plx
    jsl OWVanilla

    .return
    rtl
}
OWSearchTransition:
{
    ;A-16 XY-16
    lda $418 : bne + ;north
        lda.l OWNorthEdges,x : dec : inx #2
        cmp $22 : !bge .nomatch
        lda.l OWNorthEdges,x : cmp $22 : !blt .nomatch
            ;MATCH
            txa : !add #$0008 : tax : lda.l OWNorthEdges,x : tay ;y = record id of dest
            sep #$20 : lda #OWSouthEdges>>16 : phb : pha : plb : ldx #OWSouthEdges : jsr OWNewDestination : plb ;x = address of table
            bra .matchfound2
    + dec : bne + ;south
        lda.l OWSouthEdges,x : dec : inx #2
        cmp $22 : !bge .nomatch
        lda.l OWSouthEdges,x : cmp $22 : !blt .nomatch
            ;MATCH
            txa : !add #$0008 : tax : lda.l OWSouthEdges,x : tay ;y = record id of dest
            sep #$20 : lda #OWNorthEdges>>16 : phb : pha : plb : phx : ldx #OWNorthEdges : jsr OWNewDestination : plx : plb ;x = address of table
        .matchfound2
            bra .matchfound
        .nomatch
            bra .exitloop
    + dec : bne + ; west
        lda.l OWWestEdges,x : dec : inx #2
        cmp $20 : !bge .exitloop
        lda.l OWWestEdges,x : cmp $20 : !blt .exitloop
            ;MATCH
            txa : !add #$0008 : tax : lda.l OWWestEdges,x : tay ;y = record id of dest
            sep #$20 : lda #OWEastEdges>>16 : phb : pha : plb : ldx #OWEastEdges : jsr OWNewDestination : plb ;x = address of table
            bra .matchfound
    + lda.l OWEastEdges,x : dec : inx #2 ;east
        cmp $20 : !bge .exitloop
        lda.l OWEastEdges,x : cmp $20 : !blt .exitloop
            ;MATCH
            txa : !add #$0008 : tax : lda.l OWEastEdges,x : tay ;y = record id of dest
            sep #$20 : lda #OWWestEdges>>16 : phb : pha : plb : ldx #OWWestEdges : jsr OWNewDestination : plb ;x = address of table
            ;bra .matchfound

    .matchfound
    plx : pla : lda #$0001 : sta $140 : pha : phx
    inx #2 : rts

    .exitloop
    txa : !add #$000a : tax : rts
}
OWNewDestination:
{
    tya : sta $211b : lda #0 : sta $211b : lda #12 : sta $211c : rep #$20 : lda $2134
    phx : !add 1,s : plx : !add #$0006 : tax ;a = offset to dest record
    lda.w $0000,x : sta $06 ; set coord
    inx #2 : lda.w $0000,x : sta $04 ;save dest OW slot/ID
    sep #$10 : ldy $418
    ;;22	e0	e2	61c	61e - X
    ;;20	e6	e8	618	61a - Y
    ldx OWCoordIndex,y : lda $20,x : and #$01ff : pha
    lda $06 : and #$01ff : !sub 1,s : pha : lda $06 : sta $20,x ;set coord, a = diff
    ldx OWBGIndex,y : lda $e2,x : !add 1,s : sta $e2,x
    ldx OWCameraIndex,y : lda $618,x : !add 1,s : sta $618,x
    ldx OWCameraIndex,y : lda $61a,x : !add 1,s : sta $61a,x
    pla : lsr : pha : ldx OWBGIndex,y : lda $e0,x : !add 1,s : sta $e0,x
    pla : pla : sep #$30
    lda OWOppSlotOffset,y : !add $04 : asl : sta $700
    ;;;tempfixes
    ;;lda #$08e8 : sta $0e
    ;;lda #$0000 : sta $a9 ;clears out vert/horiz resistance
    ;;lda #$085e : sta $11e ;bg xscroll
    ;;lda #$0848 : sta $120 ;bg xscroll
    ;;lda #$08c5 : sta $2dc
    ;;lda #$0bbd : sta $2de
    ;;lda #$fff2 : sta $628
    ;;lda #$000e : sta $62a
    ;;lda #$08e0 : sta $fc2
    ;;lda #$0be3 : sta $fc4

    ;;;good ones
    ;;;lda #$0848 : sta $e0
    ;;;lda #$085e : sta $e2
    ;;;lda #$08eb : sta $61c
    ;;;lda #$08e9 : sta $61e
    ;inc $23 : inc $23
    ;inc $e1 : inc $e1
    ;inc $e3 : inc $e3
    ;inc $615 : inc $615
    ;;lda #$0700 : sta $614
    ;inc $617 : inc $617
    ;;lda #$0a00 : sta $616


    ;example: trans to lake hylia 0x35
    ;good
    ;lda #$0ae0 : sta $22
    ;lda #$7575 : sta $04
    ;lda #$0a37 : sta $e0
    ;lda #$0a6e : sta $e2
    ;lda #$0aeb : sta $61c
    ;lda #$0ae9 : sta $61e
    ;lda #$005a : sta $700
    ;end good

    ;inc $700 : inc $700
    ;;when yC = E4
    ;;40  = 0b 08
    ;;80  = 00 00 00 00 0c 18 1e 00 09 00 2c 00 96 00 
    ;;e0  = 48 08 5e 08 00 00 dc 0a 1e 0b 00 00 f8 ff 00 00
    ;;600 = 00 0a 1e 0b 00 08 00 09 00->
    ;;610 = 20 09 00 0c 00 07 00 0a 8b 0b 89 0b eb 08 e9 08
    ;;diff notes
    ;0e-f seems to be 8 pixels right of current x coord
    ;22 xcoord
    ;29-a vert/horiz resistance, clear to 0
    ;3e-f y/x next upcoming coord??? (low byte)
    ;43 unknown?
    ;53 unknown?
    ;6a unknown?
    ;74 moving water?
    ;e0-3 bg1/2 scroll
    ;100-1 index of graphics that are blitted, prob not needed
    ;11e-121 bg1/0 scroll
    ;2dc-f coord/scroll related?
    ;61c-f cameraX scroll bounds
    ;628-b unknown
    ;6a0 special object slots?
    ;ad0-3 DMA stuff
    ;ae0-3 DMA stuff
    ;daf sprite stuff
    ;f5f palette/tile stuff
    ;fa8 sprite relative coord
    ;fb7 unknown
    ;fc2-5 links coords, next frame coords?

    ;;;end-tempfixes

    ;lda #$0000
    sep #$20

    ;;lda #$e0 : sta $3f ;sets next frame x coord
    ;;lda #$0f : sta $43 ;?
    ;;lda #$d4 : sta $53 ;?
    ;;lda #$00 : sta $6a ;?
    ;;lda #$6e : sta $100 ;?
    ;;lda #$00 : sta $6a0 ;special object slots?
    ;;lda #$c2 : sta $fb7 ;?


    ;lda #$68 : sta $700
    ;lda $05 : asl : sta $700 ;might not need to set 700? 700 at this point = SRC OW slot id
    lda $05 : sta $8a : and #$40 : sta.l $7ef3ca
    rep #$30
    ;dec $21 : dec $21
    ;dec $e7 : dec $e7
    ;dec $e9 : dec $e9
    ;dec $611 : dec $611
    ;dec $613 : dec $613
    ;lda $700 : sec : sbc #$10 : sta $700
    rts
}

;Data
org $aab000
OWEdgeOffsets:
;2 bytes per each direction per each OW Slot, order is NSWE per value at $0418
;AABB, A = offset to the transition table, B = number of transitions
dw $0001, $0000, $0000, $0000 ;OW Slot 00, OWID 0x00 Lost Woods
dw $0000, $0000, $0000, $0001 ;OW Slot 01, OWID 0x00
dw $0000, $0001, $0001, $0000 ;OW Slot 02, OWID 0x02 Lumberjack
dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $0101
dw $0000, $0000, $0101, $0000
dw $0000, $0000, $0000, $0201
dw $0000, $0000, $0201, $0000

dw $0000, $0102, $0000, $0000
dw $0000, $0301, $0000, $0000
dw $0101, $0401, $0000, $0000
dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $0301
dw $0000, $0000, $0301, $0000
dw $0000, $0000, $0000, $0000
dw $0201, $0501, $0000, $0000 ;Zora

dw $0302, $0602, $0000, $0000
dw $0501, $0801, $0000, $0402
dw $0601, $0902, $0402, $0602
dw $0000, $0000, $0602, $0801
dw $0000, $0000, $0801, $0901
dw $0000, $0b03, $0901, $0a03
dw $0000, $0000, $0a03, $0d02
dw $0701, $0000, $0d02, $0000

dw $0802, $0000, $0000, $0000 ;OW Slot 18, OWID 0x18 Kakariko
dw $0a01, $0000, $0000, $0000
dw $0b02, $0000, $0000, $0f01
dw $0000, $0000, $0f01, $0000
dw $0000, $0000, $0000, $0000
dw $0d03, $0e01, $0000, $0000
dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $0000

dw $0000, $0000, $0000, $0000
dw $0000, $0f01, $0000, $1001
dw $0000, $0000, $1001, $0000
dw $0000, $1001, $0000, $0000
dw $0000, $1101, $0000, $1101
dw $1001, $1201, $1101, $0000
dw $0000, $1301, $0000, $0000
dw $0000, $1401, $0000, $0000

dw $0000, $0000, $0000, $1201
dw $1101, $0000, $1201, $1301
dw $0000, $1502, $1301, $0000
dw $1201, $1701, $0000, $1403
dw $1301, $1801, $1403, $1701 ;Links
dw $1401, $1901, $1702, $1802 ;Hobo
dw $1501, $1a02, $1902, $0000
dw $1601, $0000, $0000, $0000

dw $0000, $0000, $0000, $0000 ;OW Slot 30, OWID 0x30 Desert
dw $0000, $0000, $0000, $0000
dw $1702, $0000, $0000, $1a01
dw $1901, $1c01, $1b01, $1b03
dw $1a01, $1d01, $1c03, $0000
dw $1b01, $0000, $0000, $0000
dw $1c02, $0000, $0000, $0000
dw $0000, $1e02, $0000, $0000

dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $1e02
dw $0000, $0000, $1f02, $2002
dw $1e01, $0000, $2102, $2201
dw $1f01, $0000, $2301, $2301
dw $0000, $0000, $2401, $0000
dw $0000, $0000, $0000, $2402
dw $2002, $0000, $2502, $0000

dw $0000, $0000, $0000, $0000 ;OW Slot 40, OWID 0x40 Skull Woods
dw $0000, $0000, $0000, $2601
dw $0000, $2001, $2701, $0000
dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $2701
dw $0000, $0000, $2801, $0000
dw $0000, $0000, $0000, $2801
dw $0000, $0000, $2901, $0000

dw $0000, $2102, $0000, $0000
dw $0000, $2301, $0000, $0000
dw $2201, $2401, $0000, $0000
dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $2901
dw $0000, $0000, $2a01, $0000
dw $0000, $0000, $0000, $0000
dw $0000, $2501, $0000, $0000

dw $2302, $2602, $0000, $0000
dw $2501, $2801, $0000, $2a02
dw $2601, $2902, $2b02, $2c02
dw $0000, $0000, $2d02, $2e01
dw $0000, $0000, $2f01, $2f01
dw $0000, $2b03, $3001, $3003
dw $0000, $0000, $3103, $3302
dw $2701, $0000, $3402, $0000

dw $2802, $0000, $0000, $0000 ;OW Slot 58, OWID 0x58 Village of Outcasts
dw $2a01, $0000, $0000, $0000
dw $2b02, $0000, $0000, $0000
dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $0000
dw $2d03, $2e01, $0000, $0000
dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $0000

dw $0000, $0000, $0000, $0000
dw $0000, $2f01, $0000, $3501
dw $0000, $0000, $3601, $0000
dw $0000, $3001, $0000, $0000
dw $0000, $3101, $0000, $3601
dw $3001, $3201, $3701, $0000
dw $0000, $3301, $0000, $0000
dw $0000, $3401, $0000, $0000

dw $0000, $0000, $0000, $3702
dw $3101, $0000, $3802, $3901
dw $0000, $3502, $3a01, $0000
dw $3201, $3701, $0000, $0a03
dw $3301, $3801, $3b03, $3d01
dw $3401, $3901, $3e01, $3e02
dw $3501, $3a02, $3f02, $0000
dw $3601, $0000, $0000, $0000

dw $0000, $0000, $0000, $0000 ;OW Slot 70, OWID 0x70 Mire
dw $0000, $0000, $0000, $0000
dw $3702, $0000, $0000, $4001
dw $3901, $3c01, $4101, $4103
dw $3a01, $3d01, $4203, $0000
dw $3b01, $0000, $0000, $0000
dw $3c02, $0000, $0000, $0000
dw $0000, $3e02, $0000, $0000

dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $0000
dw $0000, $0000, $0000, $4402
dw $3e01, $0000, $4502, $4601
dw $3f01, $0000, $4701, $4701
dw $0000, $0000, $4801, $0000
dw $0000, $0000, $0000, $4802
dw $4002, $0000, $4902, $0000

dw $0000, $4001, $0000, $0000
dw $0000, $0000, $0000, $4a01
dw $0000, $4101, $0000, $0000

org $aab800
OWNorthEdges:
;Min Coord, Max Coord, Width, Midpoint, OW Slot/OWID, Dest Index
dw $00a0, $00a0, $0000, $00a0, $0000, $0040 ;Lost Woods
dw $0458, $0540, $00e8, $04cc, $0a0a, $0000
dw $0f70, $0f90, $0020, $0f80, $0f0f, $0041
dw $0058, $0058, $0000, $0058, $1010, $0001
dw $0178, $0178, $0000, $0178, $1010, $0002
dw $0388, $0388, $0000, $0388, $1111, $0003
dw $0480, $05b0, $0130, $0518, $1212, $0004
dw $0f70, $0f90, $0020, $0f80, $1717, $0005
dw $0078, $0098, $0020, $0088, $1818, $0006 ;Kakariko
dw $0138, $0158, $0020, $0148, $1818, $0007
dw $02e8, $0348, $0060, $0318, $1819, $0008
dw $0478, $04d0, $0058, $04a4, $1a1a, $0009
dw $0510, $0538, $0028, $0524, $1a1a, $000a
dw $0a48, $0af0, $00a8, $0a9c, $1d1d, $000b
dw $0b28, $0b38, $0010, $0b30, $1d1d, $000c
dw $0b70, $0ba0, $0030, $0b88, $1d1d, $000d
dw $0a40, $0b10, $00d0, $0aa8, $2525, $000e
dw $0350, $0390, $0040, $0370, $2929, $000f
dw $0670, $06a8, $0038, $068c, $2b2b, $0010
dw $0898, $09b0, $0118, $0924, $2c2c, $0011 ;Links House
dw $0a40, $0ba0, $0160, $0af0, $2d2d, $0012
dw $0c70, $0c90, $0020, $0c80, $2e2e, $0013
dw $0f70, $0f80, $0010, $0f78, $2f2f, $0014
dw $0430, $0468, $0038, $044c, $3232, $0015
dw $04d8, $04f8, $0020, $04e8, $3232, $0016
dw $0688, $06b0, $0028, $069c, $3333, $0017
dw $08d0, $08f0, $0020, $08e0, $3434, $0018
dw $0a80, $0b40, $00c0, $0ae0, $3535, $0019
dw $0d38, $0d58, $0020, $0d48, $3536, $001a
dw $0d90, $0da0, $0010, $0d98, $3536, $001b
dw $06a0, $07b0, $0110, $0728, $3b3b, $001c
dw $0830, $09b0, $0180, $08f0, $3c3c, $001d
dw $0e78, $0e88, $0010, $0e80, $3f3f, $001e
dw $0ee0, $0fc0, $00e0, $0f50, $3f3f, $001f
dw $0458, $0540, $00e8, $04cc, $4a4a, $0020
dw $0058, $0058, $0000, $0058, $5050, $0021
dw $0178, $0178, $0000, $0178, $5050, $0022
dw $0388, $0388, $0000, $0388, $5151, $0023
dw $0480, $05b0, $0130, $0518, $5252, $0024
dw $0f70, $0f90, $0020, $0f80, $5757, $0025
dw $0078, $0098, $0020, $0088, $5858, $0026 ;Village of Outcasts
dw $0138, $0158, $0020, $0148, $5858, $0027
dw $02e8, $0348, $0060, $0318, $5859, $0028
dw $0478, $04d0, $0058, $04a4, $5a5a, $0029
dw $0510, $0538, $0028, $0524, $5a5a, $002a
dw $0a48, $0af0, $00a8, $0a9c, $5d5d, $002b
dw $0b28, $0b38, $0010, $0b30, $5d5d, $002c
dw $0b70, $0ba0, $0030, $0b88, $5d5d, $002d
dw $0a40, $0b10, $00d0, $0aa8, $6565, $002e
dw $0350, $0390, $0040, $0370, $6969, $002f
dw $0670, $06a8, $0038, $068c, $6b6b, $0030
dw $0898, $09b0, $0118, $0924, $6c6c, $0031
dw $0a40, $0ba0, $0160, $0af0, $6d6d, $0032
dw $0c70, $0c90, $0020, $0c80, $6e6e, $0033
dw $0f70, $0f80, $0010, $0f78, $6f6f, $0034
dw $0430, $0468, $0038, $044c, $7272, $0035
dw $04d8, $04f8, $0020, $04e8, $7272, $0036
dw $0688, $06b0, $0028, $069c, $7373, $0037
dw $08d0, $08f0, $0020, $08e0, $7474, $0038
dw $0a80, $0b40, $00c0, $0ae0, $7575, $0039
dw $0d38, $0d58, $0020, $0d48, $7576, $003a
dw $0d90, $0da0, $0010, $0d98, $7576, $003b
dw $06a0, $07b0, $0110, $0728, $7b7b, $003c
dw $0830, $09b0, $0180, $08f0, $7c7c, $003d
dw $0e78, $0e88, $0010, $0e80, $7f7f, $003e
dw $0ee0, $0fc0, $00e0, $0f50, $7f7f, $003f
OWSouthEdges:
dw $0458, $0540, $00e8, $04cc, $0202, $0001
dw $0058, $0058, $0000, $0058, $0008, $0003
dw $0178, $0178, $0000, $0178, $0008, $0004
dw $0388, $0388, $0000, $0388, $0009, $0005
dw $0480, $05b0, $0130, $0518, $0a0a, $0006
dw $0f38, $0f60, $0028, $0f4c, $0f0f, $0007
dw $0078, $0098, $0020, $0088, $1010, $0008
dw $0138, $0158, $0020, $0148, $1010, $0009
dw $02e8, $0348, $0060, $0318, $1111, $000a
dw $0478, $04d0, $0058, $04a4, $1212, $000b
dw $0510, $0538, $0028, $0524, $1212, $000c
dw $0a48, $0af0, $00a8, $0a9c, $1515, $000d
dw $0b28, $0b38, $0010, $0b30, $1515, $000e
dw $0b70, $0ba0, $0030, $0b88, $1515, $000f
dw $0a40, $0b10, $00d0, $0aa8, $1d1d, $0010
dw $0350, $0390, $0040, $0370, $1821, $0011
dw $0670, $06a8, $0038, $068c, $1b23, $0012
dw $0898, $09b0, $0118, $0924, $1b24, $0013
dw $0a40, $0ba0, $0160, $0af0, $2525, $0014
dw $0c70, $0c90, $0020, $0c80, $1e26, $0015
dw $0f70, $0f80, $0010, $0f78, $1e27, $0016
dw $0430, $0468, $0038, $044c, $2a2a, $0017
dw $04d8, $04f8, $0020, $04e8, $2a2a, $0018
dw $0688, $06b0, $0028, $069c, $2b2b, $0019
dw $08d0, $08f0, $0020, $08e0, $2c2c, $001a
dw $0a80, $0b40, $00c0, $0ae0, $2d2d, $001b
dw $0d38, $0d58, $0020, $0d48, $2e2e, $001c
dw $0d90, $0da0, $0010, $0d98, $2e2e, $001d
dw $06a0, $07b0, $0110, $0728, $3333, $001e
dw $0830, $09b0, $0180, $08f0, $3434, $001f
dw $0e78, $0e88, $0010, $0e80, $3737, $0020
dw $0ee0, $0fc0, $00e0, $0f50, $3737, $0021
dw $0070, $00a0, $0030, $0088, $4242, $0022
dw $0058, $0058, $0000, $0058, $4048, $0023
dw $0178, $0178, $0000, $0178, $4048, $0024
dw $0388, $0388, $0000, $0388, $4049, $0025
dw $0480, $05b0, $0130, $0518, $4a4a, $0026
dw $0f70, $0f90, $0020, $0f80, $4f4f, $0027
dw $0078, $0098, $0020, $0088, $5050, $0028
dw $0138, $0158, $0020, $0148, $5050, $0029
dw $02e8, $0348, $0060, $0318, $5151, $002a
dw $0478, $04d0, $0058, $04a4, $5252, $002b
dw $0510, $0538, $0028, $0524, $5252, $002c
dw $0a48, $0af0, $00a8, $0a9c, $5555, $002d
dw $0b28, $0b38, $0010, $0b30, $5555, $002e
dw $0b70, $0ba0, $0030, $0b88, $5555, $002f
dw $0a40, $0b10, $00d0, $0aa8, $5d5d, $0030
dw $0350, $0390, $0040, $0370, $5861, $0031
dw $0670, $06a8, $0038, $068c, $5b63, $0032
dw $0898, $09b0, $0118, $0924, $5b64, $0033
dw $0a40, $0ba0, $0160, $0af0, $6565, $0034
dw $0c70, $0c90, $0020, $0c80, $5f66, $0035
dw $0f70, $0f80, $0010, $0f78, $5f67, $0036
dw $0430, $0468, $0038, $044c, $6a6a, $0037
dw $04d8, $04f8, $0020, $04e8, $6a6a, $0038
dw $0688, $06b0, $0028, $069c, $6b6b, $0039
dw $08d0, $08f0, $0020, $08e0, $6c6c, $003a
dw $0a80, $0b40, $00c0, $0ae0, $6d6d, $003b
dw $0d38, $0d58, $0020, $0d48, $6e6e, $003c
dw $0d90, $0da0, $0010, $0d98, $6e6e, $003d
dw $06a0, $07b0, $0110, $0728, $7373, $003e
dw $0830, $09b0, $0180, $08f0, $7474, $003f
dw $0e78, $0e88, $0010, $0e80, $7777, $0040
dw $0ee0, $0fc0, $00e0, $0f50, $7777, $0041
dw $0080, $0080, $0000, $0080, $8080, $0000 ;Pedestal
dw $0288, $02c0, $0038, $02a4, $8282, $0002 ;Zora
OWWestEdges:
dw $0070, $00a0, $0030, $0088, $0202, $0000
dw $0068, $0078, $0010, $0070, $0505, $0001
dw $0068, $0088, $0020, $0078, $0707, $0002
dw $0318, $0368, $0050, $0340, $0d0d, $0003
dw $0450, $0488, $0038, $046c, $1212, $0004
dw $0560, $05a0, $0040, $0580, $1212, $0005
dw $0488, $0500, $0078, $04c4, $1313, $0006
dw $0538, $05a8, $0070, $0570, $1313, $0007
dw $0470, $05a8, $0138, $050c, $1414, $0008
dw $0470, $0598, $0128, $0504, $1515, $0009
dw $0480, $0488, $0008, $0484, $1616, $000a
dw $04b0, $0510, $0060, $04e0, $1616, $000b
dw $0560, $0588, $0028, $0574, $1616, $000c
dw $0450, $0458, $0008, $0454, $1717, $000d
dw $0480, $04a8, $0028, $0494, $1717, $000e
dw $0718, $0738, $0020, $0728, $1b1b, $000f
dw $0908, $0948, $0040, $0928, $2222, $0010
dw $0878, $08a8, $0030, $0890, $2525, $0011
dw $0bb8, $0bc8, $0010, $0bc0, $2929, $0012
dw $0b60, $0ba0, $0040, $0b80, $2a2a, $0013
dw $0ab0, $0ad0, $0020, $0ac0, $2c2c, $0014
dw $0af0, $0b40, $0050, $0b18, $2c2c, $0015
dw $0b78, $0ba0, $0028, $0b8c, $2c2c, $0016
dw $0b10, $0b28, $0018, $0b1c, $2d2d, $004a
dw $0b68, $0b98, $0030, $0b80, $2d2d, $0017
dw $0a68, $0ab8, $0050, $0a90, $2e2e, $0018
dw $0b00, $0b78, $0078, $0b3c, $2e2e, $0019
dw $0c50, $0db8, $0168, $0d04, $3333, $001a
dw $0c78, $0ce3, $006b, $0cad, $3434, $001b
dw $0ce4, $0d33, $004f, $0d0b, $3434, $001c
dw $0d34, $0db8, $0084, $0d76, $3434, $001d
dw $0ea8, $0f20, $0078, $0ee4, $3a3a, $001e
dw $0f70, $0fa8, $0038, $0f8c, $3a3a, $001f
dw $0f18, $0f18, $0000, $0f18, $3b3b, $0020
dw $0fc8, $0fc8, $0000, $0fc8, $3b3b, $0021
dw $0e28, $0fb8, $0190, $0ef0, $3c3c, $0022
dw $0f78, $0fb8, $0040, $0f98, $353d, $0023
dw $0f20, $0f40, $0020, $0f30, $3f3f, $0024
dw $0f70, $0fb8, $0048, $0f94, $3f3f, $0025
dw $0458, $0540, $00e8, $04cc, $4242, $0026
dw $0068, $0078, $0010, $0070, $4545, $0027
dw $0068, $0088, $0020, $0078, $4747, $0028
dw $0318, $0368, $0050, $0340, $454d, $0029
dw $0450, $0488, $0038, $046c, $5252, $002a
dw $0560, $05a0, $0040, $0580, $5252, $002b
dw $0488, $0500, $0078, $04c4, $5353, $002c
dw $0538, $05a8, $0070, $0570, $5353, $002d
dw $0470, $05a8, $0138, $050c, $5454, $002e
dw $0470, $0598, $0128, $0504, $5555, $002f
dw $0480, $0488, $0008, $0484, $5656, $0030
dw $04b0, $0510, $0060, $04e0, $5656, $0031
dw $0560, $0588, $0028, $0574, $5656, $0032
dw $0450, $0458, $0008, $0454, $5757, $0033
dw $0480, $04a8, $0028, $0494, $5757, $0034
dw $0908, $0948, $0040, $0928, $6262, $0035
dw $0878, $08a8, $0030, $0890, $6565, $0036
dw $0b60, $0b68, $0008, $0b64, $6969, $0037
dw $0bb8, $0bc8, $0010, $0bc0, $6969, $0038
dw $0b60, $0ba0, $0040, $0b80, $6a6a, $0039
dw $0ab0, $0ad0, $0020, $0ac0, $6c6c, $003a
dw $0af0, $0b40, $0050, $0b18, $6c6c, $003b
dw $0b78, $0ba0, $0028, $0b8c, $6c6c, $003c
dw $0b68, $0b98, $0030, $0b80, $6d6d, $003d
dw $0a68, $0ab8, $0050, $0a90, $6e6e, $003e
dw $0b00, $0b78, $0078, $0b3c, $6e6e, $003f
dw $0c50, $0db8, $0168, $0d04, $7373, $0040
dw $0c78, $0ce3, $006b, $0cad, $7474, $0041
dw $0ce4, $0d33, $004f, $0d0b, $7474, $0042
dw $0d34, $0db8, $0084, $0d76, $7474, $0043
dw $0f18, $0f18, $0000, $0f18, $7b7b, $0044
dw $0fc8, $0fc8, $0000, $0fc8, $7b7b, $0045
dw $0e28, $0fb8, $0190, $0ef0, $7c7c, $0046
dw $0f78, $0fb8, $0040, $0f98, $757d, $0047
dw $0f20, $0f40, $0020, $0f30, $7f7f, $0048
dw $0f70, $0fb8, $0048, $0f94, $7f7f, $0049
OWEastEdges:
dw $0070, $00a0, $0030, $0088, $0001, $0000
dw $0068, $0078, $0010, $0070, $0304, $0001
dw $0068, $0088, $0020, $0078, $0506, $0002
dw $0318, $0368, $0050, $0340, $0b0c, $0003
dw $0450, $0488, $0038, $046c, $1111, $0004
dw $0560, $05a0, $0040, $0580, $1111, $0005
dw $0488, $0500, $0078, $04c4, $1212, $0006
dw $0538, $05a8, $0070, $0570, $1212, $0007
dw $0470, $05a8, $0138, $050c, $1313, $0008
dw $0470, $0598, $0128, $0504, $1414, $0009
dw $0480, $0488, $0008, $0484, $1515, $000a
dw $04b0, $0510, $0060, $04e0, $1515, $000b
dw $0560, $0588, $0028, $0574, $1515, $000c
dw $0450, $0458, $0008, $0454, $1616, $000d
dw $0480, $04a8, $0028, $0494, $1616, $000e
dw $0718, $0738, $0020, $0728, $1a1a, $000f
dw $0908, $0948, $0040, $0928, $1821, $0010
dw $0878, $08a8, $0030, $0890, $1b24, $0011
dw $0bb8, $0bc8, $0010, $0bc0, $2828, $0012 ;Race Game
dw $0b60, $0ba0, $0040, $0b80, $2929, $0013
dw $0ab0, $0ad0, $0020, $0ac0, $2b2b, $0014
dw $0af0, $0b40, $0050, $0b18, $2b2b, $0015
dw $0b78, $0ba0, $0028, $0b8c, $2b2b, $0016
dw $0b68, $0b98, $0030, $0b80, $2c2c, $0018
dw $0a68, $0ab8, $0050, $0a90, $2d2d, $0019
dw $0b00, $0b78, $0078, $0b3c, $2d2d, $001a
dw $0c50, $0db8, $0168, $0d04, $3232, $001b
dw $0c78, $0ce3, $006b, $0cad, $3333, $001c
dw $0ce4, $0d33, $004f, $0d0b, $3333, $001d
dw $0d34, $0db8, $0084, $0d76, $3333, $001e
dw $0ea8, $0f20, $0078, $0ee4, $3039, $001f
dw $0f70, $0fa8, $0038, $0f8c, $3039, $0020
dw $0f18, $0f18, $0000, $0f18, $3a3a, $0021
dw $0fc8, $0fc8, $0000, $0fc8, $3a3a, $0022
dw $0e28, $0fb8, $0190, $0ef0, $3b3b, $0023
dw $0f78, $0fb8, $0040, $0f98, $3c3c, $0024
dw $0f20, $0f40, $0020, $0f30, $353e, $0025
dw $0f70, $0fb8, $0048, $0f94, $353e, $0026
dw $0070, $00a0, $0030, $0088, $4041, $0027 ;Skull Woods
dw $0068, $0078, $0010, $0070, $4344, $0028
dw $0068, $0088, $0020, $0078, $4546, $0029
dw $0318, $0368, $0050, $0340, $434c, $002a
dw $0450, $0488, $0038, $046c, $5151, $002b
dw $0560, $05a0, $0040, $0580, $5151, $002c
dw $0488, $0500, $0078, $04c4, $5252, $002d
dw $0538, $05a8, $0070, $0570, $5252, $002e
dw $0470, $05a8, $0138, $050c, $5353, $002f
dw $0470, $0598, $0128, $0504, $5454, $0030
dw $0480, $0488, $0008, $0484, $5555, $0031
dw $04b0, $0510, $0060, $04e0, $5555, $0032
dw $0560, $0588, $0028, $0574, $5555, $0033
dw $0450, $0458, $0008, $0454, $5656, $0034
dw $0480, $04a8, $0028, $0494, $5656, $0035
dw $0908, $0948, $0040, $0928, $5861, $0036
dw $0878, $08a8, $0030, $0890, $5b64, $0037
dw $0b60, $0b68, $0008, $0b64, $6868, $0038 ;Dig Game
dw $0bb8, $0bc8, $0010, $0bc0, $6868, $0039
dw $0b60, $0ba0, $0040, $0b80, $6969, $003a
dw $0ab0, $0ad0, $0020, $0ac0, $6b6b, $003b
dw $0af0, $0b40, $0050, $0b18, $6b6b, $003c
dw $0b78, $0ba0, $0028, $0b8c, $6b6b, $003d
dw $0b68, $0b98, $0030, $0b80, $6c6c, $003e
dw $0a68, $0ab8, $0050, $0a90, $6d6d, $003f
dw $0b00, $0b78, $0078, $0b3c, $6d6d, $0040
dw $0c50, $0db8, $0168, $0d04, $7272, $0041
dw $0c78, $0ce3, $006b, $0cad, $7373, $0042
dw $0ce4, $0d33, $004f, $0d0b, $7373, $0043
dw $0d34, $0db8, $0084, $0d76, $7373, $0044
dw $0f18, $0f18, $0000, $0f18, $707a, $0045
dw $0fc8, $0fc8, $0000, $0fc8, $707a, $0046
dw $0e28, $0fb8, $0190, $0ef0, $7b7b, $0047
dw $0f78, $0fb8, $0040, $0f98, $7c7c, $0048
dw $0f20, $0f40, $0020, $0f30, $757e, $0049
dw $0f70, $0fb8, $0048, $0f94, $757e, $004a
dw $0058, $00c0, $0068, $008c, $8181, $0017 ;Hobo
