class Main inherits IO {
	
	main() : AUTO_TYPE { 
		let x : AUTO_TYPE <- 3 in { 
			case x of
				y : Int => out_string("Ok");
			esac; 
		}
	};
};

class A inherits IO {
	
	x: AUTO_TYPE;
	y: AUTO_TYPE;

	init(n : Int, m: Int) : SELF_TYPE { 
		{
			x <- n;
			y <- m;
			self;
		}
	};

	succ(n: Int): AUTO_TYPE { n + 1 };

	succ2(n : AUTO_TYPE) : AUTO_TYPE { n + 1 };

	fact(n: AUTO_TYPE) : AUTO_TYPE {
		if (n < 0) then 1 else n * fact(n - 1) fi
	};
};
