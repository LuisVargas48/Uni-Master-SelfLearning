criba (p:r) = p : criba [ n | n <- r, n `mod` p != 0]


primos n = take n (criba [2..1000])