class Main inherits IO {
	a: AUTO_TYPE;

	main() : Int {
		m(a, a, a)
	};

	m(x: Object, y: Main, z: IO) : Int { 4 };
};