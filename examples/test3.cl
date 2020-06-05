class Main {
    
    fact(n : AUTO_TYPE): AUTO_TYPE {
        if (n<0) then 1 else n*fact(n-1) fi
    };
};
