class Main inherits IO {
    main() : SELF_TYPE {
        let x : AUTO_TYPE <- 3 + 2 in
            case x of
                y : Int => out_string("Ok");
            esac
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
