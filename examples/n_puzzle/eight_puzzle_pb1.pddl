; Instance of 8-Puzzle from Artificial Intelligence: A Modern Approach
; by Russell and Norvig, 2nd edition.

(define (problem eight-puzzle-pb1)
  (:domain n-puzzle)
  (:init
    (adjacent S1 S2) (adjacent S1 S4)
    (adjacent S2 S1) (adjacent S2 S3) (adjacent S2 S5)
    (adjacent S3 S2) (adjacent S3 S6)
    (adjacent S4 S1) (adjacent S4 S5) (adjacent S4 S7)
    (adjacent S5 S4) (adjacent S5 S2) (adjacent S5 S6) (adjacent S5 S8)
    (adjacent S6 S3) (adjacent S6 S5) (adjacent S6 S9)
    (adjacent S7 S4) (adjacent S7 S8)
    (adjacent S8 S7) (adjacent S8 S5) (adjacent S8 S9)
    (adjacent S9 S8) (adjacent S9 S6)

    ; 7 2 4
    ; 5   6
    ; 8 3 1

    (at T7 S1) (at T2 S2) (at T4 S3) (at T5 S4) (at Blank S5) (at T6 S6) (at T8 S7) (at T3 S8) (at T1 S9)
    (equal S1 S1) (equal S2 S2) (equal S3 S3) (equal S4 S4) (equal S5 S5) (equal S6 S6) (equal S7 S7) (equal S8 S8)
  )

  ;   1 2
  ; 3 4 5
  ; 6 7 8

  (:goal (and (at Blank S1) (at T1 S2) (at T2 S3) (at T3 S4) (at T4 S5) (at T5 S6) (at T6 S7) (at T7 S8) (at T8 S9)))
)