

def clamp(val, minimum, maximum):
    return max(min(val, maximum), minimum)

class NoiseArray:
    def __init__(self, length, array = None):
        self.len = length
        if array:
            if len(array) != length:
                raise ValueError("Array must have same length as length")
            self.arr = array
        else:
            self.arr = [0] * length


    def set_values(self, array):
        if len(array) != self.len:
            raise ValueError("Value array length does not match array length")
        self.arr = array.copy()

    def add(self, other):
        if len(other) != self.len:
            raise ValueError("Value array length does not match array length")
        new_arr = NoiseArray(self.len)
        new_vals = self.arr.copy()
        for i in range(0, self.len):
            new_vals[i] = (self.arr[i][0] + other.arr[i][0],
                           self.arr[i][1] + other.arr[i][1],
                           self.arr[i][2] + other.arr[i][2])
        new_arr.set_values(new_vals)
        return new_arr

    def sub(self, other):
        if len(other) != self.len:
            raise ValueError("Value array length does not match array length")
        new_arr = NoiseArray(self.len)
        new_vals = self.arr.copy()
        for i in range(0, self.len):
            new_vals[i] = (self.arr[i][0] - other.arr[i][0],
                           self.arr[i][1] - other.arr[i][1],
                           self.arr[i][2] - other.arr[i][2])
        new_arr.set_values(new_vals)
        return new_arr

    def clamp(self):
        new_arr = NoiseArray(self.len)
        new_vals = self.arr.copy()
        for i in range(0, self.len):
            new_vals[i] = (clamp(self.arr[i][0], 0 , 255),
                           clamp(self.arr[i][1], 0 , 255),
                           clamp(self.arr[i][2], 0 , 255))
        new_arr.set_values(new_vals)
        return new_arr

    def __add__(self, other):
        if len(other) != self.len:
            raise ValueError("Value array length does not match array length")
        new_arr = NoiseArray(self.len)
        new_vals = self.arr.copy()
        for i in range(0, self.len):
            new_vals[i] = (self.arr[i][0] + other.arr[i][0],
                           self.arr[i][1] + other.arr[i][1],
                           self.arr[i][2] + other.arr[i][2])
        new_arr.set_values(new_vals)
        return new_arr

    def __mul__(self, val):
        new_arr = NoiseArray(self.len)
        new_vals = self.arr.copy()
        for i in range(self.len):
            new_vals[i] = (self.arr[i][0] * val,
                           self.arr[i][1] * val,
                           self.arr[i][2] * val)
        new_arr.set_values(new_vals)
        return new_arr

    def __floordiv__(self, val):
        new_arr = NoiseArray(self.len)
        new_vals = self.arr.copy()
        for i in range(0, self.len):
            new_vals[i] = (int(self.arr[i][0] / val),
                           int(self.arr[i][1] / val),
                           int(self.arr[i][2] / val))
        new_arr.set_values(new_vals)
        return new_arr

    def __truediv__(self, val):
        new_arr = NoiseArray(self.len)
        new_vals = self.arr.copy()
        for i in range(0, self.len):
            new_vals[i] = (self.arr[i][0] / val,
                           self.arr[i][1] / val,
                           self.arr[i][2] / val)
        new_arr.set_values(new_vals)
        return new_arr

    def __str__(self):
        out = ""
        for i in range(0, self.len):
            out += str(self.arr[i]) + (" ")
        return out

    def __len__(self):
        return self.len