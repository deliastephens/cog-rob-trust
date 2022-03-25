(define (problem robot-problem-1)
  (:domain robot-domain-1)

  (:objects
    sq0-0 sq0-1 sq0-2 - location
    sq1-0 sq1-1 sq1-2 - location
    sq2-0 sq2-1 sq2-2 - location
    robot1 - robot)

  (:init
   ;; Locations
   (at robot1 sq2-2)

   ;; Adjacency
   (adj sq0-0 sq0-1)
   (adj sq0-0 sq1-0)

   (adj sq0-1 sq1-0)
   (adj sq0-1 sq0-2)
   (adj sq0-1 sq1-1)
   
   (adj sq0-2 sq1-0)
   (adj sq0-2 sq1-2)
   
   (adj sq1-0 sq1-1)
   (adj sq1-0 sq0-0)
   (adj sq1-0 sq2-0)

   (adj sq1-1 sq0-1)
   (adj sq1-1 sq1-0)
   (adj sq1-1 sq1-2)
   (adj sq1-1 sq2-1)

   (adj sq1-2 sq0-2)
   (adj sq1-2 sq1-1)
   (adj sq1-2 sq2-2)

   (adj sq2-0 sq1-0)
   (adj sq2-0 sq2-1)
   
   (adj sq2-1 sq2-0)
   (adj sq2-1 sq1-1)
   (adj sq2-1 sq2-2)

   (adj sq2-2 sq2-1)
   (adj sq2-2 sq1-2)

   (clear sq0-0)
   (clear sq0-1)
   (clear sq0-2)
   (clear sq1-0) 
   ;; (clear sq1-1) 
   (clear sq1-2) 
   (clear sq2-0)
   (clear sq2-1)
   (clear sq2-2))

  (:goal
   (and (at robot1 sq0-2))))