; The prime factors of 13195 are 5, 7, 13 and 29.

; What is the largest prime factor of the number 600851475143 ?

(def! last (fn* (col) (nth col -1)))

(def! drop-last (fn* (seq) (take seq (- (count seq) 1))))

; Returns true if any item in the "divisors" list evenly divides "number", otherwise false.
(def! divided-by
  (fn* (number divisors)
    (if (> (first divisors) (sqrt number))
      false
      (if (= (% number (first divisors)) 0)
        true
        (divided-by number (rest divisors))
      )
    )
  )
)

; Given a list of "divisors", finds the first number that is greater or equal to "start" and is not divided by any of the divisors.
(def! find-next
  (fn* (divisors start)
    (if (not (divided-by start divisors))
      start
      (find-next divisors (+ start 2))
    )
  )
)

; Recursive function that generates all the primes numbers based on an initial list of "primes" (give at least `(2 3) as the search increments by two, checking only odd numbers), up to a "limit"
(def! gen-primes-rec
  (fn* (limit primes)
    (let* (lst (last primes))
      (if (> lst limit)
        (drop-last primes)
        (gen-primes-rec limit (concat primes (list (find-next primes (+ lst 2)))))
      )
    )
  )
)

; Function that uses gen-primes-rec to generate all the prime numbers up to "limit"
(def! gen-primes
  (fn* (limit)
    (gen-primes-rec limit `(2 3))
  )
)

; Function that finds a "number"'s largest prime factor from a list of given "primes" (aka prime numbers)
(def! largest-prime-factor
  (fn* (number primes)
    (if (empty? primes)
      nil
      (let* (lst (last primes))
        (if (= (% number lst) 0)
          lst
          (largest-prime-factor number (drop-last primes))
        )
      )
    )
  )
)

(let* (number 600851475143)
  (prn (largest-prime-factor number (gen-primes (sqrt number))))
)