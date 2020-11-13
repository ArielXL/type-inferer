class Main inherits IO {

    main () : AUTO_TYPE {
        {
            let x:A <- new B in out_string( x.f().m() );
            let x:A <- new A in x.f().m();
        }
        
    };
};

class A {
    m () : String { "A" };
    f () : AUTO_TYPE { new A };
};

class B inherits A {
    m () : String { "B" };
};
