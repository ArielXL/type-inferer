class Main inherits IO {

	a: Int;
	b: Bool;
	c: String;

	main() : Int {
		{
			m(4);
			m(5);
			m("jj");
		}
	};

	m(x: AUTO_TYPE) : Int { 4 };
};