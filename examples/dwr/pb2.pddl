(define (problem pb2)
  (:domain dwr)
  (:objects
    r1 - robot
    l1 l2 - location
    k1 k2 - crane
    p1 q1 p2 q2 - pile
    ca cb cc cd ce cf pallet - container
  )
  (:init
    (adjacent l1 l2) (adjacent l2 l1)
    (attached p1 l1) (attached q1 l1)
    (attached p2 l2) (attached q2 l2)
    (belong k1 l1)
    (belong k2 l2)
    (in ca p1) (in cb p1) (in cc p1)
    (in cd q1) (in ce q1) (in cf q1)
    (top cc p1) (on cc cb) (on cb ca) (on ca pallet)
    (top cf q1) (on cf ce) (on ce cd) (on cd pallet)
    (top pallet p2)
    (top pallet q2)
    (at r1 l1)
    (unloaded r1)
    (occupied l1)
    (empty k1)
    (empty k2)
    (equal ca ca) (equal cb cb) (equal cc cc) (equal cd cd) (equal ce ce) (equal cf cf) (equal pallet pallet)
  )
  (:goal (and (in ca p1) (in cb p1)))
)