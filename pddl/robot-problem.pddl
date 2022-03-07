(define (problem star-trek-problem-1)
  (:domain star-trek-domain-1)

  (:objects)

  (:init
   ;; Locations
   (at enterprise earth)
   (at plasmaconduit1 vulcan)
   (at plasmainjector1 betazed)
   (at warpcoil1 qonos)
   (at dilithium1 ferenginar)
   (at medicalsupply1 sb128)
   (crew-on-ship enterprise)
   (not (crew-off-ship enterprise)) ;; overspecification?

   ; (not (people-saved levinia))
   ;; Warp Speed
   (not (warp-speed-enabled))

   ;; Timing
   (= (impulse-speed-time vulcan qonos) 6.0)
   (= (impulse-speed-time qonos vulcan) 6.0)
   (= (impulse-speed-time vulcan cardassia) 7.0)
   (= (impulse-speed-time cardassia vulcan) 7.0)
   (= (impulse-speed-time cardassia betazed) 9.0)
   (= (impulse-speed-time betazed cardassia) 9.0)
   (= (impulse-speed-time betazed ferenginar) 10.0)
   (= (impulse-speed-time ferenginar betazed) 10.0)
   (= (impulse-speed-time betazed qonos) 10.0)
   (= (impulse-speed-time qonos betazed) 10.0)
   (= (impulse-speed-time earth betazed) 15.0)
   (= (impulse-speed-time betazed earth) 15.0)
   (= (impulse-speed-time earth sb128) 1)
   (= (impulse-speed-time sb128 earth) 1.0)
   (= (impulse-speed-time earth vulcan) 10.0)
   (= (impulse-speed-time vulcan earth) 10.0)
   (= (impulse-speed-time qonos levinia) 500.0)
   (= (impulse-speed-time levinia qonos) 10.0)

   (time-left)
   (at 400 (not (time-left))))

  (:goal
   (and (people-saved levinia))))