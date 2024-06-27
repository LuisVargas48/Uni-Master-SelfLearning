eratostenes :: [Int] -> [Int]
eratostenes [] = [1000]
eratostenes (x:xs) | not (null xs) && x^2 > last xs = (x:xs)
                   | otherwise = x: eratostenes [y| y <- xs, y `mod` x/= 0]