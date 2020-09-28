a = 'BigDecimal.ONE'

for i in range(0, 666):
    a = a + '.add(BigDecimal.ONE)'
a = a + '.intValue()'
print(a)
