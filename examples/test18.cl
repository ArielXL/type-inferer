class Main inherits IO {
	
	a: Object;
	b: Int;

	main() : Int {
		{
			a <- fact(0);
			b <- fact(0);
			3;
		}
	};

	fact(n: Int) : AUTO_TYPE {

		if (n < 0) then 1 else fact(n - 1) fi

	};
};