numeroDeRaices a b c | d < 0     = 0
                     | d == 0    = 1
                     | otherwise = 2
                     where d = b^2-4*a*c 