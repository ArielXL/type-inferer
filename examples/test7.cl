class Main inherits IO {
    main() : SELF_TYPE {
        let x : AUTO_TYPE <- 3 + 2 in
            case x of
                y : Int => out_string("Ok");
            esac
    };

    break(): AUTO_TYPE {
	    let x: AUTO_TYPE <- new Main.main().main() in x
    };

    succ(n : Int) : AUTO_TYPE { n + 1 };

    succ2(n : AUTO_TYPE) : AUTO_TYPE { n + 1 };

    step(p : AUTO_TYPE) : AUTO_TYPE { p.translate(1, 1) };

    test() : AUTO_TYPE {
        let p : AUTO_TYPE <- new Point in step(p)
    };

    fact(n : AUTO_TYPE): AUTO_TYPE {
        if (n<0) then 1 else n*fact(n-1) fi
    };

    ackermann(m : AUTO_TYPE, n: AUTO_TYPE) : AUTO_TYPE {
        if (m=0) then 
            n+1
        else
            if (n=0) then 
                ackermann(m-1, 1) 
            else
                ackermann(m-1, ackermann(m, n-1))
            fi
        fi
    };
    
    no_infer(x: AUTO_TYPE, y: AUTO_TYPE): AUTO_TYPE {
        {
            x <- 1;
            x <- "1";
            y <- x;
            x;
        }
    };
};
