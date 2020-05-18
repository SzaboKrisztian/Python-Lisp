;A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

;Find the largest palindrome made from the product of two 3-digit numbers.

; Utility function that returns the second item in a list
(def! second (fn* (seq) (nth seq 1)))

; Recursive function that moves the last char of source to the end of dest until source and dest have the same length. If the total length is an odd number, on the last step the last char of source will be copied to dest instead of moved.
(def! split-str
  (fn* (source dest)
    (let* (len-src (count source)
           len-dst (count dest))
      (if (= len-dst (- len-src 1))
        (list source (+ dest (nth source -1)))
        (if (= len-src len-dst)
          (list source dest)
          (split-str (take source -1) (+ dest (nth source -1)))
        )
      )
    )
  )
)

; Takes a number and returns a list of two strings that represent the first half of the number, and the second half reversed.
(def! split-num
  (fn* (number)
    (let* (nr-str (str number))
      (if (> (count nr-str) 1)
        (split-str nr-str "")
        nil
      )
    )
  )
)

; Takes a number and return true if it's palindromic, otherwise false
(def! is-palindrome 
  (fn* (number)
    (let* (parts (split-num number))
      (if (= parts nil)
        true
        (= (first parts) (second parts))
      )
    )
  )
)

; Recursive function that checks all combinations of two numbered products between op1 * op2 and limit * limit, and returns the largest palindromic number found
(def! find-largest-pali-rec
  (fn* (limit op1 op2 current)
    (if (> op1 limit)
      current
      (if (> op2 limit)
        (find-largest-pali-rec limit (+ op1 1) (+ op1 1) current)
        (let* (num (* op1 op2))
          (if (and (is-palindrome num) (> num current))
            (find-largest-pali-rec limit op1 (+ op2 1) num)
            (find-largest-pali-rec limit op1 (+ op2 1) current)
          )
        )
      )
    )
  )
)

; Driver function to simplify calling the above recursive horror
(def! find-largest-pali
  (fn* (start limit)
    (find-largest-pali-rec limit start start 0)
  )
)

(prn (find-largest-pali 900 999))