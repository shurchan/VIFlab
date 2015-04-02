X = 99

def func():
    X = 88

print func()

# Global scope
X = 99                # X and func assigned in module: global
          
def func(Y):          # Y and Z assigned in function: locals
    # local scope
    Z = X + Y         # X is a global.
    return Z


print func(1)               # func in module: result=100
print func(3)

print 2**8
print 'test string1' + 'test string2'