class A {
    a : int ;
    def suma ( a : int , b : int ) : int {
        a + b + new B ( ) ;
    }
    b : int ;
}

class B : A {
    c : A ;
    def f ( d : int , a : A ) : void {
        let f : int = 8 ;
        let c = new A ( ) . suma ( 5 , f ) ;
        d ;        
    }
    
    def test ( a : A , b : B ) : int {
        let self = 1 ;
        let z : int = a + b ;
        let z = a . suma ( 1 , 2 , 3 ) ;
        let w = b . suma ( a , b ) ;
        let w : int = b . resta ( 69 ) ;
        b ;
    }
}
