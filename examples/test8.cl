class A { };
class B inherits A { };

class Point {
    x : AUTO_TYPE;
    y : AUTO_TYPE;

    init(n : Int, m : Int) : SELF_TYPE { 
        {
            x <- n;
            y <- m;
            self;
        }
    };
};