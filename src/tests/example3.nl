int x = 5;
extern myFunc(int, byte);
byte y = 3;
func myFunc(int numb, byte otherval) int {
    return numb + 1;
}
int z = myFunc(x,y);
z = ((z + 2) % 3) + 4;